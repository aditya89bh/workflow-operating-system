from workflow_os.analytics import (
    agent_scorecards,
    approval_scorecards,
    workflow_scorecards,
)
from workflow_os.approval import ApprovalRequest
from workflow_os.memory.record import MemoryRecord


def rec(workflow_id, event_type, step_id=None, actor=None):
    return MemoryRecord.create(
        workflow_id=workflow_id, event_type=event_type, step_id=step_id, actor=actor
    )


def test_workflow_scorecards():
    records = [
        rec("wf1", "workflow_started"),
        rec("wf1", "workflow_completed"),
        rec("wf2", "workflow_started"),
        rec("wf2", "workflow_failed"),
    ]
    cards = {c.subject_id: c for c in workflow_scorecards(records)}
    assert cards["wf1"].score == 1.0
    assert cards["wf2"].score == 0.0


def test_agent_scorecards():
    records = [
        rec("wf", "step_completed", "a", actor="alice"),
        rec("wf", "step_completed", "b", actor="alice"),
        rec("wf", "step_failed", "c", actor="alice"),
        rec("wf", "step_completed", "d", actor="bob"),
    ]
    cards = {c.subject_id: c for c in agent_scorecards(records)}
    assert round(cards["alice"].score, 3) == round(2 / 3, 3)
    assert cards["bob"].score == 1.0


def test_approval_scorecards():
    request = ApprovalRequest.create(
        workflow_id="wf", requester="r", title="t", approvers=["m1", "m2"]
    )
    request.decisions = {"m1": "approved", "m2": "rejected"}
    cards = {c.subject_id: c for c in approval_scorecards([request])}
    assert cards["m1"].score == 1.0
    assert cards["m2"].score == 0.0
