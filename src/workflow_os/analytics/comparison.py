"""Workflow comparison reports.

Compares workflows against one another using the recorded event stream: whether
each finished, how long it took, and how many steps it ran. The comparison also
identifies the fastest and slowest finished workflows. Everything is derived
deterministically from the data.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field

from workflow_os.analytics.completion import (
    completed_workflow_ids,
    observed_workflow_ids,
)
from workflow_os.analytics.duration import workflow_durations
from workflow_os.analytics.failure import failed_workflow_ids
from workflow_os.analytics.step_duration import STEP_TERMINAL_EVENTS
from workflow_os.memory.record import MemoryRecord


@dataclass
class WorkflowComparisonRow:
    """A single workflow's figures within a comparison."""

    workflow_id: str
    completed: bool
    failed: bool
    duration: float | None
    step_count: int


@dataclass
class WorkflowComparison:
    """A comparison across several workflows."""

    rows: list[WorkflowComparisonRow] = field(default_factory=list)
    fastest: str | None = None
    slowest: str | None = None


def _step_counts(records: Iterable[MemoryRecord]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for record in records:
        if record.event_type in STEP_TERMINAL_EVENTS:
            counts[record.workflow_id] = counts.get(record.workflow_id, 0) + 1
    return counts


def compare_workflows(records: Iterable[MemoryRecord]) -> WorkflowComparison:
    """Build a :class:`WorkflowComparison` across all observed workflows."""
    records = list(records)
    observed = sorted(observed_workflow_ids(records))
    completed = completed_workflow_ids(records)
    failed = failed_workflow_ids(records)
    durations = workflow_durations(records)
    step_counts = _step_counts(records)

    rows = [
        WorkflowComparisonRow(
            workflow_id=workflow_id,
            completed=workflow_id in completed,
            failed=workflow_id in failed,
            duration=durations.get(workflow_id),
            step_count=step_counts.get(workflow_id, 0),
        )
        for workflow_id in observed
    ]

    timed = {wid: d for wid, d in durations.items() if wid in observed}
    fastest = min(timed, key=lambda w: (timed[w], w)) if timed else None
    slowest = max(timed, key=lambda w: (timed[w], w)) if timed else None

    return WorkflowComparison(rows=rows, fastest=fastest, slowest=slowest)
