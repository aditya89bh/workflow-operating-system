"""Decision recording APIs.

:class:`DecisionRecorder` wraps a :class:`~workflow_os.decision.store.DecisionStore`
and provides convenient methods for capturing decisions and updating their
outcomes after the fact.
"""

from __future__ import annotations

from typing import Any

from workflow_os.decision.record import DecisionRecord
from workflow_os.decision.store import DecisionStore
from workflow_os.decision.types import DecisionType


class DecisionRecorder:
    """Capture decisions into a decision store."""

    def __init__(self, store: DecisionStore) -> None:
        self.store = store

    def record_decision(
        self,
        *,
        workflow_id: str,
        decision: str,
        decision_type: str = DecisionType.MANUAL_DECISION.value,
        rationale: str = "",
        alternatives: list[str] | None = None,
        step_id: str | None = None,
        actor: str | None = None,
        outcome: str = "pending",
        confidence: float = 1.0,
        metadata: dict[str, Any] | None = None,
    ) -> DecisionRecord:
        """Capture a decision and persist it, returning the stored record."""
        record = DecisionRecord.create(
            workflow_id=workflow_id,
            decision_type=str(decision_type),
            decision=decision,
            rationale=rationale,
            alternatives=alternatives,
            step_id=step_id,
            actor=actor,
            outcome=outcome,
            confidence=confidence,
            metadata=metadata,
        )
        self.store.add(record)
        return record

    def update_decision_outcome(
        self,
        decision_id: str,
        outcome: str,
        *,
        metadata: dict[str, Any] | None = None,
    ) -> DecisionRecord:
        """Update the outcome (and optionally metadata) of a stored decision."""
        record = self.store.get(decision_id)
        record.outcome = str(outcome)
        if metadata:
            record.metadata.update(metadata)
        self.store.add(record)
        return record
