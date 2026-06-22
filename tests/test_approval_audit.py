from workflow_os.approval import ApprovalAuditLog, ApprovalRequest


def make():
    return ApprovalRequest.create(
        workflow_id="wf", requester="alice", title="t", approvers=["m"]
    )


def test_record_request_uses_requester_and_created_at():
    log = ApprovalAuditLog()
    request = make()
    event = log.record_request(request)
    assert event.event_type == "requested"
    assert event.actor == "alice"
    assert event.timestamp == request.created_at
    assert event.metadata["workflow_id"] == "wf"


def test_record_various_events():
    log = ApprovalAuditLog()
    request = make()
    log.record_request(request)
    log.record_approval(request.approval_id, "m")
    log.record_rejection(request.approval_id, "x")
    log.record_escalation(request.approval_id, "director")
    log.record_delegation(request.approval_id, "m", "deputy")

    assert len(log.all()) == 5
    assert len(log.by_type("approved")) == 1
    assert log.by_type("delegated")[0].metadata["to_approver"] == "deputy"


def test_filters():
    log = ApprovalAuditLog()
    log.record("a1", "approved", actor="m")
    log.record("a2", "rejected", actor="m")
    log.record("a1", "escalated", actor="director")
    assert len(log.for_approval("a1")) == 2
    assert len(log.for_actor("m")) == 2


def test_events_have_unique_ids():
    log = ApprovalAuditLog()
    e1 = log.record("a", "approved")
    e2 = log.record("a", "approved")
    assert e1.event_id != e2.event_id
