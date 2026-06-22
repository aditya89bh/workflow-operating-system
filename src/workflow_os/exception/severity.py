"""Exception severity definitions.

Defines how serious a workflow exception is. Severities are ordered so they can
be compared and ranked deterministically.
"""

from __future__ import annotations

from enum import Enum


class ExceptionSeverity(str, Enum):
    """How serious a workflow exception is."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

    def __str__(self) -> str:  # pragma: no cover - convenience only
        return self.value


_ORDER: dict[str, int] = {
    ExceptionSeverity.LOW.value: 0,
    ExceptionSeverity.MEDIUM.value: 1,
    ExceptionSeverity.HIGH.value: 2,
    ExceptionSeverity.CRITICAL.value: 3,
}

ALL_SEVERITIES: frozenset[ExceptionSeverity] = frozenset(ExceptionSeverity)


def severity_rank(severity: str) -> int:
    """Return a numeric rank for ``severity`` (higher is more serious)."""
    return _ORDER.get(str(severity), _ORDER[ExceptionSeverity.MEDIUM.value])


def normalize_severity(value: str) -> str:
    """Return a known severity string, defaulting to ``medium``."""
    text = str(value)
    if text in _ORDER:
        return text
    return ExceptionSeverity.MEDIUM.value
