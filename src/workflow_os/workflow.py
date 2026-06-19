"""The core :class:`Workflow` entity."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


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
    steps: list = field(default_factory=list)
    status: str = "draft"
    metadata: dict[str, Any] = field(default_factory=dict)
