from datetime import datetime

from workflow_os.decision import DecisionRecord


def test_create_fills_id_and_timestamp():
    record = DecisionRecord.create(
        workflow_id="wf",
        decision_type="workflow_decision",
        decision="Proceed with onboarding",
    )
    assert record.decision_id
    assert isinstance(record.timestamp, datetime)
    assert record.workflow_id == "wf"
    assert record.decision == "Proceed with onboarding"
    assert record.outcome == "pending"
    assert record.alternatives == []
    assert record.rationale == ""
    assert record.confidence == 1.0
    assert record.metadata == {}


def test_create_with_full_fields():
    record = DecisionRecord.create(
        workflow_id="wf",
        decision_type="step_decision",
        decision="Approve laptop request",
        rationale="Budget available and role requires it",
        alternatives=["Defer to next quarter", "Use refurbished unit"],
        step_id="assign_laptop",
        actor="it",
        outcome="successful",
        confidence=0.8,
        metadata={"cost": 1200},
    )
    assert record.step_id == "assign_laptop"
    assert record.actor == "it"
    assert record.alternatives == ["Defer to next quarter", "Use refurbished unit"]
    assert record.outcome == "successful"
    assert record.confidence == 0.8
    assert record.metadata == {"cost": 1200}


def test_alternatives_are_independent_between_records():
    a = DecisionRecord.create(workflow_id="a", decision_type="manual_decision", decision="A")
    b = DecisionRecord.create(workflow_id="b", decision_type="manual_decision", decision="B")
    a.alternatives.append("option")
    assert b.alternatives == []
