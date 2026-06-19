"""Repository abstraction for storing and retrieving workflows.

:class:`WorkflowRepository` is a structural protocol describing the storage
operations the library expects. :class:`InMemoryWorkflowRepository` is a simple
implementation useful for tests and small scripts.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from workflow_os.workflow import Workflow


class WorkflowNotFoundError(KeyError):
    """Raised when a workflow id cannot be found in a repository."""


@runtime_checkable
class WorkflowRepository(Protocol):
    """Storage interface for workflows."""

    def save(self, workflow: Workflow) -> None:
        """Persist a workflow, overwriting any existing one with the same id."""
        ...

    def load(self, workflow_id: str) -> Workflow:
        """Return the workflow with ``workflow_id`` or raise if missing."""
        ...

    def list(self) -> list[Workflow]:
        """Return all stored workflows."""
        ...

    def delete(self, workflow_id: str) -> None:
        """Remove the workflow with ``workflow_id`` or raise if missing."""
        ...


class InMemoryWorkflowRepository:
    """A :class:`WorkflowRepository` backed by an in-process dictionary."""

    def __init__(self) -> None:
        self._store: dict[str, Workflow] = {}

    def save(self, workflow: Workflow) -> None:
        self._store[workflow.id] = workflow

    def load(self, workflow_id: str) -> Workflow:
        try:
            return self._store[workflow_id]
        except KeyError as exc:
            raise WorkflowNotFoundError(workflow_id) from exc

    def list(self) -> list[Workflow]:
        return list(self._store.values())

    def delete(self, workflow_id: str) -> None:
        try:
            del self._store[workflow_id]
        except KeyError as exc:
            raise WorkflowNotFoundError(workflow_id) from exc
