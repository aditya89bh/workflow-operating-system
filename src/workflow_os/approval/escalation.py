"""Approval escalation support.

When a request stalls, it can be escalated to another approver (the escalation
target). Escalation rules describe when to escalate and to whom, and every
escalation is recorded in the request's escalation history for later auditing.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime

from workflow_os.approval.record import ApprovalRequest, utcnow
from workflow_os.approval.timeout import is_overdue

_HISTORY_KEY = "escalation_history"


@dataclass
class EscalationRule:
    """A rule describing when and to whom a request should escalate."""

    target: str
    after_seconds: float

    def __str__(self) -> str:  # pragma: no cover - convenience only
        return f"escalate to {self.target} after {self.after_seconds}s"


@dataclass
class EscalationEvent:
    """A record of a single escalation action."""

    approval_id: str
    target: str
    reason: str
    timestamp: datetime

    def to_dict(self) -> dict[str, str]:
        return {
            "approval_id": self.approval_id,
            "target": self.target,
            "reason": self.reason,
            "timestamp": self.timestamp.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> EscalationEvent:
        return cls(
            approval_id=data["approval_id"],
            target=data["target"],
            reason=data.get("reason", ""),
            timestamp=datetime.fromisoformat(data["timestamp"]),
        )


def escalation_history(request: ApprovalRequest) -> list[EscalationEvent]:
    """Return the escalation events recorded on ``request``, in order."""
    raw: Iterable[dict[str, str]] = request.metadata.get(_HISTORY_KEY, [])
    return [EscalationEvent.from_dict(item) for item in raw]


def escalate(
    request: ApprovalRequest,
    target: str,
    reason: str = "",
    now: datetime | None = None,
) -> EscalationEvent:
    """Escalate ``request`` to ``target`` and record the event.

    The target becomes an additional approver if not already present.
    """
    event = EscalationEvent(
        approval_id=request.approval_id,
        target=target,
        reason=reason,
        timestamp=now or utcnow(),
    )
    history = request.metadata.setdefault(_HISTORY_KEY, [])
    history.append(event.to_dict())
    if target not in request.approvers:
        request.approvers.append(target)
    request.updated_at = event.timestamp
    return event


def should_escalate(
    request: ApprovalRequest, rule: EscalationRule, now: datetime | None = None
) -> bool:
    """Return ``True`` if ``request`` is overdue under ``rule``."""
    return is_overdue(request, rule.after_seconds, now)


def escalate_if_overdue(
    request: ApprovalRequest, rule: EscalationRule, now: datetime | None = None
) -> EscalationEvent | None:
    """Escalate ``request`` to the rule's target if it is overdue."""
    if not should_escalate(request, rule, now):
        return None
    return escalate(request, rule.target, reason="timeout", now=now)
