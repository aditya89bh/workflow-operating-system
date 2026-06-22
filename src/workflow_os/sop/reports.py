"""SOP lifecycle reports.

Summarise the SOPs in a store: how many there are, how they break down by
status, version statistics, which workflow types are covered, and per-author
counts.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Any

from workflow_os.sop.record import ACTIVE_STATUSES
from workflow_os.sop.store import SOPQuery, SOPStore


@dataclass
class SOPLifecycleReport:
    """Aggregate lifecycle metrics over a set of SOPs."""

    total_sops: int = 0
    status_counts: dict[str, int] = field(default_factory=dict)
    active_count: int = 0
    inactive_count: int = 0
    version_statistics: dict[str, float] = field(default_factory=dict)
    workflow_coverage: dict[str, int] = field(default_factory=dict)
    author_statistics: dict[str, int] = field(default_factory=dict)

    @property
    def workflow_coverage_count(self) -> int:
        """Number of distinct workflow types covered by SOPs."""
        return len(self.workflow_coverage)

    def as_dict(self) -> dict[str, Any]:
        """Return a JSON-serialisable view of the report."""
        return {
            "total_sops": self.total_sops,
            "status_counts": dict(self.status_counts),
            "active_count": self.active_count,
            "inactive_count": self.inactive_count,
            "version_statistics": dict(self.version_statistics),
            "workflow_coverage": dict(self.workflow_coverage),
            "workflow_coverage_count": self.workflow_coverage_count,
            "author_statistics": dict(self.author_statistics),
        }


def generate_lifecycle_report(store: SOPStore) -> SOPLifecycleReport:
    """Build a :class:`SOPLifecycleReport` for all SOPs in ``store``."""
    records = store.query(SOPQuery())
    if not records:
        return SOPLifecycleReport()

    status_counts: Counter[str] = Counter(record.status for record in records)
    workflow_coverage: Counter[str] = Counter(
        record.workflow_type for record in records
    )
    author_counts: Counter[str] = Counter(
        record.author for record in records if record.author is not None
    )
    versions = [record.version for record in records]
    active_count = sum(
        1 for record in records if record.status in ACTIVE_STATUSES
    )

    version_statistics = {
        "min_version": float(min(versions)),
        "max_version": float(max(versions)),
        "average_version": round(sum(versions) / len(versions), 6),
        "total_versions": float(sum(versions)),
    }

    return SOPLifecycleReport(
        total_sops=len(records),
        status_counts=dict(status_counts),
        active_count=active_count,
        inactive_count=len(records) - active_count,
        version_statistics=version_statistics,
        workflow_coverage=dict(workflow_coverage),
        author_statistics=dict(author_counts),
    )
