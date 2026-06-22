from datetime import datetime

from workflow_os.approval import ApprovalRequest


def test_create_fills_id_and_timestamps():
    request = ApprovalRequest.create(
        workflow_id="wf",
        requester="alice",
        title="Approve budget",
        approvers=["manager"],
    )
    assert request.approval_id
    assert isinstance(request.created_at, datetime)
    assert request.created_at == request.updated_at
    assert request.state == "pending"
    assert request.approvers == ["manager"]
    assert request.decisions == {}
    assert request.metadata == {}
    assert request.step_id is None


def test_create_with_full_fields():
    request = ApprovalRequest.create(
        workflow_id="wf",
        requester="alice",
        title="Approve hire",
        approvers=["manager", "finance"],
        step_id="offer",
        description="Senior engineer offer",
        metadata={"amount": 150000},
    )
    assert request.step_id == "offer"
    assert request.description == "Senior engineer offer"
    assert request.approvers == ["manager", "finance"]
    assert request.metadata == {"amount": 150000}


def test_approvers_independent_between_requests():
    a = ApprovalRequest.create(workflow_id="a", requester="r", title="t")
    b = ApprovalRequest.create(workflow_id="b", requester="r", title="t")
    a.approvers.append("x")
    assert b.approvers == []
