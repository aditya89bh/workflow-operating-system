from workflow_os.decision import DecisionRecorder, SQLiteDecisionStore
from workflow_os.sop import (
    SOPExceptionStore,
    capture_exception,
    capture_exception_from_decision,
)
from workflow_os.step import WorkflowStep
from workflow_os.workflow import Workflow


def test_capture_exception_direct():
    store = SOPExceptionStore()
    exc = capture_exception(
        store,
        workflow_id="wf1",
        description="Skipped background check for internal transfer",
        sop_id="onb1",
        reason="internal transfer policy",
        author="hr",
    )
    assert store.for_sop("onb1") == [exc]
    assert store.for_workflow("wf1") == [exc]
    assert exc.reason == "internal transfer policy"


def test_capture_exception_from_decision():
    decisions = SQLiteDecisionStore()
    recorder = DecisionRecorder(decisions)
    workflow = Workflow(id="wf1", name="Onboarding", metadata={"owner": "people-ops"})
    step = WorkflowStep(id="provision_email", name="Provision email", assignee="it")
    decision = recorder.record_exception_decision(
        workflow,
        "Retry email provisioning with backup provider",
        step=step,
        reason="primary provider timeout",
    )

    store = SOPExceptionStore()
    exc = capture_exception_from_decision(store, decision, sop_id="onb1")
    assert exc.decision_id == decision.decision_id
    assert exc.workflow_id == "wf1"
    assert exc.reason == "primary provider timeout"
    assert exc.author == "it"
    assert exc.description == "Retry email provisioning with backup provider"
    assert exc.metadata["decision_type"] == "exception_decision"


def test_documentation_override():
    decisions = SQLiteDecisionStore()
    recorder = DecisionRecorder(decisions)
    workflow = Workflow(id="wf1", name="Onboarding")
    decision = recorder.record_exception_decision(workflow, "Pause workflow")

    store = SOPExceptionStore()
    exc = capture_exception_from_decision(
        store, decision, documentation="Documented exception handling"
    )
    assert exc.description == "Documented exception handling"
