from workflow_os import Workflow, WorkflowStep
from workflow_os.memory import (
    MemoryRecorder,
    SQLiteMemoryStore,
    get_execution_timeline,
    get_workflow_records,
)


def make_workflow() -> Workflow:
    return Workflow(
        id="wf",
        name="Onboarding",
        steps=[
            WorkflowStep(id="s1", name="Create account"),
            WorkflowStep(id="s2", name="Assign laptop", dependencies=["s1"]),
        ],
    )


def test_workflow_records_ordered_and_complete():
    store = SQLiteMemoryStore()
    recorder = MemoryRecorder(store)
    recorder.run(make_workflow())

    records = get_workflow_records(store, "wf")
    event_types = [record.event_type for record in records]
    assert event_types[0] == "workflow_started"
    assert event_types[-1] == "workflow_completed"
    assert "step_started" in event_types
    assert "step_completed" in event_types


def test_execution_timeline_has_offsets():
    store = SQLiteMemoryStore()
    recorder = MemoryRecorder(store)
    recorder.run(make_workflow())

    timeline = get_execution_timeline(store, "wf")
    assert timeline
    assert timeline[0].offset_seconds == 0.0
    assert all(entry.offset_seconds >= 0.0 for entry in timeline)


def test_timeline_empty_for_unknown_workflow():
    store = SQLiteMemoryStore()
    assert get_execution_timeline(store, "missing") == []
    assert get_workflow_records(store, "missing") == []
