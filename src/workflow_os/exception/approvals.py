"""Missing approval detection.

Detects approval requests that failed to produce an approval - those that were
rejected or expired, and optionally those still pending. Each one produces an
``approval_failure`` exception record. Builds on the Phase 5 approval layer
without modifying it.
"""

from __future__ import annotations

from collections.abc import Iterable

from workflow_os.approval.record import ApprovalRequest
from workflow_os.approval.states import ApprovalState
from workflow_os.exception.classification import ExceptionType
from workflow_os.exception.record import ExceptionRecord, utcnow
from workflow_os.exception.severity import ExceptionSeverity

_SOURCE = "approval-detector"

_FAILED_STATES = frozenset(
    {ApprovalState.REJECTED.value, ApprovalState.EXPIRED.value}
)


def _exception_for(request: ApprovalRequest) -> ExceptionRecord:
    return ExceptionRecord.create(
        workflow_id=request.workflow_id,
        step_id=request.step_id,
        exception_type=ExceptionType.APPROVAL_FAILURE.value,
        severity=ExceptionSeverity.HIGH.value,
        message=f"approval {request.approval_id!r} is {request.state}",
        source=_SOURCE,
        detected_at=utcnow(),
        metadata={"approval_id": request.approval_id, "state": request.state},
    )


def detect_missing_approvals(
    requests: Iterable[ApprovalRequest], include_pending: bool = False
) -> list[ExceptionRecord]:
    """Return ``approval_failure`` exceptions for approvals that did not succeed.

    Rejected and expired requests always count as failures. Pending requests are
    only flagged when ``include_pending`` is ``True``.
    """
    failed = set(_FAILED_STATES)
    if include_pending:
        failed = failed | {ApprovalState.PENDING.value}
    return [_exception_for(request) for request in requests if request.state in failed]
