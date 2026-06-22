"""Missing resource detection.

Detects required resources that are not available to a workflow or step. Each
missing resource produces a ``missing_resource`` exception record. Detection is a
deterministic set difference between required and available resources.
"""

from __future__ import annotations

from collections.abc import Iterable

from workflow_os.exception.classification import ExceptionType
from workflow_os.exception.record import ExceptionRecord, utcnow
from workflow_os.exception.severity import ExceptionSeverity

_SOURCE = "resource-detector"


def find_missing_resources(
    required: Iterable[str], available: Iterable[str]
) -> list[str]:
    """Return the required resources that are not available, in order."""
    have = set(available)
    seen: set[str] = set()
    missing: list[str] = []
    for resource in required:
        if resource not in have and resource not in seen:
            missing.append(resource)
            seen.add(resource)
    return missing


def detect_missing_resources(
    required: Iterable[str],
    available: Iterable[str],
    workflow_id: str,
    step_id: str | None = None,
) -> list[ExceptionRecord]:
    """Return a ``missing_resource`` exception for each unavailable resource."""
    now = utcnow()
    return [
        ExceptionRecord.create(
            workflow_id=workflow_id,
            step_id=step_id,
            exception_type=ExceptionType.MISSING_RESOURCE.value,
            severity=ExceptionSeverity.HIGH.value,
            message=f"required resource {resource!r} is unavailable",
            source=_SOURCE,
            detected_at=now,
            metadata={"resource": resource},
        )
        for resource in find_missing_resources(required, available)
    ]
