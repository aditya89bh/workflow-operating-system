"""Decision comparison reports.

These helpers compare two sets of decisions side by side using the same
:class:`~workflow_os.decision.statistics.DecisionStatistics` summary, making it
easy to contrast successful vs failed decisions, two workflows, or two actors.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from workflow_os.decision.outcome import DecisionOutcome
from workflow_os.decision.statistics import (
    DecisionStatistics,
    compute_decision_statistics,
)
from workflow_os.decision.store import DecisionQuery, DecisionStore


@dataclass
class ComparisonReport:
    """A side-by-side comparison of two groups of decisions."""

    label_a: str
    label_b: str
    stats_a: DecisionStatistics
    stats_b: DecisionStatistics

    def as_dict(self) -> dict[str, Any]:
        """Return a JSON-serialisable view of the comparison."""
        return {
            "label_a": self.label_a,
            "label_b": self.label_b,
            "stats_a": self.stats_a.as_dict(),
            "stats_b": self.stats_b.as_dict(),
        }


def compare_successful_vs_failed(store: DecisionStore) -> ComparisonReport:
    """Compare successful decisions against failed decisions."""
    successful = compute_decision_statistics(
        store, DecisionQuery(outcome=DecisionOutcome.SUCCESSFUL.value)
    )
    failed = compute_decision_statistics(
        store, DecisionQuery(outcome=DecisionOutcome.FAILED.value)
    )
    return ComparisonReport("successful", "failed", successful, failed)


def compare_workflows(
    store: DecisionStore, workflow_a: str, workflow_b: str
) -> ComparisonReport:
    """Compare the decisions of two workflows."""
    stats_a = compute_decision_statistics(store, DecisionQuery(workflow_id=workflow_a))
    stats_b = compute_decision_statistics(store, DecisionQuery(workflow_id=workflow_b))
    return ComparisonReport(workflow_a, workflow_b, stats_a, stats_b)


def compare_actors(
    store: DecisionStore, actor_a: str, actor_b: str
) -> ComparisonReport:
    """Compare the decisions made by two actors."""
    stats_a = compute_decision_statistics(store, DecisionQuery(actor=actor_a))
    stats_b = compute_decision_statistics(store, DecisionQuery(actor=actor_b))
    return ComparisonReport(actor_a, actor_b, stats_a, stats_b)
