"""Exception intelligence for the workflow operating system.

This subpackage detects workflow failures, classifies and scores them, stores
them, recommends deterministic recovery actions, and analyses recovery
effectiveness, recurring failures, and trends. It builds on the workflow,
memory, decision, SOP, and approval layers without modifying them, and is fully
deterministic and rule-based.
"""

from workflow_os.exception.approvals import detect_missing_approvals
from workflow_os.exception.classification import (
    ALL_EXCEPTION_TYPES,
    ExceptionType,
    normalize_type,
)
from workflow_os.exception.deadline import (
    Deadline,
    detect_deadline_failure,
    detect_deadline_failures,
)
from workflow_os.exception.record import (
    ExceptionRecord,
    new_exception_id,
    utcnow,
)
from workflow_os.exception.recovery import (
    RecoveryAction,
    RecoveryStatus,
    new_recovery_id,
)
from workflow_os.exception.resources import (
    detect_missing_resources,
    find_missing_resources,
)
from workflow_os.exception.severity import (
    ALL_SEVERITIES,
    ExceptionSeverity,
    normalize_severity,
    severity_rank,
)
from workflow_os.exception.sqlite_store import SQLiteExceptionStore
from workflow_os.exception.stall import detect_stalled_workflows, is_stalled
from workflow_os.exception.store import (
    ExceptionList,
    ExceptionNotFoundError,
    ExceptionQuery,
    ExceptionStore,
    InMemoryExceptionStore,
    apply_query,
    matches,
)

__all__ = [
    "ALL_EXCEPTION_TYPES",
    "ALL_SEVERITIES",
    "Deadline",
    "ExceptionList",
    "ExceptionNotFoundError",
    "ExceptionQuery",
    "ExceptionRecord",
    "ExceptionSeverity",
    "ExceptionStore",
    "ExceptionType",
    "InMemoryExceptionStore",
    "RecoveryAction",
    "RecoveryStatus",
    "SQLiteExceptionStore",
    "apply_query",
    "detect_deadline_failure",
    "detect_deadline_failures",
    "detect_missing_approvals",
    "detect_missing_resources",
    "detect_stalled_workflows",
    "find_missing_resources",
    "is_stalled",
    "matches",
    "new_exception_id",
    "new_recovery_id",
    "normalize_severity",
    "normalize_type",
    "severity_rank",
    "utcnow",
]
