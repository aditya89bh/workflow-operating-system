"""Actor attribution helpers for memory records.

Workflow-level events are attributed to the workflow owner (taken from workflow
metadata). Step-level events are attributed to the step assignee, falling back
to the workflow owner when a step has no explicit assignee.
"""

from __future__ import annotations

from workflow_os.step import WorkflowStep
from workflow_os.workflow import Workflow

OWNER_METADATA_KEY = "owner"


def workflow_owner(workflow: Workflow) -> str | None:
    """Return the workflow owner from metadata, if present."""
    owner = workflow.metadata.get(OWNER_METADATA_KEY)
    return str(owner) if owner is not None else None


def step_actor(workflow: Workflow, step: WorkflowStep) -> str | None:
    """Return the actor attributed to a step.

    Uses the step assignee when set, otherwise the workflow owner.
    """
    if step.assignee is not None:
        return step.assignee
    return workflow_owner(workflow)
