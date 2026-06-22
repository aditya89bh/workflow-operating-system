from workflow_os.exception.record import ExceptionRecord
from workflow_os.learning import (
    recurring_bottlenecks,
    recurring_exceptions,
    recurring_workflows,
    workflow_run_stats,
)
from workflow_os.memory.record import MemoryRecord


def rec(workflow_id, event_type, step_id=None, duration=None):
    metadata = {"duration_seconds": duration} if duration is not None else None
    return MemoryRecord.create(
        workflow_id=workflow_id,
        event_type=event_type,
        step_id=step_id,
        metadata=metadata,
    )


def build_runs():
    return [
        rec("wf1", "workflow_completed"),
        rec("wf1", "workflow_completed"),
        rec("wf1", "workflow_failed"),
        rec("wf2", "workflow_completed"),
    ]


def test_workflow_run_stats():
    stats = workflow_run_stats(build_runs())
    assert stats["wf1"].runs == 3
    assert stats["wf1"].successes == 2
    assert stats["wf1"].failures == 1
    assert round(stats["wf1"].success_rate, 3) == round(2 / 3, 3)


def test_recurring_workflows():
    assert recurring_workflows(build_runs(), min_runs=2) == ["wf1"]
    assert recurring_workflows(build_runs(), min_runs=1) == ["wf1", "wf2"]


def test_recurring_bottlenecks():
    records = [
        rec("wf", "step_completed", "review", 5.0),
        rec("wf", "step_completed", "review", 6.0),
        rec("wf", "step_completed", "once", 1.0),
    ]
    recurring = recurring_bottlenecks(records, min_occurrences=2)
    assert [b.step_id for b in recurring] == ["review"]


def test_recurring_exceptions():
    exceptions = [
        ExceptionRecord.create(workflow_id="wf1", exception_type="timeout"),
        ExceptionRecord.create(workflow_id="wf1", exception_type="timeout"),
        ExceptionRecord.create(workflow_id="wf2", exception_type="timeout"),
    ]
    result = recurring_exceptions(exceptions, min_occurrences=2)
    assert result == {"wf1:timeout": 2}
