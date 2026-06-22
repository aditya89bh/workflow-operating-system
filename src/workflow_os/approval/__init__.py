"""Approval and governance for the workflow operating system.

This subpackage models approval requests, policies, and approval workflows
(single, multi, sequential, parallel), together with timeouts, escalation,
delegation, auditing, and analytics. It builds on the workflow, memory,
decision, and SOP layers without modifying them, and is fully deterministic and
rule-based.
"""

from workflow_os.approval.multi import MultiApproverWorkflow, aggregate_state
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

__all__ = [
    "ACTIVE_STATES",
    "TERMINAL_STATES",
    "ApprovalError",
    "ApprovalList",
    "ApprovalNotFoundError",
    "ApprovalPolicy",
    "ApprovalQuery",
    "ApprovalRequest",
    "ApprovalState",
    "ApprovalStore",
    "InMemoryApprovalStore",
    "MultiApproverWorkflow",
    "PolicyType",
    "SQLiteApprovalStore",
    "SingleApproverWorkflow",
    "aggregate_state",
    "apply_query",
    "is_active",
    "is_terminal",
    "matches",
    "new_approval_id",
    "new_policy_id",
    "record_response",
    "set_state",
    "utcnow",
]
