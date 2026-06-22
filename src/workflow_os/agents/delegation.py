"""Task delegation.

Tracks which agent owns which task. Tasks can be assigned to an agent,
transferred to another agent, and revoked. Every change is recorded in a
deterministic delegation history.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


def new_task_id() -> str:
    """Return a fresh, unique task id."""
    return uuid.uuid4().hex


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class DelegationAction(str, Enum):
    """The kinds of delegation events."""

    ASSIGN = "assign"
    TRANSFER = "transfer"
    REVOKE = "revoke"

    def __str__(self) -> str:  # pragma: no cover - convenience only
        return self.value


class DelegationError(ValueError):
    """Raised when a delegation action is invalid."""


class TaskNotFoundError(KeyError):
    """Raised when a task id is not present in the ledger."""


@dataclass
class TaskAssignment:
    """The current ownership state of a task."""

    task_id: str
    workflow_id: str
    step_id: str | None
    owner: str | None
    assigned_by: str | None = None
    active: bool = True
    created_at: datetime = field(default_factory=_utcnow)
    updated_at: datetime = field(default_factory=_utcnow)
    metadata: dict = field(default_factory=dict)


@dataclass
class DelegationEvent:
    """A single delegation action recorded in history."""

    task_id: str
    action: str
    from_agent: str | None
    to_agent: str | None
    actor: str | None
    timestamp: datetime = field(default_factory=_utcnow)


class TaskDelegation:
    """A deterministic ledger of task assignments and their history."""

    def __init__(self) -> None:
        self._assignments: dict[str, TaskAssignment] = {}
        self._history: list[DelegationEvent] = []

    def assign(
        self,
        *,
        workflow_id: str,
        owner: str,
        step_id: str | None = None,
        assigned_by: str | None = None,
        task_id: str | None = None,
    ) -> TaskAssignment:
        """Create a new task assigned to ``owner``."""
        tid = task_id or new_task_id()
        if tid in self._assignments:
            raise DelegationError(f"task {tid!r} already assigned")
        assignment = TaskAssignment(
            task_id=tid,
            workflow_id=workflow_id,
            step_id=step_id,
            owner=owner,
            assigned_by=assigned_by,
        )
        self._assignments[tid] = assignment
        self._history.append(
            DelegationEvent(
                task_id=tid,
                action=DelegationAction.ASSIGN.value,
                from_agent=None,
                to_agent=owner,
                actor=assigned_by,
            )
        )
        return assignment

    def transfer(
        self, task_id: str, to_agent: str, *, actor: str | None = None
    ) -> TaskAssignment:
        """Transfer an active task to a different owner."""
        assignment = self._require(task_id)
        if not assignment.active:
            raise DelegationError(f"task {task_id!r} is not active")
        previous = assignment.owner
        assignment.owner = to_agent
        assignment.updated_at = _utcnow()
        self._history.append(
            DelegationEvent(
                task_id=task_id,
                action=DelegationAction.TRANSFER.value,
                from_agent=previous,
                to_agent=to_agent,
                actor=actor,
            )
        )
        return assignment

    def revoke(self, task_id: str, *, actor: str | None = None) -> TaskAssignment:
        """Revoke a task, clearing its owner and marking it inactive."""
        assignment = self._require(task_id)
        previous = assignment.owner
        assignment.owner = None
        assignment.active = False
        assignment.updated_at = _utcnow()
        self._history.append(
            DelegationEvent(
                task_id=task_id,
                action=DelegationAction.REVOKE.value,
                from_agent=previous,
                to_agent=None,
                actor=actor,
            )
        )
        return assignment

    def assignment(self, task_id: str) -> TaskAssignment:
        """Return the current assignment for a task."""
        return self._require(task_id)

    def active_assignments(self) -> list[TaskAssignment]:
        """Return all active assignments ordered by task id."""
        return [
            self._assignments[key]
            for key in sorted(self._assignments)
            if self._assignments[key].active
        ]

    def history(self, task_id: str | None = None) -> list[DelegationEvent]:
        """Return delegation history, optionally filtered to one task."""
        if task_id is None:
            return list(self._history)
        return [event for event in self._history if event.task_id == task_id]

    def _require(self, task_id: str) -> TaskAssignment:
        try:
            return self._assignments[task_id]
        except KeyError as exc:
            raise TaskNotFoundError(task_id) from exc
