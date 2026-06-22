"""Sequential approval workflow.

Approvers act in a fixed order, for example::

    Requester -> Manager -> Finance -> Operations

Each approver can only act when it is their turn (all earlier approvers have
approved). A rejection at any stage rejects the whole request; approval by the
final approver approves it.
"""

from __future__ import annotations

from workflow_os.approval.record import ApprovalRequest
from workflow_os.approval.single import ApprovalError, _require_open
from workflow_os.approval.states import ApprovalState, record_response, set_state


class SequentialApprovalWorkflow:
    """Drive a request through an ordered chain of approvers."""

    def __init__(
        self, request: ApprovalRequest, order: list[str] | None = None
    ) -> None:
        self.request = request
        self.order = list(order) if order is not None else list(request.approvers)
        if not self.order:
            raise ApprovalError("sequential workflow needs at least one approver")

    @property
    def current_approver(self) -> str | None:
        """Return the approver whose turn it is, or ``None`` if all approved."""
        for approver in self.order:
            if self.request.decisions.get(approver) != ApprovalState.APPROVED.value:
                return approver
        return None

    @property
    def pending_approvers(self) -> list[str]:
        """Return the approvers who have not yet approved, in order."""
        return [
            approver
            for approver in self.order
            if self.request.decisions.get(approver) != ApprovalState.APPROVED.value
        ]

    def approve(self, approver: str) -> ApprovalRequest:
        """Approve as the current approver and advance the chain."""
        self._require_turn(approver)
        record_response(self.request, approver, ApprovalState.APPROVED.value)
        if self.current_approver is None:
            return set_state(self.request, ApprovalState.APPROVED.value)
        return set_state(self.request, ApprovalState.PENDING.value)

    def reject(self, approver: str) -> ApprovalRequest:
        """Reject as the current approver, rejecting the whole request."""
        self._require_turn(approver)
        record_response(self.request, approver, ApprovalState.REJECTED.value)
        return set_state(self.request, ApprovalState.REJECTED.value)

    def _require_turn(self, approver: str) -> None:
        _require_open(self.request)
        if approver != self.current_approver:
            raise ApprovalError(
                f"it is not {approver!r}'s turn to act on "
                f"request {self.request.approval_id}"
            )
