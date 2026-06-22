"""Exception clustering.

Groups exception records along common dimensions - type, workflow, severity, and
recovery outcome - so related failures can be examined together. Clustering is a
deterministic grouping; it performs no inference.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable, Iterable

from workflow_os.exception.record import ExceptionRecord
from workflow_os.exception.recovery import RecoveryAction, RecoveryStatus


def _group(
    exceptions: Iterable[ExceptionRecord], key: Callable[[ExceptionRecord], str]
) -> dict[str, list[ExceptionRecord]]:
    clusters: dict[str, list[ExceptionRecord]] = defaultdict(list)
    for exception in exceptions:
        clusters[key(exception)].append(exception)
    return dict(clusters)


def cluster_by_type(
    exceptions: Iterable[ExceptionRecord],
) -> dict[str, list[ExceptionRecord]]:
    """Group exceptions by their classification type."""
    return _group(exceptions, lambda e: e.exception_type)


def cluster_by_workflow(
    exceptions: Iterable[ExceptionRecord],
) -> dict[str, list[ExceptionRecord]]:
    """Group exceptions by workflow id."""
    return _group(exceptions, lambda e: e.workflow_id)


def cluster_by_severity(
    exceptions: Iterable[ExceptionRecord],
) -> dict[str, list[ExceptionRecord]]:
    """Group exceptions by severity."""
    return _group(exceptions, lambda e: e.severity)


def recovery_outcome(
    exception_id: str, recoveries: Iterable[RecoveryAction]
) -> str:
    """Return the recovery outcome for an exception.

    ``succeeded`` if any recovery succeeded, ``failed`` if recoveries exist but
    none succeeded, otherwise ``none`` when no recovery was attempted.
    """
    statuses = [r.status for r in recoveries if r.exception_id == exception_id]
    if not statuses:
        return "none"
    if RecoveryStatus.SUCCEEDED.value in statuses:
        return RecoveryStatus.SUCCEEDED.value
    return RecoveryStatus.FAILED.value


def cluster_by_recovery_outcome(
    exceptions: Iterable[ExceptionRecord],
    recoveries: Iterable[RecoveryAction],
) -> dict[str, list[ExceptionRecord]]:
    """Group exceptions by their recovery outcome."""
    recoveries = list(recoveries)
    return _group(
        exceptions, lambda e: recovery_outcome(e.exception_id, recoveries)
    )
