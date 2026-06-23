"""Incident management workflow demonstration.

Builds an incident response workflow (detect through post-mortem) and runs it end
to end through the memory recorder, printing the resolved execution order and a
short summary of the recorded history.
"""

from __future__ import annotations

from workflow_os.executor import WorkflowExecutor
from workflow_os.memory.recorder import MemoryRecorder
from workflow_os.memory.sqlite_store import SQLiteMemoryStore
from workflow_os.step import WorkflowStep
from workflow_os.workflow import Workflow


def build_workflow() -> Workflow:
    """Return a multi-step incident management workflow."""
    return Workflow(
        id="incident-management",
        name="Incident Management",
        description="Respond to and resolve a production incident",
        metadata={"owner": "sre", "domain": "operations"},
        steps=[
            WorkflowStep(id="detect", name="Detect incident", assignee="monitoring"),
            WorkflowStep(
                id="triage",
                name="Triage and assign severity",
                assignee="on-call",
                dependencies=["detect"],
            ),
            WorkflowStep(
                id="mitigate",
                name="Apply mitigation",
                assignee="on-call",
                dependencies=["triage"],
            ),
            WorkflowStep(
                id="notify",
                name="Notify stakeholders",
                assignee="incident-commander",
                dependencies=["triage"],
            ),
            WorkflowStep(
                id="resolve",
                name="Resolve incident",
                assignee="on-call",
                dependencies=["mitigate"],
            ),
            WorkflowStep(
                id="postmortem",
                name="Write post-mortem",
                assignee="incident-commander",
                dependencies=["resolve", "notify"],
            ),
        ],
    )


def run_demo() -> Workflow:
    """Run the incident management demonstration and print a summary."""
    workflow = build_workflow()
    print(f"workflow: {workflow.name} ({len(workflow.steps)} steps)")

    order = WorkflowExecutor(workflow).execution_order()
    print("resolved execution order:")
    for index, step in enumerate(order, start=1):
        deps = ", ".join(step.dependencies) or "-"
        print(f"  {index}. {step.name} [{step.assignee}] (depends on: {deps})")

    store = SQLiteMemoryStore(":memory:")
    MemoryRecorder(store).run(workflow)
    records = store.list()
    print(f"\nworkflow finished as {workflow.status.value!r}")
    print(f"recorded {len(records)} memory events")
    return workflow


if __name__ == "__main__":  # pragma: no cover
    run_demo()
