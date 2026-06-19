"""Retrieval helpers for workflow and step execution history.

These functions read from any :class:`~workflow_os.memory.store.MemoryStore`
and present recorded events as ordered histories and timelines.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from workflow_os.memory.record import MemoryRecord
from workflow_os.memory.store import MemoryQuery, MemoryStore


@dataclass
class TimelineEntry:
    """A single point on a workflow execution timeline.

    Attributes:
        timestamp: When the event occurred.
        event_type: The recorded event type.
        step_id: The related step id, if any.
        offset_seconds: Seconds elapsed since the first event in the timeline.
    """

    timestamp: datetime
    event_type: str
    step_id: str | None
    offset_seconds: float


def get_execution_timeline(
    store: MemoryStore, workflow_id: str
) -> list[TimelineEntry]:
    """Return the ordered execution timeline for a workflow.

    Each entry carries its offset (in seconds) from the first recorded event,
    making it easy to see how a run unfolded over time.
    """
    records = store.query(MemoryQuery(workflow_id=workflow_id))
    if not records:
        return []
    start = records[0].timestamp
    return [
        TimelineEntry(
            timestamp=record.timestamp,
            event_type=record.event_type,
            step_id=record.step_id,
            offset_seconds=(record.timestamp - start).total_seconds(),
        )
        for record in records
    ]


def get_workflow_records(store: MemoryStore, workflow_id: str) -> list[MemoryRecord]:
    """Return all recorded events for a workflow, ordered by timestamp."""
    return store.query(MemoryQuery(workflow_id=workflow_id))


def get_step_records(
    store: MemoryStore, workflow_id: str, step_id: str
) -> list[MemoryRecord]:
    """Return all recorded events for a single step, ordered by timestamp."""
    return store.query(MemoryQuery(workflow_id=workflow_id, step_id=step_id))


def get_step_timeline(
    store: MemoryStore, workflow_id: str, step_id: str
) -> list[TimelineEntry]:
    """Return the ordered execution timeline for a single step.

    Offsets are measured from the first recorded event for the step, so each
    step timeline starts at zero.
    """
    records = get_step_records(store, workflow_id, step_id)
    if not records:
        return []
    start = records[0].timestamp
    return [
        TimelineEntry(
            timestamp=record.timestamp,
            event_type=record.event_type,
            step_id=record.step_id,
            offset_seconds=(record.timestamp - start).total_seconds(),
        )
        for record in records
    ]
