"""Customer onboarding workflow demonstration.

Builds a SaaS customer onboarding workflow (signup through go-live) and runs it
end to end through the memory recorder, printing the resolved execution order and
a short summary of the recorded history.
"""

from __future__ import annotations

from workflow_os.executor import WorkflowExecutor
from workflow_os.memory.recorder import MemoryRecorder
from workflow_os.memory.sqlite_store import SQLiteMemoryStore
from workflow_os.step import WorkflowStep
from workflow_os.workflow import Workflow


def build_workflow() -> Workflow:
    """Return a multi-step customer onboarding workflow."""
    return Workflow(
        id="customer-onboarding",
        name="Customer Onboarding",
        description="Onboard a new SaaS customer from signup to go-live",
        metadata={"owner": "customer-success", "domain": "sales"},
        steps=[
            WorkflowStep(id="signup", name="Account signup", assignee="sales"),
            WorkflowStep(
                id="kickoff",
                name="Kickoff call",
                assignee="customer-success",
                dependencies=["signup"],
            ),
            WorkflowStep(
                id="provision",
                name="Provision tenant",
                assignee="platform",
                dependencies=["signup"],
            ),
            WorkflowStep(
                id="data_import",
                name="Import customer data",
                assignee="platform",
                dependencies=["provision"],
            ),
            WorkflowStep(
                id="training",
                name="Train customer team",
                assignee="customer-success",
                dependencies=["kickoff", "data_import"],
            ),
            WorkflowStep(
                id="go_live",
                name="Go live",
                assignee="customer-success",
                dependencies=["training"],
            ),
        ],
    )


def run_demo() -> Workflow:
    """Run the customer onboarding demonstration and print a summary."""
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
