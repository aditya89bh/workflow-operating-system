"""Decision type definitions.

These are the canonical kinds of decisions the system records. They are plain
strings so they serialise cleanly and compare directly with the
``decision_type`` field on :class:`~workflow_os.decision.record.DecisionRecord`.
"""

from __future__ import annotations

from enum import Enum


class DecisionType(str, Enum):
    """The kinds of decisions the decision intelligence layer records."""

    WORKFLOW_DECISION = "workflow_decision"
    STEP_DECISION = "step_decision"
    EXCEPTION_DECISION = "exception_decision"
    MANUAL_DECISION = "manual_decision"
    SYSTEM_DECISION = "system_decision"

    def __str__(self) -> str:  # pragma: no cover - convenience only
        return self.value


ALL_DECISION_TYPES: frozenset[DecisionType] = frozenset(DecisionType)
