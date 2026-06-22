"""Planner agent.

The planner is a deterministic service object that derives an execution plan from
a workflow's step dependency graph: the ordered list of steps, and the resolved
dependencies for each step. It reuses the Phase 1 execution engine.
"""

from __future__ import annotations

from workflow_os.agents.record import Agent
from workflow_os.executor import WorkflowExecutor
from workflow_os.step import WorkflowStep
from workflow_os.workflow import Workflow


class PlannerAgent:
    """Builds deterministic execution plans for workflows."""

    def __init__(self, agent: Agent | None = None) -> None:
        self.agent = agent

    def determine_ordering(self, workflow: Workflow) -> list[WorkflowStep]:
        """Return the steps in a valid topological execution order."""
        return WorkflowExecutor(workflow).execution_order()

    def create_plan(self, workflow: Workflow) -> list[str]:
        """Return the ordered step ids that make up the execution plan."""
        return [step.id for step in self.determine_ordering(workflow)]

    def identify_dependencies(self, workflow: Workflow) -> dict[str, list[str]]:
        """Return each step's dependencies that exist within the workflow."""
        known = {step.id for step in workflow.steps}
        return {
            step.id: [dep for dep in step.dependencies if dep in known]
            for step in workflow.steps
        }
