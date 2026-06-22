from workflow_os.decision import DecisionRecorder, DecisionType, SQLiteDecisionStore
from workflow_os.step import WorkflowStep
from workflow_os.workflow import Workflow


def test_record_step_decision_uses_assignee_as_actor():
    store = SQLiteDecisionStore()
    recorder = DecisionRecorder(store)
    workflow = Workflow(id="wf", name="Onboarding", metadata={"owner": "people-ops"})
    step = WorkflowStep(id="assign_laptop", name="Assign laptop", assignee="it")

    record = recorder.record_step_decision(
        workflow,
        step,
        "Issue a high-spec laptop",
        rationale="Engineering role",
        alternatives=["Standard laptop"],
    )

    assert record.decision_type == DecisionType.STEP_DECISION.value
    assert record.step_id == "assign_laptop"
    assert record.actor == "it"


def test_record_step_decision_falls_back_to_owner():
    store = SQLiteDecisionStore()
    recorder = DecisionRecorder(store)
    workflow = Workflow(id="wf", name="Onboarding", metadata={"owner": "people-ops"})
    step = WorkflowStep(id="welcome", name="Welcome meeting")

    record = recorder.record_step_decision(workflow, step, "Schedule for day one")
    assert record.actor == "people-ops"
