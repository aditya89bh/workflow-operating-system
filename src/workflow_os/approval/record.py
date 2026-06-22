"""The :class:`ApprovalRequest` schema.

An approval request captures a governance ask: a requester wants a workflow (or
a specific step) approved by one or more approvers. The request carries the
people involved, a title and description, timestamps, the current state, and the
individual approver decisions recorded so far.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def new_approval_id() -> str:
    """Return a fresh, unique approval id."""
    return uuid.uuid4().hex


def utcnow() -> datetime:
    """Return the current time as a timezone-aware UTC datetime."""
    return datetime.now(timezone.utc)


@dataclass
class ApprovalRequest:
    """A structured approval request.

    Attributes:
        approval_id: Unique identifier for the request.
        workflow_id: Id of the workflow the request belongs to.
        requester: Who raised the request.
        title: Short human-readable title.
        approvers: The approvers asked to act on the request.
        step_id: Optional id of the step the request relates to.
        description: Longer description of what is being approved.
        state: Overall request state (see ``ApprovalState`` values).
        created_at: When the request was raised (timezone-aware UTC).
        updated_at: When the request last changed (timezone-aware UTC).
        decisions: Per-approver decisions, mapping approver to their state.
        metadata: Arbitrary key/value data attached to the request.
    """

    approval_id: str
    workflow_id: str
    requester: str
    title: str
    approvers: list[str] = field(default_factory=list)
    step_id: str | None = None
    description: str = ""
    state: str = "pending"
    created_at: datetime = field(default_factory=utcnow)
    updated_at: datetime = field(default_factory=utcnow)
    decisions: dict[str, str] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        *,
        workflow_id: str,
        requester: str,
        title: str,
        approvers: list[str] | None = None,
        step_id: str | None = None,
        description: str = "",
        state: str = "pending",
        metadata: dict[str, Any] | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
        decisions: dict[str, str] | None = None,
        approval_id: str | None = None,
    ) -> ApprovalRequest:
        """Build an :class:`ApprovalRequest`, filling in id and timestamps."""
        now = created_at or utcnow()
        return cls(
            approval_id=approval_id or new_approval_id(),
            workflow_id=workflow_id,
            requester=requester,
            title=title,
            approvers=list(approvers or []),
            step_id=step_id,
            description=description,
            state=str(state),
            created_at=now,
            updated_at=updated_at or now,
            decisions=dict(decisions or {}),
            metadata=dict(metadata or {}),
        )
