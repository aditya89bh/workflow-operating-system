from datetime import timedelta

from workflow_os.approval import (
    ApprovalAuditLog,
    ApprovalRequest,
    InMemoryApprovalStore,
    approvals_by_actor,
    average_response_time,
    compute_workload_metrics,
    utcnow,
)


def make(approval_id, created_at, state="pending"):
    request = ApprovalRequest.create(
        workflow_id="wf",
        requester="alice",
        title="t",
        approvers=["m"],
        created_at=created_at,
        approval_id=approval_id,
    )
    request.state = state
    return request


def test_approvals_by_actor():
    log = ApprovalAuditLog()
    log.record("1", "approved", actor="m")
    log.record("2", "approved", actor="m")
    log.record("3", "approved", actor="f")
    assert approvals_by_actor(log) == {"m": 2, "f": 1}


def test_average_response_time():
    now = utcnow()
    log = ApprovalAuditLog()
    log.record("1", "requested", actor="alice", timestamp=now)
    log.record("1", "approved", actor="m", timestamp=now + timedelta(seconds=60))
    log.record("2", "requested", actor="alice", timestamp=now)
    log.record("2", "approved", actor="m", timestamp=now + timedelta(seconds=120))
    assert average_response_time(log) == 90.0


def test_average_response_time_none_when_empty():
    assert average_response_time(ApprovalAuditLog()) is None


def test_compute_workload_metrics():
    now = utcnow()
    store = InMemoryApprovalStore()
    store.add(make("1", now, state="pending"))
    store.add(make("old", now - timedelta(hours=2), state="pending"))
    log = ApprovalAuditLog()
    log.record("1", "approved", actor="m")

    metrics = compute_workload_metrics(store, log, timeout_seconds=3600, now=now)
    assert metrics.approvals_by_actor == {"m": 1}
    assert metrics.pending_count == 2
    assert metrics.overdue_count == 1
