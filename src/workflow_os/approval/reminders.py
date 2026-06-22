"""Approval reminder support.

Generates reminders for approvers who still need to act. Pending reminders nudge
approvers who have not yet responded; overdue reminders flag requests that have
passed their timeout window. Each reminder carries the timestamp it was raised.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from workflow_os.approval.record import ApprovalRequest, utcnow
from workflow_os.approval.states import is_active
from workflow_os.approval.timeout import is_overdue


class ReminderKind(str, Enum):
    """The kinds of reminder that can be generated."""

    PENDING = "pending"
    OVERDUE = "overdue"

    def __str__(self) -> str:  # pragma: no cover - convenience only
        return self.value


@dataclass
class Reminder:
    """A reminder for one approver to act on one request."""

    approval_id: str
    approver: str
    kind: str
    timestamp: datetime


def _outstanding_approvers(request: ApprovalRequest) -> list[str]:
    return [a for a in request.approvers if a not in request.decisions]


def pending_reminders(
    requests: Iterable[ApprovalRequest], now: datetime | None = None
) -> list[Reminder]:
    """Return pending reminders for approvers who have not yet responded."""
    now = now or utcnow()
    reminders: list[Reminder] = []
    for request in requests:
        if not is_active(request.state):
            continue
        for approver in _outstanding_approvers(request):
            reminders.append(
                Reminder(request.approval_id, approver, ReminderKind.PENDING.value, now)
            )
    return reminders


def overdue_reminders(
    requests: Iterable[ApprovalRequest],
    timeout_seconds: float,
    now: datetime | None = None,
) -> list[Reminder]:
    """Return overdue reminders for requests past their timeout window."""
    now = now or utcnow()
    reminders: list[Reminder] = []
    for request in requests:
        if not is_overdue(request, timeout_seconds, now):
            continue
        for approver in _outstanding_approvers(request):
            reminders.append(
                Reminder(request.approval_id, approver, ReminderKind.OVERDUE.value, now)
            )
    return reminders


def generate_reminders(
    requests: Iterable[ApprovalRequest],
    timeout_seconds: float | None = None,
    now: datetime | None = None,
) -> list[Reminder]:
    """Return pending reminders, plus overdue reminders if a timeout is given."""
    now = now or utcnow()
    requests = list(requests)
    reminders = pending_reminders(requests, now)
    if timeout_seconds is not None:
        reminders.extend(overdue_reminders(requests, timeout_seconds, now))
    return reminders
