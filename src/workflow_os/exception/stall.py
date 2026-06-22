"""Workflow stall detection.

Detects workflows that have not made progress within an allowed idle window. A
stalled workflow produces a ``workflow_failure`` exception record. Detection is
deterministic: the gap between the last activity and ``now`` is compared against
a fixed threshold.
"""

from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime

from workflow_os.exception.classification import ExceptionType
from workflow_os.exception.record import ExceptionRecord, utcnow
from workflow_os.exception.severity import ExceptionSeverity

_SOURCE = "stall-detector"


def is_stalled(
    last_activity: datetime, max_idle_seconds: float, now: datetime | None = None
) -> bool:
    """Return ``True`` if no activity has occurred within the idle window."""
    now = now or utcnow()
    return (now - last_activity).total_seconds() > max_idle_seconds


def detect_stalled_workflows(
    activities: Mapping[str, datetime],
    max_idle_seconds: float,
    now: datetime | None = None,
) -> list[ExceptionRecord]:
    """Return ``workflow_failure`` exceptions for workflows that have stalled.

    ``activities`` maps a workflow id to the time of its last activity.
    """
    now = now or utcnow()
    records: list[ExceptionRecord] = []
    for workflow_id, last_activity in activities.items():
        if not is_stalled(last_activity, max_idle_seconds, now):
            continue
        idle = (now - last_activity).total_seconds()
        records.append(
            ExceptionRecord.create(
                workflow_id=workflow_id,
                exception_type=ExceptionType.WORKFLOW_FAILURE.value,
                severity=ExceptionSeverity.MEDIUM.value,
                message=f"workflow stalled for {idle:.0f}s",
                source=_SOURCE,
                detected_at=now,
                metadata={"last_activity": last_activity.isoformat()},
            )
        )
    return records
