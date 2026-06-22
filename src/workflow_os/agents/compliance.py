"""Compliance agent.

The compliance agent is a deterministic service object that checks governance
rules: that policies hold, that approvals were granted, and that the SOPs in play
are active. Each check returns a structured, rule-based result. It builds on the
Phase 4 SOP and Phase 5 approval layers.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field

from workflow_os.agents.record import Agent
from workflow_os.approval.record import ApprovalRequest
from workflow_os.approval.states import ApprovalState
from workflow_os.sop.record import SOPRecord, SOPStatus


@dataclass
class ComplianceResult:
    """The outcome of a compliance check."""

    compliant: bool = True
    reasons: list[str] = field(default_factory=list)


class ComplianceAgent:
    """Verifies policies, approvals, and SOP compliance deterministically."""

    def __init__(self, agent: Agent | None = None) -> None:
        self.agent = agent

    def verify_policies(self, checks: Mapping[str, bool]) -> ComplianceResult:
        """Return a result that is compliant only if every policy check passes."""
        reasons = [name for name, passed in checks.items() if not passed]
        return ComplianceResult(compliant=not reasons, reasons=reasons)

    def verify_approvals(
        self, approvals: Iterable[ApprovalRequest]
    ) -> ComplianceResult:
        """Return a result that is compliant only if every approval is approved."""
        reasons = [
            f"approval {request.approval_id!r} is {request.state}"
            for request in approvals
            if request.state != ApprovalState.APPROVED.value
        ]
        return ComplianceResult(compliant=not reasons, reasons=reasons)

    def validate_sop_compliance(
        self, sops: Iterable[SOPRecord]
    ) -> ComplianceResult:
        """Return a result that is compliant only if every SOP is active."""
        reasons = [
            f"SOP {sop.sop_id!r} is {sop.status}"
            for sop in sops
            if sop.status != SOPStatus.ACTIVE.value
        ]
        return ComplianceResult(compliant=not reasons, reasons=reasons)
