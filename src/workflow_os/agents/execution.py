"""Execution agent.

The execution agent is a deterministic service object that runs assigned steps to
completion, reports step status, and emits execution events for auditing. It
reuses the Phase 1 step state machine.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

from workflow_os.agents.record import Agent
from workflow_os.step import WorkflowStep
from workflow_os.transitions import StepStatus, transition_step
from workflow_os.workflow import Workflow


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class ExecutionEvent:
    """An event emitted while executing a step."""

    workflow_id: str
    step_id: str
    status: str
    agent_id: str | None
    timestamp: datetime = field(default_factory=_utcnow)


class ExecutionAgent:
    """Executes assigned steps and emits execution events."""

    def __init__(self, agent: Agent | None = None) -> None:
        self.agent = agent
        self._events: list[ExecutionEvent] = []

    @property
    def agent_id(self) -> str | None:
        return self.agent.agent_id if self.agent is not None else None

    def _emit(self, workflow: Workflow, step: WorkflowStep, status: str) -> None:
        self._events.append(
            ExecutionEvent(
                workflow_id=workflow.id,
                step_id=step.id,
                status=status,
                agent_id=self.agent_id,
            )
        )

    def execute_task(self, workflow: Workflow, step: WorkflowStep) -> ExecutionEvent:
        """Run ``step`` to completion, emitting running then completed events."""
        transition_step(step, StepStatus.RUNNING)
        self._emit(workflow, step, StepStatus.RUNNING.value)
        transition_step(step, StepStatus.COMPLETED)
        self._emit(workflow, step, StepStatus.COMPLETED.value)
        return self._events[-1]

    def fail_task(self, workflow: Workflow, step: WorkflowStep) -> ExecutionEvent:
        """Move a running step to failed, emitting a failed event."""
        transition_step(step, StepStatus.FAILED)
        self._emit(workflow, step, StepStatus.FAILED.value)
        return self._events[-1]

    def report_status(self, step: WorkflowStep) -> str:
        """Return the current status of a step as a string."""
        return StepStatus(step.status).value

    def events(self) -> list[ExecutionEvent]:
        """Return the execution events emitted so far, in order."""
        return list(self._events)
