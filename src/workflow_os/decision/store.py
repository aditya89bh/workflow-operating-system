"""Decision store abstraction.

:class:`DecisionStore` is a structural protocol describing how decision records
are stored and retrieved. :class:`DecisionQuery` expresses the filters a store
must support, and :func:`apply_query` provides reusable in-memory filtering so
implementations share identical query semantics.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol, runtime_checkable

from workflow_os.decision.record import DecisionRecord

DecisionList = list[DecisionRecord]


class DecisionNotFoundError(KeyError):
    """Raised when a decision id cannot be found in a decision store."""


@dataclass
class DecisionQuery:
    """A filter over decision records.

    All fields are optional; an empty query matches every record. Results are
    ordered by timestamp (ascending by default).
    """

    workflow_id: str | None = None
    step_id: str | None = None
    actor: str | None = None
    decision_types: tuple[str, ...] | None = None
    outcome: str | None = None
    since: datetime | None = None
    until: datetime | None = None
    limit: int | None = None
    order: str = "asc"


@runtime_checkable
class DecisionStore(Protocol):
    """Storage interface for decision records."""

    def add(self, record: DecisionRecord) -> None:
        """Persist a single decision record."""
        ...

    def get(self, decision_id: str) -> DecisionRecord:
        """Return the record with ``decision_id`` or raise if missing."""
        ...

    def list(self) -> DecisionList:
        """Return all stored records ordered by timestamp."""
        ...

    def delete(self, decision_id: str) -> None:
        """Remove the record with ``decision_id`` or raise if missing."""
        ...

    def query(self, query: DecisionQuery) -> DecisionList:
        """Return records matching ``query`` ordered by timestamp."""
        ...


def matches(record: DecisionRecord, query: DecisionQuery) -> bool:
    """Return ``True`` if ``record`` satisfies every filter in ``query``."""
    if query.workflow_id is not None and record.workflow_id != query.workflow_id:
        return False
    if query.step_id is not None and record.step_id != query.step_id:
        return False
    if query.actor is not None and record.actor != query.actor:
        return False
    if query.decision_types is not None:
        allowed = {str(decision_type) for decision_type in query.decision_types}
        if record.decision_type not in allowed:
            return False
    if query.outcome is not None and record.outcome != query.outcome:
        return False
    if query.since is not None and record.timestamp < query.since:
        return False
    if query.until is not None and record.timestamp > query.until:
        return False
    return True


def apply_query(
    records: Iterable[DecisionRecord], query: DecisionQuery
) -> list[DecisionRecord]:
    """Filter, order, and limit ``records`` according to ``query``."""
    result = [record for record in records if matches(record, query)]
    result.sort(key=lambda record: record.timestamp, reverse=query.order == "desc")
    if query.limit is not None:
        result = result[: query.limit]
    return result
