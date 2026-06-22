from workflow_os.analytics import detect_bottlenecks
from workflow_os.memory.record import MemoryRecord


def rec(step_id, duration):
    return MemoryRecord.create(
        workflow_id="wf",
        event_type="step_completed",
        step_id=step_id,
        metadata={"duration_seconds": duration},
    )


def test_bottlenecks_ranked_by_total():
    records = [
        rec("fast", 1.0),
        rec("slow", 10.0),
        rec("slow", 10.0),
        rec("mid", 5.0),
    ]
    bottlenecks = detect_bottlenecks(records)
    assert [b.step_id for b in bottlenecks] == ["slow", "mid", "fast"]
    assert bottlenecks[0].total_duration == 20.0
    assert bottlenecks[0].occurrences == 2
    assert bottlenecks[0].mean_duration == 10.0


def test_bottlenecks_limit():
    records = [rec("a", 1.0), rec("b", 2.0), rec("c", 3.0)]
    top = detect_bottlenecks(records, limit=2)
    assert [b.step_id for b in top] == ["c", "b"]
