"""Decision recording APIs.

:class:`DecisionRecorder` wraps a :class:`~workflow_os.decision.store.DecisionStore`
and provides convenient methods for capturing decisions and updating their
outcomes after the fact.
"""

from __future__ import annotations

from typing import Any

from workflow_os.decision.outcome import normalize_outcome
from workflow_os.decision.record import DecisionRecord
from workflow_os.decision.store import DecisionStore
from workflow_os.decision.types import DecisionType
from workflow_os.memory.actors import step_actor, workflow_owner
from workflow_os.step import WorkflowStep
from workflow_os.workflow import Workflow


class DecisionRecorder:
    """Capture decisions into a decision store."""

    def __init__(self, store: DecisionStore) -> None:
        self.store = store

    def record_decision(
        self,
        *,
        workflow_id: str,
        decision: str,
        decision_type: str = DecisionType.MANUAL_DECISION.value,
        rationale: str = "",
        alternatives: list[str] | None = None,
        step_id: str | None = None,
        actor: str | None = None,
        outcome: str = "pending",
        confidence: float = 1.0,
        metadata: dict[str, Any] | None = None,
    ) -> DecisionRecord:
        """Capture a decision and persist it, returning the stored record."""
        record = DecisionRecord.create(
            workflow_id=workflow_id,
            decision_type=str(decision_type),
            decision=decision,
            rationale=rationale,
            alternatives=alternatives,
            step_id=step_id,
            actor=actor,
            outcome=normalize_outcome(outcome),
            confidence=confidence,
            metadata=metadata,
        )
        self.store.add(record)
        return record

    def record_workflow_decision(
        self,
        workflow: Workflow,
        decision: str,
        *,
        rationale: str = "",
        alternatives: list[str] | None = None,
        actor: str | None = None,
        outcome: str = "pending",
        confidence: float = 1.0,
        metadata: dict[str, Any] | None = None,
    ) -> DecisionRecord:
        """Record a decision associated with an entire workflow.

        The actor defaults to the workflow owner when one is not supplied.
        """
        return self.record_decision(
            workflow_id=workflow.id,
            decision=decision,
            decision_type=DecisionType.WORKFLOW_DECISION.value,
            rationale=rationale,
            alternatives=alternatives,
            actor=actor if actor is not None else workflow_owner(workflow),
            outcome=outcome,
            confidence=confidence,
            metadata=metadata,
        )

    def record_step_decision(
        self,
        workflow: Workflow,
        step: WorkflowStep,
        decision: str,
        *,
        rationale: str = "",
        alternatives: list[str] | None = None,
        actor: str | None = None,
        outcome: str = "pending",
        confidence: float = 1.0,
        metadata: dict[str, Any] | None = None,
    ) -> DecisionRecord:
        """Record a decision associated with a specific workflow step.

        The actor defaults to the step assignee (or the workflow owner) when one
        is not supplied.
        """
        return self.record_decision(
            workflow_id=workflow.id,
            decision=decision,
            decision_type=DecisionType.STEP_DECISION.value,
            rationale=rationale,
            alternatives=alternatives,
            step_id=step.id,
            actor=actor if actor is not None else step_actor(workflow, step),
            outcome=outcome,
            confidence=confidence,
            metadata=metadata,
        )

    def record_exception_decision(
        self,
        workflow: Workflow,
        decision: str,
        *,
        step: WorkflowStep | None = None,
        reason: str | None = None,
        rationale: str = "",
        alternatives: list[str] | None = None,
        actor: str | None = None,
        outcome: str = "pending",
        confidence: float = 1.0,
        metadata: dict[str, Any] | None = None,
    ) -> DecisionRecord:
        """Record a decision taken during a failure or recovery.

        When ``reason`` is supplied it is stored under ``metadata["reason"]``.
        The actor defaults to the step assignee (if a step is given) or the
        workflow owner.
        """
        combined: dict[str, Any] = dict(metadata or {})
        if reason is not None:
            combined["reason"] = reason
        if actor is not None:
            resolved_actor: str | None = actor
        elif step is not None:
            resolved_actor = step_actor(workflow, step)
        else:
            resolved_actor = workflow_owner(workflow)
        return self.record_decision(
            workflow_id=workflow.id,
            decision=decision,
            decision_type=DecisionType.EXCEPTION_DECISION.value,
            rationale=rationale,
            alternatives=alternatives,
            step_id=step.id if step is not None else None,
            actor=resolved_actor,
            outcome=outcome,
            confidence=confidence,
            metadata=combined or None,
        )

    def update_decision_outcome(
        self,
        decision_id: str,
        outcome: str,
        *,
        metadata: dict[str, Any] | None = None,
    ) -> DecisionRecord:
        """Update the outcome (and optionally metadata) of a stored decision."""
        record = self.store.get(decision_id)
        record.outcome = normalize_outcome(outcome)
        if metadata:
            record.metadata.update(metadata)
        self.store.add(record)
        return record
