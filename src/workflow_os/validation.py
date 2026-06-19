"""Validation rules for workflows.

The rules cover the structural invariants a workflow must satisfy before it can
be executed:

* the workflow must have a non-empty name;
* every step id must be unique;
* every declared dependency must reference an existing step;
* a step may not depend on itself;
* the workflow must start in a valid initial state.
"""

from __future__ import annotations

from workflow_os.status import WorkflowStatus
from workflow_os.workflow import Workflow

VALID_INITIAL_STATES: frozenset[WorkflowStatus] = frozenset(
    {WorkflowStatus.DRAFT, WorkflowStatus.READY}
)


class WorkflowValidationError(ValueError):
    """Raised when a workflow fails one or more validation rules."""

    def __init__(self, errors: list[str]) -> None:
        self.errors = list(errors)
        super().__init__("; ".join(self.errors))


def validate_workflow(workflow: Workflow) -> list[str]:
    """Return a list of validation error messages (empty if the workflow is valid)."""
    errors: list[str] = []

    if not workflow.name or not workflow.name.strip():
        errors.append("workflow name must not be empty")

    seen: set[str] = set()
    for step in workflow.steps:
        if not step.id or not step.id.strip():
            errors.append("step id must not be empty")
            continue
        if step.id in seen:
            errors.append(f"duplicate step id: {step.id!r}")
        seen.add(step.id)

    step_ids = {step.id for step in workflow.steps}
    for step in workflow.steps:
        for dependency in step.dependencies:
            if dependency == step.id:
                errors.append(f"step {step.id!r} cannot depend on itself")
            elif dependency not in step_ids:
                errors.append(
                    f"step {step.id!r} depends on unknown step {dependency!r}"
                )

    if workflow.status not in VALID_INITIAL_STATES:
        valid = ", ".join(sorted(s.value for s in VALID_INITIAL_STATES))
        errors.append(
            f"workflow must start in one of [{valid}], got {workflow.status.value!r}"
        )

    return errors


def is_valid(workflow: Workflow) -> bool:
    """Return ``True`` if the workflow passes all validation rules."""
    return not validate_workflow(workflow)


def validate(workflow: Workflow) -> None:
    """Validate a workflow, raising :class:`WorkflowValidationError` on failure."""
    errors = validate_workflow(workflow)
    if errors:
        raise WorkflowValidationError(errors)
