"""Execution duration metrics.

Measures how long workflows take, using the ``duration_seconds`` metadata that
the memory recorder attaches to terminal workflow events. All figures are simple
deterministic aggregates - no estimation or smoothing.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass

from workflow_os.memory.events import MemoryEventType
from workflow_os.memory.record import MemoryRecord

DURATION_KEY = "duration_seconds"

WORKFLOW_TERMINAL_EVENTS = frozenset(
    {
        str(MemoryEventType.WORKFLOW_COMPLETED),
        str(MemoryEventType.WORKFLOW_FAILED),
    }
)


@dataclass
class DurationMetrics:
    """Aggregate duration figures in seconds."""

    count: int = 0
    total: float = 0.0
    mean: float = 0.0
    minimum: float = 0.0
    maximum: float = 0.0


def summarize_durations(values: Sequence[float]) -> DurationMetrics:
    """Summarize a sequence of durations into :class:`DurationMetrics`."""
    if not values:
        return DurationMetrics()
    total = float(sum(values))
    count = len(values)
    return DurationMetrics(
        count=count,
        total=total,
        mean=total / count,
        minimum=float(min(values)),
        maximum=float(max(values)),
    )


def _duration_of(record: MemoryRecord) -> float | None:
    value = record.metadata.get(DURATION_KEY)
    if isinstance(value, (int, float)):
        return float(value)
    return None


def workflow_durations(records: Iterable[MemoryRecord]) -> dict[str, float]:
    """Return the recorded duration for each workflow that finished."""
    durations: dict[str, float] = {}
    for record in records:
        if record.event_type in WORKFLOW_TERMINAL_EVENTS:
            value = _duration_of(record)
            if value is not None:
                durations[record.workflow_id] = value
    return durations


def execution_duration_metrics(records: Iterable[MemoryRecord]) -> DurationMetrics:
    """Compute aggregate workflow execution duration metrics."""
    return summarize_durations(list(workflow_durations(records).values()))
