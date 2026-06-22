"""Approval timeout support.

Provides deadline calculation, overdue detection, and expiration of approval
requests that have not been resolved within a timeout window. Only open
(pending) requests can become overdue or expire.
"""

from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime, timedelta

from workflow_os.approval.record import ApprovalRequest, utcnow
from workflow_os.approval.states import ApprovalState, is_active, set_state
from workflow_os.approval.store import ApprovalStore


def deadline(request: ApprovalRequest, timeout_seconds: float) -> datetime:
    """Return the time by which ``request`` must be resolved."""
    return request.created_at + timedelta(seconds=timeout_seconds)


def is_overdue(
    request: ApprovalRequest,
    timeout_seconds: float,
    now: datetime | None = None,
) -> bool:
    """Return ``True`` if an open ``request`` is past its deadline."""
    if not is_active(request.state):
        return False
    now = now or utcnow()
    return now > deadline(request, timeout_seconds)


def expire(request: ApprovalRequest) -> ApprovalRequest:
    """Mark an open request as expired (no-op if already terminal)."""
    if is_active(request.state):
        set_state(request, ApprovalState.EXPIRED.value)
    return request


def expire_if_overdue(
    request: ApprovalRequest,
    timeout_seconds: float,
    now: datetime | None = None,
) -> bool:
    """Expire ``request`` if overdue; return whether it was expired."""
    if is_overdue(request, timeout_seconds, now):
        expire(request)
        return True
    return False


def find_overdue(
    requests: Iterable[ApprovalRequest],
    timeout_seconds: float,
    now: datetime | None = None,
) -> list[ApprovalRequest]:
    """Return the open requests that are past their deadline."""
    now = now or utcnow()
    return [r for r in requests if is_overdue(r, timeout_seconds, now)]


def expire_overdue(
    store: ApprovalStore,
    timeout_seconds: float,
    now: datetime | None = None,
) -> list[ApprovalRequest]:
    """Expire all overdue requests in ``store`` and persist the changes."""
    now = now or utcnow()
    expired = find_overdue(store.list(), timeout_seconds, now)
    for request in expired:
        expire(request)
        store.update(request)
    return expired
