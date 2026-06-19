"""Organizational memory for the workflow operating system.

This subpackage records structured memory events from workflow executions and
provides storage, retrieval, auditing, and confidence scoring on top of them.
"""

from workflow_os.memory.events import (
    STEP_EVENT_TYPES,
    WORKFLOW_EVENT_TYPES,
    MemoryEventType,
)
from workflow_os.memory.record import MemoryRecord, new_event_id, utcnow
from workflow_os.memory.sqlite_store import SQLiteMemoryStore
from workflow_os.memory.store import (
    MemoryNotFoundError,
    MemoryQuery,
    MemoryStore,
    apply_query,
    matches,
)

__all__ = [
    "STEP_EVENT_TYPES",
    "WORKFLOW_EVENT_TYPES",
    "MemoryEventType",
    "MemoryNotFoundError",
    "MemoryQuery",
    "MemoryRecord",
    "MemoryStore",
    "SQLiteMemoryStore",
    "apply_query",
    "matches",
    "new_event_id",
    "utcnow",
]
