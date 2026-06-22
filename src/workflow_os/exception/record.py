"""The :class:`ExceptionRecord` schema.

An exception record captures a workflow failure: what failed, where, how severe
it was, and when it was detected. Records are deterministic data objects; they
carry no behaviour beyond construction helpers.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def new_exception_id() -> str:
    """Return a fresh, unique exception id."""
    return uuid.uuid4().hex


def utcnow() -> datetime:
    """Return the current time as a timezone-aware UTC datetime."""
    return datetime.now(timezone.utc)


@dataclass
class ExceptionRecord:
    """A structured record of a detected workflow exception.

    Attributes:
        exception_id: Unique identifier for the exception.
        workflow_id: Id of the workflow the exception belongs to.
        exception_type: Classification of the failure (see ``ExceptionType``).
        severity: How serious the failure is (see ``ExceptionSeverity``).
        message: Human-readable description of the failure.
        step_id: Optional id of the step that failed.
        source: Optional component that detected the exception.
        detected_at: When the exception was detected (timezone-aware UTC).
        resolved: Whether the exception has been resolved.
        metadata: Arbitrary key/value data attached to the exception.
    """

    exception_id: str
    workflow_id: str
    exception_type: str = "unknown"
    severity: str = "medium"
    message: str = ""
    step_id: str | None = None
    source: str | None = None
    detected_at: datetime = field(default_factory=utcnow)
    resolved: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        *,
        workflow_id: str,
        exception_type: str = "unknown",
        severity: str = "medium",
        message: str = "",
        step_id: str | None = None,
        source: str | None = None,
        detected_at: datetime | None = None,
        resolved: bool = False,
        metadata: dict[str, Any] | None = None,
        exception_id: str | None = None,
    ) -> ExceptionRecord:
        """Build an :class:`ExceptionRecord`, filling in id and timestamp."""
        return cls(
            exception_id=exception_id or new_exception_id(),
            workflow_id=workflow_id,
            exception_type=str(exception_type),
            severity=str(severity),
            message=message,
            step_id=step_id,
            source=source,
            detected_at=detected_at or utcnow(),
            resolved=resolved,
            metadata=dict(metadata or {}),
        )
