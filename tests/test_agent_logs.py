from workflow_os.agents import CollaborationLog, MessageBus


def test_records_all_event_types():
    log = CollaborationLog()
    log.record_assignment("wf", "a1", "t1")
    bus = MessageBus()
    msg = bus.send("a1", "a2", "hi")
    log.record_message(msg, workflow_id="wf")
    log.record_transfer("wf", "t1", "a1", "a2")
    log.record_participation("wf", "a3")
    assert len(log.entries()) == 4
    assert len(log.entries(event_type="assignment")) == 1
    assert len(log.entries(workflow_id="wf")) == 4


def test_filter_by_agent():
    log = CollaborationLog()
    log.record_assignment("wf", "a1", "t1")
    log.record_participation("wf", "a2")
    assert len(log.entries(agent_id="a1")) == 1


def test_participants():
    log = CollaborationLog()
    log.record_assignment("wf", "a1", "t1")
    log.record_participation("wf", "a2")
    log.record_participation("wf2", "a3")
    assert log.participants("wf") == ["a1", "a2"]
    assert log.participants("wf2") == ["a3"]
