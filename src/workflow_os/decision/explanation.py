"""Human-readable explanations of decisions.

An explanation answers three questions about a decision: what happened, why it
happened, and how it turned out. :func:`explain_decision` returns a structured
:class:`DecisionExplanation`; :func:`explain_decision_text` renders it as text.
"""

from __future__ import annotations

from dataclasses import dataclass

from workflow_os.decision.record import DecisionRecord


@dataclass
class DecisionExplanation:
    """A structured, human-readable explanation of a decision."""

    what_happened: str
    why: str
    outcome: str

    def as_text(self) -> str:
        """Render the explanation as a multi-line string."""
        return (
            f"What happened: {self.what_happened}\n"
            f"Why: {self.why}\n"
            f"Outcome: {self.outcome}"
        )


def explain_decision(record: DecisionRecord) -> DecisionExplanation:
    """Return a human-readable explanation of a single decision."""
    actor = record.actor or "an unspecified actor"
    scope = f"step {record.step_id!r}" if record.step_id else "the workflow"
    what_happened = (
        f"{actor} made a {record.decision_type} on {scope} "
        f"of workflow {record.workflow_id!r}: {record.decision}"
    )

    if record.rationale:
        why = record.rationale
    else:
        why = "no rationale was recorded"
    if record.alternatives:
        considered = ", ".join(record.alternatives)
        why = f"{why} (alternatives considered: {considered})"

    outcome = f"the decision is {record.outcome}"

    return DecisionExplanation(
        what_happened=what_happened, why=why, outcome=outcome
    )


def explain_decision_text(record: DecisionRecord) -> str:
    """Return the rendered text explanation of a single decision."""
    return explain_decision(record).as_text()
