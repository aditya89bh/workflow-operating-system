"""Performance scorecards.

Deterministic scorecards that condense activity into a single ``[0, 1]`` score
plus supporting figures. Scorecards are produced for workflows (did the run
succeed?), agents (how reliably do their steps complete?), and approvers (how
often do they approve?). Scores are computed by fixed rules - there is no
learning or weighting model.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field

from workflow_os.analytics.execution_summary import execution_summaries
from workflow_os.approval.record import ApprovalRequest
from workflow_os.approval.states import ApprovalState
from workflow_os.memory.events import MemoryEventType
from workflow_os.memory.record import MemoryRecord


@dataclass
class Scorecard:
    """A single subject's score and supporting metrics."""

    subject_id: str
    score: float
    metrics: dict[str, float] = field(default_factory=dict)


def workflow_scorecards(records: Iterable[MemoryRecord]) -> list[Scorecard]:
    """Return a scorecard per workflow (1.0 completed, 0.0 failed, 0.5 running)."""
    cards: list[Scorecard] = []
    for summary in execution_summaries(records):
        if summary.status == "completed":
            score = 1.0
        elif summary.status == "failed":
            score = 0.0
        else:
            score = 0.5
        cards.append(
            Scorecard(
                subject_id=summary.workflow_id,
                score=score,
                metrics={
                    "steps_completed": float(summary.steps_completed),
                    "steps_failed": float(summary.steps_failed),
                    "duration": float(summary.duration or 0.0),
                },
            )
        )
    return cards


def agent_scorecards(records: Iterable[MemoryRecord]) -> list[Scorecard]:
    """Return a scorecard per actor based on step success ratio."""
    completed: dict[str, int] = {}
    failed: dict[str, int] = {}
    for record in records:
        if record.actor is None:
            continue
        if record.event_type == str(MemoryEventType.STEP_COMPLETED):
            completed[record.actor] = completed.get(record.actor, 0) + 1
        elif record.event_type == str(MemoryEventType.STEP_FAILED):
            failed[record.actor] = failed.get(record.actor, 0) + 1

    actors = sorted(set(completed) | set(failed))
    cards: list[Scorecard] = []
    for actor in actors:
        done = completed.get(actor, 0)
        bad = failed.get(actor, 0)
        attempts = done + bad
        score = done / attempts if attempts else 0.0
        cards.append(
            Scorecard(
                subject_id=actor,
                score=score,
                metrics={
                    "steps_completed": float(done),
                    "steps_failed": float(bad),
                },
            )
        )
    return cards


def approval_scorecards(approvals: Iterable[ApprovalRequest]) -> list[Scorecard]:
    """Return a scorecard per approver based on how often they approve."""
    approved: dict[str, int] = {}
    decided: dict[str, int] = {}
    for request in approvals:
        for approver, decision in request.decisions.items():
            if decision in {
                ApprovalState.APPROVED.value,
                ApprovalState.REJECTED.value,
            }:
                decided[approver] = decided.get(approver, 0) + 1
                if decision == ApprovalState.APPROVED.value:
                    approved[approver] = approved.get(approver, 0) + 1

    cards: list[Scorecard] = []
    for approver in sorted(decided):
        total = decided[approver]
        yes = approved.get(approver, 0)
        cards.append(
            Scorecard(
                subject_id=approver,
                score=yes / total if total else 0.0,
                metrics={
                    "approved": float(yes),
                    "decided": float(total),
                },
            )
        )
    return cards
