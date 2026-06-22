"""Workflow pattern mining.

Finds recurring structure in the recorded history: workflows that run repeatedly,
steps that are repeatedly bottlenecks, and exceptions that recur. The per-workflow
run statistics computed here are shared by the success, failure, and maturity
modules. Everything is counted directly from the data.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from workflow_os.analytics.bottlenecks import Bottleneck, detect_bottlenecks
from workflow_os.exception.record import ExceptionRecord
from workflow_os.memory.events import MemoryEventType
from workflow_os.memory.record import MemoryRecord

_COMPLETED = str(MemoryEventType.WORKFLOW_COMPLETED)
_FAILED = str(MemoryEventType.WORKFLOW_FAILED)


@dataclass
class WorkflowRunStats:
    """Run counts for a single workflow id across the recorded history."""

    workflow_id: str
    runs: int
    successes: int
    failures: int
    success_rate: float
    failure_rate: float


def workflow_run_stats(
    records: Iterable[MemoryRecord],
) -> dict[str, WorkflowRunStats]:
    """Return per-workflow run statistics keyed by workflow id.

    A "run" is a terminal workflow event (``workflow_completed`` or
    ``workflow_failed``); repeated terminal events for the same id are repeated
    runs of that workflow.
    """
    successes: dict[str, int] = {}
    failures: dict[str, int] = {}
    for record in records:
        if record.event_type == _COMPLETED:
            successes[record.workflow_id] = successes.get(record.workflow_id, 0) + 1
        elif record.event_type == _FAILED:
            failures[record.workflow_id] = failures.get(record.workflow_id, 0) + 1

    stats: dict[str, WorkflowRunStats] = {}
    for workflow_id in sorted(set(successes) | set(failures)):
        ok = successes.get(workflow_id, 0)
        bad = failures.get(workflow_id, 0)
        runs = ok + bad
        stats[workflow_id] = WorkflowRunStats(
            workflow_id=workflow_id,
            runs=runs,
            successes=ok,
            failures=bad,
            success_rate=ok / runs if runs else 0.0,
            failure_rate=bad / runs if runs else 0.0,
        )
    return stats


def recurring_workflows(
    records: Iterable[MemoryRecord], *, min_runs: int = 2
) -> list[str]:
    """Return ids of workflows that ran at least ``min_runs`` times."""
    stats = workflow_run_stats(records)
    recurring = [s for s in stats.values() if s.runs >= min_runs]
    recurring.sort(key=lambda s: (-s.runs, s.workflow_id))
    return [s.workflow_id for s in recurring]


def recurring_bottlenecks(
    records: Iterable[MemoryRecord], *, min_occurrences: int = 2
) -> list[Bottleneck]:
    """Return bottleneck steps that occurred at least ``min_occurrences`` times."""
    return [
        bottleneck
        for bottleneck in detect_bottlenecks(records)
        if bottleneck.occurrences >= min_occurrences
    ]


def recurring_exceptions(
    exceptions: Iterable[ExceptionRecord], *, min_occurrences: int = 2
) -> dict[str, int]:
    """Return exception signatures that recur at least ``min_occurrences`` times.

    A signature is ``"<workflow_id>:<exception_type>"``.
    """
    counts: dict[str, int] = {}
    for exc in exceptions:
        signature = f"{exc.workflow_id}:{exc.exception_type}"
        counts[signature] = counts.get(signature, 0) + 1
    return {
        signature: count
        for signature, count in sorted(counts.items())
        if count >= min_occurrences
    }
