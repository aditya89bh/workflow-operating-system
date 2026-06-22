"""Parallel approval workflow.

All approvers are asked at the same time and may respond in any order, for
example Manager, Finance, and Legal reviewing simultaneously. By default every
approver must approve; a single rejection rejects the request immediately.
"""

from __future__ import annotations

from workflow_os.approval.multi import aggregate_state
from workflow_os.approval.record import ApprovalRequest
from workflow_os.approval.single import _require_approver, _require_open
from workflow_os.approval.states import ApprovalState, record_response, set_state


class ParallelApprovalWorkflow:
    """Drive a request where approvers act concurrently and independently."""

    def __init__(
        self, request: ApprovalRequest, required_approvals: int | None = None
    ) -> None:
        self.request = request
        if required_approvals is None:
            required_approvals = len(request.approvers)
        self.required_approvals = max(1, required_approvals)

    @property
    def pending_approvers(self) -> list[str]:
        """Return approvers who have not yet recorded any decision."""
        return [a for a in self.request.approvers if a not in self.request.decisions]

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
