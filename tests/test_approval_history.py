from workflow_os.approval import (
    ApprovalRequest,
    InMemoryApprovalStore,
    actor_approvals,
    completed_approvals,
    pending_approvals,
    requester_approvals,
    workflow_approvals,
)


def make(approval_id, workflow_id="wf", approvers=("m",), requester="alice", state="pending"):
    request = ApprovalRequest.create(
        workflow_id=workflow_id,
        requester=requester,
        title="t",
        approvers=list(approvers),
        approval_id=approval_id,
    )
    request.state = state
    return request


def build_store():
    store = InMemoryApprovalStore()
    store.add(make("1", workflow_id="wf1", approvers=["m"], state="pending"))
    store.add(make("2", workflow_id="wf1", approvers=["f"], state="approved"))
    store.add(make("3", workflow_id="wf2", approvers=["m"], state="rejected"))
    return store


def test_workflow_approvals():
    store = build_store()
    assert {r.approval_id for r in workflow_approvals(store, "wf1")} == {"1", "2"}


def test_actor_approvals():
    store = build_store()
    assert {r.approval_id for r in actor_approvals(store, "m")} == {"1", "3"}


def test_requester_approvals():
    store = build_store()
    assert {r.approval_id for r in requester_approvals(store, "alice")} == {"1", "2", "3"}


def test_pending_and_completed():
    store = build_store()
    assert {r.approval_id for r in pending_approvals(store)} == {"1"}
    assert {r.approval_id for r in completed_approvals(store)} == {"2", "3"}
