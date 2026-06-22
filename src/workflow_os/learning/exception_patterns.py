"""Recurring exception detection.

Looks across recorded exceptions and recovery actions for chronic problems:
exception signatures that repeat, workflows that suffer many exceptions, and
recovery actions that are applied over and over. Findings are surfaced as
deterministic insights. This builds on the Phase 6 exception layer.
"""

from __future__ import annotations

from collections.abc import Iterable

from workflow_os.exception.record import ExceptionRecord
from workflow_os.exception.recovery import RecoveryAction
from workflow_os.learning.insight import OrganizationalInsight
from workflow_os.learning.patterns import recurring_exceptions


def repeated_exceptions(
    exceptions: Iterable[ExceptionRecord], *, min_occurrences: int = 2
) -> dict[str, int]:
    """Return exception signatures that repeat at least ``min_occurrences`` times."""
    return recurring_exceptions(exceptions, min_occurrences=min_occurrences)


def chronic_workflow_problems(
    exceptions: Iterable[ExceptionRecord], *, min_occurrences: int = 3
) -> list[str]:
    """Return ids of workflows with at least ``min_occurrences`` exceptions."""
    counts: dict[str, int] = {}
    for exc in exceptions:
        counts[exc.workflow_id] = counts.get(exc.workflow_id, 0) + 1
    chronic = [wid for wid, count in counts.items() if count >= min_occurrences]
    return sorted(chronic, key=lambda wid: (-counts[wid], wid))


def recurring_recovery_actions(
    actions: Iterable[RecoveryAction], *, min_occurrences: int = 2
) -> dict[str, int]:
    """Return recovery action names applied at least ``min_occurrences`` times."""
    counts: dict[str, int] = {}
    for action in actions:
        counts[action.action] = counts.get(action.action, 0) + 1
    return {
        name: count
        for name, count in sorted(counts.items())
        if count >= min_occurrences
    }


def recurring_exception_insights(
    exceptions: Iterable[ExceptionRecord], *, min_occurrences: int = 2
) -> list[OrganizationalInsight]:
    """Return insights describing recurring exception signatures."""
    insights: list[OrganizationalInsight] = []
    for signature, count in repeated_exceptions(
        exceptions, min_occurrences=min_occurrences
    ).items():
        workflow_id, _, exception_type = signature.partition(":")
        insights.append(
            OrganizationalInsight.create(
                category="exception",
                title=f"recurring {exception_type} in {workflow_id}",
                description=(
                    f"{exception_type!r} occurred {count} times in {workflow_id}."
                ),
                evidence=[f"signature={signature}", f"count={count}"],
                confidence=1.0,
                metadata={"workflow_id": workflow_id, "exception_type": exception_type},
            )
        )
    return insights
