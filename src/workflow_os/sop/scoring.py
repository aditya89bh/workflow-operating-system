"""Deterministic SOP recommendation scoring.

Assigns each SOP a numeric score in ``[0.0, 1.0]`` from a fixed weighted sum of
four components: version recency, workflow-type match, tag match, and usage
frequency. The weights are constants, so identical inputs always produce
identical scores. No machine learning or LLM is involved.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field

from workflow_os.sop.record import SOPRecord
from workflow_os.sop.store import SOPStore

WORKFLOW_MATCH_WEIGHT = 0.4
VERSION_RECENCY_WEIGHT = 0.2
TAG_MATCH_WEIGHT = 0.2
USAGE_FREQUENCY_WEIGHT = 0.2


@dataclass
class SOPScore:
    """A SOP's overall recommendation score and its components."""

    sop_id: str
    score: float
    components: dict[str, float] = field(default_factory=dict)


def score_sop(
    record: SOPRecord,
    *,
    workflow_type: str | None = None,
    tags: list[str] | None = None,
    usage_counts: Mapping[str, int] | None = None,
    max_version: int = 1,
    max_usage: int = 0,
) -> SOPScore:
    """Return the deterministic score for a single SOP."""
    wanted_tags = set(tags or [])
    usage_counts = usage_counts or {}

    workflow_match = (
        1.0 if workflow_type is not None and record.workflow_type == workflow_type
        else 0.0
    )
    version_recency = record.version / max_version if max_version > 0 else 0.0
    version_recency = min(version_recency, 1.0)
    tag_match = (
        len(wanted_tags & set(record.tags)) / len(wanted_tags)
        if wanted_tags
        else 0.0
    )
    usage = usage_counts.get(record.sop_id, 0)
    usage_frequency = usage / max_usage if max_usage > 0 else 0.0

    components = {
        "workflow_match": workflow_match,
        "version_recency": version_recency,
        "tag_match": tag_match,
        "usage_frequency": usage_frequency,
    }
    score = (
        WORKFLOW_MATCH_WEIGHT * workflow_match
        + VERSION_RECENCY_WEIGHT * version_recency
        + TAG_MATCH_WEIGHT * tag_match
        + USAGE_FREQUENCY_WEIGHT * usage_frequency
    )
    return SOPScore(sop_id=record.sop_id, score=round(score, 6), components=components)


def score_sops(
    store: SOPStore,
    *,
    workflow_type: str | None = None,
    tags: list[str] | None = None,
    usage_counts: Mapping[str, int] | None = None,
) -> list[SOPScore]:
    """Return scores for every SOP, ordered by score (highest first).

    Ties are broken by ``sop_id`` so the ranking is fully deterministic.
    """
    records = store.list()
    usage_counts = usage_counts or {}
    max_version = max((record.version for record in records), default=1)
    max_usage = max(usage_counts.values(), default=0)

    scores = [
        score_sop(
            record,
            workflow_type=workflow_type,
            tags=tags,
            usage_counts=usage_counts,
            max_version=max_version,
            max_usage=max_usage,
        )
        for record in records
    ]
    return sorted(scores, key=lambda result: (-result.score, result.sop_id))
