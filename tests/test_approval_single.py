import pytest

from workflow_os.approval import ApprovalError, ApprovalRequest, SingleApproverWorkflow
from workflow_os.approval.single import approve, reject


def make(approvers=("m",)):
    return ApprovalRequest.create(
        workflow_id="wf", requester="alice", title="t", approvers=list(approvers)
    )


def test_approve():
    request = make()
    approve(request, "m")
    assert request.state == "approved"
    assert request.decisions == {"m": "approved"}


def test_reject():
    request = make()
    reject(request, "m")
    assert request.state == "rejected"
    assert request.decisions == {"m": "rejected"}


def test_unknown_approver_rejected():
    request = make()
    with pytest.raises(ApprovalError):
        approve(request, "stranger")


def test_cannot_act_on_terminal():
    request = make()
    approve(request, "m")
    with pytest.raises(ApprovalError):
        reject(request, "m")


def test_workflow_class_requires_one_approver():
    with pytest.raises(ApprovalError):
        SingleApproverWorkflow(make(approvers=("m", "f")))


def test_workflow_class_approve():
    wf = SingleApproverWorkflow(make())
    wf.approve()
    assert wf.request.state == "approved"
