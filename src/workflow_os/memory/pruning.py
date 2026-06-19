"""Pruning policies for keeping a memory store bounded.

Three complementary policies are supported:

* **max age** - drop records older than a cutoff;
* **max count** - keep only the newest N records;
* **workflow-scoped** - drop every record for a given workflow.

Each function returns the number of records it removed.
"""

from __future__ import annotations

from datetime import datetime, timedelta

from workflow_os.memory.record import utcnow
from workflow_os.memory.store import MemoryQuery, MemoryStore


def prune_older_than(store: MemoryStore, cutoff: datetime) -> int:
    """Delete records with a timestamp strictly before ``cutoff``."""
    stale = store.query(MemoryQuery(until=cutoff))
    removed = 0
    for record in stale:
        if record.timestamp < cutoff:
            store.delete(record.event_id)
            removed += 1
    return removed


def prune_by_max_age(
    store: MemoryStore, max_age: timedelta, *, now: datetime | None = None
) -> int:
    """Delete records older than ``max_age`` relative to ``now`` (default: utcnow)."""
    reference = now if now is not None else utcnow()
    return prune_older_than(store, reference - max_age)


def prune_to_max_count(store: MemoryStore, max_count: int) -> int:
    """Keep only the newest ``max_count`` records, deleting the rest.

    A ``max_count`` of ``0`` removes everything; negative values are treated as
    ``0``.
    """
    keep = max(max_count, 0)
    records = store.query(MemoryQuery(order="desc"))
    to_delete = records[keep:]
    for record in to_delete:
        store.delete(record.event_id)
    return len(to_delete)


def prune_workflow(store: MemoryStore, workflow_id: str) -> int:
    """Delete every record belonging to ``workflow_id``."""
    records = store.query(MemoryQuery(workflow_id=workflow_id))
    for record in records:
        store.delete(record.event_id)
    return len(records)
