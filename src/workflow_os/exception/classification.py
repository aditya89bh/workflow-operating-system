"""Exception classification definitions.

Defines the categories a workflow exception can fall into. Classification is
deterministic: a detector assigns exactly one type to each exception.
"""

from __future__ import annotations

from enum import Enum


class ExceptionType(str, Enum):
    """The categories of workflow exception."""

    WORKFLOW_FAILURE = "workflow_failure"
    STEP_FAILURE = "step_failure"
    TIMEOUT = "timeout"
    MISSING_RESOURCE = "missing_resource"
    APPROVAL_FAILURE = "approval_failure"
    VALIDATION_FAILURE = "validation_failure"
    UNKNOWN = "unknown"

    def __str__(self) -> str:  # pragma: no cover - convenience only
        return self.value


ALL_EXCEPTION_TYPES: frozenset[ExceptionType] = frozenset(ExceptionType)


def normalize_type(value: str) -> str:
    """Return a known exception type string, defaulting to ``unknown``."""
    text = str(value)
    if text in {member.value for member in ExceptionType}:
        return text
    return ExceptionType.UNKNOWN.value
