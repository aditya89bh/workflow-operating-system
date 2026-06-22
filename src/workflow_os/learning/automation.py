"""Automation opportunity recommendations.

Highlights work the organization does over and over and could automate:
repetitive steps (the same step completed many times), repeated approvals (the
same workflow approved repeatedly), and repeated recoveries (the same recovery
action applied repeatedly). Each opportunity is found by a fixed counting rule.
"""

from __future__ import annotations

from collections.abc import Iterable

from workflow_os.approval.record import ApprovalRequest
from workflow_os.exception.recovery import RecoveryAction
from workflow_os.learning.exception_patterns import recurring_recovery_actions
from workflow_os.learning.recommendation import Recommendation
from workflow_os.memory.events import MemoryEventType
from workflow_os.memory.record import MemoryRecord

_STEP_COMPLETED = str(MemoryEventType.STEP_COMPLETED)


def repetitive_task_recommendations(
    records: Iterable[MemoryRecord], *, min_occurrences: int = 3
) -> list[Recommendation]:
    """Return automation recommendations for frequently repeated steps."""
    counts: dict[str, int] = {}
    for record in records:
        if record.event_type == _STEP_COMPLETED and record.step_id is not None:
            counts[record.step_id] = counts.get(record.step_id, 0) + 1
    recommendations: list[Recommendation] = []
    for step_id, count in sorted(counts.items()):
        if count >= min_occurrences:
            recommendations.append(
                Recommendation.create(
                    category="automation",
                    title=f"automate repetitive task {step_id}",
                    description=(
                        f"step {step_id!r} completed {count} times; it is a "
                        "candidate for automation."
                    ),
                    severity="medium",
                    confidence=1.0,
                    metadata={"step_id": step_id, "action": "automate_task"},
                )
            )
    return recommendations


def repeated_approval_recommendations(
    approvals: Iterable[ApprovalRequest], *, min_occurrences: int = 3
) -> list[Recommendation]:
    """Return automation recommendations for workflows approved repeatedly."""
    counts: dict[str, int] = {}
    for approval in approvals:
        counts[approval.workflow_id] = counts.get(approval.workflow_id, 0) + 1
    recommendations: list[Recommendation] = []
    for workflow_id, count in sorted(counts.items()):
        if count >= min_occurrences:
            recommendations.append(
                Recommendation.create(
                    category="automation",
                    title=f"automate repeated approvals for {workflow_id}",
                    description=(
                        f"{workflow_id} required approval {count} times; consider "
                        "auto-approving routine cases."
                    ),
                    severity="medium",
                    confidence=1.0,
                    metadata={"workflow_id": workflow_id, "action": "automate_approval"},
                )
            )
    return recommendations


def repeated_recovery_recommendations(
    actions: Iterable[RecoveryAction], *, min_occurrences: int = 2
) -> list[Recommendation]:
    """Return automation recommendations for recovery actions applied repeatedly."""
    recommendations: list[Recommendation] = []
    for action, count in recurring_recovery_actions(
        actions, min_occurrences=min_occurrences
    ).items():
        recommendations.append(
            Recommendation.create(
                category="automation",
                title=f"automate recovery action {action}",
                description=(
                    f"recovery action {action!r} was applied {count} times; "
                    "consider automating it."
                ),
                severity="medium",
                confidence=1.0,
                metadata={"recovery_action": action, "action": "automate_recovery"},
            )
        )
    return recommendations


def automation_opportunity_recommendations(
    records: Iterable[MemoryRecord] | None = None,
    *,
    approvals: Iterable[ApprovalRequest] | None = None,
    recoveries: Iterable[RecoveryAction] | None = None,
    min_task_occurrences: int = 3,
    min_approval_occurrences: int = 3,
    min_recovery_occurrences: int = 2,
) -> list[Recommendation]:
    """Return all automation opportunity recommendations."""
    recommendations: list[Recommendation] = []
    recommendations.extend(
        repetitive_task_recommendations(
            records or [], min_occurrences=min_task_occurrences
        )
    )
    recommendations.extend(
        repeated_approval_recommendations(
            approvals or [], min_occurrences=min_approval_occurrences
        )
    )
    recommendations.extend(
        repeated_recovery_recommendations(
            recoveries or [], min_occurrences=min_recovery_occurrences
        )
    )
    return recommendations
