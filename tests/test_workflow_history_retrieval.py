from workflow_os import Workflow, WorkflowStep
from workflow_os.memory import MemoryRecorder, SQLiteMemoryStore, get_workflow_history


def make_workflow() -> Workflow:
    return Workflow(
        id="wf",
        name="Onboarding",
        steps=[WorkflowStep(id="s1", name="Create account")],
    )


def test_history_is_ordered_oldest_first():
    store = SQLiteMemoryStore()
    MemoryRecorder(store).run(make_workflow())
    history = get_workflow_history(store, "wf")
    timestamps = [record.timestamp for record in history]
    assert timestamps == sorted(timestamps)
    assert history[0].event_type == "workflow_started"


def test_history_descending_order():
    store = SQLiteMemoryStore()
    MemoryRecorder(store).run(make_workflow())
    history = get_workflow_history(store, "wf", order="desc")
    assert history[0].event_type == "workflow_completed"


def test_history_limit():
    store = SQLiteMemoryStore()
    MemoryRecorder(store).run(make_workflow())
    history = get_workflow_history(store, "wf", limit=2)
    assert len(history) == 2


def test_history_empty_for_unknown_workflow():
    store = SQLiteMemoryStore()
    assert get_workflow_history(store, "missing") == []
