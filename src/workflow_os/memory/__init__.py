"""Organizational memory for the workflow operating system.

This subpackage records structured memory events from workflow executions and
provides storage, retrieval, auditing, and confidence scoring on top of them.
"""

from workflow_os.memory.actors import (
    OWNER_METADATA_KEY,
    step_actor,
    workflow_owner,
)
from workflow_os.memory.events import (
    STEP_EVENT_TYPES,
    WORKFLOW_EVENT_TYPES,
    MemoryEventType,
)
from workflow_os.memory.history import (
    TimelineEntry,
    get_execution_timeline,
    get_step_records,
    get_step_timeline,
    get_workflow_records,
)
from workflow_os.memory.record import MemoryRecord, new_event_id, utcnow
from workflow_os.memory.recorder import MemoryRecorder
from workflow_os.memory.retrieval import get_actor_history, get_workflow_history
from workflow_os.memory.sqlite_store import SQLiteMemoryStore
from workflow_os.memory.store import (
    MemoryNotFoundError,
    MemoryQuery,
    MemoryStore,
    apply_query,
    matches,
)

__all__ = [
    "OWNER_METADATA_KEY",
    "STEP_EVENT_TYPES",
    "WORKFLOW_EVENT_TYPES",
    "MemoryEventType",
    "MemoryNotFoundError",
    "MemoryQuery",
    "MemoryRecord",
    "MemoryRecorder",
    "MemoryStore",
    "SQLiteMemoryStore",
    "TimelineEntry",
    "apply_query",
    "get_actor_history",
    "get_execution_timeline",
    "get_step_records",
    "get_step_timeline",
    "get_workflow_history",
    "get_workflow_records",
    "matches",
    "new_event_id",
    "step_actor",
    "utcnow",
    "workflow_owner",
]
