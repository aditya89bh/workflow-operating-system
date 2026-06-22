"""Approval audit logs.

Records an append-only trail of approval events - requests, approvals,
rejections, escalations, and delegations - so the full governance history of a
workflow can be reconstructed and audited later.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

from workflow_os.approval.record import ApprovalRequest, utcnow


class ApprovalEventType(str, Enum):
    """The kinds of event recorded in an approval audit log."""

    REQUESTED = "requested"
    APPROVED = "approved"
    REJECTED = "rejected"
    ESCALATED = "escalated"
    DELEGATED = "delegated"
    EXPIRED = "expired"
    CANCELLED = "cancelled"
    REMINDED = "reminded"

    def __str__(self) -> str:  # pragma: no cover - convenience only
        return self.value


@dataclass
class ApprovalAuditEvent:
    """A single entry in an approval audit log."""

    event_id: str
    approval_id: str
    event_type: str
    timestamp: datetime
    actor: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class ApprovalAuditLog:
    """An append-only collection of approval audit events."""

    def __init__(self) -> None:
        self._events: list[ApprovalAuditEvent] = []

    def record(
        self,
        approval_id: str,
        event_type: str,
        actor: str | None = None,
        timestamp: datetime | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> ApprovalAuditEvent:
        """Append an event and return it."""
        event = ApprovalAuditEvent(
            event_id=uuid.uuid4().hex,
            approval_id=approval_id,
            event_type=str(event_type),
            timestamp=timestamp or utcnow(),
            actor=actor,
            metadata=dict(metadata or {}),
        )
        self._events.append(event)
        return event

    def record_request(
        self, request: ApprovalRequest, timestamp: datetime | None = None
    ) -> ApprovalAuditEvent:
        return self.record(
            request.approval_id,
            ApprovalEventType.REQUESTED.value,
            actor=request.requester,
            timestamp=timestamp or request.created_at,
            metadata={"workflow_id": request.workflow_id},
        )

    def record_approval(
        self, approval_id: str, actor: str, timestamp: datetime | None = None
    ) -> ApprovalAuditEvent:
        return self.record(
            approval_id, ApprovalEventType.APPROVED.value, actor, timestamp
        )

    def record_rejection(
        self, approval_id: str, actor: str, timestamp: datetime | None = None
    ) -> ApprovalAuditEvent:
        return self.record(
            approval_id, ApprovalEventType.REJECTED.value, actor, timestamp
        )

    def record_escalation(
        self, approval_id: str, target: str, timestamp: datetime | None = None
    ) -> ApprovalAuditEvent:
        return self.record(
            approval_id, ApprovalEventType.ESCALATED.value, target, timestamp
        )

    def record_delegation(
        self,
        approval_id: str,
        from_approver: str,
        to_approver: str,
        timestamp: datetime | None = None,
    ) -> ApprovalAuditEvent:
        return self.record(
            approval_id,
            ApprovalEventType.DELEGATED.value,
            actor=from_approver,
            timestamp=timestamp,
            metadata={"to_approver": to_approver},
        )

    def all(self) -> list[ApprovalAuditEvent]:
        """Return every event in insertion order."""
        return list(self._events)

    def for_approval(self, approval_id: str) -> list[ApprovalAuditEvent]:
        """Return events belonging to a single approval request."""
        return [e for e in self._events if e.approval_id == approval_id]

    def for_actor(self, actor: str) -> list[ApprovalAuditEvent]:
        """Return events recorded for a particular actor."""
        return [e for e in self._events if e.actor == actor]

    def by_type(self, event_type: str) -> list[ApprovalAuditEvent]:
        """Return events of a particular type."""
        return [e for e in self._events if e.event_type == str(event_type)]
