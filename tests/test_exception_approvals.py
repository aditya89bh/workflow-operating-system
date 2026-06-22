from workflow_os.approval import ApprovalRequest
from workflow_os.exception import detect_missing_approvals


def make(state, approval_id="a1", workflow_id="wf"):
    request = ApprovalRequest.create(
        workflow_id=workflow_id,
        requester="alice",
        title="t",
        approvers=["m"],
        approval_id=approval_id,
    )
    request.state = state
    return request


def test_detects_rejected_and_expired():
    requests = [
        make("approved", "a1"),
        make("rejected", "a2"),
        make("expired", "a3"),
        make("pending", "a4"),
    ]
    records = detect_missing_approvals(requests)
    assert {r.metadata["approval_id"] for r in records} == {"a2", "a3"}
    assert all(r.exception_type == "approval_failure" for r in records)


def test_include_pending():
    requests = [make("pending", "a1"), make("approved", "a2")]
    records = detect_missing_approvals(requests, include_pending=True)
    assert {r.metadata["approval_id"] for r in records} == {"a1"}


def test_approved_only_returns_empty():
    assert detect_missing_approvals([make("approved")]) == []
