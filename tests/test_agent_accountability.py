from workflow_os.agents import (
    CollaborationLog,
    TaskDelegation,
    actions_performed,
    build_accountability,
    ownership_history,
    responsibility_chain,
)


def test_actions_performed():
    log = CollaborationLog()
    log.record_assignment("wf", "a1", "t1")
    log.record_participation("wf", "a1")
    log.record_participation("wf", "a2")
    assert len(actions_performed(log, "a1")) == 2


def test_build_accountability_counts():
    log = CollaborationLog()
    log.record_assignment("wf", "a1", "t1")
    log.record_participation("wf", "a1")
    report = build_accountability(log, "a1")
    assert report.agent_id == "a1"
    assert report.action_counts == {"assignment": 1, "participation": 1}


def test_ownership_history_and_chain():
    ledger = TaskDelegation()
    ledger.assign(workflow_id="wf", owner="a1", task_id="t1")
    ledger.transfer("t1", "a2")
    ledger.transfer("t1", "a3")
    history = ownership_history(ledger, "t1")
    assert [e.action for e in history] == ["assign", "transfer", "transfer"]
    assert responsibility_chain(ledger, "t1") == ["a1", "a2", "a3"]
