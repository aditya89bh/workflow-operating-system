"""Decision intelligence for the workflow operating system.

This subpackage captures structured decision records, stores them, and provides
retrieval, search, explanation, replay, and analysis on top of them. It builds
on the organizational memory layer without modifying it.
"""

from workflow_os.decision.record import (
    DecisionRecord,
    new_decision_id,
    utcnow,
)
from workflow_os.decision.recorder import DecisionRecorder
from workflow_os.decision.search import (
    search_by_decision_text,
    search_by_outcome,
    search_by_rationale,
    search_decisions,
)
from workflow_os.decision.sqlite_store import SQLiteDecisionStore
from workflow_os.decision.store import (
    DecisionList,
    DecisionNotFoundError,
    DecisionQuery,
    DecisionStore,
    apply_query,
    matches,
)
from workflow_os.decision.timelines import (
    DecisionTimelineEntry,
    build_timeline,
    get_actor_decision_timeline,
    get_decision_timeline,
    get_workflow_decision_timeline,
)
from workflow_os.decision.types import ALL_DECISION_TYPES, DecisionType

__all__ = [
    "ALL_DECISION_TYPES",
    "DecisionList",
    "DecisionNotFoundError",
    "DecisionQuery",
    "DecisionRecord",
    "DecisionRecorder",
    "DecisionStore",
    "DecisionTimelineEntry",
    "DecisionType",
    "SQLiteDecisionStore",
    "apply_query",
    "build_timeline",
    "get_actor_decision_timeline",
    "get_decision_timeline",
    "get_workflow_decision_timeline",
    "matches",
    "new_decision_id",
    "search_by_decision_text",
    "search_by_outcome",
    "search_by_rationale",
    "search_decisions",
    "utcnow",
]
