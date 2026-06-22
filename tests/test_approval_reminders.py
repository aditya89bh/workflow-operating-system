from datetime import timedelta

from workflow_os.approval import (
    ApprovalRequest,
    generate_reminders,
    overdue_reminders,
    pending_reminders,
    utcnow,
)


def make(created_at=None, approvers=("a", "b"), approval_id="1"):
    return ApprovalRequest.create(
        workflow_id="wf",
        requester="alice",
        title="t",
        approvers=list(approvers),
        created_at=created_at or utcnow(),
        approval_id=approval_id,
    )


def test_pending_reminders_for_outstanding_approvers():
    request = make()
    request.decisions["a"] = "approved"
    reminders = pending_reminders([request])
    assert [r.approver for r in reminders] == ["b"]
    assert reminders[0].kind == "pending"


def test_no_reminders_for_terminal_requests():
    request = make()
    request.state = "approved"
    assert pending_reminders([request]) == []


def test_overdue_reminders():
    now = utcnow()
    old = make(created_at=now - timedelta(hours=2), approval_id="old")
    fresh = make(created_at=now, approval_id="fresh")
    reminders = overdue_reminders([old, fresh], timeout_seconds=3600, now=now)
    assert {r.approval_id for r in reminders} == {"old"}
    assert all(r.kind == "overdue" for r in reminders)


def test_generate_combines():
    now = utcnow()
    old = make(created_at=now - timedelta(hours=2), approval_id="old")
    reminders = generate_reminders([old], timeout_seconds=3600, now=now)
    kinds = {r.kind for r in reminders}
    assert kinds == {"pending", "overdue"}
