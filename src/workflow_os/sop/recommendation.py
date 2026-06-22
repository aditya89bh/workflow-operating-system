"""Deterministic SOP recommendation engine.

Given a workflow type (and optional tags), this ranks SOPs using a fixed,
rule-based priority order. There is no machine learning or LLM involved: the
same inputs always produce the same ranking.

Priority, highest first:

1. Explicit link from the workflow type to the SOP.
2. Matching ``workflow_type``.
3. Number of overlapping tags.
4. Active lifecycle status.
5. Latest version.

Ties are broken by ``sop_id`` so the ordering is fully deterministic.
"""

from __future__ import annotations

from workflow_os.sop.linking import WorkflowSOPLinks
from workflow_os.sop.record import ACTIVE_STATUSES, SOPRecord
from workflow_os.sop.store import SOPStore


def _sort_key(
    record: SOPRecord,
    workflow_type: str | None,
    wanted_tags: set[str],
    linked_ids: set[str],
) -> tuple[int, int, int, int, int, str]:
    explicit = 1 if record.sop_id in linked_ids else 0
    type_match = (
        1 if workflow_type is not None and record.workflow_type == workflow_type else 0
    )
    tag_match = len(wanted_tags & set(record.tags))
    active = 1 if record.status in ACTIVE_STATUSES else 0
    # Negated numerics sort descending; sop_id ascending breaks ties stably.
    return (-explicit, -type_match, -tag_match, -active, -record.version, record.sop_id)


def recommend_sops(
    store: SOPStore,
    *,
    workflow_type: str | None = None,
    tags: list[str] | None = None,
    links: WorkflowSOPLinks | None = None,
) -> list[SOPRecord]:
    """Return all SOPs ranked best-first for the given criteria."""
    wanted_tags = set(tags or [])
    linked_ids = (
        links.sop_ids_for_workflow_type(workflow_type)
        if links is not None and workflow_type is not None
        else set()
    )
    return sorted(
        store.list(),
        key=lambda record: _sort_key(record, workflow_type, wanted_tags, linked_ids),
    )


def recommend_sop(
    store: SOPStore,
    *,
    workflow_type: str | None = None,
    tags: list[str] | None = None,
    links: WorkflowSOPLinks | None = None,
) -> SOPRecord | None:
    """Return the single best SOP for the given criteria, or ``None`` if empty."""
    ranked = recommend_sops(
        store, workflow_type=workflow_type, tags=tags, links=links
    )
    return ranked[0] if ranked else None
