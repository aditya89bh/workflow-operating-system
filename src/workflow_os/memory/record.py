"""The :class:`MemoryRecord` schema.

A memory record is a single, immutable-ish fact about something that happened
during a workflow's life: an event with a type, a timestamp, an optional actor
and step, a confidence score, and free-form metadata.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def new_event_id() -> str:
    """Return a fresh, unique event id."""
    return uuid.uuid4().hex


def utcnow() -> datetime:
    """Return the current time as a timezone-aware UTC datetime."""
    return datetime.now(timezone.utc)


@dataclass
class MemoryRecord:
    """A structured record of a single workflow memory event.

    Attributes:
        event_id: Unique identifier for the event.
        workflow_id: Id of the workflow the event belongs to.
        event_type: The kind of event (see ``MemoryEventType`` values).
        timestamp: When the event occurred (timezone-aware UTC).
        step_id: Optional id of the step the event relates to.
        actor: Optional actor responsible for or attributed to the event.
        confidence: How much trust to place in the record, in ``[0.0, 1.0]``.
        metadata: Arbitrary key/value data attached to the event.
    """

    event_id: str
    workflow_id: str
    event_type: str
    timestamp: datetime
    step_id: str | None = None
    actor: str | None = None
    confidence: float = 1.0
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        *,
        workflow_id: str,
        event_type: str,
        step_id: str | None = None,
        actor: str | None = None,
        confidence: float = 1.0,
        metadata: dict[str, Any] | None = None,
        timestamp: datetime | None = None,
        event_id: str | None = None,
    ) -> MemoryRecord:
        """Build a :class:`MemoryRecord`, filling in id and timestamp by default."""
        return cls(
            event_id=event_id or new_event_id(),
            workflow_id=workflow_id,
            event_type=str(event_type),
            timestamp=timestamp or utcnow(),
            step_id=step_id,
            actor=actor,
            confidence=confidence,
            metadata=dict(metadata or {}),
        )
