from workflow_os import Workflow, WorkflowStatus, WorkflowStep
from workflow_os.memory import MemoryEventType, MemoryRecorder, SQLiteMemoryStore


def make_workflow():
    return Workflow(
        id="wf",
        name="Onboarding",
        steps=[
            WorkflowStep(id="s1", name="Create account"),
            WorkflowStep(id="s2", name="Assign laptop", dependencies=["s1"]),
        ],
    )


def test_run_logs_workflow_and_step_events():
    store = SQLiteMemoryStore()
    recorder = MemoryRecorder(store)
    wf = recorder.run(make_workflow())

    assert wf.status is WorkflowStatus.COMPLETED
    types = [r.event_type for r in store.list()]
    assert types == [
        MemoryEventType.WORKFLOW_STARTED,
        MemoryEventType.STEP_STARTED,
        MemoryEventType.STEP_COMPLETED,
        MemoryEventType.STEP_STARTED,
        MemoryEventType.STEP_COMPLETED,
        MemoryEventType.WORKFLOW_COMPLETED,
    ]
    step_records = [r for r in store.list() if r.step_id is not None]
    assert {r.step_id for r in step_records} == {"s1", "s2"}


def test_fail_step_records_event():
    store = SQLiteMemoryStore()
    recorder = MemoryRecorder(store)
    wf = make_workflow()
    recorder.start(wf)
    recorder.start_step(wf, wf.steps[0])
    recorder.fail_step(wf, wf.steps[0], reason="missing data")
    failed = [r for r in store.list() if r.event_type == MemoryEventType.STEP_FAILED]
    assert len(failed) == 1
    assert failed[0].step_id == "s1"
    assert failed[0].metadata["reason"] == "missing data"


def test_skip_step_records_event():
    store = SQLiteMemoryStore()
    recorder = MemoryRecorder(store)
    wf = make_workflow()
    recorder.start(wf)
    recorder.skip_step(wf, wf.steps[1])
    skipped = [r for r in store.list() if r.event_type == MemoryEventType.STEP_SKIPPED]
    assert len(skipped) == 1
    assert skipped[0].step_id == "s2"
