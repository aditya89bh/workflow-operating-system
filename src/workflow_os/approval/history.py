"""Approval history retrieval.

Convenience queries over an :class:`~workflow_os.approval.store.ApprovalStore`
for common questions: which approvals belong to a workflow or actor, which are
still pending, and which have completed.
"""

from __future__ import annotations

from workflow_os.approval.states import ApprovalState, is_terminal
from workflow_os.approval.store import ApprovalList, ApprovalQuery, ApprovalStore


def workflow_approvals(store: ApprovalStore, workflow_id: str) -> ApprovalList:
    """Return all approval requests for a workflow."""
    return store.query(ApprovalQuery(workflow_id=workflow_id))


def actor_approvals(store: ApprovalStore, actor: str) -> ApprovalList:
    """Return all requests where ``actor`` is one of the approvers."""
    return store.query(ApprovalQuery(approver=actor))


def requester_approvals(store: ApprovalStore, requester: str) -> ApprovalList:
    """Return all requests raised by ``requester``."""
    return store.query(ApprovalQuery(requester=requester))


def pending_approvals(store: ApprovalStore) -> ApprovalList:
    """Return all requests still awaiting a decision."""
    return store.query(ApprovalQuery(states=(ApprovalState.PENDING.value,)))


def completed_approvals(store: ApprovalStore) -> ApprovalList:
    """Return all requests in a terminal state, ordered by ``created_at``."""
    return [request for request in store.list() if is_terminal(request.state)]
