"""Best-practice capture.

Captures the standards a team chooses to follow: practices, guidelines,
conventions, and standards. Each entry can be linked to a SOP and/or a workflow
type and is stored in a simple in-memory collection.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

from workflow_os.sop.record import utcnow


def new_practice_id() -> str:
    """Return a fresh, unique best-practice id."""
    return uuid.uuid4().hex


BestPracticeList = list["BestPracticeRecord"]


class BestPracticeType(str, Enum):
    """The kinds of best-practice entries."""

    PRACTICE = "practice"
    GUIDELINE = "guideline"
    CONVENTION = "convention"
    STANDARD = "standard"

    def __str__(self) -> str:  # pragma: no cover - convenience only
        return self.value


@dataclass
class BestPracticeRecord:
    """A single captured practice, guideline, convention, or standard."""

    practice_id: str
    practice_type: str
    text: str
    sop_id: str | None = None
    workflow_type: str | None = None
    author: str | None = None
    created_at: datetime = field(default_factory=utcnow)
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        *,
        text: str,
        practice_type: str = BestPracticeType.PRACTICE.value,
        sop_id: str | None = None,
        workflow_type: str | None = None,
        author: str | None = None,
        metadata: dict[str, Any] | None = None,
        created_at: datetime | None = None,
        practice_id: str | None = None,
    ) -> BestPracticeRecord:
        """Build a record, filling in id and timestamp by default."""
        return cls(
            practice_id=practice_id or new_practice_id(),
            practice_type=str(practice_type),
            text=text,
            sop_id=sop_id,
            workflow_type=workflow_type,
            author=author,
            created_at=created_at or utcnow(),
            metadata=dict(metadata or {}),
        )


class BestPracticeStore:
    """An in-memory collection of best-practice records."""

    def __init__(self) -> None:
        self._records: dict[str, BestPracticeRecord] = {}

    def add(self, record: BestPracticeRecord) -> None:
        """Store a best-practice record."""
        self._records[record.practice_id] = record

    def get(self, practice_id: str) -> BestPracticeRecord:
        """Return a best practice by id or raise ``KeyError`` if missing."""
        return self._records[practice_id]

    def list(self) -> BestPracticeList:
        """Return all best practices ordered by creation time."""
        return sorted(self._records.values(), key=lambda record: record.created_at)

    def for_sop(self, sop_id: str) -> BestPracticeList:
        """Return best practices linked to a SOP."""
        return [record for record in self.list() if record.sop_id == sop_id]

    def for_type(self, practice_type: str) -> BestPracticeList:
        """Return best practices of a given type."""
        return [
            record
            for record in self.list()
            if record.practice_type == str(practice_type)
        ]


def capture_best_practice(
    store: BestPracticeStore,
    text: str,
    *,
    practice_type: str = BestPracticeType.PRACTICE.value,
    sop_id: str | None = None,
    workflow_type: str | None = None,
    author: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> BestPracticeRecord:
    """Capture a best practice into ``store`` and return the stored record."""
    record = BestPracticeRecord.create(
        text=text,
        practice_type=practice_type,
        sop_id=sop_id,
        workflow_type=workflow_type,
        author=author,
        metadata=metadata,
    )
    store.add(record)
    return record
