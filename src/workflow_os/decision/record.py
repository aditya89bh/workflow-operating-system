"""The :class:`DecisionRecord` schema.

A decision record captures a single decision taken during a workflow's life:
what was decided, why, which alternatives were considered, who decided, and how
it turned out. Records are the atomic unit of the decision intelligence layer.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def new_decision_id() -> str:
    """Return a fresh, unique decision id."""
    return uuid.uuid4().hex


def utcnow() -> datetime:
    """Return the current time as a timezone-aware UTC datetime."""
    return datetime.now(timezone.utc)


@dataclass
class DecisionRecord:
    """A structured record of a single decision.

    Attributes:
        decision_id: Unique identifier for the decision.
        workflow_id: Id of the workflow the decision belongs to.
        decision_type: The kind of decision (see ``DecisionType`` values).
        decision: A short statement of what was decided.
        timestamp: When the decision was made (timezone-aware UTC).
        step_id: Optional id of the step the decision relates to.
        actor: Optional actor who made or owns the decision.
        rationale: Why the decision was made.
        alternatives: Other options that were considered.
        outcome: How the decision turned out (defaults to ``"pending"``).
        confidence: How much trust to place in the record, in ``[0.0, 1.0]``.
        metadata: Arbitrary key/value data attached to the decision.
    """

    decision_id: str
    workflow_id: str
    decision_type: str
    decision: str
    timestamp: datetime
    step_id: str | None = None
    actor: str | None = None
    rationale: str = ""
    alternatives: list[str] = field(default_factory=list)
    outcome: str = "pending"
    confidence: float = 1.0
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        *,
        workflow_id: str,
        decision_type: str,
        decision: str,
        rationale: str = "",
        alternatives: list[str] | None = None,
        step_id: str | None = None,
        actor: str | None = None,
        outcome: str = "pending",
        confidence: float = 1.0,
        metadata: dict[str, Any] | None = None,
        timestamp: datetime | None = None,
        decision_id: str | None = None,
    ) -> DecisionRecord:
        """Build a :class:`DecisionRecord`, filling in id and timestamp by default."""
        return cls(
            decision_id=decision_id or new_decision_id(),
            workflow_id=workflow_id,
            decision_type=str(decision_type),
            decision=decision,
            timestamp=timestamp or utcnow(),
            step_id=step_id,
            actor=actor,
            rationale=rationale,
            alternatives=list(alternatives or []),
            outcome=str(outcome),
            confidence=confidence,
            metadata=dict(metadata or {}),
        )
