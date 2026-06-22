from workflow_os.approval import (
    ApprovalRequest,
    ApprovalState,
    is_active,
    is_terminal,
    record_response,
    set_state,
)


def test_state_values():
    assert {s.value for s in ApprovalState} == {
        "pending",
        "approved",
        "rejected",
        "cancelled",
        "expired",
    }


def test_terminal_and_active_classification():
    assert is_active(ApprovalState.PENDING.value)
    assert not is_terminal(ApprovalState.PENDING.value)
    for state in ("approved", "rejected", "cancelled", "expired"):
        assert is_terminal(state)
        assert not is_active(state)


def test_set_state_bumps_updated_at():
    request = ApprovalRequest.create(workflow_id="wf", requester="r", title="t")
    original = request.updated_at
    set_state(request, ApprovalState.APPROVED.value)
    assert request.state == "approved"
    assert request.updated_at >= original


def test_record_response():
    request = ApprovalRequest.create(
        workflow_id="wf", requester="r", title="t", approvers=["m"]
    )
    record_response(request, "m", ApprovalState.APPROVED.value)
    assert request.decisions["m"] == "approved"
