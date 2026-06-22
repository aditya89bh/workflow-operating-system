"""Ordered decision timelines.

A timeline presents recorded decisions in chronological order, each annotated
with its offset from the first decision in the series. Timelines can be built
for a workflow, for an actor, or for an arbitrary query.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from workflow_os.decision.record import DecisionRecord
from workflow_os.decision.store import DecisionQuery, DecisionStore


@dataclass
class DecisionTimelineEntry:
    """A single point on a decision timeline.

    Attributes:
        timestamp: When the decision was made.
        decision_id: Id of the decision.
        decision_type: The kind of decision.
        decision: A short statement of what was decided.
        step_id: The related step id, if any.
        actor: The actor attributed to the decision, if any.
        outcome: The decision outcome at the time the timeline was built.
        offset_seconds: Seconds elapsed since the first decision in the timeline.
    """

    timestamp: datetime
    decision_id: str
    decision_type: str
    decision: str
    step_id: str | None
    actor: str | None
    outcome: str
    offset_seconds: float


def build_timeline(records: list[DecisionRecord]) -> list[DecisionTimelineEntry]:
    """Build a timeline from already-ordered decision records."""
    if not records:
        return []
    start = records[0].timestamp
    return [
        DecisionTimelineEntry(
            timestamp=record.timestamp,
            decision_id=record.decision_id,
            decision_type=record.decision_type,
            decision=record.decision,
            step_id=record.step_id,
            actor=record.actor,
            outcome=record.outcome,
            offset_seconds=(record.timestamp - start).total_seconds(),
        )
        for record in records
    ]


def get_workflow_decision_timeline(
    store: DecisionStore, workflow_id: str
) -> list[DecisionTimelineEntry]:
    """Return the ordered decision timeline for a workflow."""
    return build_timeline(store.query(DecisionQuery(workflow_id=workflow_id)))


def get_actor_decision_timeline(
    store: DecisionStore, actor: str
) -> list[DecisionTimelineEntry]:
    """Return the ordered decision timeline for a single actor."""
    return build_timeline(store.query(DecisionQuery(actor=actor)))


def get_decision_timeline(
    store: DecisionStore, query: DecisionQuery | None = None
) -> list[DecisionTimelineEntry]:
    """Return an ordered decision timeline for the records matching ``query``."""
    return build_timeline(store.query(query if query is not None else DecisionQuery()))
