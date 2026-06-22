"""Step duration metrics.

Measures how long individual steps take, using the ``duration_seconds`` metadata
attached to terminal step events. Durations are grouped by step id so a step that
runs many times across workflows is aggregated together.
"""

from __future__ import annotations

from collections.abc import Iterable

from workflow_os.analytics.duration import (
    DURATION_KEY,
    DurationMetrics,
    summarize_durations,
)
from workflow_os.memory.events import MemoryEventType
from workflow_os.memory.record import MemoryRecord

STEP_TERMINAL_EVENTS = frozenset(
    {
        str(MemoryEventType.STEP_COMPLETED),
        str(MemoryEventType.STEP_FAILED),
    }
)


def _duration_of(record: MemoryRecord) -> float | None:
    value = record.metadata.get(DURATION_KEY)
    if isinstance(value, (int, float)):
        return float(value)
    return None


def step_durations(records: Iterable[MemoryRecord]) -> dict[str, list[float]]:
    """Return recorded durations grouped by step id."""
    durations: dict[str, list[float]] = {}
    for record in records:
        if record.event_type in STEP_TERMINAL_EVENTS and record.step_id is not None:
            value = _duration_of(record)
            if value is not None:
                durations.setdefault(record.step_id, []).append(value)
    return durations


def step_duration_metrics(
    records: Iterable[MemoryRecord],
) -> dict[str, DurationMetrics]:
    """Return aggregate duration metrics per step id."""
    return {
        step_id: summarize_durations(values)
        for step_id, values in step_durations(records).items()
    }
