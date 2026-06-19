"""JSON serialization for workflows.

Workflows are converted to and from plain dictionaries and JSON text. On load,
payloads are passed through :func:`workflow_os.versioning.migrate` so older
schema versions are upgraded before they are materialised.
"""

from __future__ import annotations

import json
from typing import Any

from workflow_os.status import WorkflowStatus
from workflow_os.step import WorkflowStep
from workflow_os.transitions import StepStatus
from workflow_os.versioning import migrate
from workflow_os.workflow import Workflow


def step_to_dict(step: WorkflowStep) -> dict[str, Any]:
    """Convert a :class:`WorkflowStep` into a JSON-serialisable dict."""
    return {
        "id": step.id,
        "name": step.name,
        "description": step.description,
        "status": StepStatus(step.status).value,
        "dependencies": list(step.dependencies),
        "assignee": step.assignee,
        "metadata": dict(step.metadata),
    }


def step_from_dict(data: dict[str, Any]) -> WorkflowStep:
    """Build a :class:`WorkflowStep` from a dict."""
    return WorkflowStep(
        id=data["id"],
        name=data["name"],
        description=data.get("description", ""),
        status=StepStatus(data.get("status", StepStatus.PENDING.value)),
        dependencies=list(data.get("dependencies", [])),
        assignee=data.get("assignee"),
        metadata=dict(data.get("metadata", {})),
    )


def workflow_to_dict(workflow: Workflow) -> dict[str, Any]:
    """Convert a :class:`Workflow` into a JSON-serialisable dict."""
    return {
        "schema_version": workflow.schema_version,
        "id": workflow.id,
        "name": workflow.name,
        "description": workflow.description,
        "status": WorkflowStatus(workflow.status).value,
        "metadata": dict(workflow.metadata),
        "steps": [step_to_dict(step) for step in workflow.steps],
    }


def workflow_from_dict(data: dict[str, Any]) -> Workflow:
    """Build a :class:`Workflow` from a dict, migrating the schema first."""
    payload = migrate(data)
    return Workflow(
        id=payload["id"],
        name=payload["name"],
        description=payload.get("description", ""),
        steps=[step_from_dict(step) for step in payload.get("steps", [])],
        status=WorkflowStatus(payload.get("status", WorkflowStatus.DRAFT.value)),
        metadata=dict(payload.get("metadata", {})),
        schema_version=payload["schema_version"],
    )


def workflow_to_json(workflow: Workflow, *, indent: int = 2) -> str:
    """Serialise a workflow to a JSON string."""
    return json.dumps(workflow_to_dict(workflow), indent=indent, sort_keys=False)


def workflow_from_json(text: str) -> Workflow:
    """Deserialise a workflow from a JSON string."""
    return workflow_from_dict(json.loads(text))
