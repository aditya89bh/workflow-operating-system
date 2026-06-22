"""Decision benchmark datasets.

Ready-made decision datasets for common organizational scenarios: employee
onboarding, procurement, incident response, and customer support. They are used
by tests, demos, and ad-hoc exploration of the analysis tooling. Datasets use
stable decision ids and deterministic timestamps so they replay identically.
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime, timedelta, timezone

from workflow_os.decision.outcome import DecisionOutcome
from workflow_os.decision.record import DecisionRecord
from workflow_os.decision.store import DecisionStore
from workflow_os.decision.types import DecisionType

_BASE = datetime(2026, 1, 1, tzinfo=timezone.utc)


class UnknownBenchmarkError(KeyError):
    """Raised when an unknown benchmark dataset name is requested."""


def _record(
    workflow_id: str,
    index: int,
    decision_type: DecisionType,
    decision: str,
    rationale: str,
    alternatives: list[str],
    actor: str,
    outcome: DecisionOutcome,
    *,
    step_id: str | None = None,
) -> DecisionRecord:
    return DecisionRecord.create(
        decision_id=f"{workflow_id}-{index:02d}",
        workflow_id=workflow_id,
        decision_type=decision_type.value,
        decision=decision,
        rationale=rationale,
        alternatives=alternatives,
        actor=actor,
        outcome=outcome.value,
        step_id=step_id,
        timestamp=_BASE + timedelta(minutes=index),
    )


def onboarding_dataset() -> list[DecisionRecord]:
    """Decisions taken while onboarding a new employee."""
    wf = "onboarding"
    return [
        _record(wf, 1, DecisionType.WORKFLOW_DECISION, "Run standard onboarding",
                "New hire with a typical engineering role", ["Fast-track onboarding"],
                "people-ops", DecisionOutcome.SUCCESSFUL),
        _record(wf, 2, DecisionType.STEP_DECISION, "Provision SSO account",
                "Required for all systems", [], "it", DecisionOutcome.SUCCESSFUL,
                step_id="create_account"),
        _record(wf, 3, DecisionType.STEP_DECISION, "Issue standard laptop",
                "Role does not need high-spec hardware", ["Issue high-spec laptop"],
                "it", DecisionOutcome.SUCCESSFUL, step_id="assign_laptop"),
        _record(wf, 4, DecisionType.EXCEPTION_DECISION, "Retry email provisioning",
                "Primary mail provider timed out", ["Provision mailbox manually"],
                "it", DecisionOutcome.FAILED, step_id="provision_email"),
        _record(wf, 5, DecisionType.MANUAL_DECISION, "Schedule welcome meeting",
                "Manager available on day one", [], "manager",
                DecisionOutcome.SUCCESSFUL, step_id="welcome_meeting"),
    ]


def procurement_dataset() -> list[DecisionRecord]:
    """Decisions taken during a procurement workflow."""
    wf = "procurement"
    return [
        _record(wf, 1, DecisionType.WORKFLOW_DECISION, "Select vendor A",
                "Best price and delivery terms", ["Vendor B", "Vendor C"],
                "procurement", DecisionOutcome.SUCCESSFUL),
        _record(wf, 2, DecisionType.STEP_DECISION, "Negotiate net-60 terms",
                "Improves cash flow", ["Net-30 terms"], "finance",
                DecisionOutcome.SUCCESSFUL),
        _record(wf, 3, DecisionType.EXCEPTION_DECISION, "Escalate budget overrun",
                "Quote exceeds approved budget", ["Reduce order quantity"],
                "finance", DecisionOutcome.FAILED),
        _record(wf, 4, DecisionType.MANUAL_DECISION, "Defer non-critical items",
                "Not needed this quarter", [], "procurement",
                DecisionOutcome.PENDING),
    ]


def incident_dataset() -> list[DecisionRecord]:
    """Decisions taken during incident response."""
    wf = "incident"
    return [
        _record(wf, 1, DecisionType.WORKFLOW_DECISION, "Declare SEV-2 incident",
                "Customer-facing degradation, not full outage", ["SEV-1", "SEV-3"],
                "incident-commander", DecisionOutcome.SUCCESSFUL),
        _record(wf, 2, DecisionType.STEP_DECISION, "Page on-call engineer",
                "Fast escalation required", [], "incident-commander",
                DecisionOutcome.SUCCESSFUL),
        _record(wf, 3, DecisionType.EXCEPTION_DECISION, "Roll back deployment",
                "Latest release correlates with errors", ["Hotfix forward"],
                "sre", DecisionOutcome.SUCCESSFUL),
        _record(wf, 4, DecisionType.EXCEPTION_DECISION, "Failover to secondary region",
                "Primary region still unstable", ["Wait for recovery"], "sre",
                DecisionOutcome.FAILED),
        _record(wf, 5, DecisionType.MANUAL_DECISION, "Schedule postmortem",
                "Standard practice after SEV-2", [], "incident-commander",
                DecisionOutcome.PENDING),
    ]


def customer_support_dataset() -> list[DecisionRecord]:
    """Decisions taken while handling a customer support case."""
    wf = "support"
    return [
        _record(wf, 1, DecisionType.STEP_DECISION, "Issue full refund",
                "Defective product within return window",
                ["Partial refund", "Store credit"], "agent",
                DecisionOutcome.SUCCESSFUL),
        _record(wf, 2, DecisionType.MANUAL_DECISION, "Escalate to tier 2",
                "Requires engineering investigation", [], "agent",
                DecisionOutcome.SUCCESSFUL),
        _record(wf, 3, DecisionType.EXCEPTION_DECISION, "Reopen ticket after SLA breach",
                "Customer reported recurrence", ["Open new ticket"], "supervisor",
                DecisionOutcome.FAILED),
        _record(wf, 4, DecisionType.WORKFLOW_DECISION, "Close ticket",
                "Issue resolved and confirmed by customer", [], "agent",
                DecisionOutcome.SUCCESSFUL),
    ]


BENCHMARK_DATASETS: dict[str, Callable[[], list[DecisionRecord]]] = {
    "onboarding": onboarding_dataset,
    "procurement": procurement_dataset,
    "incidents": incident_dataset,
    "customer_support": customer_support_dataset,
}


def list_benchmarks() -> list[str]:
    """Return the names of the available benchmark datasets."""
    return sorted(BENCHMARK_DATASETS)


def load_benchmark(name: str) -> list[DecisionRecord]:
    """Return the decisions for a named benchmark dataset."""
    try:
        builder = BENCHMARK_DATASETS[name]
    except KeyError as exc:
        available = ", ".join(list_benchmarks())
        raise UnknownBenchmarkError(
            f"unknown benchmark {name!r}; available: [{available}]"
        ) from exc
    return builder()


def load_benchmark_into(store: DecisionStore, name: str) -> int:
    """Load a named benchmark dataset into ``store`` and return the count added."""
    records = load_benchmark(name)
    for record in records:
        store.add(record)
    return len(records)


def load_all_benchmarks_into(store: DecisionStore) -> int:
    """Load every benchmark dataset into ``store`` and return the total count."""
    return sum(load_benchmark_into(store, name) for name in list_benchmarks())
