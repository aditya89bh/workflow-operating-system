"""Memory agent.

The memory agent is a deterministic service object that mediates access to the
Phase 2 organizational memory: it writes memory records, retrieves them by query,
and answers history questions about workflows and actors. It wraps a
:class:`~workflow_os.memory.store.MemoryStore` without changing it.
"""

from __future__ import annotations

from typing import Any

from workflow_os.agents.record import Agent
from workflow_os.memory.record import MemoryRecord
from workflow_os.memory.store import MemoryQuery, MemoryStore


class MemoryAgent:
    """Reads and writes organizational memory on behalf of other agents."""

    def __init__(self, store: MemoryStore, agent: Agent | None = None) -> None:
        self.store = store
        self.agent = agent

    def write(
        self,
        *,
        workflow_id: str,
        event_type: str,
        step_id: str | None = None,
        actor: str | None = None,
        confidence: float = 1.0,
        metadata: dict[str, Any] | None = None,
    ) -> MemoryRecord:
        """Create and persist a memory record, returning it."""
        record = MemoryRecord.create(
            workflow_id=workflow_id,
            event_type=event_type,
            step_id=step_id,
            actor=actor,
            confidence=confidence,
            metadata=metadata,
        )
        self.store.add(record)
        return record

    def retrieve(self, query: MemoryQuery) -> list[MemoryRecord]:
        """Return memory records matching ``query``."""
        return self.store.query(query)

    def workflow_history(self, workflow_id: str) -> list[MemoryRecord]:
        """Return all memory records for a workflow, oldest first."""
        return self.store.query(MemoryQuery(workflow_id=workflow_id))

    def actor_history(self, actor: str) -> list[MemoryRecord]:
        """Return all memory records attributed to an actor, oldest first."""
        return self.store.query(MemoryQuery(actor=actor))
