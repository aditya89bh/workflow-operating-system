import pytest

from workflow_os.approval import (
    ApprovalError,
    ApprovalRequest,
    SequentialApprovalWorkflow,
)


def make():
    return ApprovalRequest.create(
        workflow_id="wf",
        requester="alice",
        title="t",
        approvers=["manager", "finance", "operations"],
    )


def test_full_chain_approves():
    wf = SequentialApprovalWorkflow(make())
    assert wf.current_approver == "manager"
    wf.approve("manager")
    assert wf.request.state == "pending"
    assert wf.current_approver == "finance"
    wf.approve("finance")
    assert wf.current_approver == "operations"
    wf.approve("operations")
    assert wf.request.state == "approved"
    assert wf.current_approver is None


def test_out_of_order_rejected():
    wf = SequentialApprovalWorkflow(make())
    with pytest.raises(ApprovalError):
        wf.approve("finance")


def test_reject_anywhere_rejects():
    wf = SequentialApprovalWorkflow(make())
    wf.approve("manager")
    wf.reject("finance")
    assert wf.request.state == "rejected"


def test_pending_approvers():
    wf = SequentialApprovalWorkflow(make())
    wf.approve("manager")
    assert wf.pending_approvers == ["finance", "operations"]
