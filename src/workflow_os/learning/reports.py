"""Learning reports.

Combines the insight generators and recommendation generators into a single
report: what the organization is observing (insights), what it should do
(recommendations), and a small numeric summary of both. The report is built
deterministically from the recorded history.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field

from workflow_os.approval.record import ApprovalRequest
from workflow_os.exception.record import ExceptionRecord
from workflow_os.exception.recovery import RecoveryAction
from workflow_os.learning.continuous_improvement import improvement_opportunities
from workflow_os.learning.exception_patterns import recurring_exception_insights
from workflow_os.learning.failure_patterns import failure_pattern_insights
from workflow_os.learning.insight import OrganizationalInsight
from workflow_os.learning.recommendation import Recommendation
from workflow_os.learning.success import successful_workflow_insights
from workflow_os.memory.record import MemoryRecord
from workflow_os.sop.record import SOPRecord


def organizational_insights(
    records: Iterable[MemoryRecord] | None = None,
    *,
    exceptions: Iterable[ExceptionRecord] | None = None,
) -> list[OrganizationalInsight]:
    """Return all organizational insights across success, failure, exceptions."""
    record_list = list(records or [])
    exception_list = list(exceptions or [])
    insights: list[OrganizationalInsight] = []
    insights.extend(successful_workflow_insights(record_list))
    insights.extend(failure_pattern_insights(record_list))
    insights.extend(recurring_exception_insights(exception_list))
    return insights


@dataclass
class LearningReport:
    """A combined report of insights, recommendations, and a summary."""

    insights: list[OrganizationalInsight] = field(default_factory=list)
    recommendations: list[Recommendation] = field(default_factory=list)
    summary: dict[str, int] = field(default_factory=dict)


def _summarize(
    insights: list[OrganizationalInsight], recommendations: list[Recommendation]
) -> dict[str, int]:
    summary = {
        "insight_count": len(insights),
        "recommendation_count": len(recommendations),
    }
    for recommendation in recommendations:
        key = f"recommendations_{recommendation.category}"
        summary[key] = summary.get(key, 0) + 1
    return summary


def learning_report(
    records: Iterable[MemoryRecord] | None = None,
    *,
    sops: Iterable[SOPRecord] | None = None,
    exceptions: Iterable[ExceptionRecord] | None = None,
    approvals: Iterable[ApprovalRequest] | None = None,
    recoveries: Iterable[RecoveryAction] | None = None,
) -> LearningReport:
    """Build a deterministic learning report."""
    record_list = list(records or [])
    sop_list = list(sops or [])
    exception_list = list(exceptions or [])
    approval_list = list(approvals or [])
    recovery_list = list(recoveries or [])
    insights = organizational_insights(record_list, exceptions=exception_list)
    recommendations = improvement_opportunities(
        record_list,
        sops=sop_list,
        exceptions=exception_list,
        approvals=approval_list,
        recoveries=recovery_list,
    )
    return LearningReport(
        insights=insights,
        recommendations=recommendations,
        summary=_summarize(insights, recommendations),
    )
