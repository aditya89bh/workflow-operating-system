"""End-to-end integration tests for the organizational memory system."""

from datetime import timedelta

from workflow_os import Workflow, WorkflowStatus, WorkflowStep
from workflow_os.memory import (
    MemoryRecorder,
    SQLiteMemoryStore,
    generate_audit_report,
    get_actor_history,
    get_events_since,
    get_execution_timeline,
    get_workflow_history,
    prune_workflow,
    utcnow,
)


def make_workflow(workflow_id: str) -> Workflow:
    return Workflow(
        id=workflow_id,
        name="Employee Onboarding",
        metadata={"owner": "people-ops"},
        steps=[
            WorkflowStep(id="create_account", name="Create account", assignee="it"),
            WorkflowStep(
                id="welcome",
                name="Welcome",
                dependencies=["create_account"],
                assignee="manager",
            ),
        ],
    )


def test_full_lifecycle_generates_and_persists_memory():
    store = SQLiteMemoryStore()
    recorder = MemoryRecorder(store)

    workflow = recorder.run(make_workflow("wf-1"))
    assert workflow.status is WorkflowStatus.COMPLETED

    history = get_workflow_history(store, "wf-1")
    event_types = [record.event_type for record in history]
    assert event_types[0] == "workflow_started"
    assert event_types[-1] == "workflow_completed"
    assert event_types.count("step_completed") == 2

    timeline = get_execution_timeline(store, "wf-1")
    assert timeline[0].offset_seconds == 0.0
    assert len(timeline) == len(history)


def test_pause_resume_flow_is_recorded():
    store = SQLiteMemoryStore()
    recorder = MemoryRecorder(store)
    workflow = make_workflow("wf-2")

    recorder.start(workflow)
    recorder.pause(workflow)
    recorder.resume(workflow)
    for step in workflow.steps:
        recorder.start_step(workflow, step)
        recorder.complete_step(workflow, step)
    recorder.complete(workflow)

    types = [r.event_type for r in get_workflow_history(store, "wf-2")]
    assert "workflow_paused" in types
    assert "workflow_resumed" in types


def test_cross_workflow_audit_and_retrieval():
    store = SQLiteMemoryStore()
    recorder = MemoryRecorder(store)
    recorder.run(make_workflow("wf-a"))
    recorder.run(make_workflow("wf-b"))

    report = generate_audit_report(store)
    assert report.workflow_count == 2
    assert report.event_type_counts["workflow_started"] == 2
    # "it" owns create_account: step_started + step_completed per workflow.
    assert report.actor_counts["it"] == 4

    it_history = get_actor_history(store, "it")
    assert {r.workflow_id for r in it_history} == {"wf-a", "wf-b"}

    recent = get_events_since(store, utcnow() - timedelta(hours=1))
    assert len(recent) == report.total_events


def test_workflow_scoped_pruning_preserves_others():
    store = SQLiteMemoryStore()
    recorder = MemoryRecorder(store)
    recorder.run(make_workflow("wf-keep"))
    recorder.run(make_workflow("wf-drop"))

    removed = prune_workflow(store, "wf-drop")
    assert removed > 0
    assert get_workflow_history(store, "wf-drop") == []
    assert get_workflow_history(store, "wf-keep")
