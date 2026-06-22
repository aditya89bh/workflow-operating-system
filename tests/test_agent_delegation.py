import pytest

from workflow_os.agents import (
    DelegationError,
    TaskDelegation,
    TaskNotFoundError,
)


def test_assign_creates_assignment():
    ledger = TaskDelegation()
    a = ledger.assign(
        workflow_id="wf", owner="agent-1", step_id="s1", assigned_by="coord", task_id="t1"
    )
    assert a.owner == "agent-1"
    assert a.active
    assert ledger.assignment("t1").owner == "agent-1"


def test_duplicate_assign_raises():
    ledger = TaskDelegation()
    ledger.assign(workflow_id="wf", owner="a1", task_id="t1")
    with pytest.raises(DelegationError):
        ledger.assign(workflow_id="wf", owner="a2", task_id="t1")


def test_transfer():
    ledger = TaskDelegation()
    ledger.assign(workflow_id="wf", owner="a1", task_id="t1")
    ledger.transfer("t1", "a2", actor="coord")
    assert ledger.assignment("t1").owner == "a2"


def test_revoke_marks_inactive():
    ledger = TaskDelegation()
    ledger.assign(workflow_id="wf", owner="a1", task_id="t1")
    ledger.revoke("t1", actor="coord")
    assignment = ledger.assignment("t1")
    assert assignment.owner is None
    assert not assignment.active
    assert ledger.active_assignments() == []
    with pytest.raises(DelegationError):
        ledger.transfer("t1", "a3")


def test_history_and_missing():
    ledger = TaskDelegation()
    ledger.assign(workflow_id="wf", owner="a1", task_id="t1")
    ledger.transfer("t1", "a2")
    ledger.revoke("t1")
    actions = [e.action for e in ledger.history("t1")]
    assert actions == ["assign", "transfer", "revoke"]
    assert len(ledger.history()) == 3
    with pytest.raises(TaskNotFoundError):
        ledger.assignment("nope")
