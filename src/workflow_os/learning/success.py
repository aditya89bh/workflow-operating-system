"""Successful workflow detection.

Identifies the workflows the organization runs well: those with the highest
success rate, those that are reliable across many runs, and those that are
consistently healthy (every recorded run succeeded). Findings are surfaced as
deterministic insights.
"""

from __future__ import annotations

from collections.abc import Iterable

from workflow_os.learning.insight import OrganizationalInsight
from workflow_os.learning.patterns import WorkflowRunStats, workflow_run_stats
from workflow_os.memory.record import MemoryRecord


def highest_success_rate_workflows(
    records: Iterable[MemoryRecord],
    *,
    min_runs: int = 1,
    limit: int | None = None,
) -> list[WorkflowRunStats]:
    """Return workflows ranked by success rate (then run count), best first."""
    stats = [
        s for s in workflow_run_stats(records).values() if s.runs >= min_runs
    ]
    stats.sort(key=lambda s: (-s.success_rate, -s.runs, s.workflow_id))
    if limit is not None:
        stats = stats[:limit]
    return stats


def most_reliable_workflows(
    records: Iterable[MemoryRecord],
    *,
    min_runs: int = 2,
    min_success_rate: float = 0.8,
) -> list[str]:
    """Return ids of workflows with many runs and a high success rate."""
    stats = workflow_run_stats(records)
    reliable = [
        s
        for s in stats.values()
        if s.runs >= min_runs and s.success_rate >= min_success_rate
    ]
    reliable.sort(key=lambda s: (-s.success_rate, -s.runs, s.workflow_id))
    return [s.workflow_id for s in reliable]


def consistently_healthy_workflows(
    records: Iterable[MemoryRecord], *, min_runs: int = 2
) -> list[str]:
    """Return ids of workflows where every recorded run succeeded."""
    stats = workflow_run_stats(records)
    healthy = [
        s.workflow_id
        for s in stats.values()
        if s.runs >= min_runs and s.failures == 0
    ]
    return sorted(healthy)


def successful_workflow_insights(
    records: Iterable[MemoryRecord], *, min_runs: int = 2
) -> list[OrganizationalInsight]:
    """Return insights describing consistently healthy workflows."""
    records = list(records)
    stats = workflow_run_stats(records)
    insights: list[OrganizationalInsight] = []
    for workflow_id in consistently_healthy_workflows(records, min_runs=min_runs):
        run = stats[workflow_id]
        insights.append(
            OrganizationalInsight.create(
                category="success",
                title=f"{workflow_id} is consistently healthy",
                description=(
                    f"{workflow_id} succeeded in all {run.runs} recorded runs."
                ),
                evidence=[f"runs={run.runs}", f"success_rate={run.success_rate:.2f}"],
                confidence=1.0,
                metadata={"workflow_id": workflow_id},
            )
        )
    return insights
