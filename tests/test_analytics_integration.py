import json

from workflow_os.analytics import (
    compare_workflows,
    detect_bottlenecks,
    execution_summaries,
    to_csv,
    to_json,
    trend_report,
    workflow_completion_metrics,
    workflow_failure_metrics,
    workflow_health_score,
    workflow_scorecards,
    workflow_statistics,
)
from workflow_os.memory import MemoryRecorder, SQLiteMemoryStore
from workflow_os.step import WorkflowStep
from workflow_os.workflow import Workflow


def build_workflow(workflow_id):
    return Workflow(
        id=workflow_id,
        name=f"Flow {workflow_id}",
        steps=[
            WorkflowStep(id="collect", name="Collect"),
            WorkflowStep(id="review", name="Review", dependencies=["collect"]),
        ],
    )


def generate_records():
    store = SQLiteMemoryStore(":memory:")
    recorder = MemoryRecorder(store)
    recorder.run(build_workflow("wf1"))
    recorder.run(build_workflow("wf2"))
    return store.list()


def test_end_to_end_analytics_pipeline():
    records = generate_records()

    completion = workflow_completion_metrics(records)
    assert completion.total_workflows == 2
    assert completion.completed_workflows == 2
    assert completion.completion_rate == 1.0

    failure = workflow_failure_metrics(records)
    assert failure.failure_rate == 0.0

    stats = workflow_statistics(records)
    assert stats.completed_workflows == 2

    summaries = execution_summaries(records)
    assert all(s.status == "completed" for s in summaries)

    bottlenecks = detect_bottlenecks(records)
    assert {b.step_id for b in bottlenecks} == {"collect", "review"}

    comparison = compare_workflows(records)
    assert len(comparison.rows) == 2

    health = workflow_health_score(records)
    assert 0.0 <= health.score <= 1.0
    assert health.success_rate == 1.0

    cards = workflow_scorecards(records)
    assert all(c.score == 1.0 for c in cards)

    report = trend_report(records)
    assert sum(report.workflow_trends.values()) == 2


def test_exports_round_trip():
    records = generate_records()
    summaries = execution_summaries(records)

    csv_text = to_csv(summaries, fieldnames=["workflow_id", "status"])
    assert "workflow_id,status" in csv_text

    payload = json.loads(to_json(summaries))
    assert len(payload) == 2
