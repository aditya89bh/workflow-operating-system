"""Execution engine that runs a workflow through its steps.

The executor resolves a valid execution order from the step dependency graph
and then drives each step to completion. Higher-level lifecycle operations
(start, pause, resume, complete) build on top of this engine.
"""

from __future__ import annotations

from workflow_os.status import WorkflowStatus
from workflow_os.step import WorkflowStep
from workflow_os.transitions import StepStatus, transition_step
from workflow_os.validation import validate
from workflow_os.workflow import Workflow


class CycleError(ValueError):
    """Raised when step dependencies form a cycle and cannot be ordered."""


class WorkflowExecutor:
    """Runs a :class:`Workflow` through a valid sequence of step transitions."""

    def __init__(self, workflow: Workflow) -> None:
        self.workflow = workflow

    def execution_order(self) -> list[WorkflowStep]:
        """Return steps in dependency order (a topological sort).

        Steps with no outstanding dependencies are emitted in their original
        definition order to keep execution deterministic.
        """
        steps = {step.id: step for step in self.workflow.steps}
        position = {step.id: index for index, step in enumerate(self.workflow.steps)}
        indegree = {step_id: 0 for step_id in steps}
        dependents: dict[str, list[str]] = {step_id: [] for step_id in steps}

        for step in self.workflow.steps:
            for dependency in step.dependencies:
                if dependency in steps:
                    indegree[step.id] += 1
                    dependents[dependency].append(step.id)

        ready = sorted(
            (step_id for step_id, count in indegree.items() if count == 0),
            key=position.__getitem__,
        )
        order: list[WorkflowStep] = []
        while ready:
            current = ready.pop(0)
            order.append(steps[current])
            for dependent in dependents[current]:
                indegree[dependent] -= 1
                if indegree[dependent] == 0:
                    ready.append(dependent)
            ready.sort(key=position.__getitem__)

        if len(order) != len(steps):
            raise CycleError("workflow steps contain a dependency cycle")
        return order

    def run(self) -> Workflow:
        """Validate the workflow and run every step to completion in order."""
        validate(self.workflow)
        order = self.execution_order()
        self.workflow.status = WorkflowStatus.RUNNING
        for step in order:
            transition_step(step, StepStatus.RUNNING)
            transition_step(step, StepStatus.COMPLETED)
        return self.workflow
