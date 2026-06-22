"""Lessons-learned capture.

Captures operational knowledge that informs SOPs: lessons, observations,
postmortems, and operational notes. Each note can be linked to a SOP and/or a
workflow type and is stored in a simple in-memory collection.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

from workflow_os.sop.record import utcnow


def new_lesson_id() -> str:
    """Return a fresh, unique lesson id."""
    return uuid.uuid4().hex


LessonList = list["LessonRecord"]


class LessonType(str, Enum):
    """The kinds of lessons-learned notes."""

    LESSON = "lesson"
    OBSERVATION = "observation"
    POSTMORTEM = "postmortem"
    OPERATIONAL_NOTE = "operational_note"

    def __str__(self) -> str:  # pragma: no cover - convenience only
        return self.value


@dataclass
class LessonRecord:
    """A single captured lesson, observation, postmortem, or note."""

    lesson_id: str
    lesson_type: str
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
        lesson_type: str = LessonType.LESSON.value,
        sop_id: str | None = None,
        workflow_type: str | None = None,
        author: str | None = None,
        metadata: dict[str, Any] | None = None,
        created_at: datetime | None = None,
        lesson_id: str | None = None,
    ) -> LessonRecord:
        """Build a :class:`LessonRecord`, filling in id and timestamp by default."""
        return cls(
            lesson_id=lesson_id or new_lesson_id(),
            lesson_type=str(lesson_type),
            text=text,
            sop_id=sop_id,
            workflow_type=workflow_type,
            author=author,
            created_at=created_at or utcnow(),
            metadata=dict(metadata or {}),
        )


class LessonStore:
    """An in-memory collection of lessons-learned records."""

    def __init__(self) -> None:
        self._records: dict[str, LessonRecord] = {}

    def add(self, record: LessonRecord) -> None:
        """Store a lesson record."""
        self._records[record.lesson_id] = record

    def get(self, lesson_id: str) -> LessonRecord:
        """Return a lesson by id or raise ``KeyError`` if missing."""
        return self._records[lesson_id]

    def list(self) -> LessonList:
        """Return all lessons ordered by creation time."""
        return sorted(self._records.values(), key=lambda record: record.created_at)

    def for_sop(self, sop_id: str) -> LessonList:
        """Return lessons linked to a SOP."""
        return [record for record in self.list() if record.sop_id == sop_id]

    def for_type(self, lesson_type: str) -> LessonList:
        """Return lessons of a given type."""
        return [
            record for record in self.list() if record.lesson_type == str(lesson_type)
        ]


def capture_lesson(
    store: LessonStore,
    text: str,
    *,
    lesson_type: str = LessonType.LESSON.value,
    sop_id: str | None = None,
    workflow_type: str | None = None,
    author: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> LessonRecord:
    """Capture a lesson into ``store`` and return the stored record."""
    record = LessonRecord.create(
        text=text,
        lesson_type=lesson_type,
        sop_id=sop_id,
        workflow_type=workflow_type,
        author=author,
        metadata=metadata,
    )
    store.add(record)
    return record
