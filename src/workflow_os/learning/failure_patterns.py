"""Failure pattern detection.

Identifies where the organization struggles: workflows that fail frequently, the
steps that are failure hotspots, and workflows that are unstable (a mix of
successes and failures across runs). Findings are surfaced as deterministic
insights.
"""

from __future__ import annotations

from collections.abc import Iterable

from workflow_os.learning.insight import OrganizationalInsight
from workflow_os.learning.patterns import workflow_run_stats
from workflow_os.memory.events import MemoryEventType
from workflow_os.memory.record import MemoryRecord

_STEP_FAILED = str(MemoryEventType.STEP_FAILED)


def frequently_failing_workflows(
    records: Iterable[MemoryRecord], *, min_failures: int = 2
) -> list[str]:
    """Return ids of workflows that failed at least ``min_failures`` times."""
    stats = workflow_run_stats(records)
    failing = [s for s in stats.values() if s.failures >= min_failures]
    failing.sort(key=lambda s: (-s.failures, s.workflow_id))
    return [s.workflow_id for s in failing]


def failure_hotspots(
    records: Iterable[MemoryRecord], *, min_failures: int = 2
) -> list[tuple[str, int]]:
    """Return ``(step_id, failure_count)`` for steps that fail repeatedly."""
    counts: dict[str, int] = {}
    for record in records:
        if record.event_type == _STEP_FAILED and record.step_id is not None:
            counts[record.step_id] = counts.get(record.step_id, 0) + 1
    hotspots = [
        (step_id, count) for step_id, count in counts.items() if count >= min_failures
    ]
    hotspots.sort(key=lambda item: (-item[1], item[0]))
    return hotspots


def unstable_workflows(
    records: Iterable[MemoryRecord], *, min_runs: int = 2
) -> list[str]:
    """Return ids of workflows with both successes and failures across runs."""
    stats = workflow_run_stats(records)
    unstable = [
        s.workflow_id
        for s in stats.values()
        if s.runs >= min_runs and 0 < s.failures < s.runs
    ]
    return sorted(unstable)


def failure_pattern_insights(
    records: Iterable[MemoryRecord], *, min_failures: int = 2
) -> list[OrganizationalInsight]:
    """Return insights describing frequently failing workflows."""
    records = list(records)
    stats = workflow_run_stats(records)
    insights: list[OrganizationalInsight] = []
    for workflow_id in frequently_failing_workflows(records, min_failures=min_failures):
        run = stats[workflow_id]
        insights.append(
            OrganizationalInsight.create(
                category="failure",
                title=f"{workflow_id} fails frequently",
                description=(
                    f"{workflow_id} failed {run.failures} of {run.runs} runs."
                ),
                evidence=[
                    f"failures={run.failures}",
                    f"failure_rate={run.failure_rate:.2f}",
                ],
                confidence=run.failure_rate,
                metadata={"workflow_id": workflow_id},
            )
        )
    return insights
