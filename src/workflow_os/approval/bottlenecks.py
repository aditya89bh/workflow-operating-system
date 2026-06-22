"""Approval bottleneck analysis.

Identifies where approvals slow down: which approvers take longest to respond,
which workflows have the slowest approvals, and which workflows attract the most
escalations.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass, field

from workflow_os.approval.audit import ApprovalAuditLog, ApprovalEventType
from workflow_os.approval.metrics import _request_times
from workflow_os.approval.store import ApprovalStore

_RESPONSE_TYPES = (
    ApprovalEventType.APPROVED.value,
    ApprovalEventType.REJECTED.value,
)


@dataclass
class BottleneckReport:
    """A summary of approval bottlenecks."""

    slowest_approvers: list[tuple[str, float]] = field(default_factory=list)
    workflow_bottlenecks: list[tuple[str, float]] = field(default_factory=list)
    escalation_hotspots: dict[str, int] = field(default_factory=dict)


def _averages(sums: dict[str, float], counts: dict[str, int]) -> list[tuple[str, float]]:
    averages = [(key, sums[key] / counts[key]) for key in sums if counts[key]]
    averages.sort(key=lambda item: item[1], reverse=True)
    return averages


def slowest_approvers(log: ApprovalAuditLog) -> list[tuple[str, float]]:
    """Return (actor, average response seconds) ordered slowest first."""
    requested = _request_times(log)
    sums: dict[str, float] = defaultdict(float)
    counts: dict[str, int] = defaultdict(int)
    for event in log.all():
        if event.event_type not in _RESPONSE_TYPES or event.actor is None:
            continue
        start = requested.get(event.approval_id)
        if start is None:
            continue
        sums[event.actor] += (event.timestamp - start).total_seconds()
        counts[event.actor] += 1
    return _averages(sums, counts)


def workflow_bottlenecks(
    store: ApprovalStore, log: ApprovalAuditLog
) -> list[tuple[str, float]]:
    """Return (workflow_id, average response seconds) ordered slowest first."""
    workflow_of = {r.approval_id: r.workflow_id for r in store.list()}
    requested = _request_times(log)
    sums: dict[str, float] = defaultdict(float)
    counts: dict[str, int] = defaultdict(int)
    for event in log.all():
        if event.event_type not in _RESPONSE_TYPES:
            continue
        workflow_id = workflow_of.get(event.approval_id)
        start = requested.get(event.approval_id)
        if workflow_id is None or start is None:
            continue
        sums[workflow_id] += (event.timestamp - start).total_seconds()
        counts[workflow_id] += 1
    return _averages(sums, counts)


def escalation_hotspots(store: ApprovalStore, log: ApprovalAuditLog) -> dict[str, int]:
    """Return the number of escalations per workflow."""
    workflow_of = {r.approval_id: r.workflow_id for r in store.list()}
    counter: Counter[str] = Counter()
    for event in log.by_type(ApprovalEventType.ESCALATED.value):
        workflow_id = workflow_of.get(event.approval_id)
        if workflow_id is not None:
            counter[workflow_id] += 1
    return dict(counter)


def analyze_bottlenecks(
    store: ApprovalStore, log: ApprovalAuditLog
) -> BottleneckReport:
    """Build a :class:`BottleneckReport` from a store and audit log."""
    return BottleneckReport(
        slowest_approvers=slowest_approvers(log),
        workflow_bottlenecks=workflow_bottlenecks(store, log),
        escalation_hotspots=escalation_hotspots(store, log),
    )
