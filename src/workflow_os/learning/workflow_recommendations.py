"""Workflow improvement recommendations.

Turns observed patterns into concrete, deterministic suggestions: simplify
workflows that fail often, split workflows that have grown large, and remove the
steps that are recurring bottlenecks. Each recommendation is produced by a fixed
rule with evidence drawn from the recorded history.
"""

from __future__ import annotations

from collections.abc import Iterable

from workflow_os.learning.failure_patterns import frequently_failing_workflows
from workflow_os.learning.patterns import recurring_bottlenecks, workflow_run_stats
from workflow_os.learning.recommendation import Recommendation
from workflow_os.memory.events import MemoryEventType
from workflow_os.memory.record import MemoryRecord

_STEP_EVENTS = {
    str(MemoryEventType.STEP_STARTED),
    str(MemoryEventType.STEP_COMPLETED),
    str(MemoryEventType.STEP_FAILED),
    str(MemoryEventType.STEP_SKIPPED),
}


def _steps_per_workflow(records: Iterable[MemoryRecord]) -> dict[str, set[str]]:
    steps: dict[str, set[str]] = {}
    for record in records:
        if record.event_type in _STEP_EVENTS and record.step_id is not None:
            steps.setdefault(record.workflow_id, set()).add(record.step_id)
    return steps


def workflow_improvement_recommendations(
    records: Iterable[MemoryRecord],
    *,
    large_workflow_steps: int = 5,
    min_failures: int = 2,
    bottleneck_min_occurrences: int = 2,
) -> list[Recommendation]:
    """Return deterministic workflow improvement recommendations."""
    records = list(records)
    stats = workflow_run_stats(records)
    steps = _steps_per_workflow(records)
    recommendations: list[Recommendation] = []

    for workflow_id in frequently_failing_workflows(records, min_failures=min_failures):
        run = stats[workflow_id]
        recommendations.append(
            Recommendation.create(
                category="workflow",
                title=f"simplify {workflow_id}",
                description=(
                    f"{workflow_id} failed {run.failures} of {run.runs} runs; "
                    "consider simplifying it to improve reliability."
                ),
                severity="high",
                confidence=run.failure_rate,
                metadata={"workflow_id": workflow_id, "action": "simplify"},
            )
        )

    for workflow_id in sorted(steps):
        size = len(steps[workflow_id])
        if size >= large_workflow_steps:
            recommendations.append(
                Recommendation.create(
                    category="workflow",
                    title=f"split {workflow_id}",
                    description=(
                        f"{workflow_id} has {size} steps; consider splitting it "
                        "into smaller workflows."
                    ),
                    severity="medium",
                    confidence=1.0,
                    metadata={
                        "workflow_id": workflow_id,
                        "action": "split",
                        "step_count": size,
                    },
                )
            )

    for bottleneck in recurring_bottlenecks(
        records, min_occurrences=bottleneck_min_occurrences
    ):
        recommendations.append(
            Recommendation.create(
                category="workflow",
                title=f"remove bottleneck {bottleneck.step_id}",
                description=(
                    f"step {bottleneck.step_id!r} consumed "
                    f"{bottleneck.total_duration:.2f}s across "
                    f"{bottleneck.occurrences} runs; consider optimizing it."
                ),
                severity="medium",
                confidence=1.0,
                metadata={"step_id": bottleneck.step_id, "action": "remove_bottleneck"},
            )
        )

    return recommendations
