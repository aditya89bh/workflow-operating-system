"""SOP change history.

A :class:`SOPChangeLog` records why a SOP changed, when, which fields changed,
and who changed it. :func:`diff_fields` computes the set of fields that differ
between two SOP records so changes can be logged precisely.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from workflow_os.sop.record import SOPRecord, utcnow

_TRACKED_FIELDS = (
    "title",
    "description",
    "workflow_type",
    "version",
    "status",
    "author",
    "tags",
    "metadata",
)


@dataclass
class SOPChange:
    """A single recorded change to a SOP."""

    sop_id: str
    version: int
    change_reason: str
    changed_by: str | None
    changed_at: datetime
    changed_fields: list[str] = field(default_factory=list)


def diff_fields(old: SOPRecord, new: SOPRecord) -> list[str]:
    """Return the names of the tracked fields that differ between two SOPs."""
    changed: list[str] = []
    for name in _TRACKED_FIELDS:
        if getattr(old, name) != getattr(new, name):
            changed.append(name)
    return changed


class SOPChangeLog:
    """An append-only log of SOP changes, grouped by SOP id."""

    def __init__(self) -> None:
        self._by_sop: dict[str, list[SOPChange]] = {}

    def record(
        self,
        sop_id: str,
        version: int,
        *,
        change_reason: str,
        changed_fields: list[str],
        changed_by: str | None = None,
        changed_at: datetime | None = None,
    ) -> SOPChange:
        """Record a change against a SOP."""
        change = SOPChange(
            sop_id=sop_id,
            version=version,
            change_reason=change_reason,
            changed_by=changed_by,
            changed_at=changed_at or utcnow(),
            changed_fields=list(changed_fields),
        )
        self._by_sop.setdefault(sop_id, []).append(change)
        return change

    def record_change(
        self,
        old: SOPRecord,
        new: SOPRecord,
        *,
        change_reason: str,
        changed_by: str | None = None,
        changed_at: datetime | None = None,
    ) -> SOPChange:
        """Record a change computed by diffing ``old`` against ``new``."""
        return self.record(
            new.sop_id,
            new.version,
            change_reason=change_reason,
            changed_fields=diff_fields(old, new),
            changed_by=changed_by,
            changed_at=changed_at,
        )

    def for_sop(self, sop_id: str) -> list[SOPChange]:
        """Return the recorded changes for a SOP, oldest-first."""
        return list(self._by_sop.get(sop_id, []))

    def all(self) -> list[SOPChange]:
        """Return every recorded change across all SOPs."""
        return [change for changes in self._by_sop.values() for change in changes]
