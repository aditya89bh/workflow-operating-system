from workflow_os.decision import (
    DecisionRecorder,
    SQLiteDecisionStore,
    compute_decision_statistics,
)


def _seed() -> SQLiteDecisionStore:
    store = SQLiteDecisionStore()
    recorder = DecisionRecorder(store)
    recorder.record_decision(
        workflow_id="wf", decision="a", decision_type="workflow_decision",
        actor="it", outcome="successful",
    )
    recorder.record_decision(
        workflow_id="wf", decision="b", decision_type="step_decision",
        actor="it", outcome="failed",
    )
    recorder.record_decision(
        workflow_id="wf", decision="c", decision_type="step_decision",
        actor="hr", outcome="successful",
    )
    recorder.record_decision(
        workflow_id="wf", decision="d", decision_type="manual_decision",
        actor="hr", outcome="pending",
    )
    return store


def test_statistics_counts_and_rates():
    stats = compute_decision_statistics(_seed())
    assert stats.total_decisions == 4
    assert stats.decisions_by_type["step_decision"] == 2
    assert stats.outcome_counts["successful"] == 2
    # resolved = 2 successful + 1 failed = 3
    assert round(stats.success_rate, 3) == round(2 / 3, 3)
    assert round(stats.failure_rate, 3) == round(1 / 3, 3)


def test_actor_statistics():
    stats = compute_decision_statistics(_seed())
    assert stats.actor_statistics["it"].total == 2
    assert stats.actor_statistics["it"].successful == 1
    assert stats.actor_statistics["it"].failed == 1
    assert stats.actor_statistics["hr"].successful == 1


def test_empty_store_statistics():
    stats = compute_decision_statistics(SQLiteDecisionStore())
    assert stats.total_decisions == 0
    assert stats.success_rate == 0.0
    assert stats.as_dict()["actor_statistics"] == {}
