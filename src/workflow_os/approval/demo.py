"""A runnable demonstration of the approval system.

The demo walks through the governance loop: it creates an approval request, runs
a sequential approval workflow, escalates and delegates, then generates an audit
trail and a bottleneck analysis.
"""

from __future__ import annotations

from datetime import timedelta

from workflow_os.approval.audit import ApprovalAuditLog
from workflow_os.approval.bottlenecks import analyze_bottlenecks
from workflow_os.approval.delegation import delegate
from workflow_os.approval.escalation import escalate
from workflow_os.approval.metrics import compute_workload_metrics
from workflow_os.approval.multi import MultiApproverWorkflow
from workflow_os.approval.record import ApprovalRequest, utcnow
from workflow_os.approval.sqlite_store import SQLiteApprovalStore
from workflow_os.approval.store import ApprovalStore


def run_demo(store: ApprovalStore | None = None) -> ApprovalStore:
    """Run the approval system demonstration, printing each stage."""
    store = store if store is not None else SQLiteApprovalStore()
    log = ApprovalAuditLog()
    start = utcnow() - timedelta(hours=3)

    # 1. Create an approval request.
    print("1. creating approval request")
    request = ApprovalRequest.create(
        workflow_id="wf-budget-001",
        requester="alice",
        title="Approve Q3 marketing budget",
        approvers=["manager", "finance"],
        created_at=start,
        approval_id="budget-approval",
    )
    store.add(request)
    log.record_request(request)
    print(f"   created {request.approval_id!r} with approvers {request.approvers}")

    # 2. Run a multi-approver workflow (two approvals required).
    print("\n2. running multi-approver workflow")
    workflow = MultiApproverWorkflow(request, required_approvals=2)
    workflow.approve("manager")
    log.record_approval(request.approval_id, "manager", start + timedelta(minutes=30))
    print(f"   manager approved; state: {request.state}")

    # 3. Escalate the request.
    print("\n3. escalating request")
    event = escalate(request, "director", reason="finance unavailable")
    log.record_escalation(request.approval_id, "director")
    print(f"   escalated to {event.target!r}; approvers now {request.approvers}")

    # 4. Delegate an approval.
    print("\n4. delegating approval")
    delegation = delegate(request, "finance", "finance-deputy")
    log.record_delegation(request.approval_id, "finance", "finance-deputy")
    print(f"   {delegation.from_approver!r} delegated to {delegation.to_approver!r}")
    workflow.approve("finance-deputy")
    log.record_approval(
        request.approval_id, "finance-deputy", start + timedelta(minutes=150)
    )
    store.update(request)
    print(f"   request state: {request.state}")

    # 5. Generate an audit report.
    print("\n5. audit report")
    for entry in log.for_approval(request.approval_id):
        actor = entry.actor or "-"
        print(f"   {entry.event_type:<10} by {actor}")
    metrics = compute_workload_metrics(store, log)
    print(f"   approvals by actor: {metrics.approvals_by_actor}")
    if metrics.average_response_seconds is not None:
        print(f"   average response: {metrics.average_response_seconds:.0f}s")

    # 6. Generate a bottleneck analysis.
    print("\n6. bottleneck analysis")
    report = analyze_bottlenecks(store, log)
    if report.slowest_approvers:
        actor, seconds = report.slowest_approvers[0]
        print(f"   slowest approver: {actor} ({seconds:.0f}s)")
    print(f"   escalation hotspots: {report.escalation_hotspots}")

    print("\ndone.")
    return store


if __name__ == "__main__":  # pragma: no cover
    run_demo()
