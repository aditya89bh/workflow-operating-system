"""Memory event type definitions.

These are the canonical event types recorded by the memory system. They are
plain strings so they serialise cleanly and compare directly with the
``event_type`` field on :class:`~workflow_os.memory.record.MemoryRecord`.
"""

from __future__ import annotations

from enum import Enum


class MemoryEventType(str, Enum):
    """The kinds of events the memory system records."""

    WORKFLOW_STARTED = "workflow_started"
    WORKFLOW_PAUSED = "workflow_paused"
    WORKFLOW_RESUMED = "workflow_resumed"
    WORKFLOW_COMPLETED = "workflow_completed"
    WORKFLOW_FAILED = "workflow_failed"
    STEP_STARTED = "step_started"
    STEP_COMPLETED = "step_completed"
    STEP_FAILED = "step_failed"
    STEP_SKIPPED = "step_skipped"

    def __str__(self) -> str:  # pragma: no cover - convenience only
        return self.value


WORKFLOW_EVENT_TYPES: frozenset[MemoryEventType] = frozenset(
    {
        MemoryEventType.WORKFLOW_STARTED,
        MemoryEventType.WORKFLOW_PAUSED,
        MemoryEventType.WORKFLOW_RESUMED,
        MemoryEventType.WORKFLOW_COMPLETED,
        MemoryEventType.WORKFLOW_FAILED,
    }
)

STEP_EVENT_TYPES: frozenset[MemoryEventType] = frozenset(
    {
        MemoryEventType.STEP_STARTED,
        MemoryEventType.STEP_COMPLETED,
        MemoryEventType.STEP_FAILED,
        MemoryEventType.STEP_SKIPPED,
    }
)
