from datetime import timedelta

from workflow_os.approval import (
    ApprovalRequest,
    EscalationRule,
    escalate,
    escalate_if_overdue,
    escalation_history,
    should_escalate,
    utcnow,
)


def make(created_at=None):
    return ApprovalRequest.create(
        workflow_id="wf",
        requester="alice",
        title="t",
        approvers=["m"],
        created_at=created_at or utcnow(),
    )


def test_escalate_records_history_and_adds_approver():
    request = make()
    event = escalate(request, "director", reason="urgent")
    assert event.target == "director"
    assert "director" in request.approvers
    history = escalation_history(request)
    assert len(history) == 1
    assert history[0].reason == "urgent"


def test_should_escalate_when_overdue():
    request = make(created_at=utcnow() - timedelta(hours=2))
    rule = EscalationRule(target="director", after_seconds=3600)
    assert should_escalate(request, rule)


def test_escalate_if_overdue():
    now = utcnow()
    request = make(created_at=now - timedelta(hours=2))
    rule = EscalationRule(target="director", after_seconds=3600)
    event = escalate_if_overdue(request, rule, now=now)
    assert event is not None
    assert event.target == "director"

    fresh = make(created_at=now)
    assert escalate_if_overdue(fresh, rule, now=now) is None
