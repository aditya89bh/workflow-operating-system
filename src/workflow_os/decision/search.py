"""Search helpers over a decision store.

These functions provide case-insensitive text search across decision text and
rationale, plus exact matching on outcome. They read through the store's
``list`` method so they work with any :class:`~workflow_os.decision.store.DecisionStore`.
"""

from __future__ import annotations

from workflow_os.decision.record import DecisionRecord
from workflow_os.decision.store import DecisionStore


def _contains(haystack: str, needle: str) -> bool:
    return needle.casefold() in haystack.casefold()


def search_by_decision_text(store: DecisionStore, text: str) -> list[DecisionRecord]:
    """Return decisions whose decision text contains ``text`` (case-insensitive)."""
    return [record for record in store.list() if _contains(record.decision, text)]


def search_by_rationale(store: DecisionStore, text: str) -> list[DecisionRecord]:
    """Return decisions whose rationale contains ``text`` (case-insensitive)."""
    return [record for record in store.list() if _contains(record.rationale, text)]


def search_by_outcome(store: DecisionStore, outcome: str) -> list[DecisionRecord]:
    """Return decisions whose outcome equals ``outcome``."""
    return [record for record in store.list() if record.outcome == outcome]


def search_decisions(
    store: DecisionStore,
    *,
    text: str | None = None,
    rationale: str | None = None,
    outcome: str | None = None,
) -> list[DecisionRecord]:
    """Return decisions matching all supplied criteria.

    ``text`` matches the decision text, ``rationale`` matches the rationale, and
    ``outcome`` matches the outcome exactly. Criteria left as ``None`` are
    ignored; with no criteria every record is returned.
    """
    results: list[DecisionRecord] = []
    for record in store.list():
        if text is not None and not _contains(record.decision, text):
            continue
        if rationale is not None and not _contains(record.rationale, rationale):
            continue
        if outcome is not None and record.outcome != outcome:
            continue
        results.append(record)
    return results
