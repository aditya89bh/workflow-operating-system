"""Execution summaries.

Builds a per-workflow execution summary from the memory event stream: when the
run started and ended, its final status, how long it took, and how many steps
completed or failed. Summaries are derived purely from recorded events.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime

from workflow_os.analytics.completion import (
    completed_workflow_ids,
    observed_workflow_ids,
)
from workflow_os.analytics.failure import failed_workflow_ids
from workflow_os.memory.events import MemoryEventType
from workflow_os.memory.record import MemoryRecord


@dataclass
class ExecutionSummary:
    """A summary of a single workflow execution."""

    workflow_id: str
    status: str
    started_at: datetime | None
    ended_at: datetime | None
    duration: float | None
    steps_completed: int
    steps_failed: int


def _first_timestamp(
    records: list[MemoryRecord], workflow_id: str, event_type: MemoryEventType
) -> datetime | None:
    times = [
        r.timestamp
        for r in records
        if r.workflow_id == workflow_id and r.event_type == str(event_type)
    ]
    return min(times) if times else None


def execution_summaries(
    records: Iterable[MemoryRecord],
) -> list[ExecutionSummary]:
    """Return an :class:`ExecutionSummary` for each observed workflow."""
    records = list(records)
    completed = completed_workflow_ids(records)
    failed = failed_workflow_ids(records)

    summaries: list[ExecutionSummary] = []
    for workflow_id in sorted(observed_workflow_ids(records)):
        started_at = _first_timestamp(
            records, workflow_id, MemoryEventType.WORKFLOW_STARTED
        )
        if workflow_id in completed:
            status = "completed"
            ended_at = _first_timestamp(
                records, workflow_id, MemoryEventType.WORKFLOW_COMPLETED
            )
        elif workflow_id in failed:
            status = "failed"
            ended_at = _first_timestamp(
                records, workflow_id, MemoryEventType.WORKFLOW_FAILED
            )
        else:
            status = "running"
            ended_at = None

        duration: float | None = None
        if started_at is not None and ended_at is not None:
            duration = (ended_at - started_at).total_seconds()

        steps_completed = sum(
            1
            for r in records
            if r.workflow_id == workflow_id
            and r.event_type == str(MemoryEventType.STEP_COMPLETED)
        )
        steps_failed = sum(
            1
            for r in records
            if r.workflow_id == workflow_id
            and r.event_type == str(MemoryEventType.STEP_FAILED)
        )

        summaries.append(
            ExecutionSummary(
                workflow_id=workflow_id,
                status=status,
                started_at=started_at,
                ended_at=ended_at,
                duration=duration,
                steps_completed=steps_completed,
                steps_failed=steps_failed,
            )
        )
    return summaries
