"""Exception intelligence for the workflow operating system.

This subpackage detects workflow failures, classifies and scores them, stores
them, recommends deterministic recovery actions, and analyses recovery
effectiveness, recurring failures, and trends. It builds on the workflow,
memory, decision, SOP, and approval layers without modifying them, and is fully
deterministic and rule-based.
"""

from workflow_os.exception.classification import (
    ALL_EXCEPTION_TYPES,
    ExceptionType,
    normalize_type,
)
from workflow_os.exception.record import (
    ExceptionRecord,
    new_exception_id,
    utcnow,
)
from workflow_os.exception.severity import (
    ALL_SEVERITIES,
    ExceptionSeverity,
    normalize_severity,
    severity_rank,
)

__all__ = [
    "ALL_EXCEPTION_TYPES",
    "ALL_SEVERITIES",
    "ExceptionRecord",
    "ExceptionSeverity",
    "ExceptionType",
    "new_exception_id",
    "normalize_severity",
    "normalize_type",
    "severity_rank",
    "utcnow",
]
