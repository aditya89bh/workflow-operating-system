from workflow_os.approval.escalation import escalate
from workflow_os.approval.record import ApprovalRequest
from workflow_os.learning import (
    approval_improvement_recommendations,
    approver_bottleneck_recommendations,
    escalation_recommendations,
    reduce_approver_recommendations,
)


def test_reduce_approvers():
    req = ApprovalRequest.create(
        workflow_id="wf", requester="r", title="t", approvers=["a", "b", "c", "d"]
    )
    recs = reduce_approver_recommendations([req], max_approvers=3)
    assert recs and recs[0].metadata["action"] == "reduce_approvers"


def test_escalation():
    req = ApprovalRequest.create(workflow_id="wf", requester="r", title="t")
    escalate(req, "mgr1")
    escalate(req, "mgr2")
    recs = escalation_recommendations([req], min_escalations=2)
    assert recs and recs[0].metadata["workflow_id"] == "wf"


def test_approver_bottleneck():
    approvals = [
        ApprovalRequest.create(
            workflow_id=f"wf{i}", requester="r", title="t", approvers=["boss"]
        )
        for i in range(3)
    ]
    recs = approver_bottleneck_recommendations(approvals, min_requests=3)
    assert recs and recs[0].metadata["approver"] == "boss"


def test_combined():
    req = ApprovalRequest.create(
        workflow_id="wf", requester="r", title="t", approvers=["a", "b", "c", "d"]
    )
    recs = approval_improvement_recommendations([req], max_approvers=3, min_requests=99)
    assert all(r.category == "approval" for r in recs)
