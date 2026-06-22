"""Exception trend reports.

Deterministic aggregate reports over exception records: how failures are
distributed over time, which failures recur, and which workflows carry the most
risk. No forecasting or learning is performed.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from collections.abc import Iterable
from dataclasses import dataclass, field

from workflow_os.exception.record import ExceptionRecord
from workflow_os.exception.severity import severity_rank

_GRANULARITY_FORMATS: dict[str, str] = {
    "hour": "%Y-%m-%dT%H",
    "day": "%Y-%m-%d",
    "month": "%Y-%m",
}


def failures_over_time(
    exceptions: Iterable[ExceptionRecord], granularity: str = "day"
) -> dict[str, int]:
    """Return failure counts bucketed by time, ordered chronologically."""
    fmt = _GRANULARITY_FORMATS.get(granularity, _GRANULARITY_FORMATS["day"])
    counts: Counter[str] = Counter()
    for exception in exceptions:
        counts[exception.detected_at.strftime(fmt)] += 1
    return {bucket: counts[bucket] for bucket in sorted(counts)}


def failure_signature(exception: ExceptionRecord) -> str:
    """Return a stable signature identifying a recurring failure."""
    return f"{exception.workflow_id}:{exception.exception_type}"


def recurring_failures(
    exceptions: Iterable[ExceptionRecord], min_count: int = 2
) -> dict[str, int]:
    """Return failure signatures that occur at least ``min_count`` times."""
    counts: Counter[str] = Counter(failure_signature(e) for e in exceptions)
    return {
        signature: count
        for signature, count in counts.most_common()
        if count >= min_count
    }


@dataclass
class WorkflowRiskReport:
    """A risk summary for a single workflow."""

    workflow_id: str
    total: int = 0
    risk_score: int = 0
    by_severity: dict[str, int] = field(default_factory=dict)
    by_type: dict[str, int] = field(default_factory=dict)


def workflow_risk_reports(
    exceptions: Iterable[ExceptionRecord],
) -> list[WorkflowRiskReport]:
    """Return per-workflow risk reports, ordered by risk score (highest first)."""
    grouped: dict[str, list[ExceptionRecord]] = defaultdict(list)
    for exception in exceptions:
        grouped[exception.workflow_id].append(exception)

    reports: list[WorkflowRiskReport] = []
    for workflow_id, items in grouped.items():
        severities: Counter[str] = Counter(e.severity for e in items)
        types: Counter[str] = Counter(e.exception_type for e in items)
        score = sum(severity_rank(e.severity) + 1 for e in items)
        reports.append(
            WorkflowRiskReport(
                workflow_id=workflow_id,
                total=len(items),
                risk_score=score,
                by_severity=dict(severities),
                by_type=dict(types),
            )
        )
    reports.sort(key=lambda report: report.risk_score, reverse=True)
    return reports
