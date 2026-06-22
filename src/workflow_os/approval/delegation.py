"""Approval delegation.

An approver can delegate their authority to another person, either permanently
or temporarily (with an expiry). Every delegation is recorded in the request's
delegation history so it can be audited later.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime

from workflow_os.approval.record import ApprovalRequest, utcnow
from workflow_os.approval.single import ApprovalError

_HISTORY_KEY = "delegation_history"


@dataclass
class DelegationEvent:
    """A record of one approver delegating to another."""

    approval_id: str
    from_approver: str
    to_approver: str
    reason: str
    timestamp: datetime
    expires_at: datetime | None = None

    @property
    def temporary(self) -> bool:
        return self.expires_at is not None

    def is_active(self, now: datetime | None = None) -> bool:
        """Return ``True`` if this delegation is still in effect."""
        if self.expires_at is None:
            return True
        return (now or utcnow()) < self.expires_at

    def to_dict(self) -> dict[str, str | None]:
        return {
            "approval_id": self.approval_id,
            "from_approver": self.from_approver,
            "to_approver": self.to_approver,
            "reason": self.reason,
            "timestamp": self.timestamp.isoformat(),
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
        }

    @classmethod
    def from_dict(cls, data: dict[str, str | None]) -> DelegationEvent:
        expires = data.get("expires_at")
        return cls(
            approval_id=str(data["approval_id"]),
            from_approver=str(data["from_approver"]),
            to_approver=str(data["to_approver"]),
            reason=str(data.get("reason") or ""),
            timestamp=datetime.fromisoformat(str(data["timestamp"])),
            expires_at=datetime.fromisoformat(expires) if expires else None,
        )


def delegation_history(request: ApprovalRequest) -> list[DelegationEvent]:
    """Return the delegation events recorded on ``request``, in order."""
    raw: Iterable[dict[str, str | None]] = request.metadata.get(_HISTORY_KEY, [])
    return [DelegationEvent.from_dict(item) for item in raw]


def delegate(
    request: ApprovalRequest,
    from_approver: str,
    to_approver: str,
    reason: str = "",
    expires_at: datetime | None = None,
    now: datetime | None = None,
) -> DelegationEvent:
    """Delegate ``from_approver``'s authority to ``to_approver``.

    The delegate is added as an approver. A permanent delegation (no
    ``expires_at``) removes the original approver; a temporary delegation keeps
    both so authority reverts when it lapses.
    """
    if from_approver not in request.approvers:
        raise ApprovalError(
            f"{from_approver!r} is not an approver of request {request.approval_id}"
        )
    event = DelegationEvent(
        approval_id=request.approval_id,
        from_approver=from_approver,
        to_approver=to_approver,
        reason=reason,
        timestamp=now or utcnow(),
        expires_at=expires_at,
    )
    history = request.metadata.setdefault(_HISTORY_KEY, [])
    history.append(event.to_dict())
    if to_approver not in request.approvers:
        request.approvers.append(to_approver)
    if not event.temporary:
        request.approvers.remove(from_approver)
    request.updated_at = event.timestamp
    return event


def active_delegations(
    request: ApprovalRequest, now: datetime | None = None
) -> list[DelegationEvent]:
    """Return delegations that are currently in effect."""
    now = now or utcnow()
    return [event for event in delegation_history(request) if event.is_active(now)]
