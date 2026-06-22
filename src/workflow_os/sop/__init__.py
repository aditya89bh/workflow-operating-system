"""SOP memory for the workflow operating system.

This subpackage captures standard operating procedures as versioned, searchable
records and links them to workflow types. It builds on the workflow, memory, and
decision layers without modifying them. Everything is deterministic and
rule-based.
"""

from workflow_os.sop.record import (
    ACTIVE_STATUSES,
    SOPRecord,
    SOPStatus,
    new_sop_id,
    utcnow,
)
from workflow_os.sop.store import (
    SOPList,
    SOPNotFoundError,
    SOPQuery,
    SOPStore,
    apply_query,
    matches,
)

__all__ = [
    "ACTIVE_STATUSES",
    "SOPList",
    "SOPNotFoundError",
    "SOPQuery",
    "SOPRecord",
    "SOPStatus",
    "SOPStore",
    "apply_query",
    "matches",
    "new_sop_id",
    "utcnow",
]
