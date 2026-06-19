from workflow_os import Workflow, WorkflowStep
from workflow_os.memory import (
    MemoryQuery,
    MemoryRecorder,
    SQLiteMemoryStore,
    step_actor,
    workflow_owner,
)


def make_workflow() -> Workflow:
    return Workflow(
        id="wf",
        name="Onboarding",
        metadata={"owner": "people-ops"},
        steps=[
            WorkflowStep(id="s1", name="Create account", assignee="it"),
            WorkflowStep(id="s2", name="Welcome", dependencies=["s1"]),
        ],
    )


def test_owner_and_step_actor_helpers():
    wf = make_workflow()
    assert workflow_owner(wf) == "people-ops"
    assert step_actor(wf, wf.steps[0]) == "it"
    assert step_actor(wf, wf.steps[1]) == "people-ops"


def test_workflow_events_attributed_to_owner():
    store = SQLiteMemoryStore()
    MemoryRecorder(store).run(make_workflow())
    started = store.query(MemoryQuery(event_types=("workflow_started",)))
    assert started[0].actor == "people-ops"


def test_step_events_attributed_to_assignee_then_owner():
    store = SQLiteMemoryStore()
    MemoryRecorder(store).run(make_workflow())

    s1 = store.query(MemoryQuery(step_id="s1", event_types=("step_completed",)))
    s2 = store.query(MemoryQuery(step_id="s2", event_types=("step_completed",)))
    assert s1[0].actor == "it"
    assert s2[0].actor == "people-ops"


def test_no_owner_leaves_actor_none():
    store = SQLiteMemoryStore()
    wf = Workflow(id="wf", name="No owner", steps=[WorkflowStep(id="s1", name="A")])
    MemoryRecorder(store).run(wf)
    started = store.query(MemoryQuery(event_types=("workflow_started",)))
    assert started[0].actor is None
