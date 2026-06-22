import pytest

from workflow_os.decision import (
    RESOLVED_OUTCOMES,
    VALID_OUTCOMES,
    DecisionOutcome,
    DecisionRecorder,
    InvalidOutcomeError,
    SQLiteDecisionStore,
    normalize_outcome,
    set_decision_outcome,
)


def test_outcome_values():
    assert VALID_OUTCOMES == {"pending", "successful", "failed", "unknown"}
    assert RESOLVED_OUTCOMES == {"successful", "failed"}
    assert DecisionOutcome.PENDING.value == "pending"


def test_normalize_outcome_validates():
    assert normalize_outcome(DecisionOutcome.SUCCESSFUL) == "successful"
    with pytest.raises(InvalidOutcomeError):
        normalize_outcome("maybe")


def test_set_decision_outcome_updates_store():
    store = SQLiteDecisionStore()
    recorder = DecisionRecorder(store)
    record = recorder.record_decision(workflow_id="wf", decision="Ship")

    updated = set_decision_outcome(store, record.decision_id, "successful")
    assert updated.outcome == "successful"
    assert store.get(record.decision_id).outcome == "successful"


def test_recorder_rejects_invalid_outcome():
    store = SQLiteDecisionStore()
    recorder = DecisionRecorder(store)
    with pytest.raises(InvalidOutcomeError):
        recorder.record_decision(workflow_id="wf", decision="x", outcome="bogus")
