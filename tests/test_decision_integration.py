"""End-to-end integration tests for the decision intelligence layer.

These exercise the full Capture -> Store -> Retrieve -> Replay -> Analyze loop
across the decision modules working together.
"""

from __future__ import annotations

from workflow_os.decision import (
    DecisionRecorder,
    SQLiteDecisionStore,
    compare_successful_vs_failed,
    compute_decision_statistics,
    explain_decision,
    get_workflow_decision_timeline,
    load_benchmark_into,
    replay_workflow_decisions,
    search_by_decision_text,
    set_decision_outcome,
)
from workflow_os.step import WorkflowStep
from workflow_os.workflow import Workflow


def _workflow() -> Workflow:
    return Workflow(
        id="onboarding",
        name="Employee Onboarding",
        metadata={"owner": "people-ops"},
        steps=[
            WorkflowStep(id="create_account", name="Create account", assignee="it"),
            WorkflowStep(id="provision_email", name="Provision email", assignee="it"),
        ],
    )


def test_capture_store_retrieve_replay_analyze():
    store = SQLiteDecisionStore()
    recorder = DecisionRecorder(store)
    workflow = _workflow()

    # Capture
    wf_decision = recorder.record_workflow_decision(
        workflow, "Run standard onboarding", rationale="Typical role"
    )
    recorder.record_step_decision(
        workflow,
        workflow.steps[0],
        "Provision SSO account",
        rationale="Required for access",
        outcome="successful",
    )
    exc = recorder.record_exception_decision(
        workflow,
        "Retry email provisioning",
        step=workflow.steps[1],
        reason="provider timeout",
    )

    # Store + Retrieve
    assert len(store.list()) == 3
    assert search_by_decision_text(store, "onboarding")[0].decision_id == (
        wf_decision.decision_id
    )

    # Update outcomes after the fact
    set_decision_outcome(store, wf_decision.decision_id, "successful")
    set_decision_outcome(store, exc.decision_id, "failed")

    # Replay
    replay = replay_workflow_decisions(store, "onboarding")
    assert [event.sequence for event in replay] == [0, 1, 2]
    assert "Retry email provisioning" in replay[2].decision.decision

    # Timeline
    timeline = get_workflow_decision_timeline(store, "onboarding")
    assert len(timeline) == 3
    assert timeline[0].offset_seconds == 0.0

    # Analyze
    stats = compute_decision_statistics(store)
    assert stats.total_decisions == 3
    assert stats.outcome_counts["successful"] == 2
    assert stats.outcome_counts["failed"] == 1

    comparison = compare_successful_vs_failed(store)
    assert comparison.stats_a.total_decisions == 2
    assert comparison.stats_b.total_decisions == 1

    # Explanation
    explanation = explain_decision(exc)
    assert "Retry email provisioning" in explanation.what_happened


def test_benchmark_dataset_analysis():
    store = SQLiteDecisionStore()
    load_benchmark_into(store, "incidents")
    stats = compute_decision_statistics(store)
    assert stats.total_decisions == 5
    assert stats.decisions_by_type["exception_decision"] == 2
    assert "incident-commander" in stats.actor_statistics
