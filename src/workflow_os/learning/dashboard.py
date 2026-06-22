"""Organizational insights dashboard data.

Produces plain, JSON-serializable summaries suited to dashboards and
visualizations: the maturity score and its components, the most successful and
most failing workflows, recurring bottlenecks, day-bucketed trends, and counts of
insights and recommendations by category. Everything is built from the
deterministic learning primitives.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from workflow_os.analytics.trends import trend_report
from workflow_os.approval.record import ApprovalRequest
from workflow_os.exception.record import ExceptionRecord
from workflow_os.exception.recovery import RecoveryAction
from workflow_os.learning.continuous_improvement import improvement_opportunities
from workflow_os.learning.failure_patterns import frequently_failing_workflows
from workflow_os.learning.maturity import organizational_maturity_score
from workflow_os.learning.patterns import recurring_bottlenecks, workflow_run_stats
from workflow_os.learning.reports import organizational_insights
from workflow_os.learning.success import highest_success_rate_workflows
from workflow_os.memory.record import MemoryRecord
from workflow_os.sop.record import SOPRecord


def _counts_by_category(items: Iterable[Any]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in items:
        counts[item.category] = counts.get(item.category, 0) + 1
    return counts


def organizational_dashboard(
    records: Iterable[MemoryRecord] | None = None,
    *,
    sops: Iterable[SOPRecord] | None = None,
    exceptions: Iterable[ExceptionRecord] | None = None,
    approvals: Iterable[ApprovalRequest] | None = None,
    recoveries: Iterable[RecoveryAction] | None = None,
    top_n: int = 5,
) -> dict[str, Any]:
    """Return structured dashboard data summarizing organizational learning."""
    record_list = list(records or [])
    sop_list = list(sops or [])
    exception_list = list(exceptions or [])
    approval_list = list(approvals or [])
    recovery_list = list(recoveries or [])

    stats = workflow_run_stats(record_list)
    maturity = organizational_maturity_score(
        record_list,
        sops=sop_list,
        exceptions=exception_list,
        approvals=approval_list,
        recoveries=recovery_list,
    )
    insights = organizational_insights(record_list, exceptions=exception_list)
    recommendations = improvement_opportunities(
        record_list,
        sops=sop_list,
        exceptions=exception_list,
        approvals=approval_list,
        recoveries=recovery_list,
    )
    trends = trend_report(
        record_list, approvals=approval_list, exceptions=exception_list
    )

    top_successful = [
        {
            "workflow_id": s.workflow_id,
            "success_rate": round(s.success_rate, 4),
            "runs": s.runs,
        }
        for s in highest_success_rate_workflows(record_list, limit=top_n)
    ]
    top_failing = [
        {
            "workflow_id": workflow_id,
            "failures": stats[workflow_id].failures,
            "failure_rate": round(stats[workflow_id].failure_rate, 4),
        }
        for workflow_id in frequently_failing_workflows(record_list, min_failures=1)[
            :top_n
        ]
    ]
    bottlenecks = [
        {
            "step_id": b.step_id,
            "occurrences": b.occurrences,
            "total_duration": round(b.total_duration, 4),
        }
        for b in recurring_bottlenecks(record_list, min_occurrences=2)
    ]

    return {
        "maturity": {
            "overall": round(maturity.overall, 4),
            "level": maturity.level,
            "components": {k: round(v, 4) for k, v in maturity.components.items()},
        },
        "totals": {
            "workflows": len(stats),
            "insights": len(insights),
            "recommendations": len(recommendations),
        },
        "top_successful_workflows": top_successful,
        "top_failing_workflows": top_failing,
        "recurring_bottlenecks": bottlenecks,
        "insight_counts": _counts_by_category(insights),
        "recommendation_counts": _counts_by_category(recommendations),
        "trends": {
            "workflow": trends.workflow_trends,
            "failure": trends.failure_trends,
            "approval": trends.approval_trends,
            "exception": trends.exception_trends,
        },
    }
