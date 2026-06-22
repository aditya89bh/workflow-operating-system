"""A runnable demonstration of the decision intelligence layer.

The demo walks through the full loop: it executes a workflow (recording
organizational memory), captures decisions about that workflow, stores them,
retrieves and explains them, compares outcomes, and replays them.
"""

from __future__ import annotations

from workflow_os.decision.comparison import compare_successful_vs_failed
from workflow_os.decision.recorder import DecisionRecorder
from workflow_os.decision.replay import replay_workflow_decisions
from workflow_os.decision.sqlite_store import SQLiteDecisionStore
from workflow_os.decision.statistics import compute_decision_statistics
from workflow_os.decision.store import DecisionStore
from workflow_os.decision.timelines import get_workflow_decision_timeline
from workflow_os.memory.recorder import MemoryRecorder
from workflow_os.memory.sqlite_store import SQLiteMemoryStore
from workflow_os.step import WorkflowStep
from workflow_os.workflow import Workflow


def build_demo_workflow() -> Workflow:
    """Return a small onboarding workflow used by the demonstration."""
    return Workflow(
        id="onboarding",
        name="Employee Onboarding",
        description="Bring a new hire on board",
        metadata={"owner": "people-ops"},
        steps=[
            WorkflowStep(id="create_account", name="Create account", assignee="it"),
            WorkflowStep(
                id="provision_email",
                name="Provision email",
                assignee="it",
                dependencies=["create_account"],
            ),
            WorkflowStep(
                id="welcome_meeting",
                name="Welcome meeting",
                assignee="manager",
                dependencies=["create_account"],
            ),
        ],
    )


def run_demo(store: DecisionStore | None = None) -> DecisionStore:
    """Run the decision intelligence demonstration, printing each stage."""
    workflow = build_demo_workflow()

    # 1. Execute the workflow, recording organizational memory.
    print("1. executing workflow with organizational memory")
    MemoryRecorder(SQLiteMemoryStore()).run(workflow)
    print(f"   workflow {workflow.id!r} finished as {workflow.status.value!r}")

    # 2 + 3. Record and store decisions taken during the workflow.
    store = store if store is not None else SQLiteDecisionStore()
    recorder = DecisionRecorder(store)
    print("\n2. recording decisions")
    wf_decision = recorder.record_workflow_decision(
        workflow,
        "Run standard onboarding track",
        rationale="New hire fills a typical engineering role",
        alternatives=["Fast-track onboarding"],
        outcome="successful",
    )
    recorder.record_step_decision(
        workflow,
        workflow.steps[0],
        "Provision SSO account",
        rationale="Required for system access",
        outcome="successful",
    )
    exception = recorder.record_exception_decision(
        workflow,
        "Retry email provisioning with backup provider",
        step=workflow.steps[1],
        reason="primary mail provider timed out",
        alternatives=["Provision mailbox manually"],
    )
    print(f"   stored {len(store.list())} decisions")

    # Outcomes can be updated after the fact.
    recorder.update_decision_outcome(exception.decision_id, "failed")

    # 4. Retrieve the decision timeline.
    print("\n3. retrieving decision timeline")
    for entry in get_workflow_decision_timeline(store, workflow.id):
        print(f"   +{entry.offset_seconds:6.2f}s  {entry.decision_type:18}  "
              f"{entry.decision} -> {entry.outcome}")

    # 5. Compare successful vs failed decisions.
    print("\n4. comparing successful vs failed decisions")
    comparison = compare_successful_vs_failed(store)
    print(f"   successful: {comparison.stats_a.total_decisions}  "
          f"failed: {comparison.stats_b.total_decisions}")
    stats = compute_decision_statistics(store)
    print(f"   success rate: {stats.success_rate:.0%}")

    # 6. Replay the decisions with explanations.
    print("\n5. replaying decisions")
    for event in replay_workflow_decisions(store, workflow.id):
        print(f"   [{event.sequence}] {event.explanation.what_happened}")
        print(f"       why: {event.explanation.why}")
        print(f"       {event.explanation.outcome}")

    print(f"\ndone. first decision id: {wf_decision.decision_id}")
    return store


if __name__ == "__main__":  # pragma: no cover
    run_demo()
