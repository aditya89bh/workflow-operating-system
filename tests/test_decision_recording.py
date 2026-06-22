from workflow_os.decision import (
    DecisionRecorder,
    DecisionType,
    SQLiteDecisionStore,
)


def test_record_decision_persists_and_returns():
    store = SQLiteDecisionStore()
    recorder = DecisionRecorder(store)
    record = recorder.record_decision(
        workflow_id="wf",
        decision="Approve request",
        rationale="Within budget",
        alternatives=["Reject", "Defer"],
        actor="manager",
    )
    assert record.decision_type == DecisionType.MANUAL_DECISION.value
    assert store.get(record.decision_id) == record
    assert record.outcome == "pending"


def test_update_decision_outcome():
    store = SQLiteDecisionStore()
    recorder = DecisionRecorder(store)
    record = recorder.record_decision(workflow_id="wf", decision="Ship it")

    updated = recorder.update_decision_outcome(
        record.decision_id, "successful", metadata={"verified_by": "qa"}
    )
    assert updated.outcome == "successful"
    assert updated.metadata["verified_by"] == "qa"
    assert store.get(record.decision_id).outcome == "successful"
