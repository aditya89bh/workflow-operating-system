from datetime import timedelta

import pytest

from workflow_os.approval import (
    ApprovalError,
    ApprovalRequest,
    active_delegations,
    delegate,
    delegation_history,
    utcnow,
)


def make(approvers=("manager",)):
    return ApprovalRequest.create(
        workflow_id="wf", requester="alice", title="t", approvers=list(approvers)
    )


def test_permanent_delegation_replaces_approver():
    request = make()
    delegate(request, "manager", "deputy")
    assert request.approvers == ["deputy"]
    history = delegation_history(request)
    assert len(history) == 1
    assert history[0].from_approver == "manager"
    assert history[0].to_approver == "deputy"


def test_temporary_delegation_keeps_both():
    request = make()
    expires = utcnow() + timedelta(hours=1)
    event = delegate(request, "manager", "deputy", expires_at=expires)
    assert set(request.approvers) == {"manager", "deputy"}
    assert event.temporary


def test_delegate_unknown_approver_raises():
    request = make()
    with pytest.raises(ApprovalError):
        delegate(request, "stranger", "deputy")


def test_active_delegations_filters_expired():
    request = make()
    now = utcnow()
    delegate(
        request,
        "manager",
        "deputy",
        expires_at=now - timedelta(hours=1),
        now=now - timedelta(hours=2),
    )
    assert delegation_history(request)
    assert active_delegations(request, now=now) == []
