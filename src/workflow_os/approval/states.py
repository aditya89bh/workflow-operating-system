"""Approval state definitions.

Defines the lifecycle states an approval request (and an individual approver
decision) can be in, plus small helpers for classifying states and recording
state changes on a request.
"""

from __future__ import annotations

from enum import Enum

from workflow_os.approval.record import ApprovalRequest, utcnow


class ApprovalState(str, Enum):
    """The states an approval request or decision can be in."""

    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"
    EXPIRED = "expired"

    def __str__(self) -> str:  # pragma: no cover - convenience only
        return self.value


TERMINAL_STATES: frozenset[str] = frozenset(
    {
        ApprovalState.APPROVED.value,
        ApprovalState.REJECTED.value,
        ApprovalState.CANCELLED.value,
        ApprovalState.EXPIRED.value,
    }
)

ACTIVE_STATES: frozenset[str] = frozenset({ApprovalState.PENDING.value})


def is_terminal(state: str) -> bool:
    """Return ``True`` if ``state`` is a final state."""
    return str(state) in TERMINAL_STATES


def is_active(state: str) -> bool:
    """Return ``True`` if ``state`` is still open."""
    return str(state) in ACTIVE_STATES


def set_state(request: ApprovalRequest, state: str) -> ApprovalRequest:
    """Set the overall state of a request and bump its ``updated_at``."""
    request.state = str(state)
    request.updated_at = utcnow()
    return request


def record_response(
    request: ApprovalRequest, approver: str, decision: str
) -> ApprovalRequest:
    """Record an individual approver's decision and bump ``updated_at``."""
    request.decisions[approver] = str(decision)
    request.updated_at = utcnow()
    return request
