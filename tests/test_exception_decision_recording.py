from workflow_os.decision import DecisionRecorder, DecisionType, SQLiteDecisionStore
from workflow_os.step import WorkflowStep
from workflow_os.workflow import Workflow


def test_record_exception_decision_for_step_failure():
    store = SQLiteDecisionStore()
    recorder = DecisionRecorder(store)
    workflow = Workflow(id="wf", name="Onboarding", metadata={"owner": "people-ops"})
    step = WorkflowStep(id="provision_email", name="Provision email", assignee="it")

    record = recorder.record_exception_decision(
        workflow,
        "Retry email provisioning with backup provider",
        step=step,
        reason="primary provider timeout",
        alternatives=["Abort onboarding", "Provision manually"],
    )

    assert record.decision_type == DecisionType.EXCEPTION_DECISION.value
    assert record.step_id == "provision_email"
    assert record.actor == "it"
    assert record.metadata["reason"] == "primary provider timeout"


def test_record_exception_decision_without_step_uses_owner():
    store = SQLiteDecisionStore()
    recorder = DecisionRecorder(store)
    workflow = Workflow(id="wf", name="Onboarding", metadata={"owner": "people-ops"})

    record = recorder.record_exception_decision(
        workflow, "Pause workflow pending investigation"
    )
    assert record.step_id is None
    assert record.actor == "people-ops"
