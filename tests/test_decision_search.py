from workflow_os.decision import (
    DecisionRecorder,
    SQLiteDecisionStore,
    search_by_decision_text,
    search_by_outcome,
    search_by_rationale,
    search_decisions,
)


def _seed() -> SQLiteDecisionStore:
    store = SQLiteDecisionStore()
    recorder = DecisionRecorder(store)
    recorder.record_decision(
        workflow_id="wf",
        decision="Approve laptop purchase",
        rationale="Engineering role needs hardware",
        outcome="successful",
    )
    recorder.record_decision(
        workflow_id="wf",
        decision="Reject travel request",
        rationale="Budget exceeded",
        outcome="failed",
    )
    return store


def test_search_by_decision_text_is_case_insensitive():
    store = _seed()
    results = search_by_decision_text(store, "laptop")
    assert len(results) == 1
    assert results[0].decision == "Approve laptop purchase"


def test_search_by_rationale():
    store = _seed()
    results = search_by_rationale(store, "budget")
    assert [r.decision for r in results] == ["Reject travel request"]


def test_search_by_outcome():
    store = _seed()
    assert len(search_by_outcome(store, "successful")) == 1
    assert len(search_by_outcome(store, "failed")) == 1


def test_search_decisions_combines_criteria():
    store = _seed()
    results = search_decisions(store, text="approve", outcome="successful")
    assert len(results) == 1
    assert search_decisions(store, text="approve", outcome="failed") == []
