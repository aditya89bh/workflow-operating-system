"""Search helpers over a SOP store.

These provide case-insensitive search by title and free text, exact matching by
workflow type, and tag matching. They read through the store's ``list`` method
so they work with any :class:`~workflow_os.sop.store.SOPStore`.
"""

from __future__ import annotations

from workflow_os.sop.record import SOPRecord
from workflow_os.sop.store import SOPStore


def _contains(haystack: str, needle: str) -> bool:
    return needle.casefold() in haystack.casefold()


def search_by_title(store: SOPStore, text: str) -> list[SOPRecord]:
    """Return SOPs whose title contains ``text`` (case-insensitive)."""
    return [record for record in store.list() if _contains(record.title, text)]


def search_by_workflow_type(store: SOPStore, workflow_type: str) -> list[SOPRecord]:
    """Return SOPs that document a given workflow type."""
    return [
        record for record in store.list() if record.workflow_type == workflow_type
    ]


def search_by_tags(
    store: SOPStore, tags: list[str], *, match_all: bool = True
) -> list[SOPRecord]:
    """Return SOPs matching the requested tags.

    With ``match_all`` (the default) a SOP must carry every requested tag; with
    ``match_all=False`` it must carry at least one.
    """
    wanted = set(tags)
    results: list[SOPRecord] = []
    for record in store.list():
        have = set(record.tags)
        if match_all and wanted.issubset(have):
            results.append(record)
        elif not match_all and wanted & have:
            results.append(record)
    return results


def text_search(store: SOPStore, text: str) -> list[SOPRecord]:
    """Return SOPs whose title or description contains ``text``."""
    return [
        record
        for record in store.list()
        if _contains(record.title, text) or _contains(record.description, text)
    ]


def search_sops(
    store: SOPStore,
    *,
    title: str | None = None,
    workflow_type: str | None = None,
    tags: list[str] | None = None,
    text: str | None = None,
) -> list[SOPRecord]:
    """Return SOPs matching all supplied criteria.

    Criteria left as ``None`` are ignored; with no criteria every SOP is
    returned. ``text`` matches title or description; ``title`` matches the title
    only; ``tags`` requires every listed tag.
    """
    results: list[SOPRecord] = []
    wanted_tags = set(tags) if tags is not None else None
    for record in store.list():
        if title is not None and not _contains(record.title, title):
            continue
        if workflow_type is not None and record.workflow_type != workflow_type:
            continue
        if wanted_tags is not None and not wanted_tags.issubset(set(record.tags)):
            continue
        if text is not None and not (
            _contains(record.title, text) or _contains(record.description, text)
        ):
            continue
        results.append(record)
    return results
