"""Decision replay engine.

Replaying a set of decisions reconstructs them in order, pairing each decision
with a human-readable explanation and its offset from the first decision. This
supports after-the-fact analysis without re-executing anything: it is a
read-only reconstruction of what was decided and why.
"""

from __future__ import annotations

from dataclasses import dataclass

from workflow_os.decision.explanation import DecisionExplanation, explain_decision
from workflow_os.decision.record import DecisionRecord
from workflow_os.decision.store import DecisionQuery, DecisionStore
from workflow_os.decision.timelines import (
    DecisionTimelineEntry,
    get_decision_timeline,
)


@dataclass
class ReplayEvent:
    """A single replayed decision.

    Attributes:
        sequence: Zero-based position of the decision in the replay.
        decision: The decision record being replayed.
        explanation: A human-readable explanation of the decision.
        offset_seconds: Seconds elapsed since the first decision in the replay.
    """

    sequence: int
    decision: DecisionRecord
    explanation: DecisionExplanation
    offset_seconds: float


def _replay(records: list[DecisionRecord]) -> list[ReplayEvent]:
    if not records:
        return []
    start = records[0].timestamp
    return [
        ReplayEvent(
            sequence=index,
            decision=record,
            explanation=explain_decision(record),
            offset_seconds=(record.timestamp - start).total_seconds(),
        )
        for index, record in enumerate(records)
    ]


class DecisionReplay:
    """Reconstruct and replay decisions held in a decision store."""

    def __init__(self, store: DecisionStore) -> None:
        self.store = store

    def replay_workflow(self, workflow_id: str) -> list[ReplayEvent]:
        """Replay every decision recorded for a workflow, in order."""
        return _replay(self.store.query(DecisionQuery(workflow_id=workflow_id)))

    def replay_actor(self, actor: str) -> list[ReplayEvent]:
        """Replay every decision made by an actor, in order."""
        return _replay(self.store.query(DecisionQuery(actor=actor)))

    def reconstruct_timeline(
        self, query: DecisionQuery | None = None
    ) -> list[DecisionTimelineEntry]:
        """Reconstruct the decision timeline for the records matching ``query``."""
        return get_decision_timeline(self.store, query)


def replay_workflow_decisions(
    store: DecisionStore, workflow_id: str
) -> list[ReplayEvent]:
    """Replay the decisions recorded for a workflow."""
    return DecisionReplay(store).replay_workflow(workflow_id)


def replay_actor_decisions(store: DecisionStore, actor: str) -> list[ReplayEvent]:
    """Replay the decisions made by an actor."""
    return DecisionReplay(store).replay_actor(actor)


def reconstruct_decision_timeline(
    store: DecisionStore, query: DecisionQuery | None = None
) -> list[DecisionTimelineEntry]:
    """Reconstruct a decision timeline from a store."""
    return DecisionReplay(store).reconstruct_timeline(query)
