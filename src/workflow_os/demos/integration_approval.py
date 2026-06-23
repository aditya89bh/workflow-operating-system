"""Workflow + approval integration demonstration.

Shows the flow ``workflow -> approval -> audit``: a workflow step requires sign-off,
an approval request is raised and approved through a multi-approver workflow, and
the governance audit trail is then printed.
"""

from __future__ import annotations

from datetime import timedelta

from workflow_os.approval.audit import ApprovalAuditLog
from workflow_os.approval.multi import MultiApproverWorkflow
from workflow_os.approval.record import ApprovalRequest, utcnow
from workflow_os.approval.sqlite_store import SQLiteApprovalStore
from workflow_os.demos.procurement import build_workflow


def run_demo() -> None:
    """Run the workflow-approval integration demonstration and print a summary."""
    workflow = build_workflow()
    gate_step = next(s for s in workflow.steps if s.id == "manager_approval")

    # 1. Workflow: a step needs governance sign-off.
    print("1. workflow -> step requires approval")
    print(f"   {workflow.id!r} step {gate_step.id!r}: {gate_step.name}")

    # 2. Approval: raise and resolve a multi-approver request.
    print("\n2. approval -> raising and resolving the request")
    store = SQLiteApprovalStore(":memory:")
    log = ApprovalAuditLog()
    start = utcnow() - timedelta(hours=2)
    request = ApprovalRequest.create(
        workflow_id=workflow.id,
        requester="requester",
        title="Approve procurement spend",
        approvers=["manager", "finance"],
        step_id=gate_step.id,
        created_at=start,
        approval_id="procurement-approval",
    )
    store.add(request)
    log.record_request(request)

    approval = MultiApproverWorkflow(request, required_approvals=2)
    approval.approve("manager")
    log.record_approval(request.approval_id, "manager", start + timedelta(minutes=20))
    approval.approve("finance")
    log.record_approval(request.approval_id, "finance", start + timedelta(minutes=45))
    store.update(request)
    print(f"   request {request.approval_id!r} state: {request.state}")

    # 3. Audit: print the governance trail.
    print("\n3. audit -> governance trail")
    for entry in log.for_approval(request.approval_id):
        actor = entry.actor or "-"
        print(f"   {entry.event_type:<10} by {actor}")

    print("\ndone.")


if __name__ == "__main__":  # pragma: no cover
    run_demo()
