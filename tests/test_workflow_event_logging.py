from workflow_os import Workflow, WorkflowStatus, WorkflowStep
from workflow_os.memory import (
    MemoryEventType,
    MemoryRecorder,
    SQLiteMemoryStore,
)


def make_workflow():
    return Workflow(
        id="wf",
        name="Onboarding",
        steps=[WorkflowStep(id="s1", name="Create account")],
    )


def event_types(store, workflow_id="wf"):
    return [r.event_type for r in store.list() if r.workflow_id == workflow_id]


def test_start_logs_workflow_started():
    store = SQLiteMemoryStore()
    recorder = MemoryRecorder(store)
    wf = recorder.start(make_workflow())
    assert wf.status is WorkflowStatus.RUNNING
    assert event_types(store) == [MemoryEventType.WORKFLOW_STARTED]


def test_pause_resume_complete_sequence():
    store = SQLiteMemoryStore()
    recorder = MemoryRecorder(store)
    wf = make_workflow()
    recorder.start(wf)
    recorder.pause(wf)
    recorder.resume(wf)
    # complete the only step so completion is allowed
    wf.steps[0].status = "completed"
    recorder.complete(wf)
    assert event_types(store) == [
        MemoryEventType.WORKFLOW_STARTED,
        MemoryEventType.WORKFLOW_PAUSED,
        MemoryEventType.WORKFLOW_RESUMED,
        MemoryEventType.WORKFLOW_COMPLETED,
    ]
    assert wf.status is WorkflowStatus.COMPLETED


def test_fail_logs_workflow_failed_with_reason():
    store = SQLiteMemoryStore()
    recorder = MemoryRecorder(store)
    wf = make_workflow()
    recorder.start(wf)
    recorder.fail(wf, reason="boom")
    assert wf.status is WorkflowStatus.FAILED
    failed = [r for r in store.list() if r.event_type == MemoryEventType.WORKFLOW_FAILED]
    assert len(failed) == 1
    assert failed[0].metadata["reason"] == "boom"
