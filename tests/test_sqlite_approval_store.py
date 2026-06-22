import pytest

from workflow_os.approval import (
    ApprovalNotFoundError,
    ApprovalQuery,
    ApprovalRequest,
    ApprovalStore,
    SQLiteApprovalStore,
)


def make(**kwargs):
    base = dict(workflow_id="wf", requester="alice", title="t", approvers=["m"])
    base.update(kwargs)
    return ApprovalRequest.create(**base)


def test_is_protocol_instance():
    store = SQLiteApprovalStore()
    assert isinstance(store, ApprovalStore)
    store.close()


def test_round_trip_preserves_fields():
    store = SQLiteApprovalStore()
    request = make(
        approvers=["m", "f"],
        step_id="s1",
        description="desc",
        metadata={"k": "v"},
    )
    request.decisions["m"] = "approved"
    store.add(request)

    loaded = store.get(request.approval_id)
    assert loaded.approvers == ["m", "f"]
    assert loaded.step_id == "s1"
    assert loaded.description == "desc"
    assert loaded.metadata == {"k": "v"}
    assert loaded.decisions == {"m": "approved"}
    assert loaded.created_at == request.created_at
    store.close()


def test_update_and_delete():
    store = SQLiteApprovalStore()
    request = make()
    store.add(request)
    request.state = "approved"
    store.update(request)
    assert store.get(request.approval_id).state == "approved"

    store.delete(request.approval_id)
    with pytest.raises(ApprovalNotFoundError):
        store.get(request.approval_id)
    store.close()


def test_update_missing_raises():
    store = SQLiteApprovalStore()
    with pytest.raises(ApprovalNotFoundError):
        store.update(make())
    store.close()


def test_query(tmp_path):
    db = tmp_path / "approvals.db"
    store = SQLiteApprovalStore(str(db))
    store.add(make(workflow_id="wf1", approval_id="1"))
    store.add(make(workflow_id="wf2", approval_id="2"))
    assert {r.approval_id for r in store.query(ApprovalQuery(workflow_id="wf1"))} == {
        "1"
    }
    assert len(store.list()) == 2
    store.close()
