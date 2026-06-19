"""Record memory events for workflow lifecycle operations.

:class:`MemoryRecorder` wraps a :class:`~workflow_os.memory.store.MemoryStore`
and the Phase 1 lifecycle operations so that every state change automatically
produces a :class:`~workflow_os.memory.record.MemoryRecord`. The underlying
workflow operations are reused unchanged, preserving backward compatibility.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from workflow_os.executor import WorkflowExecutor
from workflow_os.memory.actors import step_actor, workflow_owner
from workflow_os.memory.confidence import confidence_for
from workflow_os.memory.events import MemoryEventType
from workflow_os.memory.record import MemoryRecord, utcnow
from workflow_os.memory.store import MemoryStore
from workflow_os.operations import (
    complete_workflow,
    pause_workflow,
    resume_workflow,
    start_workflow,
)
from workflow_os.status import WorkflowStatus
from workflow_os.step import WorkflowStep
from workflow_os.transitions import StepStatus, transition_step
from workflow_os.workflow import Workflow


class MemoryRecorder:
    """Performs workflow operations while recording memory events."""

    def __init__(self, store: MemoryStore) -> None:
        self.store = store
        self._workflow_started_at: dict[str, datetime] = {}
        self._step_started_at: dict[tuple[str, str], datetime] = {}

    def _workflow_duration(self, workflow_id: str) -> float | None:
        start = self._workflow_started_at.get(workflow_id)
        if start is None:
            return None
        return (utcnow() - start).total_seconds()

    def _step_duration(self, workflow_id: str, step_id: str) -> float | None:
        start = self._step_started_at.get((workflow_id, step_id))
        if start is None:
            return None
        return (utcnow() - start).total_seconds()

    @staticmethod
    def _with_duration(
        metadata: dict[str, Any] | None, duration: float | None
    ) -> dict[str, Any] | None:
        if duration is None:
            return metadata
        result = dict(metadata or {})
        result["duration_seconds"] = duration
        return result

    def _emit(
        self,
        workflow: Workflow,
        event_type: MemoryEventType,
        *,
        step_id: str | None = None,
        actor: str | None = None,
        confidence: float | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> MemoryRecord:
        resolved_confidence = (
            confidence if confidence is not None else confidence_for(str(event_type))
        )
        record = MemoryRecord.create(
            workflow_id=workflow.id,
            event_type=str(event_type),
            step_id=step_id,
            actor=actor,
            confidence=resolved_confidence,
            metadata=metadata,
        )
        self.store.add(record)
        return record

    def record_workflow_started(self, workflow: Workflow) -> MemoryRecord:
        record = self._emit(
            workflow, MemoryEventType.WORKFLOW_STARTED, actor=workflow_owner(workflow)
        )
        self._workflow_started_at[workflow.id] = record.timestamp
        return record

    def record_workflow_paused(self, workflow: Workflow) -> MemoryRecord:
        return self._emit(
            workflow, MemoryEventType.WORKFLOW_PAUSED, actor=workflow_owner(workflow)
        )

    def record_workflow_resumed(self, workflow: Workflow) -> MemoryRecord:
        return self._emit(
            workflow, MemoryEventType.WORKFLOW_RESUMED, actor=workflow_owner(workflow)
        )

    def record_workflow_completed(self, workflow: Workflow) -> MemoryRecord:
        metadata = self._with_duration(None, self._workflow_duration(workflow.id))
        return self._emit(
            workflow,
            MemoryEventType.WORKFLOW_COMPLETED,
            actor=workflow_owner(workflow),
            metadata=metadata,
        )

    def record_workflow_failed(
        self, workflow: Workflow, *, reason: str | None = None
    ) -> MemoryRecord:
        metadata: dict[str, Any] | None = {"reason": reason} if reason else None
        metadata = self._with_duration(metadata, self._workflow_duration(workflow.id))
        return self._emit(
            workflow,
            MemoryEventType.WORKFLOW_FAILED,
            actor=workflow_owner(workflow),
            metadata=metadata,
        )

    def start(self, workflow: Workflow) -> Workflow:
        """Start a workflow and record a ``workflow_started`` event."""
        start_workflow(workflow)
        self.record_workflow_started(workflow)
        return workflow

    def pause(self, workflow: Workflow) -> Workflow:
        """Pause a workflow and record a ``workflow_paused`` event."""
        pause_workflow(workflow)
        self.record_workflow_paused(workflow)
        return workflow

    def resume(self, workflow: Workflow) -> Workflow:
        """Resume a workflow and record a ``workflow_resumed`` event."""
        resume_workflow(workflow)
        self.record_workflow_resumed(workflow)
        return workflow

    def complete(self, workflow: Workflow) -> Workflow:
        """Complete a workflow and record a ``workflow_completed`` event."""
        complete_workflow(workflow)
        self.record_workflow_completed(workflow)
        return workflow

    def fail(self, workflow: Workflow, *, reason: str | None = None) -> Workflow:
        """Mark a workflow failed and record a ``workflow_failed`` event."""
        workflow.status = WorkflowStatus.FAILED
        self.record_workflow_failed(workflow, reason=reason)
        return workflow

    def record_step_started(
        self, workflow: Workflow, step: WorkflowStep
    ) -> MemoryRecord:
        record = self._emit(
            workflow,
            MemoryEventType.STEP_STARTED,
            step_id=step.id,
            actor=step_actor(workflow, step),
        )
        self._step_started_at[(workflow.id, step.id)] = record.timestamp
        return record

    def record_step_completed(
        self, workflow: Workflow, step: WorkflowStep
    ) -> MemoryRecord:
        metadata = self._with_duration(
            None, self._step_duration(workflow.id, step.id)
        )
        return self._emit(
            workflow,
            MemoryEventType.STEP_COMPLETED,
            step_id=step.id,
            actor=step_actor(workflow, step),
            metadata=metadata,
        )

    def record_step_failed(
        self, workflow: Workflow, step: WorkflowStep, *, reason: str | None = None
    ) -> MemoryRecord:
        metadata: dict[str, Any] | None = {"reason": reason} if reason else None
        metadata = self._with_duration(
            metadata, self._step_duration(workflow.id, step.id)
        )
        return self._emit(
            workflow,
            MemoryEventType.STEP_FAILED,
            step_id=step.id,
            actor=step_actor(workflow, step),
            metadata=metadata,
        )

    def record_step_skipped(
        self, workflow: Workflow, step: WorkflowStep
    ) -> MemoryRecord:
        return self._emit(
            workflow,
            MemoryEventType.STEP_SKIPPED,
            step_id=step.id,
            actor=step_actor(workflow, step),
        )

    def start_step(self, workflow: Workflow, step: WorkflowStep) -> MemoryRecord:
        """Transition a step to running and record a ``step_started`` event."""
        transition_step(step, StepStatus.RUNNING)
        return self.record_step_started(workflow, step)

    def complete_step(self, workflow: Workflow, step: WorkflowStep) -> MemoryRecord:
        """Transition a step to completed and record a ``step_completed`` event."""
        transition_step(step, StepStatus.COMPLETED)
        return self.record_step_completed(workflow, step)

    def fail_step(
        self, workflow: Workflow, step: WorkflowStep, *, reason: str | None = None
    ) -> MemoryRecord:
        """Transition a step to failed and record a ``step_failed`` event."""
        transition_step(step, StepStatus.FAILED)
        return self.record_step_failed(workflow, step, reason=reason)

    def skip_step(self, workflow: Workflow, step: WorkflowStep) -> MemoryRecord:
        """Transition a step to skipped and record a ``step_skipped`` event."""
        transition_step(step, StepStatus.SKIPPED)
        return self.record_step_skipped(workflow, step)

    def run(self, workflow: Workflow) -> Workflow:
        """Run a workflow end to end, recording workflow and step events."""
        order = WorkflowExecutor(workflow).execution_order()
        self.start(workflow)
        for step in order:
            self.start_step(workflow, step)
            self.complete_step(workflow, step)
        self.complete(workflow)
        return workflow
