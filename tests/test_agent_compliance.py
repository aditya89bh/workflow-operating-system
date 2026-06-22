from workflow_os.agents import ComplianceAgent
from workflow_os.approval import ApprovalRequest
from workflow_os.sop import SOPRecord, SOPStatus


def approval(state, approval_id="a1"):
    request = ApprovalRequest.create(
        workflow_id="wf", requester="r", title="t", approvers=["m"], approval_id=approval_id
    )
    request.state = state
    return request


def test_verify_policies():
    agent = ComplianceAgent()
    ok = agent.verify_policies({"budget": True, "headcount": True})
    assert ok.compliant
    bad = agent.verify_policies({"budget": True, "headcount": False})
    assert not bad.compliant
    assert bad.reasons == ["headcount"]


def test_verify_approvals():
    agent = ComplianceAgent()
    ok = agent.verify_approvals([approval("approved")])
    assert ok.compliant
    bad = agent.verify_approvals([approval("approved", "a1"), approval("rejected", "a2")])
    assert not bad.compliant
    assert len(bad.reasons) == 1


def test_validate_sop_compliance():
    agent = ComplianceAgent()
    active = SOPRecord.create(
        title="T", workflow_type="onboarding", status=SOPStatus.ACTIVE.value
    )
    draft = SOPRecord.create(
        title="T2", workflow_type="onboarding", status=SOPStatus.DRAFT.value
    )
    assert agent.validate_sop_compliance([active]).compliant
    result = agent.validate_sop_compliance([active, draft])
    assert not result.compliant
    assert len(result.reasons) == 1
