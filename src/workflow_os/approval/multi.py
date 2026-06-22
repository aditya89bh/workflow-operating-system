"""Multi-approver workflow.

Several approvers each record a decision. The request is approved once the
number of approvals reaches a configurable threshold, and rejected as soon as
enough approvers reject that the threshold can no longer be reached.
"""

from __future__ import annotations

from workflow_os.approval.record import ApprovalRequest
from workflow_os.approval.single import _require_approver, _require_open
from workflow_os.approval.states import ApprovalState, record_response, set_state


def _count(request: ApprovalRequest, state: str) -> int:
    return sum(1 for value in request.decisions.values() if value == state)


def aggregate_state(request: ApprovalRequest, required_approvals: int) -> str:
    """Return the state implied by the decisions recorded so far.

    Returns ``approved`` once ``required_approvals`` approvals exist, ``rejected``
    once the remaining approvers cannot reach the threshold, and ``pending``
    otherwise.
    """
    approvals = _count(request, ApprovalState.APPROVED.value)
    rejections = _count(request, ApprovalState.REJECTED.value)
    if approvals >= required_approvals:
        return ApprovalState.APPROVED.value
    reachable = len(request.approvers) - rejections
    if reachable < required_approvals:
        return ApprovalState.REJECTED.value
    return ApprovalState.PENDING.value


class MultiApproverWorkflow:
    """Drive a request approved by a threshold of multiple approvers."""

    def __init__(
        self, request: ApprovalRequest, required_approvals: int | None = None
    ) -> None:
        self.request = request
        if required_approvals is None:
            required_approvals = len(request.approvers)
        self.required_approvals = max(1, required_approvals)

    def approve(self, approver: str) -> ApprovalRequest:
        """Record an approval from ``approver`` and re-evaluate the state."""
        return self._respond(approver, ApprovalState.APPROVED.value)

    def reject(self, approver: str) -> ApprovalRequest:
        """Record a rejection from ``approver`` and re-evaluate the state."""
        return self._respond(approver, ApprovalState.REJECTED.value)

    def evaluate(self) -> str:
        """Return the aggregate state without mutating the request."""
        return aggregate_state(self.request, self.required_approvals)

    def _respond(self, approver: str, decision: str) -> ApprovalRequest:
        _require_open(self.request)
        _require_approver(self.request, approver)
        record_response(self.request, approver, decision)
        return set_state(self.request, self.evaluate())
