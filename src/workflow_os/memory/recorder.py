"""Record memory events for workflow lifecycle operations.

:class:`MemoryRecorder` wraps a :class:`~workflow_os.memory.store.MemoryStore`
and the Phase 1 lifecycle operations so that every state change automatically
produces a :class:`~workflow_os.memory.record.MemoryRecord`. The underlying
workflow operations are reused unchanged, preserving backward compatibility.
"""

from __future__ import annotations

from typing import Any

from workflow_os.memory.events import MemoryEventType
from workflow_os.memory.record import MemoryRecord
from workflow_os.memory.store import MemoryStore
from workflow_os.operations import (
    complete_workflow,
    pause_workflow,
    resume_workflow,
    start_workflow,
)
from workflow_os.status import WorkflowStatus
from workflow_os.workflow import Workflow


class MemoryRecorder:
    """Performs workflow operations while recording memory events."""

    def __init__(self, store: MemoryStore) -> None:
        self.store = store

    def _emit(
        self,
        workflow: Workflow,
        event_type: MemoryEventType,
        *,
        step_id: str | None = None,
        actor: str | None = None,
        confidence: float = 1.0,
        metadata: dict[str, Any] | None = None,
    ) -> MemoryRecord:
        record = MemoryRecord.create(
            workflow_id=workflow.id,
            event_type=str(event_type),
            step_id=step_id,
            actor=actor,
            confidence=confidence,
            metadata=metadata,
        )
        self.store.add(record)
        return record

    def record_workflow_started(self, workflow: Workflow) -> MemoryRecord:
        return self._emit(workflow, MemoryEventType.WORKFLOW_STARTED)

    def record_workflow_paused(self, workflow: Workflow) -> MemoryRecord:
        return self._emit(workflow, MemoryEventType.WORKFLOW_PAUSED)

    def record_workflow_resumed(self, workflow: Workflow) -> MemoryRecord:
        return self._emit(workflow, MemoryEventType.WORKFLOW_RESUMED)

    def record_workflow_completed(self, workflow: Workflow) -> MemoryRecord:
        return self._emit(workflow, MemoryEventType.WORKFLOW_COMPLETED)

    def record_workflow_failed(
        self, workflow: Workflow, *, reason: str | None = None
    ) -> MemoryRecord:
        metadata = {"reason": reason} if reason else None
        return self._emit(workflow, MemoryEventType.WORKFLOW_FAILED, metadata=metadata)

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
