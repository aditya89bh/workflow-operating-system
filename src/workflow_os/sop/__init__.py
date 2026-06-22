"""SOP memory for the workflow operating system.

This subpackage captures standard operating procedures as versioned, searchable
records and links them to workflow types. It builds on the workflow, memory, and
decision layers without modifying them. Everything is deterministic and
rule-based.
"""

from workflow_os.sop.authorship import (
    CONTRIBUTORS_KEY,
    OWNERS_KEY,
    REVIEWERS_KEY,
    SOPAuthorship,
    add_contributor,
    add_owner,
    add_reviewer,
    get_authorship,
    set_contributors,
    set_owners,
    set_reviewers,
)
from workflow_os.sop.change_history import (
    SOPChange,
    SOPChangeLog,
    diff_fields,
)
from workflow_os.sop.record import (
    ACTIVE_STATUSES,
    SOPRecord,
    SOPStatus,
    new_sop_id,
    utcnow,
)
from workflow_os.sop.sqlite_store import SQLiteSOPStore
from workflow_os.sop.store import (
    SOPList,
    SOPNotFoundError,
    SOPQuery,
    SOPStore,
    apply_query,
    matches,
)
from workflow_os.sop.versioning import SOPVersion, SOPVersionHistory

__all__ = [
    "ACTIVE_STATUSES",
    "CONTRIBUTORS_KEY",
    "OWNERS_KEY",
    "REVIEWERS_KEY",
    "SOPAuthorship",
    "SOPChange",
    "SOPChangeLog",
    "SOPList",
    "SOPNotFoundError",
    "SOPQuery",
    "SOPRecord",
    "SOPStatus",
    "SOPStore",
    "SOPVersion",
    "SOPVersionHistory",
    "SQLiteSOPStore",
    "add_contributor",
    "add_owner",
    "add_reviewer",
    "apply_query",
    "diff_fields",
    "get_authorship",
    "matches",
    "new_sop_id",
    "set_contributors",
    "set_owners",
    "set_reviewers",
    "utcnow",
]
