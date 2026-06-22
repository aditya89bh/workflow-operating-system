"""Coordinator agent.

The coordinator is a deterministic service object that assigns tasks to agents,
derives the execution order for a workflow, and manages workflow lifecycle state.
It does not plan or execute itself; it orchestrates the other agents.
"""

from __future__ import annotations

from collections.abc import Mapping

from workflow_os.agents.record import Agent
from workflow_os.executor import WorkflowExecutor
from workflow_os.operations import (
    complete_workflow,
    pause_workflow,
    resume_workflow,
    start_workflow,
)
from workflow_os.step import WorkflowStep
from workflow_os.workflow import Workflow


class CoordinationError(ValueError):
    """Raised when a coordination action is invalid."""


class CoordinatorAgent:
    """Assigns work and manages workflow state deterministically."""

    def __init__(self, agent: Agent | None = None) -> None:
        self.agent = agent

    def assign_tasks(
        self, workflow: Workflow, assignments: Mapping[str, str]
    ) -> dict[str, str]:
        """Assign workflow steps to agents by setting each step's assignee.

        ``assignments`` maps a step id to an agent id. Unknown step ids raise a
        :class:`CoordinationError`.
        """
        steps = {step.id: step for step in workflow.steps}
        result: dict[str, str] = {}
        for step_id, agent_id in assignments.items():
            if step_id not in steps:
                raise CoordinationError(
                    f"unknown step {step_id!r} in workflow {workflow.id!r}"
                )
            steps[step_id].assignee = agent_id
            result[step_id] = agent_id
        return result

    def coordinate_execution(self, workflow: Workflow) -> list[WorkflowStep]:
        """Return the steps in a valid execution order."""
        return WorkflowExecutor(workflow).execution_order()

    def start(self, workflow: Workflow) -> Workflow:
        """Start the workflow."""
        start_workflow(workflow)
        return workflow

    def pause(self, workflow: Workflow) -> Workflow:
        """Pause the workflow."""
        pause_workflow(workflow)
        return workflow

    def resume(self, workflow: Workflow) -> Workflow:
        """Resume the workflow."""
        resume_workflow(workflow)
        return workflow

    def complete(self, workflow: Workflow) -> Workflow:
        """Complete the workflow."""
        complete_workflow(workflow)
        return workflow
