"""Approval improvement recommendations.

Reviews recorded approval requests and suggests deterministic governance
improvements: reduce the number of approvers on heavy requests, adjust escalation
for workflows that escalate repeatedly, and relieve approver bottlenecks where a
single approver is on the critical path of many requests.
"""

from __future__ import annotations

from collections.abc import Iterable

from workflow_os.approval.escalation import escalation_history
from workflow_os.approval.record import ApprovalRequest
from workflow_os.learning.recommendation import Recommendation


def reduce_approver_recommendations(
    approvals: Iterable[ApprovalRequest], *, max_approvers: int = 3
) -> list[Recommendation]:
    """Return recommendations to reduce approvers on heavy workflows."""
    worst: dict[str, int] = {}
    for approval in approvals:
        count = len(approval.approvers)
        if count > max_approvers and count > worst.get(approval.workflow_id, 0):
            worst[approval.workflow_id] = count
    recommendations: list[Recommendation] = []
    for workflow_id, count in sorted(worst.items()):
        recommendations.append(
            Recommendation.create(
                category="approval",
                title=f"reduce approvers for {workflow_id}",
                description=(
                    f"{workflow_id} requires {count} approvers; consider reducing "
                    f"to at most {max_approvers}."
                ),
                severity="medium",
                confidence=1.0,
                metadata={"workflow_id": workflow_id, "action": "reduce_approvers"},
            )
        )
    return recommendations


def escalation_recommendations(
    approvals: Iterable[ApprovalRequest], *, min_escalations: int = 2
) -> list[Recommendation]:
    """Return recommendations to adjust escalation for frequently escalated work."""
    counts: dict[str, int] = {}
    for approval in approvals:
        escalations = len(escalation_history(approval))
        if escalations:
            counts[approval.workflow_id] = (
                counts.get(approval.workflow_id, 0) + escalations
            )
    recommendations: list[Recommendation] = []
    for workflow_id, count in sorted(counts.items()):
        if count >= min_escalations:
            recommendations.append(
                Recommendation.create(
                    category="approval",
                    title=f"adjust escalation for {workflow_id}",
                    description=(
                        f"{workflow_id} escalated {count} times; review its "
                        "escalation thresholds and targets."
                    ),
                    severity="high",
                    confidence=1.0,
                    metadata={"workflow_id": workflow_id, "action": "adjust_escalation"},
                )
            )
    return recommendations


def approver_bottleneck_recommendations(
    approvals: Iterable[ApprovalRequest], *, min_requests: int = 3
) -> list[Recommendation]:
    """Return recommendations to relieve overloaded approvers."""
    counts: dict[str, int] = {}
    for approval in approvals:
        for approver in approval.approvers:
            counts[approver] = counts.get(approver, 0) + 1
    recommendations: list[Recommendation] = []
    for approver, count in sorted(counts.items()):
        if count >= min_requests:
            recommendations.append(
                Recommendation.create(
                    category="approval",
                    title=f"eliminate approval bottleneck at {approver}",
                    description=(
                        f"{approver} is an approver on {count} requests; distribute "
                        "the load to avoid a bottleneck."
                    ),
                    severity="medium",
                    confidence=1.0,
                    metadata={"approver": approver, "action": "eliminate_bottleneck"},
                )
            )
    return recommendations


def approval_improvement_recommendations(
    approvals: Iterable[ApprovalRequest],
    *,
    max_approvers: int = 3,
    min_escalations: int = 2,
    min_requests: int = 3,
) -> list[Recommendation]:
    """Return all approval improvement recommendations."""
    approvals = list(approvals)
    recommendations: list[Recommendation] = []
    recommendations.extend(
        reduce_approver_recommendations(approvals, max_approvers=max_approvers)
    )
    recommendations.extend(
        escalation_recommendations(approvals, min_escalations=min_escalations)
    )
    recommendations.extend(
        approver_bottleneck_recommendations(approvals, min_requests=min_requests)
    )
    return recommendations
