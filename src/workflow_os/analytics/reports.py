"""Workflow reports.

Brings the individual metrics together into reusable reports: per-workflow
summaries, aggregate statistics, and simple completion trends over time. The day
bucketing helper here is shared by the dedicated trend analysis module.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field

from workflow_os.analytics.completion import (
    completed_workflow_ids,
    observed_workflow_ids,
    workflow_completion_metrics,
)
from workflow_os.analytics.duration import (
    DurationMetrics,
    execution_duration_metrics,
    workflow_durations,
)
from workflow_os.analytics.failure import (
    failed_workflow_ids,
    workflow_failure_metrics,
)
from workflow_os.memory.events import MemoryEventType
from workflow_os.memory.record import MemoryRecord


@dataclass
class WorkflowSummary:
    """A one-line summary of a single workflow."""

    workflow_id: str
    status: str
    duration: float | None
    step_count: int


@dataclass
class WorkflowStatistics:
    """Aggregate statistics across all observed workflows."""

    total_workflows: int = 0
    completed_workflows: int = 0
    failed_workflows: int = 0
    completion_rate: float = 0.0
    failure_rate: float = 0.0
    duration: DurationMetrics = field(default_factory=DurationMetrics)


def _status(workflow_id: str, completed: set[str], failed: set[str]) -> str:
    if workflow_id in completed:
        return "completed"
    if workflow_id in failed:
        return "failed"
    return "running"


def counts_by_day(
    records: Iterable[MemoryRecord], event_type: str
) -> dict[str, int]:
    """Return a count of events of ``event_type`` bucketed by UTC date."""
    counts: dict[str, int] = {}
    for record in records:
        if record.event_type == str(event_type):
            day = record.timestamp.date().isoformat()
            counts[day] = counts.get(day, 0) + 1
    return dict(sorted(counts.items()))


def workflow_summaries(records: Iterable[MemoryRecord]) -> list[WorkflowSummary]:
    """Return a :class:`WorkflowSummary` for each observed workflow."""
    records = list(records)
    completed = completed_workflow_ids(records)
    failed = failed_workflow_ids(records)
    durations = workflow_durations(records)
    step_counts: dict[str, int] = {}
    for record in records:
        if record.step_id is not None and record.event_type in {
            str(MemoryEventType.STEP_COMPLETED),
            str(MemoryEventType.STEP_FAILED),
            str(MemoryEventType.STEP_SKIPPED),
        }:
            step_counts[record.workflow_id] = (
                step_counts.get(record.workflow_id, 0) + 1
            )
    return [
        WorkflowSummary(
            workflow_id=workflow_id,
            status=_status(workflow_id, completed, failed),
            duration=durations.get(workflow_id),
            step_count=step_counts.get(workflow_id, 0),
        )
        for workflow_id in sorted(observed_workflow_ids(records))
    ]


def workflow_statistics(records: Iterable[MemoryRecord]) -> WorkflowStatistics:
    """Return aggregate :class:`WorkflowStatistics`."""
    records = list(records)
    completion = workflow_completion_metrics(records)
    failure = workflow_failure_metrics(records)
    return WorkflowStatistics(
        total_workflows=completion.total_workflows,
        completed_workflows=completion.completed_workflows,
        failed_workflows=failure.failed_workflows,
        completion_rate=completion.completion_rate,
        failure_rate=failure.failure_rate,
        duration=execution_duration_metrics(records),
    )


def workflow_trends(records: Iterable[MemoryRecord]) -> dict[str, int]:
    """Return workflow completions per UTC day."""
    return counts_by_day(records, str(MemoryEventType.WORKFLOW_COMPLETED))


__all__ = [
    "WorkflowStatistics",
    "WorkflowSummary",
    "counts_by_day",
    "workflow_statistics",
    "workflow_summaries",
    "workflow_trends",
]
