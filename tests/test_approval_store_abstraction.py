import pytest

from workflow_os.approval import (
    ApprovalNotFoundError,
    ApprovalQuery,
    ApprovalRequest,
    ApprovalStore,
    InMemoryApprovalStore,
)


def make(**kwargs):
    base = dict(workflow_id="wf", requester="alice", title="t", approvers=["m"])
    base.update(kwargs)
    return ApprovalRequest.create(**base)


def test_in_memory_store_is_protocol_instance():
    store = InMemoryApprovalStore()
    assert isinstance(store, ApprovalStore)


def test_add_get_update_delete():
    store = InMemoryApprovalStore()
    request = make()
    store.add(request)
    assert store.get(request.approval_id) is request

    request.state = "approved"
    store.update(request)
    assert store.get(request.approval_id).state == "approved"

    store.delete(request.approval_id)
    with pytest.raises(ApprovalNotFoundError):
        store.get(request.approval_id)


def test_update_missing_raises():
    store = InMemoryApprovalStore()
    with pytest.raises(ApprovalNotFoundError):
        store.update(make())


def test_query_filters():
    store = InMemoryApprovalStore()
    store.add(make(workflow_id="wf1", approvers=["m"], approval_id="1"))
    store.add(make(workflow_id="wf2", approvers=["f"], approval_id="2"))
    pending = make(workflow_id="wf1", approvers=["m"], approval_id="3")
    pending.state = "approved"
    store.add(pending)

    assert len(store.list()) == 3
    assert {r.approval_id for r in store.query(ApprovalQuery(workflow_id="wf1"))} == {
        "1",
        "3",
    }
    assert {r.approval_id for r in store.query(ApprovalQuery(approver="f"))} == {"2"}
    assert {
        r.approval_id for r in store.query(ApprovalQuery(states=("approved",)))
    } == {"3"}
