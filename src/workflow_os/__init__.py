"""Workflow Operating System.

A small, dependency-free library to model, validate, and execute workflows.
"""

from workflow_os.status import WorkflowStatus
from workflow_os.step import WorkflowStep
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
    "SchemaVersionError",
    "Workflow",
    "WorkflowStatus",
    "WorkflowStep",
    "WorkflowValidationError",
    "__version__",
    "is_supported_version",
    "is_valid",
    "migrate",
    "validate",
    "validate_schema_version",
    "validate_workflow",
]
