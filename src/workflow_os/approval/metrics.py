"""Approval workload metrics.

Aggregate measures of approval activity derived from an audit log and a store:
how many approvals each actor has handled, how long approvals take on average,
and how many requests are currently pending or overdue.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime

from workflow_os.approval.audit import ApprovalAuditLog, ApprovalEventType
from workflow_os.approval.history import pending_approvals
from workflow_os.approval.store import ApprovalStore
from workflow_os.approval.timeout import find_overdue

_RESPONSE_TYPES = (
    ApprovalEventType.APPROVED.value,
    ApprovalEventType.REJECTED.value,
)


@dataclass
class WorkloadMetrics:
    """A snapshot of approval workload."""

    approvals_by_actor: dict[str, int] = field(default_factory=dict)
    average_response_seconds: float | None = None
    pending_count: int = 0
    overdue_count: int = 0


def approvals_by_actor(log: ApprovalAuditLog) -> dict[str, int]:
    """Return the number of approvals recorded per actor."""
    counter: Counter[str] = Counter()
    for event in log.by_type(ApprovalEventType.APPROVED.value):
        if event.actor is not None:
            counter[event.actor] += 1
    return dict(counter)


def _request_times(log: ApprovalAuditLog) -> dict[str, datetime]:
    times: dict[str, datetime] = {}
    for event in log.by_type(ApprovalEventType.REQUESTED.value):
        times.setdefault(event.approval_id, event.timestamp)
    return times


def response_times(log: ApprovalAuditLog) -> list[float]:
    """Return response durations (seconds) between request and each decision."""
    requested = _request_times(log)
    durations: list[float] = []
    for event in log.all():
        if event.event_type not in _RESPONSE_TYPES:
            continue
        start = requested.get(event.approval_id)
        if start is None:
            continue
        durations.append((event.timestamp - start).total_seconds())
    return durations


def average_response_time(log: ApprovalAuditLog) -> float | None:
    """Return the mean response time in seconds, or ``None`` if no responses."""
    durations = response_times(log)
    if not durations:
        return None
    return sum(durations) / len(durations)


def pending_count(store: ApprovalStore) -> int:
    """Return the number of pending requests in ``store``."""
    return len(pending_approvals(store))


def overdue_count(
    store: ApprovalStore, timeout_seconds: float, now: datetime | None = None
) -> int:
    """Return the number of overdue requests in ``store``."""
    return len(find_overdue(store.list(), timeout_seconds, now))


def compute_workload_metrics(
    store: ApprovalStore,
    log: ApprovalAuditLog,
    timeout_seconds: float | None = None,
    now: datetime | None = None,
) -> WorkloadMetrics:
    """Build a :class:`WorkloadMetrics` snapshot from a store and audit log."""
    overdue = (
        overdue_count(store, timeout_seconds, now)
        if timeout_seconds is not None
        else 0
    )
    return WorkloadMetrics(
        approvals_by_actor=approvals_by_actor(log),
        average_response_seconds=average_response_time(log),
        pending_count=pending_count(store),
        overdue_count=overdue,
    )
