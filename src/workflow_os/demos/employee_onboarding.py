"""Employee onboarding workflow demonstration.

Builds a realistic new-hire onboarding workflow and runs it end to end through
the memory recorder, printing the resolved execution order and a short summary
of the recorded history.
"""

from __future__ import annotations

from workflow_os.executor import WorkflowExecutor
from workflow_os.memory.recorder import MemoryRecorder
from workflow_os.memory.sqlite_store import SQLiteMemoryStore
from workflow_os.step import WorkflowStep
from workflow_os.workflow import Workflow


def build_workflow() -> Workflow:
    """Return a multi-step employee onboarding workflow."""
    return Workflow(
        id="employee-onboarding",
        name="Employee Onboarding",
        description="Bring a new engineering hire on board",
        metadata={"owner": "people-ops", "domain": "hr"},
        steps=[
            WorkflowStep(id="offer_signed", name="Offer signed", assignee="recruiting"),
            WorkflowStep(
                id="create_account",
                name="Create IT account",
                assignee="it",
                dependencies=["offer_signed"],
            ),
            WorkflowStep(
                id="provision_email",
                name="Provision email",
                assignee="it",
                dependencies=["create_account"],
            ),
            WorkflowStep(
                id="assign_equipment",
                name="Assign laptop and equipment",
                assignee="it",
                dependencies=["create_account"],
            ),
            WorkflowStep(
                id="welcome_meeting",
                name="Welcome meeting",
                assignee="manager",
                dependencies=["provision_email", "assign_equipment"],
            ),
            WorkflowStep(
                id="first_task",
                name="Assign first task",
                assignee="manager",
                dependencies=["welcome_meeting"],
            ),
        ],
    )


def run_demo() -> Workflow:
    """Run the employee onboarding demonstration and print a summary."""
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
