"""High-level workflow lifecycle operations.

These functions move a whole workflow between lifecycle states, enforcing the
rules that govern each transition.
"""

from __future__ import annotations

from workflow_os.status import WorkflowStatus
from workflow_os.step import WorkflowStep
from workflow_os.transitions import StepStatus
from workflow_os.validation import validate
from workflow_os.workflow import Workflow

STARTABLE_STATES: frozenset[WorkflowStatus] = frozenset(
    {WorkflowStatus.DRAFT, WorkflowStatus.READY}
)

COMPLETABLE_STATES: frozenset[WorkflowStatus] = frozenset(
    {WorkflowStatus.RUNNING, WorkflowStatus.PAUSED}
)


class WorkflowOperationError(ValueError):
    """Raised when a lifecycle operation is not allowed in the current state."""


def start_workflow(workflow: Workflow) -> Workflow:
    """Start a draft or ready workflow, moving it to the running state.

    The workflow is validated before it starts; invalid workflows cannot run.
    """
    if workflow.status not in STARTABLE_STATES:
        startable = ", ".join(sorted(s.value for s in STARTABLE_STATES))
        raise WorkflowOperationError(
            f"workflow can only start from [{startable}], "
            f"current state is {workflow.status.value!r}"
        )
    validate(workflow)
    workflow.status = WorkflowStatus.RUNNING
    return workflow


def pause_workflow(workflow: Workflow) -> Workflow:
    """Pause a running workflow, moving it to the paused state."""
    if workflow.status is not WorkflowStatus.RUNNING:
        raise WorkflowOperationError(
            f"only running workflows can be paused, "
            f"current state is {workflow.status.value!r}"
        )
    workflow.status = WorkflowStatus.PAUSED
    return workflow


def resume_workflow(workflow: Workflow) -> Workflow:
    """Resume a paused workflow, moving it back to the running state."""
    if workflow.status is not WorkflowStatus.PAUSED:
        raise WorkflowOperationError(
            f"only paused workflows can be resumed, "
            f"current state is {workflow.status.value!r}"
        )
    workflow.status = WorkflowStatus.RUNNING
    return workflow


def is_required(step: WorkflowStep) -> bool:
    """Return ``True`` unless the step is explicitly marked optional in metadata."""
    return not bool(step.metadata.get("optional", False))


def complete_workflow(workflow: Workflow) -> Workflow:
    """Mark a workflow completed, but only when all required steps are completed.

    A step is required unless its metadata sets ``"optional": True``. Required
    steps must be in the completed state; optional steps may be completed or
    skipped.
    """
    if workflow.status not in COMPLETABLE_STATES:
        completable = ", ".join(sorted(s.value for s in COMPLETABLE_STATES))
        raise WorkflowOperationError(
            f"workflow can only complete from [{completable}], "
            f"current state is {workflow.status.value!r}"
        )

    pending = [
        step.id
        for step in workflow.steps
        if is_required(step) and StepStatus(step.status) is not StepStatus.COMPLETED
    ]
    if pending:
        raise WorkflowOperationError(
            f"cannot complete workflow; required steps not completed: {pending}"
        )

    workflow.status = WorkflowStatus.COMPLETED
    return workflow
