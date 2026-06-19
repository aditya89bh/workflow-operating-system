"""Workflow Operating System.

A small, dependency-free library to model, validate, and execute workflows.
"""

from workflow_os.status import WorkflowStatus
from workflow_os.step import WorkflowStep
from workflow_os.workflow import Workflow

__version__ = "0.1.0"

__all__ = ["Workflow", "WorkflowStatus", "WorkflowStep", "__version__"]
