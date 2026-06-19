from workflow_os import Workflow, WorkflowStep
from workflow_os.memory import (
    AuditReport,
    MemoryRecorder,
    SQLiteMemoryStore,
    generate_audit_report,
)


def make_workflow(workflow_id: str = "wf") -> Workflow:
    return Workflow(
        id=workflow_id,
        name="Onboarding",
        metadata={"owner": "people-ops"},
        steps=[
            WorkflowStep(id="s1", name="Create account", assignee="it"),
            WorkflowStep(id="s2", name="Welcome", dependencies=["s1"]),
        ],
    )


def test_empty_store_report():
    report = generate_audit_report(SQLiteMemoryStore())
    assert report == AuditReport()
    assert report.total_events == 0
    assert report.oldest_event is None


def test_report_counts_and_span():
    store = SQLiteMemoryStore()
    recorder = MemoryRecorder(store)
    recorder.run(make_workflow("wf-a"))
    recorder.run(make_workflow("wf-b"))

    report = generate_audit_report(store)
    assert report.total_events == len(store.list())
    assert report.workflow_count == 2
    assert report.event_type_counts["workflow_completed"] == 2
    assert "it" in report.actor_counts
    assert report.oldest_event is not None
    assert report.newest_event is not None
    assert report.oldest_event <= report.newest_event


def test_report_as_dict_is_serialisable():
    store = SQLiteMemoryStore()
    MemoryRecorder(store).run(make_workflow())
    data = generate_audit_report(store).as_dict()
    assert data["total_events"] > 0
    assert data["workflow_count"] == 1
    assert isinstance(data["event_type_counts"], dict)
