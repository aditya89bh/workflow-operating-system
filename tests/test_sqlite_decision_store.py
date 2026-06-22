import pytest

from workflow_os.decision import (
    DecisionNotFoundError,
    DecisionQuery,
    DecisionRecord,
    SQLiteDecisionStore,
)


def _record(**kwargs) -> DecisionRecord:
    base = dict(workflow_id="wf", decision_type="workflow_decision", decision="go")
    base.update(kwargs)
    return DecisionRecord.create(**base)


def test_add_get_round_trip():
    store = SQLiteDecisionStore()
    record = _record(
        rationale="best option",
        alternatives=["wait", "escalate"],
        actor="ops",
        metadata={"score": 3},
    )
    store.add(record)
    loaded = store.get(record.decision_id)
    assert loaded == record


def test_list_and_query():
    store = SQLiteDecisionStore()
    store.add(_record(decision="a", actor="it"))
    store.add(_record(decision="b", actor="hr"))
    assert len(store.list()) == 2
    it_only = store.query(DecisionQuery(actor="it"))
    assert [r.decision for r in it_only] == ["a"]


def test_update_existing_record():
    store = SQLiteDecisionStore()
    record = _record(outcome="pending")
    store.add(record)
    record.outcome = "successful"
    store.update(record)
    assert store.get(record.decision_id).outcome == "successful"


def test_update_missing_raises():
    store = SQLiteDecisionStore()
    with pytest.raises(DecisionNotFoundError):
        store.update(_record())


def test_get_and_delete_missing_raise():
    store = SQLiteDecisionStore()
    with pytest.raises(DecisionNotFoundError):
        store.get("missing")
    with pytest.raises(DecisionNotFoundError):
        store.delete("missing")


def test_delete_removes_record():
    store = SQLiteDecisionStore()
    record = _record()
    store.add(record)
    store.delete(record.decision_id)
    assert store.list() == []
