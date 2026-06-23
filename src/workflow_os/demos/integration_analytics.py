"""Workflow + analytics integration demonstration.

Shows the flow ``workflow -> metrics -> reports -> exports``: several workflows are
executed, aggregate metrics and statistics are computed over the recorded events,
and the results are exported to CSV and JSON.
"""

from __future__ import annotations

from workflow_os.analytics.completion import workflow_completion_metrics
from workflow_os.analytics.csv_export import to_csv
from workflow_os.analytics.duration import execution_duration_metrics
from workflow_os.analytics.execution_summary import execution_summaries
from workflow_os.analytics.failure import workflow_failure_metrics
from workflow_os.analytics.json_export import to_json
from workflow_os.analytics.reports import workflow_statistics
from workflow_os.demos.employee_onboarding import build_workflow as build_onboarding
from workflow_os.demos.procurement import build_workflow as build_procurement
from workflow_os.memory.recorder import MemoryRecorder
from workflow_os.memory.sqlite_store import SQLiteMemoryStore


def run_demo() -> None:
    """Run the workflow-analytics integration demonstration and print a summary."""
    store = SQLiteMemoryStore(":memory:")
    recorder = MemoryRecorder(store)

    # 1. Workflow: execute a few workflows (with one failure).
    print("1. workflow -> executing several runs")
    recorder.run(build_onboarding())
    recorder.run(build_procurement())
    failing = build_onboarding()
    failing.id = "employee-onboarding-2"
    recorder.start(failing)
    first = failing.steps[0]
    recorder.start_step(failing, first)
    recorder.fail_step(failing, first, reason="offer rescinded")
    recorder.fail(failing, reason="hire cancelled")
    records = store.list()
    print(f"   recorded {len(records)} events across 3 runs")

    # 2. Metrics: completion, failure, and duration.
    print("\n2. metrics -> aggregate measures")
    completion = workflow_completion_metrics(records)
    failure = workflow_failure_metrics(records)
    duration = execution_duration_metrics(records)
    print(
        f"   completion_rate={completion.completion_rate:.2f} "
        f"failure_rate={failure.failure_rate:.2f} "
        f"mean_duration={duration.mean:.4f}s"
    )

    # 3. Reports: workflow statistics and execution summaries.
    print("\n3. reports -> statistics and summaries")
    stats = workflow_statistics(records)
    print(
        f"   total={stats.total_workflows} completed={stats.completed_workflows} "
        f"failed={stats.failed_workflows}"
    )

    # 4. Exports: CSV and JSON.
    print("\n4. exports -> CSV and JSON")
    csv_text = to_csv(execution_summaries(records), fieldnames=["workflow_id", "status"])
    print(f"   csv export: {len(csv_text.splitlines())} lines")
    json_text = to_json(stats)
    print(f"   json export: {len(json_text)} chars")

    print("\ndone.")


if __name__ == "__main__":  # pragma: no cover
    run_demo()
