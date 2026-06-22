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
from workflow_os.exception.clustering import (
    cluster_by_recovery_outcome,
    cluster_by_severity,
    cluster_by_type,
    cluster_by_workflow,
    recovery_outcome,
)
from workflow_os.exception.deadline import (
    Deadline,
    detect_deadline_failure,
    detect_deadline_failures,
)
from workflow_os.exception.effectiveness import (
    EffectivenessMetrics,
    compute_effectiveness,
    mean_recovery_time,
    recovery_success_rate,
    retry_success_rate,
)
from workflow_os.exception.fallback import FallbackStrategy
from workflow_os.exception.recommendation import (
    recommend_action,
    recommend_recovery,
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
from workflow_os.exception.retry import RetryStrategy, count_retries
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
from workflow_os.exception.trends import (
    WorkflowRiskReport,
    failure_signature,
    failures_over_time,
    recurring_failures,
    workflow_risk_reports,
)

__all__ = [
    "ALL_EXCEPTION_TYPES",
    "ALL_SEVERITIES",
    "Deadline",
    "EffectivenessMetrics",
    "ExceptionList",
    "ExceptionNotFoundError",
    "ExceptionQuery",
    "ExceptionRecord",
    "ExceptionSeverity",
    "ExceptionStore",
    "ExceptionType",
    "FallbackStrategy",
    "InMemoryExceptionStore",
    "RecoveryAction",
    "RecoveryStatus",
    "RetryStrategy",
    "SQLiteExceptionStore",
    "WorkflowRiskReport",
    "apply_query",
    "cluster_by_recovery_outcome",
    "cluster_by_severity",
    "cluster_by_type",
    "cluster_by_workflow",
    "compute_effectiveness",
    "count_retries",
    "detect_deadline_failure",
    "detect_deadline_failures",
    "detect_missing_approvals",
    "detect_missing_resources",
    "detect_stalled_workflows",
    "failure_signature",
    "failures_over_time",
    "find_missing_resources",
    "is_stalled",
    "matches",
    "mean_recovery_time",
    "new_exception_id",
    "new_recovery_id",
    "normalize_severity",
    "normalize_type",
    "recommend_action",
    "recommend_recovery",
    "recovery_outcome",
    "recovery_success_rate",
    "recurring_failures",
    "retry_success_rate",
    "severity_rank",
    "utcnow",
    "workflow_risk_reports",
]
