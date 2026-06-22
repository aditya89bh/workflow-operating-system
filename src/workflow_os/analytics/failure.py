"""Workflow failure metrics.

Measures how often workflows fail, derived deterministically from the memory
event stream. A workflow is considered failed if it has a ``workflow_failed``
event.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from workflow_os.analytics.completion import observed_workflow_ids
from workflow_os.memory.events import MemoryEventType
from workflow_os.memory.record import MemoryRecord


@dataclass
class FailureMetrics:
    """Aggregate workflow failure figures."""

    total_workflows: int = 0
    failed_workflows: int = 0
    failure_rate: float = 0.0


def failed_workflow_ids(records: Iterable[MemoryRecord]) -> set[str]:
    """Return the ids of workflows that have a ``workflow_failed`` event."""
    return {
        r.workflow_id
        for r in records
        if r.event_type == str(MemoryEventType.WORKFLOW_FAILED)
    }


def workflow_failure_metrics(records: Iterable[MemoryRecord]) -> FailureMetrics:
    """Compute :class:`FailureMetrics` for the given memory records."""
    records = list(records)
    observed = observed_workflow_ids(records)
    failed = failed_workflow_ids(records)
    total = len(observed)
    failed_count = len(failed)
    rate = failed_count / total if total else 0.0
    return FailureMetrics(
        total_workflows=total, failed_workflows=failed_count, failure_rate=rate
    )
