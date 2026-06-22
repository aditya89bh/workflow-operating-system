"""Approval and governance for the workflow operating system.

This subpackage models approval requests, policies, and approval workflows
(single, multi, sequential, parallel), together with timeouts, escalation,
delegation, auditing, and analytics. It builds on the workflow, memory,
decision, and SOP layers without modifying them, and is fully deterministic and
rule-based.
"""

from workflow_os.approval.record import (
    ApprovalRequest,
    new_approval_id,
    utcnow,
)

__all__ = [
    "ApprovalRequest",
    "new_approval_id",
    "utcnow",
]
