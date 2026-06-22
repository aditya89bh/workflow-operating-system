from datetime import timedelta

from workflow_os.approval import (
    ApprovalAuditLog,
    ApprovalRequest,
    InMemoryApprovalStore,
    analyze_bottlenecks,
    escalation_hotspots,
    slowest_approvers,
    utcnow,
    workflow_bottlenecks,
)


def make(approval_id, workflow_id):
    return ApprovalRequest.create(
        workflow_id=workflow_id,
        requester="alice",
        title="t",
        approvers=["m"],
        approval_id=approval_id,
    )


def build():
    now = utcnow()
    store = InMemoryApprovalStore()
    store.add(make("1", "wf1"))
    store.add(make("2", "wf2"))
    log = ApprovalAuditLog()
    log.record("1", "requested", actor="alice", timestamp=now)
    log.record("1", "approved", actor="slow", timestamp=now + timedelta(seconds=300))
    log.record("2", "requested", actor="alice", timestamp=now)
    log.record("2", "approved", actor="fast", timestamp=now + timedelta(seconds=30))
    log.record("1", "escalated", actor="director")
    return store, log


def test_slowest_approvers_ordered():
    _, log = build()
    result = slowest_approvers(log)
    assert result[0][0] == "slow"
    assert result[0][1] == 300.0
    assert result[1][0] == "fast"


def test_workflow_bottlenecks():
    store, log = build()
    result = workflow_bottlenecks(store, log)
    assert result[0][0] == "wf1"
    assert result[0][1] == 300.0


def test_escalation_hotspots():
    store, log = build()
    assert escalation_hotspots(store, log) == {"wf1": 1}


def test_analyze_bottlenecks():
    store, log = build()
    report = analyze_bottlenecks(store, log)
    assert report.slowest_approvers[0][0] == "slow"
    assert report.escalation_hotspots == {"wf1": 1}
