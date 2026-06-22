from datetime import timedelta

from workflow_os.approval import (
    ApprovalRequest,
    InMemoryApprovalStore,
    expire_overdue,
    find_overdue,
    is_overdue,
    utcnow,
)
from workflow_os.approval.single import approve


def make(created_at, approval_id="1"):
    return ApprovalRequest.create(
        workflow_id="wf",
        requester="alice",
        title="t",
        approvers=["m"],
        created_at=created_at,
        approval_id=approval_id,
    )


def test_is_overdue():
    old = make(utcnow() - timedelta(hours=2))
    assert is_overdue(old, timeout_seconds=3600)
    fresh = make(utcnow())
    assert not is_overdue(fresh, timeout_seconds=3600)


def test_resolved_never_overdue():
    request = make(utcnow() - timedelta(hours=2))
    approve(request, "m")
    assert not is_overdue(request, timeout_seconds=3600)


def test_find_overdue():
    now = utcnow()
    old = make(now - timedelta(hours=2), approval_id="old")
    fresh = make(now, approval_id="fresh")
    overdue = find_overdue([old, fresh], timeout_seconds=3600, now=now)
    assert [r.approval_id for r in overdue] == ["old"]


def test_expire_overdue_updates_store():
    now = utcnow()
    store = InMemoryApprovalStore()
    store.add(make(now - timedelta(hours=2), approval_id="old"))
    store.add(make(now, approval_id="fresh"))
    expired = expire_overdue(store, timeout_seconds=3600, now=now)
    assert [r.approval_id for r in expired] == ["old"]
    assert store.get("old").state == "expired"
    assert store.get("fresh").state == "pending"
