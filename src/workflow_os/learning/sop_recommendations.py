"""SOP update recommendations.

Compares the SOP catalogue against observed exceptions and produces deterministic
suggestions: refresh SOPs that are no longer active, revise exception handling for
documented workflows that keep failing, and add missing guidance for workflows
that suffer recurring exceptions but have no SOP. Workflows are linked to SOPs by
shared identifier (``workflow_type``).
"""

from __future__ import annotations

from collections.abc import Iterable

from workflow_os.exception.record import ExceptionRecord
from workflow_os.learning.recommendation import Recommendation
from workflow_os.sop.record import SOPRecord, SOPStatus


def _exception_counts(exceptions: Iterable[ExceptionRecord]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for exc in exceptions:
        counts[exc.workflow_id] = counts.get(exc.workflow_id, 0) + 1
    return counts


def sop_update_recommendations(
    sops: Iterable[SOPRecord],
    *,
    exceptions: Iterable[ExceptionRecord] | None = None,
    min_exception_occurrences: int = 2,
) -> list[Recommendation]:
    """Return deterministic SOP update recommendations."""
    sop_list = list(sops)
    counts = _exception_counts(exceptions or [])
    covered = {sop.workflow_type for sop in sop_list}
    recommendations: list[Recommendation] = []

    for sop in sop_list:
        if sop.status != SOPStatus.ACTIVE.value:
            recommendations.append(
                Recommendation.create(
                    category="sop",
                    title=f"update outdated SOP {sop.sop_id}",
                    description=(
                        f"SOP {sop.title!r} for {sop.workflow_type!r} is "
                        f"{sop.status!r}; review and reactivate it."
                    ),
                    severity="medium",
                    confidence=1.0,
                    metadata={"sop_id": sop.sop_id, "action": "update_outdated"},
                )
            )

    chronic = {
        workflow_type
        for workflow_type, count in counts.items()
        if count >= min_exception_occurrences
    }

    for workflow_type in sorted(chronic & covered):
        recommendations.append(
            Recommendation.create(
                category="sop",
                title=f"revise exception handling for {workflow_type}",
                description=(
                    f"{workflow_type} had {counts[workflow_type]} exceptions; "
                    "revise its SOP's exception handling guidance."
                ),
                severity="high",
                confidence=1.0,
                metadata={"workflow_type": workflow_type, "action": "revise_exceptions"},
            )
        )

    for workflow_type in sorted(chronic - covered):
        recommendations.append(
            Recommendation.create(
                category="sop",
                title=f"add missing guidance for {workflow_type}",
                description=(
                    f"{workflow_type} had {counts[workflow_type]} exceptions but "
                    "has no SOP; add documented guidance."
                ),
                severity="high",
                confidence=1.0,
                metadata={"workflow_type": workflow_type, "action": "add_missing"},
            )
        )

    return recommendations
