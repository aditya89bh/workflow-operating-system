"""SOP store abstraction.

:class:`SOPStore` is a structural protocol describing how SOP records are
stored and retrieved. :class:`SOPQuery` expresses the filters a store must
support, and :func:`apply_query` provides reusable in-memory filtering so
implementations share identical query semantics.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from workflow_os.sop.record import SOPRecord

SOPList = list[SOPRecord]


class SOPNotFoundError(KeyError):
    """Raised when a SOP id cannot be found in a SOP store."""


@dataclass
class SOPQuery:
    """A filter over SOP records.

    All fields are optional; an empty query matches every record. Tag filters
    match records that contain *all* of the requested tags. Results are ordered
    by ``updated_at`` (ascending by default).
    """

    workflow_type: str | None = None
    status: str | None = None
    author: str | None = None
    tags: tuple[str, ...] | None = None
    version: int | None = None
    limit: int | None = None
    order: str = "asc"


@runtime_checkable
class SOPStore(Protocol):
    """Storage interface for SOP records."""

    def add(self, record: SOPRecord) -> None:
        """Persist a single SOP record."""
        ...

    def get(self, sop_id: str) -> SOPRecord:
        """Return the record with ``sop_id`` or raise if missing."""
        ...

    def update(self, record: SOPRecord) -> None:
        """Update an existing SOP record or raise if missing."""
        ...

    def delete(self, sop_id: str) -> None:
        """Remove the record with ``sop_id`` or raise if missing."""
        ...

    def list(self) -> SOPList:
        """Return all stored records ordered by ``updated_at``."""
        ...

    def query(self, query: SOPQuery) -> SOPList:
        """Return records matching ``query`` ordered by ``updated_at``."""
        ...


def matches(record: SOPRecord, query: SOPQuery) -> bool:
    """Return ``True`` if ``record`` satisfies every filter in ``query``."""
    if query.workflow_type is not None and record.workflow_type != query.workflow_type:
        return False
    if query.status is not None and record.status != query.status:
        return False
    if query.author is not None and record.author != query.author:
        return False
    if query.version is not None and record.version != query.version:
        return False
    if query.tags is not None:
        if not set(query.tags).issubset(set(record.tags)):
            return False
    return True


def apply_query(records: Iterable[SOPRecord], query: SOPQuery) -> list[SOPRecord]:
    """Filter, order, and limit ``records`` according to ``query``."""
    result = [record for record in records if matches(record, query)]
    result.sort(key=lambda record: record.updated_at, reverse=query.order == "desc")
    if query.limit is not None:
        result = result[: query.limit]
    return result
