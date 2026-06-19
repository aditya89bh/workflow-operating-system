"""Memory store abstraction.

:class:`MemoryStore` is a structural protocol describing how memory records are
stored and retrieved. :class:`MemoryQuery` expresses the filters a store must
support, and :func:`apply_query` provides reusable in-memory filtering so that
implementations share identical query semantics.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol, runtime_checkable

from workflow_os.memory.record import MemoryRecord

RecordList = list[MemoryRecord]


class MemoryNotFoundError(KeyError):
    """Raised when an event id cannot be found in a memory store."""


@dataclass
class MemoryQuery:
    """A filter over memory records.

    All fields are optional; an empty query matches every record. Results are
    ordered by timestamp (ascending by default).
    """

    workflow_id: str | None = None
    step_id: str | None = None
    actor: str | None = None
    event_types: tuple[str, ...] | None = None
    since: datetime | None = None
    until: datetime | None = None
    limit: int | None = None
    order: str = "asc"


@runtime_checkable
class MemoryStore(Protocol):
    """Storage interface for memory records."""

    def add(self, record: MemoryRecord) -> None:
        """Persist a single memory record."""
        ...

    def get(self, event_id: str) -> MemoryRecord:
        """Return the record with ``event_id`` or raise if missing."""
        ...

    def list(self) -> RecordList:
        """Return all stored records ordered by timestamp."""
        ...

    def delete(self, event_id: str) -> None:
        """Remove the record with ``event_id`` or raise if missing."""
        ...

    def query(self, query: MemoryQuery) -> RecordList:
        """Return records matching ``query`` ordered by timestamp."""
        ...


def matches(record: MemoryRecord, query: MemoryQuery) -> bool:
    """Return ``True`` if ``record`` satisfies every filter in ``query``."""
    if query.workflow_id is not None and record.workflow_id != query.workflow_id:
        return False
    if query.step_id is not None and record.step_id != query.step_id:
        return False
    if query.actor is not None and record.actor != query.actor:
        return False
    if query.event_types is not None:
        allowed = {str(event_type) for event_type in query.event_types}
        if record.event_type not in allowed:
            return False
    if query.since is not None and record.timestamp < query.since:
        return False
    if query.until is not None and record.timestamp > query.until:
        return False
    return True


def apply_query(
    records: Iterable[MemoryRecord], query: MemoryQuery
) -> list[MemoryRecord]:
    """Filter, order, and limit ``records`` according to ``query``."""
    result = [record for record in records if matches(record, query)]
    result.sort(key=lambda record: record.timestamp, reverse=query.order == "desc")
    if query.limit is not None:
        result = result[: query.limit]
    return result
