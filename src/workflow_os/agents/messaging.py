"""Agent messaging.

A deterministic message bus that lets agents send messages to one another. Every
message is retained so the full message history can be queried and audited.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def new_message_id() -> str:
    """Return a fresh, unique message id."""
    return uuid.uuid4().hex


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class Message:
    """A message exchanged between two agents."""

    message_id: str
    sender: str
    recipient: str
    body: str
    subject: str = ""
    timestamp: datetime = field(default_factory=_utcnow)
    metadata: dict[str, Any] = field(default_factory=dict)


class MessageBus:
    """A deterministic in-memory bus that retains all messages."""

    def __init__(self) -> None:
        self._messages: list[Message] = []

    def send(
        self,
        sender: str,
        recipient: str,
        body: str,
        *,
        subject: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> Message:
        """Send a message and return it."""
        message = Message(
            message_id=new_message_id(),
            sender=sender,
            recipient=recipient,
            body=body,
            subject=subject,
            metadata=dict(metadata or {}),
        )
        self._messages.append(message)
        return message

    def receive(self, agent_id: str) -> list[Message]:
        """Return all messages addressed to ``agent_id`` in send order."""
        return [m for m in self._messages if m.recipient == agent_id]

    def history(
        self, *, sender: str | None = None, recipient: str | None = None
    ) -> list[Message]:
        """Return messages, optionally filtered by sender and/or recipient."""
        result = self._messages
        if sender is not None:
            result = [m for m in result if m.sender == sender]
        if recipient is not None:
            result = [m for m in result if m.recipient == recipient]
        return list(result)

    def all(self) -> list[Message]:
        """Return every message in send order."""
        return list(self._messages)
