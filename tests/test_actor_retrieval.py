from workflow_os import Workflow, WorkflowStep
from workflow_os.memory import MemoryRecorder, SQLiteMemoryStore, get_actor_history


def make_workflow() -> Workflow:
    return Workflow(
        id="wf",
        name="Onboarding",
        metadata={"owner": "people-ops"},
        steps=[
            WorkflowStep(id="s1", name="Create account", assignee="it"),
            WorkflowStep(id="s2", name="Welcome", dependencies=["s1"], assignee="hr"),
        ],
    )


def test_actor_history_returns_only_that_actor():
    store = SQLiteMemoryStore()
    MemoryRecorder(store).run(make_workflow())

    it_events = get_actor_history(store, "it")
    assert it_events
    assert all(record.actor == "it" for record in it_events)
    assert all(record.step_id == "s1" for record in it_events)


def test_owner_actor_history_includes_workflow_events():
    store = SQLiteMemoryStore()
    MemoryRecorder(store).run(make_workflow())

    owner_events = get_actor_history(store, "people-ops")
    event_types = {record.event_type for record in owner_events}
    assert "workflow_started" in event_types
    assert "workflow_completed" in event_types


def test_unknown_actor_returns_empty():
    store = SQLiteMemoryStore()
    MemoryRecorder(store).run(make_workflow())
    assert get_actor_history(store, "nobody") == []
