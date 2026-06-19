"""Audit reporting over a memory store.

An :class:`AuditReport` summarises the contents of a store: how many events it
holds, how they break down by type, workflow, and actor, and the span of time
they cover.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from workflow_os.memory.store import MemoryQuery, MemoryStore


@dataclass
class AuditReport:
    """A summary of the events held in a memory store."""

    total_events: int = 0
    event_type_counts: dict[str, int] = field(default_factory=dict)
    workflow_counts: dict[str, int] = field(default_factory=dict)
    actor_counts: dict[str, int] = field(default_factory=dict)
    oldest_event: datetime | None = None
    newest_event: datetime | None = None

    @property
    def workflow_count(self) -> int:
        """Number of distinct workflows represented in the report."""
        return len(self.workflow_counts)

    @property
    def actor_count(self) -> int:
        """Number of distinct actors represented in the report."""
        return len(self.actor_counts)

    def as_dict(self) -> dict[str, Any]:
        """Return a JSON-serialisable view of the report."""
        return {
            "total_events": self.total_events,
            "event_type_counts": dict(self.event_type_counts),
            "workflow_counts": dict(self.workflow_counts),
            "actor_counts": dict(self.actor_counts),
            "workflow_count": self.workflow_count,
            "actor_count": self.actor_count,
            "oldest_event": (
                self.oldest_event.isoformat() if self.oldest_event else None
            ),
            "newest_event": (
                self.newest_event.isoformat() if self.newest_event else None
            ),
        }


def generate_audit_report(
    store: MemoryStore, query: MemoryQuery | None = None
) -> AuditReport:
    """Build an :class:`AuditReport` for the records matching ``query``."""
    records = store.query(query if query is not None else MemoryQuery())
    if not records:
        return AuditReport()

    event_types: Counter[str] = Counter(record.event_type for record in records)
    workflows: Counter[str] = Counter(record.workflow_id for record in records)
    actors: Counter[str] = Counter(
        record.actor for record in records if record.actor is not None
    )
    timestamps = [record.timestamp for record in records]

    return AuditReport(
        total_events=len(records),
        event_type_counts=dict(event_types),
        workflow_counts=dict(workflows),
        actor_counts=dict(actors),
        oldest_event=min(timestamps),
        newest_event=max(timestamps),
    )
