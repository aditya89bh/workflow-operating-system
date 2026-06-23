"""Procurement workflow demonstration.

Builds a purchase-request procurement workflow and runs it end to end through the
memory recorder, printing the resolved execution order and a short summary of the
recorded history.
"""

from __future__ import annotations

from workflow_os.executor import WorkflowExecutor
from workflow_os.memory.recorder import MemoryRecorder
from workflow_os.memory.sqlite_store import SQLiteMemoryStore
from workflow_os.step import WorkflowStep
from workflow_os.workflow import Workflow


def build_workflow() -> Workflow:
    """Return a multi-step procurement workflow."""
    return Workflow(
        id="procurement",
        name="Procurement Request",
        description="Purchase request from intake through delivery",
        metadata={"owner": "procurement", "domain": "finance"},
        steps=[
            WorkflowStep(id="request", name="Submit purchase request", assignee="requester"),
            WorkflowStep(
                id="budget_check",
                name="Budget check",
                assignee="finance",
                dependencies=["request"],
            ),
            WorkflowStep(
                id="manager_approval",
                name="Manager approval",
                assignee="manager",
                dependencies=["budget_check"],
            ),
            WorkflowStep(
                id="select_vendor",
                name="Select vendor",
                assignee="procurement",
                dependencies=["manager_approval"],
            ),
            WorkflowStep(
                id="purchase_order",
                name="Issue purchase order",
                assignee="procurement",
                dependencies=["select_vendor"],
            ),
            WorkflowStep(
                id="receive_goods",
                name="Receive goods",
                assignee="warehouse",
                dependencies=["purchase_order"],
            ),
        ],
    )


def run_demo() -> Workflow:
    """Run the procurement demonstration and print a summary."""
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
