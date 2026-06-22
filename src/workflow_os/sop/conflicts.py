"""SOP conflict detection.

Deterministic, rule-based checks that surface inconsistencies in a SOP store:
duplicate SOPs, version conflicts, ownership conflicts, and ambiguous workflow
mappings. Each detector returns structured :class:`SOPConflict` entries.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from enum import Enum

from workflow_os.sop.authorship import OWNERS_KEY
from workflow_os.sop.record import ACTIVE_STATUSES, SOPRecord
from workflow_os.sop.store import SOPStore


class ConflictType(str, Enum):
    """The kinds of SOP conflicts that can be detected."""

    DUPLICATE = "duplicate"
    VERSION = "version"
    OWNERSHIP = "ownership"
    WORKFLOW_MAPPING = "workflow_mapping"

    def __str__(self) -> str:  # pragma: no cover - convenience only
        return self.value


@dataclass(frozen=True)
class SOPConflict:
    """A detected conflict between two or more SOPs."""

    conflict_type: str
    workflow_type: str | None
    sop_ids: tuple[str, ...]
    detail: str


def _owners(record: SOPRecord) -> tuple[str, ...]:
    value = record.metadata.get(OWNERS_KEY, [])
    if isinstance(value, list):
        return tuple(sorted(str(person) for person in value))
    return ()


def detect_duplicate_sops(store: SOPStore) -> list[SOPConflict]:
    """Detect SOPs that share a title and workflow type."""
    groups: dict[tuple[str, str], list[str]] = defaultdict(list)
    for record in store.list():
        key = (record.title.strip().casefold(), record.workflow_type)
        groups[key].append(record.sop_id)
    conflicts: list[SOPConflict] = []
    for (title, workflow_type), sop_ids in groups.items():
        if len(sop_ids) > 1:
            conflicts.append(
                SOPConflict(
                    conflict_type=ConflictType.DUPLICATE.value,
                    workflow_type=workflow_type,
                    sop_ids=tuple(sorted(sop_ids)),
                    detail=f"{len(sop_ids)} SOPs share title {title!r}",
                )
            )
    return conflicts


def detect_version_conflicts(store: SOPStore) -> list[SOPConflict]:
    """Detect SOPs of one workflow type that claim the same version number."""
    by_type_version: dict[tuple[str, int], list[str]] = defaultdict(list)
    for record in store.list():
        by_type_version[(record.workflow_type, record.version)].append(record.sop_id)
    conflicts: list[SOPConflict] = []
    for (workflow_type, version), sop_ids in by_type_version.items():
        if len(sop_ids) > 1:
            conflicts.append(
                SOPConflict(
                    conflict_type=ConflictType.VERSION.value,
                    workflow_type=workflow_type,
                    sop_ids=tuple(sorted(sop_ids)),
                    detail=f"version {version} used by {len(sop_ids)} SOPs",
                )
            )
    return conflicts


def detect_ownership_conflicts(store: SOPStore) -> list[SOPConflict]:
    """Detect a workflow type owned by differing sets of owners."""
    by_type: dict[str, list[SOPRecord]] = defaultdict(list)
    for record in store.list():
        by_type[record.workflow_type].append(record)
    conflicts: list[SOPConflict] = []
    for workflow_type, records in by_type.items():
        owner_sets = {_owners(record) for record in records if _owners(record)}
        if len(owner_sets) > 1:
            sop_ids = tuple(
                sorted(record.sop_id for record in records if _owners(record))
            )
            conflicts.append(
                SOPConflict(
                    conflict_type=ConflictType.OWNERSHIP.value,
                    workflow_type=workflow_type,
                    sop_ids=sop_ids,
                    detail=f"{len(owner_sets)} differing owner sets",
                )
            )
    return conflicts


def detect_workflow_mapping_conflicts(store: SOPStore) -> list[SOPConflict]:
    """Detect more than one active SOP mapped to the same workflow type."""
    by_type: dict[str, list[str]] = defaultdict(list)
    for record in store.list():
        if record.status in ACTIVE_STATUSES:
            by_type[record.workflow_type].append(record.sop_id)
    conflicts: list[SOPConflict] = []
    for workflow_type, sop_ids in by_type.items():
        if len(sop_ids) > 1:
            conflicts.append(
                SOPConflict(
                    conflict_type=ConflictType.WORKFLOW_MAPPING.value,
                    workflow_type=workflow_type,
                    sop_ids=tuple(sorted(sop_ids)),
                    detail=f"{len(sop_ids)} active SOPs map to {workflow_type!r}",
                )
            )
    return conflicts


def detect_conflicts(store: SOPStore) -> list[SOPConflict]:
    """Run every detector and return conflicts in a deterministic order."""
    conflicts = (
        detect_duplicate_sops(store)
        + detect_version_conflicts(store)
        + detect_ownership_conflicts(store)
        + detect_workflow_mapping_conflicts(store)
    )
    return sorted(
        conflicts,
        key=lambda conflict: (
            conflict.conflict_type,
            conflict.workflow_type or "",
            conflict.sop_ids,
        ),
    )
