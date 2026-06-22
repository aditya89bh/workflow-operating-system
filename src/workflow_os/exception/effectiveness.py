"""Recovery effectiveness metrics.

Deterministic measures of how well recovery is working: the overall recovery
success rate, the retry success rate, and the mean time to recover. Rates are
computed over resolved (succeeded or failed) recovery actions only.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from workflow_os.exception.record import ExceptionRecord
from workflow_os.exception.recovery import RecoveryAction, RecoveryStatus

_RETRY_ACTION = "retry"


def _success_rate(recoveries: list[RecoveryAction]) -> float:
    resolved = [
        r
        for r in recoveries
        if r.status
        in {RecoveryStatus.SUCCEEDED.value, RecoveryStatus.FAILED.value}
    ]
    if not resolved:
        return 0.0
    succeeded = sum(1 for r in resolved if r.status == RecoveryStatus.SUCCEEDED.value)
    return succeeded / len(resolved)


@dataclass
class EffectivenessMetrics:
    """A snapshot of recovery effectiveness."""

    recovery_success_rate: float = 0.0
    retry_success_rate: float = 0.0
    mean_recovery_seconds: float | None = None
    total_recoveries: int = 0
    successful_recoveries: int = 0


def recovery_success_rate(recoveries: Iterable[RecoveryAction]) -> float:
    """Return the fraction of resolved recoveries that succeeded."""
    return _success_rate(list(recoveries))


def retry_success_rate(recoveries: Iterable[RecoveryAction]) -> float:
    """Return the success rate of retry recoveries specifically."""
    retries = [r for r in recoveries if r.action == _RETRY_ACTION]
    return _success_rate(retries)


def mean_recovery_time(
    exceptions: Iterable[ExceptionRecord],
    recoveries: Iterable[RecoveryAction],
) -> float | None:
    """Return the mean seconds between detection and successful recovery."""
    detected = {e.exception_id: e.detected_at for e in exceptions}
    durations: list[float] = []
    for recovery in recoveries:
        if recovery.status != RecoveryStatus.SUCCEEDED.value:
            continue
        start = detected.get(recovery.exception_id)
        if start is None:
            continue
        durations.append((recovery.timestamp - start).total_seconds())
    if not durations:
        return None
    return sum(durations) / len(durations)


def compute_effectiveness(
    exceptions: Iterable[ExceptionRecord],
    recoveries: Iterable[RecoveryAction],
) -> EffectivenessMetrics:
    """Build an :class:`EffectivenessMetrics` snapshot."""
    recoveries = list(recoveries)
    successful = sum(
        1 for r in recoveries if r.status == RecoveryStatus.SUCCEEDED.value
    )
    return EffectivenessMetrics(
        recovery_success_rate=recovery_success_rate(recoveries),
        retry_success_rate=retry_success_rate(recoveries),
        mean_recovery_seconds=mean_recovery_time(exceptions, recoveries),
        total_recoveries=len(recoveries),
        successful_recoveries=successful,
    )
