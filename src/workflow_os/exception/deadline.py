"""Deadline failure detection.

Detects workflows (or steps) that have passed their deadline without completing.
Each missed deadline produces a ``timeout`` exception record. Detection is
deterministic: a deadline is either in the past relative to ``now`` or it is not.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime

from workflow_os.exception.classification import ExceptionType
from workflow_os.exception.record import ExceptionRecord, utcnow
from workflow_os.exception.severity import ExceptionSeverity

_SOURCE = "deadline-detector"


@dataclass
class Deadline:
    """A deadline that a workflow or step must meet."""

    workflow_id: str
    deadline: datetime
    step_id: str | None = None


def detect_deadline_failure(
    deadline: Deadline, now: datetime | None = None
) -> ExceptionRecord | None:
    """Return a ``timeout`` exception if ``deadline`` has passed, else ``None``."""
    now = now or utcnow()
    if now <= deadline.deadline:
        return None
    overshoot = (now - deadline.deadline).total_seconds()
    return ExceptionRecord.create(
        workflow_id=deadline.workflow_id,
        step_id=deadline.step_id,
        exception_type=ExceptionType.TIMEOUT.value,
        severity=ExceptionSeverity.HIGH.value,
        message=f"deadline missed by {overshoot:.0f}s",
        source=_SOURCE,
        detected_at=now,
        metadata={"deadline": deadline.deadline.isoformat()},
    )


def detect_deadline_failures(
    deadlines: Iterable[Deadline], now: datetime | None = None
) -> list[ExceptionRecord]:
    """Return ``timeout`` exceptions for every passed deadline."""
    now = now or utcnow()
    records = [detect_deadline_failure(d, now) for d in deadlines]
    return [record for record in records if record is not None]
