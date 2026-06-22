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

__all__ = [
    "ACTIVE_STATUSES",
    "SOPRecord",
    "SOPStatus",
    "new_sop_id",
    "utcnow",
]
