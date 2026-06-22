from workflow_os.learning import (
    consistently_healthy_workflows,
    highest_success_rate_workflows,
    most_reliable_workflows,
    successful_workflow_insights,
)
from workflow_os.memory.record import MemoryRecord


def rec(workflow_id, event_type):
    return MemoryRecord.create(workflow_id=workflow_id, event_type=event_type)


def build():
    return [
        rec("healthy", "workflow_completed"),
        rec("healthy", "workflow_completed"),
        rec("healthy", "workflow_completed"),
        rec("flaky", "workflow_completed"),
        rec("flaky", "workflow_failed"),
    ]


def test_highest_success_rate():
    ranked = highest_success_rate_workflows(build())
    assert ranked[0].workflow_id == "healthy"
    assert ranked[0].success_rate == 1.0


def test_most_reliable():
    assert most_reliable_workflows(build(), min_runs=2, min_success_rate=0.8) == [
        "healthy"
    ]


def test_consistently_healthy():
    assert consistently_healthy_workflows(build(), min_runs=2) == ["healthy"]


def test_successful_insights():
    insights = successful_workflow_insights(build(), min_runs=2)
    assert len(insights) == 1
    assert insights[0].category == "success"
    assert insights[0].metadata["workflow_id"] == "healthy"
