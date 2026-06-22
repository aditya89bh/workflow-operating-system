"""Decision statistics.

Summarise the decisions in a store: how many there are, how they break down by
type, the success and failure rates over resolved decisions, and per-actor
counts. Success and failure rates are computed over *resolved* decisions (those
that are successful or failed), so pending and unknown decisions do not distort
them.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Any

from workflow_os.decision.outcome import DecisionOutcome
from workflow_os.decision.store import DecisionQuery, DecisionStore


@dataclass
class ActorDecisionStats:
    """Per-actor decision counts."""

    total: int = 0
    successful: int = 0
    failed: int = 0

    def as_dict(self) -> dict[str, int]:
        return {
            "total": self.total,
            "successful": self.successful,
            "failed": self.failed,
        }


@dataclass
class DecisionStatistics:
    """Aggregate metrics over a set of decisions."""

    total_decisions: int = 0
    decisions_by_type: dict[str, int] = field(default_factory=dict)
    outcome_counts: dict[str, int] = field(default_factory=dict)
    success_rate: float = 0.0
    failure_rate: float = 0.0
    actor_statistics: dict[str, ActorDecisionStats] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        """Return a JSON-serialisable view of the statistics."""
        return {
            "total_decisions": self.total_decisions,
            "decisions_by_type": dict(self.decisions_by_type),
            "outcome_counts": dict(self.outcome_counts),
            "success_rate": self.success_rate,
            "failure_rate": self.failure_rate,
            "actor_statistics": {
                actor: stats.as_dict()
                for actor, stats in self.actor_statistics.items()
            },
        }


def compute_decision_statistics(
    store: DecisionStore, query: DecisionQuery | None = None
) -> DecisionStatistics:
    """Compute :class:`DecisionStatistics` for the records matching ``query``."""
    records = store.query(query if query is not None else DecisionQuery())
    if not records:
        return DecisionStatistics()

    by_type: Counter[str] = Counter(record.decision_type for record in records)
    outcomes: Counter[str] = Counter(record.outcome for record in records)

    successful = outcomes.get(DecisionOutcome.SUCCESSFUL.value, 0)
    failed = outcomes.get(DecisionOutcome.FAILED.value, 0)
    resolved = successful + failed
    success_rate = successful / resolved if resolved else 0.0
    failure_rate = failed / resolved if resolved else 0.0

    actor_stats: dict[str, ActorDecisionStats] = {}
    for record in records:
        if record.actor is None:
            continue
        stats = actor_stats.setdefault(record.actor, ActorDecisionStats())
        stats.total += 1
        if record.outcome == DecisionOutcome.SUCCESSFUL.value:
            stats.successful += 1
        elif record.outcome == DecisionOutcome.FAILED.value:
            stats.failed += 1

    return DecisionStatistics(
        total_decisions=len(records),
        decisions_by_type=dict(by_type),
        outcome_counts=dict(outcomes),
        success_rate=success_rate,
        failure_rate=failure_rate,
        actor_statistics=actor_stats,
    )
