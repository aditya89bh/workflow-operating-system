"""Workflow health scores.

Combines several deterministic signals into a single ``[0, 1]`` health score:
the workflow success rate, the failure rate, the number of bottleneck steps, and
the exception recovery rate. The score is a fixed weighted blend - it is fully
explainable and carries no learned weights or predictions.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from workflow_os.analytics.bottlenecks import detect_bottlenecks
from workflow_os.analytics.completion import workflow_completion_metrics
from workflow_os.analytics.failure import workflow_failure_metrics
from workflow_os.exception.record import ExceptionRecord
from workflow_os.memory.record import MemoryRecord

SUCCESS_WEIGHT = 0.4
FAILURE_WEIGHT = 0.3
RECOVERY_WEIGHT = 0.2
BOTTLENECK_WEIGHT = 0.1


@dataclass
class HealthScore:
    """A workflow health score and the components that produced it."""

    score: float
    success_rate: float
    failure_rate: float
    bottleneck_count: int
    recovery_rate: float


def _bottleneck_count(records: list[MemoryRecord]) -> int:
    bottlenecks = detect_bottlenecks(records)
    if not bottlenecks:
        return 0
    average = sum(b.total_duration for b in bottlenecks) / len(bottlenecks)
    return sum(1 for b in bottlenecks if b.total_duration > average)


def _recovery_rate(exceptions: list[ExceptionRecord]) -> float:
    if not exceptions:
        return 1.0
    resolved = sum(1 for e in exceptions if e.resolved)
    return resolved / len(exceptions)


def workflow_health_score(
    records: Iterable[MemoryRecord],
    *,
    exceptions: Iterable[ExceptionRecord] | None = None,
) -> HealthScore:
    """Compute a deterministic :class:`HealthScore` for the recorded activity."""
    records = list(records)
    exception_list = list(exceptions or [])

    success_rate = workflow_completion_metrics(records).completion_rate
    failure_rate = workflow_failure_metrics(records).failure_rate
    bottleneck_count = _bottleneck_count(records)
    recovery_rate = _recovery_rate(exception_list)

    bottleneck_health = 1.0 / (1 + bottleneck_count)
    score = (
        SUCCESS_WEIGHT * success_rate
        + FAILURE_WEIGHT * (1.0 - failure_rate)
        + RECOVERY_WEIGHT * recovery_rate
        + BOTTLENECK_WEIGHT * bottleneck_health
    )
    score = max(0.0, min(1.0, score))

    return HealthScore(
        score=score,
        success_rate=success_rate,
        failure_rate=failure_rate,
        bottleneck_count=bottleneck_count,
        recovery_rate=recovery_rate,
    )
