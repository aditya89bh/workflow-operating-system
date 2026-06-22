"""Organizational learning example datasets.

Small, deterministic datasets that illustrate distinct organizational states: a
successful organization, a struggling organization, and an organization on an
improvement journey. They are useful for tests, demos, and exploring the learning
APIs without wiring up the full stack.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from workflow_os.approval.record import ApprovalRequest
from workflow_os.exception.record import ExceptionRecord
from workflow_os.exception.recovery import RecoveryAction, RecoveryStatus
from workflow_os.memory.record import MemoryRecord
from workflow_os.sop.record import SOPRecord, SOPStatus


@dataclass
class OrganizationExample:
    """A bundle of recorded history describing one organization's state."""

    name: str
    records: list[MemoryRecord] = field(default_factory=list)
    sops: list[SOPRecord] = field(default_factory=list)
    exceptions: list[ExceptionRecord] = field(default_factory=list)
    approvals: list[ApprovalRequest] = field(default_factory=list)
    recoveries: list[RecoveryAction] = field(default_factory=list)


def _completed(workflow_id: str, count: int) -> list[MemoryRecord]:
    return [
        MemoryRecord.create(workflow_id=workflow_id, event_type="workflow_completed")
        for _ in range(count)
    ]


def _failed(workflow_id: str, count: int) -> list[MemoryRecord]:
    return [
        MemoryRecord.create(workflow_id=workflow_id, event_type="workflow_failed")
        for _ in range(count)
    ]


def successful_organization() -> OrganizationExample:
    """Return an organization with reliable, well-documented workflows."""
    records = _completed("onboarding", 5) + _completed("billing", 4)
    sops = [
        SOPRecord.create(
            title="Onboarding", workflow_type="onboarding", status=SOPStatus.ACTIVE.value
        ),
        SOPRecord.create(
            title="Billing", workflow_type="billing", status=SOPStatus.ACTIVE.value
        ),
    ]
    approvals = [
        ApprovalRequest.create(
            workflow_id="onboarding",
            requester="alice",
            title="Approve onboarding",
            approvers=["mgr"],
            state="approved",
        )
    ]
    recoveries = [
        RecoveryAction.create(
            exception_id="none", action="retry", status=RecoveryStatus.SUCCEEDED.value
        )
    ]
    return OrganizationExample(
        name="successful",
        records=records,
        sops=sops,
        approvals=approvals,
        recoveries=recoveries,
    )


def struggling_organization() -> OrganizationExample:
    """Return an organization with failing workflows and recurring exceptions."""
    records = (
        _failed("onboarding", 4)
        + _completed("onboarding", 1)
        + _failed("billing", 3)
        + [
            MemoryRecord.create(
                workflow_id="onboarding", event_type="step_failed", step_id="verify"
            )
            for _ in range(3)
        ]
    )
    exceptions = [
        ExceptionRecord.create(workflow_id="onboarding", exception_type="timeout")
        for _ in range(4)
    ]
    approvals = [
        ApprovalRequest.create(
            workflow_id="billing",
            requester="bob",
            title="Approve billing",
            approvers=["a", "b", "c", "d", "e"],
            state="pending",
        )
    ]
    recoveries = [
        RecoveryAction.create(
            exception_id=f"e{i}", action="manual_fix", status=RecoveryStatus.FAILED.value
        )
        for i in range(3)
    ]
    return OrganizationExample(
        name="struggling",
        records=records,
        exceptions=exceptions,
        approvals=approvals,
        recoveries=recoveries,
    )


def improvement_journey() -> OrganizationExample:
    """Return an organization that improved over time (failures, then successes)."""
    records = (
        _failed("deploy", 3)
        + _completed("deploy", 6)
        + _completed("review", 4)
    )
    sops = [
        SOPRecord.create(
            title="Deploy", workflow_type="deploy", status=SOPStatus.ACTIVE.value
        )
    ]
    exceptions = [
        ExceptionRecord.create(workflow_id="deploy", exception_type="timeout")
    ]
    recoveries = [
        RecoveryAction.create(
            exception_id="e1", action="retry", status=RecoveryStatus.SUCCEEDED.value
        )
    ]
    return OrganizationExample(
        name="improvement_journey",
        records=records,
        sops=sops,
        exceptions=exceptions,
        recoveries=recoveries,
    )


def all_examples() -> list[OrganizationExample]:
    """Return all built-in organization examples."""
    return [
        successful_organization(),
        struggling_organization(),
        improvement_journey(),
    ]
