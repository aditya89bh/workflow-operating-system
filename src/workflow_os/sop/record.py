"""The :class:`SOPRecord` schema.

A standard operating procedure (SOP) record captures institutional knowledge
about how a kind of workflow is normally performed: a titled, versioned,
authored document with a lifecycle status, tags, and free-form metadata.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


def new_sop_id() -> str:
    """Return a fresh, unique SOP id."""
    return uuid.uuid4().hex


def utcnow() -> datetime:
    """Return the current time as a timezone-aware UTC datetime."""
    return datetime.now(timezone.utc)


class SOPStatus(str, Enum):
    """The lifecycle states a SOP can be in."""

    DRAFT = "draft"
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"

    def __str__(self) -> str:  # pragma: no cover - convenience only
        return self.value


ACTIVE_STATUSES: frozenset[str] = frozenset({SOPStatus.ACTIVE.value})


@dataclass
class SOPRecord:
    """A structured standard operating procedure record.

    Attributes:
        sop_id: Unique identifier for the SOP.
        title: Human-readable title.
        workflow_type: The kind of workflow this SOP documents.
        description: Longer description of the procedure.
        version: Monotonic version number, starting at 1.
        status: Lifecycle status (see :class:`SOPStatus`).
        author: The primary author of the SOP, if known.
        created_at: When the SOP was first created (timezone-aware UTC).
        updated_at: When the SOP was last updated (timezone-aware UTC).
        tags: Free-form labels for search and grouping.
        metadata: Arbitrary key/value data attached to the SOP.
    """

    sop_id: str
    title: str
    workflow_type: str
    description: str = ""
    version: int = 1
    status: str = SOPStatus.DRAFT.value
    author: str | None = None
    created_at: datetime = field(default_factory=utcnow)
    updated_at: datetime = field(default_factory=utcnow)
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        *,
        title: str,
        workflow_type: str,
        description: str = "",
        version: int = 1,
        status: str = SOPStatus.DRAFT.value,
        author: str | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
        sop_id: str | None = None,
    ) -> SOPRecord:
        """Build a :class:`SOPRecord`, filling in id and timestamps by default."""
        now = created_at or utcnow()
        return cls(
            sop_id=sop_id or new_sop_id(),
            title=title,
            workflow_type=workflow_type,
            description=description,
            version=version,
            status=str(status),
            author=author,
            created_at=now,
            updated_at=updated_at or now,
            tags=list(tags or []),
            metadata=dict(metadata or {}),
        )
