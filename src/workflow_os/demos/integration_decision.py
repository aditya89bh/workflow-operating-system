"""Workflow + decision integration demonstration.

Shows the flow ``workflow -> decisions -> replay``: a workflow is executed, the
decisions taken during it are captured and stored, and they are then replayed
with deterministic explanations.
"""

from __future__ import annotations

from workflow_os.decision.recorder import DecisionRecorder
from workflow_os.decision.replay import replay_workflow_decisions
from workflow_os.decision.sqlite_store import SQLiteDecisionStore
from workflow_os.demos.employee_onboarding import build_workflow
from workflow_os.memory.recorder import MemoryRecorder
from workflow_os.memory.sqlite_store import SQLiteMemoryStore


def run_demo() -> None:
    """Run the workflow-decision integration demonstration and print a summary."""
    workflow = build_workflow()

    # 1. Execute the workflow (recording organizational memory).
    print("1. workflow -> executing")
    MemoryRecorder(SQLiteMemoryStore(":memory:")).run(workflow)
    print(f"   {workflow.id!r} finished as {workflow.status.value!r}")

    # 2. Decisions: capture the choices made during the workflow.
    print("\n2. decisions -> capturing")
    store = SQLiteDecisionStore(":memory:")
    recorder = DecisionRecorder(store)
    recorder.record_workflow_decision(
        workflow,
        "Run standard onboarding track",
        rationale="New hire fills a typical engineering role",
        alternatives=["Fast-track onboarding"],
        outcome="successful",
    )
    recorder.record_step_decision(
        workflow,
        workflow.steps[1],
        "Provision SSO account",
        rationale="Required for downstream system access",
        outcome="successful",
    )
    recorder.record_exception_decision(
        workflow,
        "Retry email provisioning with backup provider",
        step=workflow.steps[2],
        reason="primary mail provider timed out",
        alternatives=["Provision mailbox manually"],
    )
    print(f"   stored {len(store.list())} decisions")

    # 3. Replay: walk the decisions with explanations.
    print("\n3. replay -> explaining each decision")
    for event in replay_workflow_decisions(store, workflow.id):
        print(f"   [{event.sequence}] {event.explanation.what_happened}")
        print(f"       why: {event.explanation.why}")

    print("\ndone.")


if __name__ == "__main__":  # pragma: no cover
    run_demo()
