"""The :class:`Recommendation` schema.

A recommendation is a deterministic, rule-derived suggestion for improving an
organizational process. It carries a category, human-readable title and
description, a severity, and a confidence score derived from the supporting
evidence. Recommendations are plain data; the rules that build them live in the
dedicated recommendation modules.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def new_recommendation_id() -> str:
    """Return a fresh, unique recommendation id."""
    return uuid.uuid4().hex


def utcnow() -> datetime:
    """Return the current time as a timezone-aware UTC datetime."""
    return datetime.now(timezone.utc)


@dataclass
class Recommendation:
    """A deterministic improvement recommendation.

    Attributes:
        recommendation_id: Unique identifier for the recommendation.
        category: The area the recommendation applies to (e.g. ``workflow``).
        title: Short human-readable title.
        description: Longer description of the suggested change.
        severity: How pressing the recommendation is (e.g. ``low``/``high``).
        confidence: How strongly the evidence supports it, in ``[0.0, 1.0]``.
        created_at: When the recommendation was produced (timezone-aware UTC).
        metadata: Arbitrary key/value data attached to the recommendation.
    """

    recommendation_id: str
    category: str
    title: str
    description: str = ""
    severity: str = "medium"
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
        severity: str = "medium",
        confidence: float = 1.0,
        metadata: dict[str, Any] | None = None,
        created_at: datetime | None = None,
        recommendation_id: str | None = None,
    ) -> Recommendation:
        """Build a :class:`Recommendation`, filling in id and timestamp."""
        return cls(
            recommendation_id=recommendation_id or new_recommendation_id(),
            category=str(category),
            title=title,
            description=description,
            severity=str(severity),
            confidence=confidence,
            created_at=created_at or utcnow(),
            metadata=dict(metadata or {}),
        )
