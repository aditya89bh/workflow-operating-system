"""Single-approver workflow.

The simplest approval workflow: one approver either approves or rejects the
request. Approving moves the request to ``approved``; rejecting moves it to
``rejected``.
"""

from __future__ import annotations

from workflow_os.approval.record import ApprovalRequest
from workflow_os.approval.states import (
    ApprovalState,
    is_terminal,
    record_response,
    set_state,
)


class ApprovalError(ValueError):
    """Raised when an approval action is invalid."""


def _require_open(request: ApprovalRequest) -> None:
    if is_terminal(request.state):
        raise ApprovalError(
            f"request {request.approval_id} is already {request.state}"
        )


def _require_approver(request: ApprovalRequest, approver: str) -> None:
    if approver not in request.approvers:
        raise ApprovalError(
            f"{approver!r} is not an approver of request {request.approval_id}"
        )


class SingleApproverWorkflow:
    """Drive a request that requires exactly one approver's decision."""

    def __init__(self, request: ApprovalRequest) -> None:
        if len(request.approvers) != 1:
            raise ApprovalError("single-approver workflow needs exactly one approver")
        self.request = request

    @property
    def approver(self) -> str:
        return self.request.approvers[0]

    def approve(self, approver: str | None = None) -> ApprovalRequest:
        """Approve the request on behalf of its single approver."""
        return approve(self.request, approver or self.approver)

    def reject(self, approver: str | None = None) -> ApprovalRequest:
        """Reject the request on behalf of its single approver."""
        return reject(self.request, approver or self.approver)


def approve(request: ApprovalRequest, approver: str) -> ApprovalRequest:
    """Record an approval and mark the request approved."""
    _require_open(request)
    _require_approver(request, approver)
    record_response(request, approver, ApprovalState.APPROVED.value)
    return set_state(request, ApprovalState.APPROVED.value)


def reject(request: ApprovalRequest, approver: str) -> ApprovalRequest:
    """Record a rejection and mark the request rejected."""
    _require_open(request)
    _require_approver(request, approver)
    record_response(request, approver, ApprovalState.REJECTED.value)
    return set_state(request, ApprovalState.REJECTED.value)
