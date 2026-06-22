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
from workflow_os.sop.best_practices import (
    BestPracticeRecord,
    BestPracticeStore,
    BestPracticeType,
    capture_best_practice,
    new_practice_id,
)
from workflow_os.sop.change_history import (
    SOPChange,
    SOPChangeLog,
    diff_fields,
)
from workflow_os.sop.conflicts import (
    ConflictType,
    SOPConflict,
    detect_conflicts,
    detect_duplicate_sops,
    detect_ownership_conflicts,
    detect_version_conflicts,
    detect_workflow_mapping_conflicts,
)
from workflow_os.sop.demo import run_demo
from workflow_os.sop.exceptions import (
    SOPExceptionRecord,
    SOPExceptionStore,
    capture_exception,
    capture_exception_from_decision,
    new_exception_id,
)
from workflow_os.sop.lessons import (
    LessonRecord,
    LessonStore,
    LessonType,
    capture_lesson,
    new_lesson_id,
)
from workflow_os.sop.linking import (
    WORKFLOW_TYPE_METADATA_KEY,
    WorkflowSOPLinks,
    get_sops_for_workflow,
    get_sops_for_workflow_type,
    get_workflow_types_for_sop,
    workflow_type_of,
)
from workflow_os.sop.recommendation import recommend_sop, recommend_sops
from workflow_os.sop.record import (
    ACTIVE_STATUSES,
    SOPRecord,
    SOPStatus,
    new_sop_id,
    utcnow,
)
from workflow_os.sop.reports import (
    SOPLifecycleReport,
    generate_lifecycle_report,
)
from workflow_os.sop.scoring import SOPScore, score_sop, score_sops
from workflow_os.sop.search import (
    search_by_tags,
    search_by_title,
    search_by_workflow_type,
    search_sops,
    text_search,
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
    "WORKFLOW_TYPE_METADATA_KEY",
    "BestPracticeRecord",
    "BestPracticeStore",
    "BestPracticeType",
    "ConflictType",
    "LessonRecord",
    "LessonStore",
    "LessonType",
    "SOPAuthorship",
    "SOPChange",
    "SOPChangeLog",
    "SOPConflict",
    "SOPExceptionRecord",
    "SOPExceptionStore",
    "SOPLifecycleReport",
    "SOPList",
    "SOPScore",
    "SOPNotFoundError",
    "SOPQuery",
    "SOPRecord",
    "SOPStatus",
    "SOPStore",
    "SOPVersion",
    "SOPVersionHistory",
    "SQLiteSOPStore",
    "WorkflowSOPLinks",
    "add_contributor",
    "add_owner",
    "add_reviewer",
    "apply_query",
    "capture_best_practice",
    "capture_exception",
    "capture_exception_from_decision",
    "capture_lesson",
    "detect_conflicts",
    "detect_duplicate_sops",
    "detect_ownership_conflicts",
    "detect_version_conflicts",
    "detect_workflow_mapping_conflicts",
    "diff_fields",
    "generate_lifecycle_report",
    "get_authorship",
    "get_sops_for_workflow",
    "get_sops_for_workflow_type",
    "get_workflow_types_for_sop",
    "matches",
    "new_exception_id",
    "new_lesson_id",
    "new_practice_id",
    "new_sop_id",
    "recommend_sop",
    "recommend_sops",
    "run_demo",
    "score_sop",
    "score_sops",
    "search_by_tags",
    "search_by_title",
    "search_by_workflow_type",
    "search_sops",
    "set_contributors",
    "set_owners",
    "set_reviewers",
    "text_search",
    "utcnow",
    "workflow_type_of",
]
