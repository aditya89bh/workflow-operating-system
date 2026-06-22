"""The :class:`RecoveryAction` schema.

A recovery action records an attempt to recover from an exception: what action
was taken, by whom, its status, and when. Recovery actions are deterministic data
objects produced by the recommendation engine and recovery strategies.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

from workflow_os.exception.record import utcnow


def new_recovery_id() -> str:
    """Return a fresh, unique recovery id."""
    return uuid.uuid4().hex


class RecoveryStatus(str, Enum):
    """The lifecycle status of a recovery action."""

    PENDING = "pending"
    SUCCEEDED = "succeeded"
    FAILED = "failed"

    def __str__(self) -> str:  # pragma: no cover - convenience only
        return self.value


@dataclass
class RecoveryAction:
    """A recorded recovery attempt for an exception.

    Attributes:
        recovery_id: Unique identifier for the recovery action.
        exception_id: Id of the exception this action addresses.
        action: The recovery action taken (for example ``retry``).
        actor: Who (or what component) performed the action.
        status: One of the :class:`RecoveryStatus` values.
        timestamp: When the action was recorded (timezone-aware UTC).
        metadata: Arbitrary key/value data attached to the action.
    """

    recovery_id: str
    exception_id: str
    action: str
    actor: str | None = None
    status: str = RecoveryStatus.PENDING.value
    timestamp: datetime = field(default_factory=utcnow)
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        *,
        exception_id: str,
        action: str,
        actor: str | None = None,
        status: str = RecoveryStatus.PENDING.value,
        timestamp: datetime | None = None,
        metadata: dict[str, Any] | None = None,
        recovery_id: str | None = None,
    ) -> RecoveryAction:
        """Build a :class:`RecoveryAction`, filling in id and timestamp."""
        return cls(
            recovery_id=recovery_id or new_recovery_id(),
            exception_id=exception_id,
            action=action,
            actor=actor,
            status=str(status),
            timestamp=timestamp or utcnow(),
            metadata=dict(metadata or {}),
        )
