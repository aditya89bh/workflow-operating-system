"""Approval and governance for the workflow operating system.

This subpackage models approval requests, policies, and approval workflows
(single, multi, sequential, parallel), together with timeouts, escalation,
delegation, auditing, and analytics. It builds on the workflow, memory,
decision, and SOP layers without modifying them, and is fully deterministic and
rule-based.
"""

from workflow_os.approval.audit import (
    ApprovalAuditEvent,
    ApprovalAuditLog,
    ApprovalEventType,
)
from workflow_os.approval.bottlenecks import (
    BottleneckReport,
    analyze_bottlenecks,
    escalation_hotspots,
    slowest_approvers,
    workflow_bottlenecks,
)
from workflow_os.approval.delegation import (
    DelegationEvent,
    active_delegations,
    delegate,
    delegation_history,
)
from workflow_os.approval.demo import run_demo
from workflow_os.approval.escalation import (
    EscalationEvent,
    EscalationRule,
    escalate,
    escalate_if_overdue,
    escalation_history,
    should_escalate,
)
from workflow_os.approval.history import (
    actor_approvals,
    completed_approvals,
    pending_approvals,
    requester_approvals,
    workflow_approvals,
)
from workflow_os.approval.metrics import (
    WorkloadMetrics,
    approvals_by_actor,
    average_response_time,
    compute_workload_metrics,
    overdue_count,
    pending_count,
    response_times,
)
from workflow_os.approval.multi import MultiApproverWorkflow, aggregate_state
from workflow_os.approval.parallel import ParallelApprovalWorkflow
from workflow_os.approval.policy import (
    ApprovalPolicy,
    PolicyType,
    new_policy_id,
)
from workflow_os.approval.record import (
    ApprovalRequest,
    new_approval_id,
    utcnow,
)
from workflow_os.approval.reminders import (
    Reminder,
    ReminderKind,
    generate_reminders,
    overdue_reminders,
    pending_reminders,
)
from workflow_os.approval.sequential import SequentialApprovalWorkflow
from workflow_os.approval.single import (
    ApprovalError,
    SingleApproverWorkflow,
)
from workflow_os.approval.sqlite_store import SQLiteApprovalStore
from workflow_os.approval.states import (
    ACTIVE_STATES,
    TERMINAL_STATES,
    ApprovalState,
    is_active,
    is_terminal,
    record_response,
    set_state,
)
from workflow_os.approval.store import (
    ApprovalList,
    ApprovalNotFoundError,
    ApprovalQuery,
    ApprovalStore,
    InMemoryApprovalStore,
    apply_query,
    matches,
)
from workflow_os.approval.timeout import (
    deadline,
    expire,
    expire_if_overdue,
    expire_overdue,
    find_overdue,
    is_overdue,
)

__all__ = [
    "ACTIVE_STATES",
    "TERMINAL_STATES",
    "ApprovalAuditEvent",
    "ApprovalAuditLog",
    "ApprovalError",
    "ApprovalEventType",
    "ApprovalList",
    "ApprovalNotFoundError",
    "ApprovalPolicy",
    "ApprovalQuery",
    "ApprovalRequest",
    "ApprovalState",
    "ApprovalStore",
    "BottleneckReport",
    "DelegationEvent",
    "EscalationEvent",
    "EscalationRule",
    "InMemoryApprovalStore",
    "MultiApproverWorkflow",
    "ParallelApprovalWorkflow",
    "PolicyType",
    "Reminder",
    "ReminderKind",
    "SQLiteApprovalStore",
    "SequentialApprovalWorkflow",
    "SingleApproverWorkflow",
    "WorkloadMetrics",
    "active_delegations",
    "actor_approvals",
    "aggregate_state",
    "analyze_bottlenecks",
    "apply_query",
    "approvals_by_actor",
    "average_response_time",
    "completed_approvals",
    "compute_workload_metrics",
    "deadline",
    "delegate",
    "delegation_history",
    "escalate",
    "escalate_if_overdue",
    "escalation_history",
    "escalation_hotspots",
    "expire",
    "expire_if_overdue",
    "expire_overdue",
    "find_overdue",
    "generate_reminders",
    "is_active",
    "is_overdue",
    "is_terminal",
    "matches",
    "new_approval_id",
    "new_policy_id",
    "overdue_count",
    "overdue_reminders",
    "pending_approvals",
    "pending_count",
    "pending_reminders",
    "record_response",
    "requester_approvals",
    "response_times",
    "run_demo",
    "set_state",
    "should_escalate",
    "slowest_approvers",
    "utcnow",
    "workflow_approvals",
    "workflow_bottlenecks",
]
