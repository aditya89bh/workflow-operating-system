from workflow_os import Workflow, WorkflowStep
from workflow_os.memory import MemoryQuery, MemoryRecorder, SQLiteMemoryStore


def make_workflow() -> Workflow:
    return Workflow(
        id="wf",
        name="Onboarding",
        steps=[WorkflowStep(id="s1", name="Create account")],
    )


def test_workflow_completion_records_duration():
    store = SQLiteMemoryStore()
    MemoryRecorder(store).run(make_workflow())
    completed = store.query(MemoryQuery(event_types=("workflow_completed",)))
    duration = completed[0].metadata["duration_seconds"]
    assert isinstance(duration, float)
    assert duration >= 0.0


def test_step_completion_records_duration():
    store = SQLiteMemoryStore()
    MemoryRecorder(store).run(make_workflow())
    completed = store.query(MemoryQuery(event_types=("step_completed",)))
    duration = completed[0].metadata["duration_seconds"]
    assert isinstance(duration, float)
    assert duration >= 0.0


def test_started_events_have_no_duration():
    store = SQLiteMemoryStore()
    MemoryRecorder(store).run(make_workflow())
    started = store.query(MemoryQuery(event_types=("workflow_started",)))
    assert "duration_seconds" not in started[0].metadata
