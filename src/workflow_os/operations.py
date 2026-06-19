"""High-level workflow lifecycle operations.

These functions move a whole workflow between lifecycle states, enforcing the
rules that govern each transition.
"""

from __future__ import annotations

from workflow_os.status import WorkflowStatus
from workflow_os.validation import validate
from workflow_os.workflow import Workflow

STARTABLE_STATES: frozenset[WorkflowStatus] = frozenset(
    {WorkflowStatus.DRAFT, WorkflowStatus.READY}
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
