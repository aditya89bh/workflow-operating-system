from workflow_os.decision import DecisionRecorder, DecisionType, SQLiteDecisionStore
from workflow_os.workflow import Workflow


def test_record_workflow_decision_uses_owner_as_actor():
    store = SQLiteDecisionStore()
    recorder = DecisionRecorder(store)
    workflow = Workflow(id="wf", name="Onboarding", metadata={"owner": "people-ops"})

    record = recorder.record_workflow_decision(
        workflow,
        "Run onboarding in fast-track mode",
        rationale="New hire starts Monday",
        alternatives=["Standard track"],
    )

    assert record.decision_type == DecisionType.WORKFLOW_DECISION.value
    assert record.workflow_id == "wf"
    assert record.actor == "people-ops"
    assert record.step_id is None


def test_record_workflow_decision_explicit_actor_overrides_owner():
    store = SQLiteDecisionStore()
    recorder = DecisionRecorder(store)
    workflow = Workflow(id="wf", name="Onboarding", metadata={"owner": "people-ops"})

    record = recorder.record_workflow_decision(
        workflow, "Escalate", actor="director"
    )
    assert record.actor == "director"
