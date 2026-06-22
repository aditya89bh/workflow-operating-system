"""Bottleneck detection.

Identifies the steps that consume the most cumulative execution time across all
workflows. Bottlenecks are ranked deterministically by total time spent, so the
steps that dominate end-to-end duration surface first.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from workflow_os.analytics.step_duration import step_durations
from workflow_os.memory.record import MemoryRecord


@dataclass
class Bottleneck:
    """A step ranked by the time it consumes."""

    step_id: str
    total_duration: float
    occurrences: int
    mean_duration: float


def detect_bottlenecks(
    records: Iterable[MemoryRecord], *, limit: int | None = None
) -> list[Bottleneck]:
    """Return steps ranked by total duration, slowest first.

    Ties are broken by step id for deterministic ordering. ``limit`` caps the
    number of bottlenecks returned.
    """
    bottlenecks: list[Bottleneck] = []
    for step_id, values in step_durations(records).items():
        total = float(sum(values))
        occurrences = len(values)
        bottlenecks.append(
            Bottleneck(
                step_id=step_id,
                total_duration=total,
                occurrences=occurrences,
                mean_duration=total / occurrences if occurrences else 0.0,
            )
        )
    bottlenecks.sort(key=lambda b: (-b.total_duration, b.step_id))
    if limit is not None:
        bottlenecks = bottlenecks[:limit]
    return bottlenecks
