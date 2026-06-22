"""The :class:`OrganizationalInsight` schema.

An insight is a deterministic observation about the organization derived from its
recorded history: a categorized statement backed by concrete evidence and a
confidence score. Insights describe what is happening; recommendations describe
what to do about it.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def new_insight_id() -> str:
    """Return a fresh, unique insight id."""
    return uuid.uuid4().hex


def utcnow() -> datetime:
    """Return the current time as a timezone-aware UTC datetime."""
    return datetime.now(timezone.utc)


@dataclass
class OrganizationalInsight:
    """A deterministic, evidence-backed organizational observation.

    Attributes:
        insight_id: Unique identifier for the insight.
        category: The area the insight relates to (e.g. ``success``).
        title: Short human-readable title.
        description: Longer description of the observation.
        evidence: Concrete supporting facts (e.g. ids, counts, rates).
        confidence: How strongly the evidence supports it, in ``[0.0, 1.0]``.
        created_at: When the insight was produced (timezone-aware UTC).
        metadata: Arbitrary key/value data attached to the insight.
    """

    insight_id: str
    category: str
    title: str
    description: str = ""
    evidence: list[str] = field(default_factory=list)
    confidence: float = 1.0
    created_at: datetime = field(default_factory=utcnow)
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        *,
        category: str,
        title: str,
        description: str = "",
        evidence: list[str] | None = None,
        confidence: float = 1.0,
        metadata: dict[str, Any] | None = None,
        created_at: datetime | None = None,
        insight_id: str | None = None,
    ) -> OrganizationalInsight:
        """Build an :class:`OrganizationalInsight`, filling in id and timestamp."""
        return cls(
            insight_id=insight_id or new_insight_id(),
            category=str(category),
            title=title,
            description=description,
            evidence=list(evidence or []),
            confidence=confidence,
            created_at=created_at or utcnow(),
            metadata=dict(metadata or {}),
        )
