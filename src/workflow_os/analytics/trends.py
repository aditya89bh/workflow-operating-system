"""Trend analysis reports.

Buckets activity by UTC day so changes over time are visible: workflow
completions, workflow failures, approvals raised, and exceptions detected. The
buckets are exact counts taken from recorded timestamps - there is no smoothing,
forecasting, or projection.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field
from datetime import datetime

from workflow_os.analytics.reports import counts_by_day
from workflow_os.approval.record import ApprovalRequest
from workflow_os.exception.record import ExceptionRecord
from workflow_os.memory.events import MemoryEventType
from workflow_os.memory.record import MemoryRecord


@dataclass
class TrendReport:
    """Day-bucketed trends across the major layers."""

    workflow_trends: dict[str, int] = field(default_factory=dict)
    failure_trends: dict[str, int] = field(default_factory=dict)
    approval_trends: dict[str, int] = field(default_factory=dict)
    exception_trends: dict[str, int] = field(default_factory=dict)


def _bucket_timestamps(timestamps: Iterable[datetime]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for timestamp in timestamps:
        day = timestamp.date().isoformat()
        counts[day] = counts.get(day, 0) + 1
    return dict(sorted(counts.items()))


def workflow_completion_trends(records: Iterable[MemoryRecord]) -> dict[str, int]:
    """Return workflow completions per UTC day."""
    return counts_by_day(records, str(MemoryEventType.WORKFLOW_COMPLETED))


def failure_trends(records: Iterable[MemoryRecord]) -> dict[str, int]:
    """Return workflow failures per UTC day."""
    return counts_by_day(records, str(MemoryEventType.WORKFLOW_FAILED))


def approval_trends(approvals: Iterable[ApprovalRequest]) -> dict[str, int]:
    """Return approval requests raised per UTC day."""
    return _bucket_timestamps(request.created_at for request in approvals)


def exception_trends(exceptions: Iterable[ExceptionRecord]) -> dict[str, int]:
    """Return exceptions detected per UTC day."""
    return _bucket_timestamps(exc.detected_at for exc in exceptions)


def trend_report(
    records: Iterable[MemoryRecord],
    *,
    approvals: Iterable[ApprovalRequest] | None = None,
    exceptions: Iterable[ExceptionRecord] | None = None,
) -> TrendReport:
    """Build a combined :class:`TrendReport` across the supplied sources."""
    records = list(records)
    return TrendReport(
        workflow_trends=workflow_completion_trends(records),
        failure_trends=failure_trends(records),
        approval_trends=approval_trends(approvals or []),
        exception_trends=exception_trends(exceptions or []),
    )
