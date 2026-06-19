"""The core :class:`Workflow` entity."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from workflow_os.status import WorkflowStatus
from workflow_os.step import WorkflowStep


@dataclass
class Workflow:
    """A workflow: a named, ordered collection of steps with a lifecycle status.

    Attributes:
        id: Stable, unique identifier for the workflow.
        name: Human-readable workflow name.
        description: Optional longer description of what the workflow does.
        steps: The steps that make up the workflow.
        status: Current lifecycle status of the workflow.
        metadata: Arbitrary user-supplied key/value data.
    """

    id: str
    name: str
    description: str = ""
    steps: list[WorkflowStep] = field(default_factory=list)
    status: WorkflowStatus = WorkflowStatus.DRAFT
    metadata: dict[str, Any] = field(default_factory=dict)
