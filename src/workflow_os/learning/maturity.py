"""Organizational maturity scoring.

Combines several deterministic signals - workflow health, documentation coverage,
exception rate, approval efficiency, and recovery effectiveness - into a single
maturity score in ``[0.0, 1.0]`` plus a named maturity level. Each component is a
simple, explainable ratio; only the components with data contribute to the
overall score.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field

from workflow_os.approval.record import ApprovalRequest
from workflow_os.approval.states import ApprovalState
from workflow_os.exception.record import ExceptionRecord
from workflow_os.exception.recovery import RecoveryAction, RecoveryStatus
from workflow_os.learning.patterns import workflow_run_stats
from workflow_os.memory.record import MemoryRecord
from workflow_os.sop.record import SOPRecord, SOPStatus

_MATURITY_LEVELS = (
    (0.4, "initial"),
    (0.6, "developing"),
    (0.8, "defined"),
    (0.95, "managed"),
)


def maturity_level(score: float) -> str:
    """Return the named maturity level for a numeric ``score``."""
    for threshold, name in _MATURITY_LEVELS:
        if score < threshold:
            return name
    return "optimizing"


@dataclass
class MaturityScore:
    """A composite organizational maturity score and its components.

    Attributes:
        overall: Mean of the populated component scores, in ``[0.0, 1.0]``.
        level: Named maturity level derived from ``overall``.
        components: Per-dimension scores that contributed to ``overall``.
    """

    overall: float
    level: str
    components: dict[str, float] = field(default_factory=dict)


def _workflow_health(records: list[MemoryRecord]) -> float | None:
    stats = workflow_run_stats(records)
    total_runs = sum(s.runs for s in stats.values())
    if total_runs == 0:
        return None
    successes = sum(s.successes for s in stats.values())
    return successes / total_runs


def _documentation_coverage(
    records: list[MemoryRecord], sops: list[SOPRecord]
) -> float | None:
    observed = {r.workflow_id for r in records}
    if not observed:
        return None
    documented = {
        sop.workflow_type for sop in sops if sop.status == SOPStatus.ACTIVE.value
    }
    covered = sum(1 for workflow_id in observed if workflow_id in documented)
    return covered / len(observed)


def _exception_health(
    records: list[MemoryRecord], exceptions: list[ExceptionRecord]
) -> float | None:
    stats = workflow_run_stats(records)
    total_runs = sum(s.runs for s in stats.values())
    if total_runs == 0:
        return None
    rate = len(exceptions) / total_runs
    return max(0.0, 1.0 - rate)


def _approval_efficiency(approvals: list[ApprovalRequest]) -> float | None:
    if not approvals:
        return None
    approved = sum(1 for a in approvals if a.state == ApprovalState.APPROVED.value)
    return approved / len(approvals)


def _recovery_effectiveness(recoveries: list[RecoveryAction]) -> float | None:
    if not recoveries:
        return None
    succeeded = sum(
        1 for r in recoveries if r.status == RecoveryStatus.SUCCEEDED.value
    )
    return succeeded / len(recoveries)


def organizational_maturity_score(
    records: Iterable[MemoryRecord] | None = None,
    *,
    sops: Iterable[SOPRecord] | None = None,
    exceptions: Iterable[ExceptionRecord] | None = None,
    approvals: Iterable[ApprovalRequest] | None = None,
    recoveries: Iterable[RecoveryAction] | None = None,
) -> MaturityScore:
    """Return a deterministic organizational maturity score."""
    record_list = list(records or [])
    sop_list = list(sops or [])
    exception_list = list(exceptions or [])
    approval_list = list(approvals or [])
    recovery_list = list(recoveries or [])

    candidates = {
        "workflow_health": _workflow_health(record_list),
        "documentation_coverage": _documentation_coverage(record_list, sop_list),
        "exception_health": _exception_health(record_list, exception_list),
        "approval_efficiency": _approval_efficiency(approval_list),
        "recovery_effectiveness": _recovery_effectiveness(recovery_list),
    }
    components = {name: value for name, value in candidates.items() if value is not None}
    overall = sum(components.values()) / len(components) if components else 0.0
    return MaturityScore(
        overall=overall,
        level=maturity_level(overall),
        components=components,
    )
