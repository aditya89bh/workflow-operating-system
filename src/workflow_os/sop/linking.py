"""Workflow-to-SOP linking.

Each SOP names a ``workflow_type`` it documents, which gives an implicit link
from workflows of that type to the SOP. :class:`WorkflowSOPLinks` adds explicit
many-to-many associations on top, so a SOP can apply to more than one workflow
type and vice versa.
"""

from __future__ import annotations

from workflow_os.sop.record import SOPRecord
from workflow_os.sop.store import SOPStore
from workflow_os.workflow import Workflow

WORKFLOW_TYPE_METADATA_KEY = "workflow_type"


def workflow_type_of(workflow: Workflow) -> str:
    """Return the workflow type of a workflow.

    Uses the ``workflow_type`` metadata key when present, otherwise falls back
    to the workflow id.
    """
    value = workflow.metadata.get(WORKFLOW_TYPE_METADATA_KEY)
    return str(value) if value is not None else workflow.id


class WorkflowSOPLinks:
    """An explicit many-to-many registry between workflow types and SOPs."""

    def __init__(self) -> None:
        self._type_to_sops: dict[str, set[str]] = {}
        self._sop_to_types: dict[str, set[str]] = {}

    def link(self, workflow_type: str, sop_id: str) -> None:
        """Associate a workflow type with a SOP."""
        self._type_to_sops.setdefault(workflow_type, set()).add(sop_id)
        self._sop_to_types.setdefault(sop_id, set()).add(workflow_type)

    def unlink(self, workflow_type: str, sop_id: str) -> None:
        """Remove an association if it exists."""
        self._type_to_sops.get(workflow_type, set()).discard(sop_id)
        self._sop_to_types.get(sop_id, set()).discard(workflow_type)

    def sop_ids_for_workflow_type(self, workflow_type: str) -> set[str]:
        """Return the SOP ids explicitly linked to a workflow type."""
        return set(self._type_to_sops.get(workflow_type, set()))

    def workflow_types_for_sop(self, sop_id: str) -> set[str]:
        """Return the workflow types explicitly linked to a SOP."""
        return set(self._sop_to_types.get(sop_id, set()))


def get_sops_for_workflow_type(
    store: SOPStore,
    workflow_type: str,
    links: WorkflowSOPLinks | None = None,
) -> list[SOPRecord]:
    """Return SOPs that apply to a workflow type (implicit and explicit)."""
    explicit = links.sop_ids_for_workflow_type(workflow_type) if links else set()
    results: list[SOPRecord] = []
    for record in store.list():
        if record.workflow_type == workflow_type or record.sop_id in explicit:
            results.append(record)
    return results


def get_sops_for_workflow(
    store: SOPStore,
    workflow: Workflow,
    links: WorkflowSOPLinks | None = None,
) -> list[SOPRecord]:
    """Return SOPs that apply to a specific workflow, by its type."""
    return get_sops_for_workflow_type(store, workflow_type_of(workflow), links)


def get_workflow_types_for_sop(
    record: SOPRecord, links: WorkflowSOPLinks | None = None
) -> set[str]:
    """Return all workflow types a SOP applies to (implicit and explicit)."""
    types = {record.workflow_type}
    if links is not None:
        types |= links.workflow_types_for_sop(record.sop_id)
    return types
