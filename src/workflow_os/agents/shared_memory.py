"""Shared memory access.

:class:`SharedMemory` is the access layer that lets multiple agents read, write,
and query the same organizational memory store. Every access is recorded so the
collaboration can be audited deterministically.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

from workflow_os.memory.record import MemoryRecord
from workflow_os.memory.store import MemoryQuery, MemoryStore


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class MemoryAccess:
    """A record of a single shared-memory access by an agent."""

    agent_id: str | None
    action: str
    event_id: str | None = None
    timestamp: datetime = field(default_factory=_utcnow)


class SharedMemory:
    """A shared, auditable view over a :class:`MemoryStore`."""

    def __init__(self, store: MemoryStore) -> None:
        self.store = store
        self._access_log: list[MemoryAccess] = []

    def _record(self, agent_id: str | None, action: str, event_id: str | None) -> None:
        self._access_log.append(
            MemoryAccess(agent_id=agent_id, action=action, event_id=event_id)
        )

    def write(self, record: MemoryRecord, *, agent_id: str | None = None) -> MemoryRecord:
        """Add a record to shared memory, logging the write access."""
        self.store.add(record)
        self._record(agent_id, "write", record.event_id)
        return record

    def read(self, event_id: str, *, agent_id: str | None = None) -> MemoryRecord:
        """Read a record by id, logging the read access."""
        record = self.store.get(event_id)
        self._record(agent_id, "read", event_id)
        return record

    def query(
        self, query: MemoryQuery, *, agent_id: str | None = None
    ) -> list[MemoryRecord]:
        """Query shared memory, logging the query access."""
        results = self.store.query(query)
        self._record(agent_id, "query", None)
        return results

    def access_log(self) -> list[MemoryAccess]:
        """Return the recorded accesses in order."""
        return list(self._access_log)
