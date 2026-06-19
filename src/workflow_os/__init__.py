"""Workflow Operating System.

A small, dependency-free library to model, validate, and execute workflows.
"""

from workflow_os.executor import CycleError, WorkflowExecutor
from workflow_os.fileio import import_workflow
from workflow_os.operations import (
    WorkflowOperationError,
    complete_workflow,
    pause_workflow,
    resume_workflow,
    start_workflow,
)
from workflow_os.persistence import (
    workflow_from_dict,
    workflow_from_json,
    workflow_to_dict,
    workflow_to_json,
)
from workflow_os.repository import (
    InMemoryWorkflowRepository,
    WorkflowNotFoundError,
    WorkflowRepository,
)
from workflow_os.status import WorkflowStatus
from workflow_os.step import WorkflowStep
from workflow_os.transitions import (
    StepStatus,
    StepTransitionError,
    available_transitions,
    can_transition,
    transition_step,
)
from workflow_os.validation import (
    WorkflowValidationError,
    is_valid,
    validate,
    validate_workflow,
)
from workflow_os.versioning import (
    CURRENT_SCHEMA_VERSION,
    SchemaVersionError,
    is_supported_version,
    migrate,
    validate_schema_version,
)
from workflow_os.workflow import Workflow

__version__ = "0.1.0"

__all__ = [
    "CURRENT_SCHEMA_VERSION",
    "CycleError",
    "InMemoryWorkflowRepository",
    "SchemaVersionError",
    "StepStatus",
    "StepTransitionError",
    "Workflow",
    "WorkflowExecutor",
    "WorkflowNotFoundError",
    "WorkflowOperationError",
    "WorkflowRepository",
    "WorkflowStatus",
    "WorkflowStep",
    "WorkflowValidationError",
    "__version__",
    "available_transitions",
    "can_transition",
    "complete_workflow",
    "import_workflow",
    "is_supported_version",
    "is_valid",
    "migrate",
    "pause_workflow",
    "resume_workflow",
    "start_workflow",
    "transition_step",
    "validate",
    "validate_schema_version",
    "validate_workflow",
    "workflow_from_dict",
    "workflow_from_json",
    "workflow_to_dict",
    "workflow_to_json",
]
