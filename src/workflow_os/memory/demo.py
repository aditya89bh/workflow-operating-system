"""A runnable demonstration of the organizational memory system.

The :func:`run_demo` function walks through the full memory lifecycle:

1. execute a workflow,
2. generate memory events automatically,
3. store them,
4. retrieve the workflow history, and
5. generate an audit report.

It is shared by the ``examples/memory_demo.py`` script and the
``workflow-os memory-demo`` CLI command.
"""

from __future__ import annotations

from workflow_os.memory.audit import AuditReport, generate_audit_report
from workflow_os.memory.recorder import MemoryRecorder
from workflow_os.memory.retrieval import get_workflow_history
from workflow_os.memory.sqlite_store import SQLiteMemoryStore
from workflow_os.memory.store import MemoryStore
from workflow_os.step import WorkflowStep
from workflow_os.workflow import Workflow


def build_demo_workflow() -> Workflow:
    """Return the employee-onboarding workflow used by the demo."""
    return Workflow(
        id="employee-onboarding",
        name="Employee Onboarding",
        description="Onboard a new employee end to end.",
        metadata={"owner": "people-ops"},
        steps=[
            WorkflowStep(id="create_account", name="Create account", assignee="it"),
            WorkflowStep(
                id="provision_email",
                name="Provision email",
                dependencies=["create_account"],
                assignee="it",
            ),
            WorkflowStep(
                id="welcome_meeting",
                name="Schedule welcome meeting",
                dependencies=["provision_email"],
                assignee="manager",
            ),
        ],
    )


def run_demo(store: MemoryStore | None = None) -> AuditReport:
    """Run the memory demo end to end and return the resulting audit report."""
    store = store if store is not None else SQLiteMemoryStore()
    workflow = build_demo_workflow()

    print(f"1. Executing workflow {workflow.name!r} ({workflow.id})")
    recorder = MemoryRecorder(store)
    recorder.run(workflow)
    print(f"   workflow finished with status {workflow.status.value!r}")

    history = get_workflow_history(store, workflow.id)
    print(f"2-3. Generated and stored {len(history)} memory events")

    print("4. Workflow history:")
    for record in history:
        target = record.step_id or "-"
        actor = record.actor or "-"
        print(
            f"   {record.timestamp.isoformat()} "
            f"{record.event_type:<18} step={target:<16} actor={actor}"
        )

    report = generate_audit_report(store)
    print("5. Audit report:")
    print(f"   total events : {report.total_events}")
    print(f"   event types  : {report.event_type_counts}")
    print(f"   workflows    : {report.workflow_count}")
    print(f"   actors       : {report.actor_counts}")
    print(f"   oldest event : {report.oldest_event}")
    print(f"   newest event : {report.newest_event}")

    return report
