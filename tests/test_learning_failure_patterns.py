from workflow_os.learning import (
    failure_hotspots,
    failure_pattern_insights,
    frequently_failing_workflows,
    unstable_workflows,
)
from workflow_os.memory.record import MemoryRecord


def rec(workflow_id, event_type, step_id=None):
    return MemoryRecord.create(
        workflow_id=workflow_id, event_type=event_type, step_id=step_id
    )


def build():
    return [
        rec("bad", "workflow_failed"),
        rec("bad", "workflow_failed"),
        rec("bad", "step_failed", "review"),
        rec("bad", "step_failed", "review"),
        rec("flaky", "workflow_completed"),
        rec("flaky", "workflow_failed"),
    ]


def test_frequently_failing():
    assert frequently_failing_workflows(build(), min_failures=2) == ["bad"]


def test_failure_hotspots():
    assert failure_hotspots(build(), min_failures=2) == [("review", 2)]


def test_unstable_workflows():
    assert unstable_workflows(build(), min_runs=2) == ["flaky"]


def test_failure_insights():
    insights = failure_pattern_insights(build(), min_failures=2)
    assert len(insights) == 1
    assert insights[0].category == "failure"
    assert insights[0].metadata["workflow_id"] == "bad"
