from workflow_os.analytics import team_statistics
from workflow_os.memory.record import MemoryRecord


def rec(event_type, actor, step_id=None):
    return MemoryRecord.create(
        workflow_id="wf", event_type=event_type, actor=actor, step_id=step_id
    )


def test_team_statistics():
    records = [
        rec("step_started", "alice", "a"),
        rec("step_completed", "alice", "a"),
        rec("step_completed", "alice", "b"),
        rec("step_started", "bob", "c"),
        rec("workflow_started", None),
    ]
    stats = {s.actor: s for s in team_statistics(records)}
    assert stats["alice"].workload == 3
    assert stats["alice"].throughput == 2
    assert round(stats["alice"].utilization, 3) == round(2 / 3, 3)
    assert stats["bob"].throughput == 0
    assert stats["bob"].utilization == 0.0
    assert "alice" in stats and len(stats) == 2


def test_team_statistics_empty():
    assert team_statistics([]) == []
