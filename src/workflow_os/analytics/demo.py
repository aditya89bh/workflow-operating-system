"""Workflow analytics demonstration.

Executes a couple of workflows through the memory recorder, then runs the
analytics pipeline over the recorded events: metrics, reports, scorecards, and
CSV/JSON export. Everything is deterministic and rule-based.
"""

from __future__ import annotations

from workflow_os.analytics.bottlenecks import detect_bottlenecks
from workflow_os.analytics.completion import workflow_completion_metrics
from workflow_os.analytics.csv_export import to_csv
from workflow_os.analytics.duration import execution_duration_metrics
from workflow_os.analytics.execution_summary import execution_summaries
from workflow_os.analytics.failure import workflow_failure_metrics
from workflow_os.analytics.health import workflow_health_score
from workflow_os.analytics.json_export import to_json
from workflow_os.analytics.reports import workflow_statistics
from workflow_os.analytics.scorecards import workflow_scorecards
from workflow_os.memory.recorder import MemoryRecorder
from workflow_os.memory.sqlite_store import SQLiteMemoryStore
from workflow_os.step import WorkflowStep
from workflow_os.workflow import Workflow


def _build_workflow(workflow_id: str, name: str) -> Workflow:
    return Workflow(
        id=workflow_id,
        name=name,
        steps=[
            WorkflowStep(id="collect", name="Collect documents"),
            WorkflowStep(id="review", name="Review", dependencies=["collect"]),
            WorkflowStep(id="finalize", name="Finalize", dependencies=["review"]),
        ],
    )


def run_demo() -> None:
    """Run the workflow analytics demonstration and print a summary."""
    store = SQLiteMemoryStore(":memory:")
    recorder = MemoryRecorder(store)

    # Two successful runs and one that fails partway through.
    recorder.run(_build_workflow("onboarding-1", "Onboarding 1"))
    recorder.run(_build_workflow("onboarding-2", "Onboarding 2"))

    failing = _build_workflow("onboarding-3", "Onboarding 3")
    recorder.start(failing)
    first, second = failing.steps[0], failing.steps[1]
    recorder.start_step(failing, first)
    recorder.complete_step(failing, first)
    recorder.start_step(failing, second)
    recorder.fail_step(failing, second, reason="missing data")
    recorder.fail(failing, reason="review failed")

    records = store.list()
    print(f"recorded {len(records)} memory events from 3 workflow runs")

    completion = workflow_completion_metrics(records)
    failure = workflow_failure_metrics(records)
    duration = execution_duration_metrics(records)
    print(
        "metrics: "
        f"completion_rate={completion.completion_rate:.2f} "
        f"failure_rate={failure.failure_rate:.2f} "
        f"mean_duration={duration.mean:.4f}s"
    )

    stats = workflow_statistics(records)
    print(
        f"statistics: total={stats.total_workflows} "
        f"completed={stats.completed_workflows} failed={stats.failed_workflows}"
    )

    print("execution summaries:")
    for summary in execution_summaries(records):
        print(
            f"  {summary.workflow_id}: status={summary.status} "
            f"steps_completed={summary.steps_completed} "
            f"steps_failed={summary.steps_failed}"
        )

    bottlenecks = detect_bottlenecks(records, limit=3)
    print("top bottlenecks:")
    for bottleneck in bottlenecks:
        print(
            f"  {bottleneck.step_id}: total={bottleneck.total_duration:.4f}s "
            f"occurrences={bottleneck.occurrences}"
        )

    health = workflow_health_score(records)
    print(f"health score: {health.score:.3f}")

    print("scorecards:")
    for card in workflow_scorecards(records):
        print(f"  {card.subject_id}: {card.score:.2f}")

    csv_text = to_csv(execution_summaries(records), fieldnames=["workflow_id", "status"])
    print(f"csv export ({len(csv_text.splitlines())} lines):")
    print(csv_text.strip())

    json_text = to_json(stats)
    print(f"json export: {len(json_text)} chars")


if __name__ == "__main__":  # pragma: no cover
    run_demo()
