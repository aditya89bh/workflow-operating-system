"""Workflow completion metrics.

Measures how often workflows succeed, derived deterministically from the
organizational memory event stream. A workflow is considered observed if it has
any workflow-level event, and completed if it has a ``workflow_completed`` event.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from workflow_os.memory.events import MemoryEventType
from workflow_os.memory.record import MemoryRecord


@dataclass
class CompletionMetrics:
    """Aggregate workflow completion figures."""

    total_workflows: int = 0
    completed_workflows: int = 0
    completion_rate: float = 0.0


def _ids_with_event(
    records: Iterable[MemoryRecord], event_type: MemoryEventType
) -> set[str]:
    return {r.workflow_id for r in records if r.event_type == str(event_type)}


def started_workflow_ids(records: Iterable[MemoryRecord]) -> set[str]:
    """Return the ids of workflows that have a ``workflow_started`` event."""
    return _ids_with_event(records, MemoryEventType.WORKFLOW_STARTED)


def completed_workflow_ids(records: Iterable[MemoryRecord]) -> set[str]:
    """Return the ids of workflows that have a ``workflow_completed`` event."""
    return _ids_with_event(records, MemoryEventType.WORKFLOW_COMPLETED)


def observed_workflow_ids(records: Iterable[MemoryRecord]) -> set[str]:
    """Return the ids of workflows that have any workflow-level event."""
    records = list(records)
    return (
        started_workflow_ids(records)
        | completed_workflow_ids(records)
        | _ids_with_event(records, MemoryEventType.WORKFLOW_FAILED)
    )


def workflow_completion_metrics(records: Iterable[MemoryRecord]) -> CompletionMetrics:
    """Compute :class:`CompletionMetrics` for the given memory records."""
    records = list(records)
    observed = observed_workflow_ids(records)
    completed = completed_workflow_ids(records)
    total = len(observed)
    done = len(completed)
    rate = done / total if total else 0.0
    return CompletionMetrics(
        total_workflows=total, completed_workflows=done, completion_rate=rate
    )
