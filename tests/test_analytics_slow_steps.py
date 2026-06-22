from workflow_os.analytics import slow_steps, slowest_steps
from workflow_os.memory.record import MemoryRecord


def rec(step_id, duration):
    return MemoryRecord.create(
        workflow_id="wf",
        event_type="step_completed",
        step_id=step_id,
        metadata={"duration_seconds": duration},
    )


def test_slowest_steps_ranked_by_mean():
    records = [
        rec("a", 2.0),
        rec("a", 4.0),  # mean 3
        rec("b", 10.0),  # mean 10
        rec("c", 1.0),  # mean 1
    ]
    ranked = slowest_steps(records)
    assert [s.step_id for s in ranked] == ["b", "a", "c"]
    assert ranked[0].mean_duration == 10.0
    assert ranked[1].mean_duration == 3.0


def test_slow_steps_threshold():
    records = [rec("a", 3.0), rec("b", 10.0), rec("c", 1.0)]
    result = slow_steps(records, threshold=3.0)
    assert [s.step_id for s in result] == ["b", "a"]


def test_slowest_steps_limit():
    records = [rec("a", 3.0), rec("b", 10.0), rec("c", 1.0)]
    assert [s.step_id for s in slowest_steps(records, limit=1)] == ["b"]
