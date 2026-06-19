"""High-level retrieval helpers over a memory store.

These functions provide convenient, intention-revealing queries on top of the
generic :class:`~workflow_os.memory.store.MemoryQuery` interface.
"""

from __future__ import annotations

from workflow_os.memory.record import MemoryRecord
from workflow_os.memory.store import MemoryQuery, MemoryStore


def get_workflow_history(
    store: MemoryStore,
    workflow_id: str,
    *,
    order: str = "asc",
    limit: int | None = None,
) -> list[MemoryRecord]:
    """Return the ordered event history for a workflow.

    Events are returned oldest-first by default; pass ``order="desc"`` for
    newest-first.
    """
    return store.query(
        MemoryQuery(workflow_id=workflow_id, order=order, limit=limit)
    )
