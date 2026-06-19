"""Confidence scoring for memory records.

Each event type is assigned a default confidence describing how much trust to
place in the recorded fact. Observed lifecycle events (a workflow completing, a
step starting) are high confidence; failure events are medium confidence
because the underlying cause is often uncertain. Manually recorded events use a
configurable confidence supplied by the caller.
"""

from __future__ import annotations

from collections.abc import Mapping

from workflow_os.memory.events import MemoryEventType

HIGH_CONFIDENCE = 0.9
MEDIUM_CONFIDENCE = 0.6
LOW_CONFIDENCE = 0.3
DEFAULT_CONFIDENCE = 0.5
DEFAULT_MANUAL_CONFIDENCE = 0.5

CONFIDENCE_BY_EVENT_TYPE: dict[str, float] = {
    MemoryEventType.WORKFLOW_STARTED.value: HIGH_CONFIDENCE,
    MemoryEventType.WORKFLOW_PAUSED.value: HIGH_CONFIDENCE,
    MemoryEventType.WORKFLOW_RESUMED.value: HIGH_CONFIDENCE,
    MemoryEventType.WORKFLOW_COMPLETED.value: HIGH_CONFIDENCE,
    MemoryEventType.WORKFLOW_FAILED.value: MEDIUM_CONFIDENCE,
    MemoryEventType.STEP_STARTED.value: HIGH_CONFIDENCE,
    MemoryEventType.STEP_COMPLETED.value: HIGH_CONFIDENCE,
    MemoryEventType.STEP_FAILED.value: MEDIUM_CONFIDENCE,
    MemoryEventType.STEP_SKIPPED.value: MEDIUM_CONFIDENCE,
}


def confidence_for(
    event_type: str,
    *,
    manual: bool = False,
    manual_confidence: float = DEFAULT_MANUAL_CONFIDENCE,
    overrides: Mapping[str, float] | None = None,
) -> float:
    """Return the confidence score for an event type.

    Args:
        event_type: The event type to score.
        manual: If ``True``, the event was recorded by hand and
            ``manual_confidence`` is used directly.
        manual_confidence: The confidence to use for manual events.
        overrides: Optional per-event-type overrides applied before the
            built-in defaults.
    """
    if manual:
        return manual_confidence
    key = str(event_type)
    if overrides is not None and key in overrides:
        return overrides[key]
    return CONFIDENCE_BY_EVENT_TYPE.get(key, DEFAULT_CONFIDENCE)
