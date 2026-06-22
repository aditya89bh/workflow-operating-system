"""SOP version tracking.

A :class:`SOPVersionHistory` keeps an ordered list of immutable version
snapshots for each SOP, so callers can look up the full history, the current
(latest) version, and the immediately previous version.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from workflow_os.sop.record import SOPRecord


@dataclass(frozen=True)
class SOPVersion:
    """An immutable snapshot of a SOP at a particular version."""

    sop_id: str
    version: int
    title: str
    description: str
    workflow_type: str
    status: str
    author: str | None
    recorded_at: datetime

    @classmethod
    def from_record(cls, record: SOPRecord) -> SOPVersion:
        """Build a snapshot from the current state of a SOP record."""
        return cls(
            sop_id=record.sop_id,
            version=record.version,
            title=record.title,
            description=record.description,
            workflow_type=record.workflow_type,
            status=record.status,
            author=record.author,
            recorded_at=record.updated_at,
        )


class SOPVersionHistory:
    """Tracks the ordered version snapshots of SOPs."""

    def __init__(self) -> None:
        self._by_sop: dict[str, list[SOPVersion]] = {}

    def record(self, record: SOPRecord) -> SOPVersion:
        """Record the current state of ``record`` as a version snapshot."""
        version = SOPVersion.from_record(record)
        snapshots = self._by_sop.setdefault(record.sop_id, [])
        snapshots.append(version)
        snapshots.sort(key=lambda snapshot: snapshot.version)
        return version

    def history(self, sop_id: str) -> list[SOPVersion]:
        """Return all recorded versions for a SOP, ordered oldest-first."""
        return list(self._by_sop.get(sop_id, []))

    def versions(self, sop_id: str) -> list[int]:
        """Return the recorded version numbers for a SOP, ascending."""
        return [snapshot.version for snapshot in self.history(sop_id)]

    def current_version(self, sop_id: str) -> SOPVersion | None:
        """Return the latest recorded version of a SOP, if any."""
        snapshots = self._by_sop.get(sop_id)
        return snapshots[-1] if snapshots else None

    def previous_version(self, sop_id: str) -> SOPVersion | None:
        """Return the version immediately before the current one, if any."""
        snapshots = self._by_sop.get(sop_id)
        if not snapshots or len(snapshots) < 2:
            return None
        return snapshots[-2]
