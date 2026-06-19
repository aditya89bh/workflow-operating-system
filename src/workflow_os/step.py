"""The :class:`WorkflowStep` entity."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from workflow_os.transitions import StepStatus


@dataclass
class WorkflowStep:
    """A single unit of work within a workflow.

    Attributes:
        id: Stable, unique identifier for the step (unique within a workflow).
        name: Human-readable step name.
        description: Optional longer description of the step.
        status: Current execution status of the step.
        dependencies: Ids of steps that must complete before this step runs.
        assignee: Optional owner responsible for the step.
        metadata: Arbitrary user-supplied key/value data.
    """

    id: str
    name: str
    description: str = ""
    status: StepStatus = StepStatus.PENDING
    dependencies: list[str] = field(default_factory=list)
    assignee: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
