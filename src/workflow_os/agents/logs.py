"""Collaboration logs.

A single, deterministic log that records collaboration events: task assignments,
messages, task transfers, and workflow participation. The log is the raw material
for accountability tracking, efficiency metrics, and performance reports.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from workflow_os.agents.messaging import Message


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class CollaborationEventType(str, Enum):
    """The kinds of events tracked in the collaboration log."""

    ASSIGNMENT = "assignment"
    MESSAGE = "message"
    TASK_TRANSFER = "task_transfer"
    PARTICIPATION = "participation"

    def __str__(self) -> str:  # pragma: no cover - convenience only
        return self.value


@dataclass
class CollaborationEntry:
    """A single recorded collaboration event."""

    event_type: str
    workflow_id: str | None
    agent_id: str | None
    detail: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=_utcnow)


class CollaborationLog:
    """A deterministic, append-only log of collaboration events."""

    def __init__(self) -> None:
        self._entries: list[CollaborationEntry] = []

    def _append(
        self,
        event_type: CollaborationEventType,
        workflow_id: str | None,
        agent_id: str | None,
        detail: dict[str, Any],
    ) -> CollaborationEntry:
        entry = CollaborationEntry(
            event_type=event_type.value,
            workflow_id=workflow_id,
            agent_id=agent_id,
            detail=detail,
        )
        self._entries.append(entry)
        return entry

    def record_assignment(
        self, workflow_id: str | None, agent_id: str, task_id: str
    ) -> CollaborationEntry:
        """Record that ``task_id`` was assigned to ``agent_id``."""
        return self._append(
            CollaborationEventType.ASSIGNMENT,
            workflow_id,
            agent_id,
            {"task_id": task_id},
        )

    def record_message(
        self, message: Message, *, workflow_id: str | None = None
    ) -> CollaborationEntry:
        """Record an exchanged message."""
        return self._append(
            CollaborationEventType.MESSAGE,
            workflow_id,
            message.sender,
            {
                "message_id": message.message_id,
                "recipient": message.recipient,
                "subject": message.subject,
            },
        )

    def record_transfer(
        self,
        workflow_id: str | None,
        task_id: str,
        from_agent: str | None,
        to_agent: str | None,
    ) -> CollaborationEntry:
        """Record a task transfer between agents."""
        return self._append(
            CollaborationEventType.TASK_TRANSFER,
            workflow_id,
            to_agent,
            {"task_id": task_id, "from_agent": from_agent, "to_agent": to_agent},
        )

    def record_participation(
        self, workflow_id: str, agent_id: str
    ) -> CollaborationEntry:
        """Record that ``agent_id`` participated in ``workflow_id``."""
        return self._append(
            CollaborationEventType.PARTICIPATION,
            workflow_id,
            agent_id,
            {},
        )

    def entries(
        self,
        *,
        workflow_id: str | None = None,
        agent_id: str | None = None,
        event_type: str | None = None,
    ) -> list[CollaborationEntry]:
        """Return log entries filtered by workflow, agent, and/or event type."""
        result = self._entries
        if workflow_id is not None:
            result = [e for e in result if e.workflow_id == workflow_id]
        if agent_id is not None:
            result = [e for e in result if e.agent_id == agent_id]
        if event_type is not None:
            result = [e for e in result if e.event_type == str(event_type)]
        return list(result)

    def participants(self, workflow_id: str) -> list[str]:
        """Return the distinct agents involved in a workflow, ordered."""
        seen = {
            entry.agent_id
            for entry in self._entries
            if entry.workflow_id == workflow_id and entry.agent_id is not None
        }
        return sorted(seen)
