from datetime import timedelta

from workflow_os.approval import (
    ApprovalAuditLog,
    ApprovalRequest,
    MultiApproverWorkflow,
    SQLiteApprovalStore,
    analyze_bottlenecks,
    completed_approvals,
    compute_workload_metrics,
    delegate,
    escalate,
    pending_approvals,
    utcnow,
)


def test_end_to_end_governance_flow():
    store = SQLiteApprovalStore()
    log = ApprovalAuditLog()
    start = utcnow() - timedelta(hours=2)

    request = ApprovalRequest.create(
        workflow_id="wf1",
        requester="alice",
        title="Budget",
        approvers=["manager", "finance"],
        created_at=start,
        approval_id="a1",
    )
    store.add(request)
    log.record_request(request)
    assert {r.approval_id for r in pending_approvals(store)} == {"a1"}

    workflow = MultiApproverWorkflow(request, required_approvals=2)
    workflow.approve("manager")
    log.record_approval("a1", "manager", start + timedelta(minutes=10))

    escalate(request, "director", reason="finance slow")
    log.record_escalation("a1", "director")

    delegate(request, "finance", "deputy")
    log.record_delegation("a1", "finance", "deputy")
    workflow.approve("deputy")
    log.record_approval("a1", "deputy", start + timedelta(minutes=90))
    store.update(request)

    assert request.state == "approved"
    assert {r.approval_id for r in completed_approvals(store)} == {"a1"}

    metrics = compute_workload_metrics(store, log)
    assert metrics.approvals_by_actor["manager"] == 1
    assert metrics.pending_count == 0

    report = analyze_bottlenecks(store, log)
    assert report.escalation_hotspots == {"wf1": 1}
    store.close()
