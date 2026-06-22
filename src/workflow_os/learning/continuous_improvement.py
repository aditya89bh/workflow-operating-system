"""Continuous improvement reports.

Brings together the recommendation generators, the analytics trend report, and
the maturity score into one rolled-up view of where the organization stands and
what to work on next. Everything is assembled deterministically from the recorded
history.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field

from workflow_os.analytics.trends import TrendReport, trend_report
from workflow_os.approval.record import ApprovalRequest
from workflow_os.exception.record import ExceptionRecord
from workflow_os.exception.recovery import RecoveryAction
from workflow_os.learning.approval_recommendations import (
    approval_improvement_recommendations,
)
from workflow_os.learning.automation import automation_opportunity_recommendations
from workflow_os.learning.maturity import MaturityScore, organizational_maturity_score
from workflow_os.learning.recommendation import Recommendation
from workflow_os.learning.sop_recommendations import sop_update_recommendations
from workflow_os.learning.workflow_recommendations import (
    workflow_improvement_recommendations,
)
from workflow_os.memory.record import MemoryRecord
from workflow_os.sop.record import SOPRecord


def improvement_opportunities(
    records: Iterable[MemoryRecord] | None = None,
    *,
    sops: Iterable[SOPRecord] | None = None,
    exceptions: Iterable[ExceptionRecord] | None = None,
    approvals: Iterable[ApprovalRequest] | None = None,
    recoveries: Iterable[RecoveryAction] | None = None,
) -> list[Recommendation]:
    """Return every improvement recommendation, across all categories."""
    record_list = list(records or [])
    exception_list = list(exceptions or [])
    approval_list = list(approvals or [])
    opportunities: list[Recommendation] = []
    opportunities.extend(workflow_improvement_recommendations(record_list))
    opportunities.extend(
        sop_update_recommendations(sops or [], exceptions=exception_list)
    )
    opportunities.extend(
        automation_opportunity_recommendations(
            record_list, approvals=approval_list, recoveries=recoveries or []
        )
    )
    opportunities.extend(approval_improvement_recommendations(approval_list))
    return opportunities


@dataclass
class ContinuousImprovementReport:
    """A rolled-up view of opportunities, trends, and maturity."""

    opportunities: list[Recommendation] = field(default_factory=list)
    trends: TrendReport = field(default_factory=TrendReport)
    maturity: MaturityScore | None = None


def continuous_improvement_report(
    records: Iterable[MemoryRecord] | None = None,
    *,
    sops: Iterable[SOPRecord] | None = None,
    exceptions: Iterable[ExceptionRecord] | None = None,
    approvals: Iterable[ApprovalRequest] | None = None,
    recoveries: Iterable[RecoveryAction] | None = None,
) -> ContinuousImprovementReport:
    """Build a deterministic continuous improvement report."""
    record_list = list(records or [])
    sop_list = list(sops or [])
    exception_list = list(exceptions or [])
    approval_list = list(approvals or [])
    recovery_list = list(recoveries or [])
    return ContinuousImprovementReport(
        opportunities=improvement_opportunities(
            record_list,
            sops=sop_list,
            exceptions=exception_list,
            approvals=approval_list,
            recoveries=recovery_list,
        ),
        trends=trend_report(
            record_list, approvals=approval_list, exceptions=exception_list
        ),
        maturity=organizational_maturity_score(
            record_list,
            sops=sop_list,
            exceptions=exception_list,
            approvals=approval_list,
            recoveries=recovery_list,
        ),
    )
