from workflow_os import Workflow, WorkflowStep
from workflow_os.memory import (
    MemoryRecorder,
    SQLiteMemoryStore,
    get_step_records,
    get_step_timeline,
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


def test_step_records_only_include_that_step():
    store = SQLiteMemoryStore()
    MemoryRecorder(store).run(make_workflow())

    records = get_step_records(store, "wf", "s1")
    assert records
    assert all(record.step_id == "s1" for record in records)
    event_types = [record.event_type for record in records]
    assert event_types == ["step_started", "step_completed"]


def test_step_timeline_starts_at_zero():
    store = SQLiteMemoryStore()
    MemoryRecorder(store).run(make_workflow())

    timeline = get_step_timeline(store, "wf", "s2")
    assert timeline
    assert timeline[0].offset_seconds == 0.0
    assert all(entry.step_id == "s2" for entry in timeline)


def test_step_history_empty_for_unknown_step():
    store = SQLiteMemoryStore()
    MemoryRecorder(store).run(make_workflow())
    assert get_step_records(store, "wf", "missing") == []
    assert get_step_timeline(store, "wf", "missing") == []
