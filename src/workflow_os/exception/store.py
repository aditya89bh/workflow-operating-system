"""Exception store abstraction.

:class:`ExceptionStore` is a structural protocol describing how exception records
are stored and retrieved. :class:`ExceptionQuery` expresses the filters a store
must support, and :func:`apply_query` provides reusable in-memory filtering so
implementations share identical query semantics. :class:`InMemoryExceptionStore`
is a dictionary-backed implementation used in tests and demos.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol, runtime_checkable

from workflow_os.exception.record import ExceptionRecord

ExceptionList = list[ExceptionRecord]


class ExceptionNotFoundError(KeyError):
    """Raised when an exception id cannot be found in an exception store."""


@dataclass
class ExceptionQuery:
    """A filter over exception records.

    All fields are optional; an empty query matches every record. Results are
    ordered by ``detected_at`` (ascending by default).
    """

    workflow_id: str | None = None
    step_id: str | None = None
    exception_types: tuple[str, ...] | None = None
    severities: tuple[str, ...] | None = None
    resolved: bool | None = None
    source: str | None = None
    since: datetime | None = None
    until: datetime | None = None
    limit: int | None = None
    order: str = "asc"


@runtime_checkable
class ExceptionStore(Protocol):
    """Storage interface for exception records."""

    def add(self, record: ExceptionRecord) -> None:
        """Persist a single exception record."""
        ...

    def get(self, exception_id: str) -> ExceptionRecord:
        """Return the record with ``exception_id`` or raise if missing."""
        ...

    def update(self, record: ExceptionRecord) -> None:
        """Persist changes to an existing record or raise if missing."""
        ...

    def delete(self, exception_id: str) -> None:
        """Remove the record with ``exception_id`` or raise if missing."""
        ...

    def list(self) -> ExceptionList:
        """Return all stored records ordered by ``detected_at``."""
        ...

    def query(self, query: ExceptionQuery) -> ExceptionList:
        """Return records matching ``query`` ordered by ``detected_at``."""
        ...


def matches(record: ExceptionRecord, query: ExceptionQuery) -> bool:
    """Return ``True`` if ``record`` satisfies every filter in ``query``."""
    if query.workflow_id is not None and record.workflow_id != query.workflow_id:
        return False
    if query.step_id is not None and record.step_id != query.step_id:
        return False
    if query.exception_types is not None and record.exception_type not in {
        str(value) for value in query.exception_types
    }:
        return False
    if query.severities is not None and record.severity not in {
        str(value) for value in query.severities
    }:
        return False
    if query.resolved is not None and record.resolved is not query.resolved:
        return False
    if query.source is not None and record.source != query.source:
        return False
    if query.since is not None and record.detected_at < query.since:
        return False
    if query.until is not None and record.detected_at > query.until:
        return False
    return True


def apply_query(
    records: Iterable[ExceptionRecord], query: ExceptionQuery
) -> list[ExceptionRecord]:
    """Filter, order, and limit ``records`` according to ``query``."""
    result = [record for record in records if matches(record, query)]
    result.sort(key=lambda record: record.detected_at, reverse=query.order == "desc")
    if query.limit is not None:
        result = result[: query.limit]
    return result


class InMemoryExceptionStore:
    """A dictionary-backed :class:`ExceptionStore` implementation."""

    def __init__(self) -> None:
        self._records: dict[str, ExceptionRecord] = {}

    def add(self, record: ExceptionRecord) -> None:
        self._records[record.exception_id] = record

    def get(self, exception_id: str) -> ExceptionRecord:
        try:
            return self._records[exception_id]
        except KeyError as exc:
            raise ExceptionNotFoundError(exception_id) from exc

    def update(self, record: ExceptionRecord) -> None:
        if record.exception_id not in self._records:
            raise ExceptionNotFoundError(record.exception_id)
        self._records[record.exception_id] = record

    def delete(self, exception_id: str) -> None:
        if exception_id not in self._records:
            raise ExceptionNotFoundError(exception_id)
        del self._records[exception_id]

    def list(self) -> ExceptionList:
        return apply_query(self._records.values(), ExceptionQuery())

    def query(self, query: ExceptionQuery) -> ExceptionList:
        return apply_query(self._records.values(), query)
