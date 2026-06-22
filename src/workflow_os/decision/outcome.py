"""Decision outcome tracking.

Outcomes describe how a decision turned out. They are kept deliberately small
and are validated so stored data stays consistent. Outcomes can be set when a
decision is recorded and updated later as results become known.
"""

from __future__ import annotations

from enum import Enum

from workflow_os.decision.record import DecisionRecord
from workflow_os.decision.store import DecisionStore


class DecisionOutcome(str, Enum):
    """The possible outcomes of a decision."""

    PENDING = "pending"
    SUCCESSFUL = "successful"
    FAILED = "failed"
    UNKNOWN = "unknown"

    def __str__(self) -> str:  # pragma: no cover - convenience only
        return self.value


VALID_OUTCOMES: frozenset[str] = frozenset(outcome.value for outcome in DecisionOutcome)

RESOLVED_OUTCOMES: frozenset[str] = frozenset(
    {DecisionOutcome.SUCCESSFUL.value, DecisionOutcome.FAILED.value}
)


class InvalidOutcomeError(ValueError):
    """Raised when an unknown outcome value is used."""


def normalize_outcome(outcome: str) -> str:
    """Return the canonical string for ``outcome`` or raise if it is unknown."""
    value = str(outcome)
    if value not in VALID_OUTCOMES:
        valid = ", ".join(sorted(VALID_OUTCOMES))
        raise InvalidOutcomeError(f"unknown outcome {value!r}; valid: [{valid}]")
    return value


def set_decision_outcome(
    store: DecisionStore, decision_id: str, outcome: str
) -> DecisionRecord:
    """Update the outcome of a stored decision, validating ``outcome`` first."""
    normalized = normalize_outcome(outcome)
    record = store.get(decision_id)
    record.outcome = normalized
    store.add(record)
    return record
