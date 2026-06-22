"""Slow step analysis.

Where bottleneck detection ranks steps by total time, slow step analysis focuses
on per-execution slowness: the steps whose mean duration is highest, and those
that exceed a caller-supplied threshold. Both are deterministic.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from workflow_os.analytics.step_duration import step_durations
from workflow_os.memory.record import MemoryRecord


@dataclass
class SlowStep:
    """A step summarized by how slow it runs on average."""

    step_id: str
    mean_duration: float
    max_duration: float
    occurrences: int


def _slow_steps(records: Iterable[MemoryRecord]) -> list[SlowStep]:
    steps: list[SlowStep] = []
    for step_id, values in step_durations(records).items():
        occurrences = len(values)
        steps.append(
            SlowStep(
                step_id=step_id,
                mean_duration=sum(values) / occurrences if occurrences else 0.0,
                max_duration=float(max(values)) if values else 0.0,
                occurrences=occurrences,
            )
        )
    steps.sort(key=lambda s: (-s.mean_duration, s.step_id))
    return steps


def slowest_steps(
    records: Iterable[MemoryRecord], *, limit: int | None = None
) -> list[SlowStep]:
    """Return steps ranked by mean duration, slowest first."""
    steps = _slow_steps(records)
    if limit is not None:
        steps = steps[:limit]
    return steps


def slow_steps(
    records: Iterable[MemoryRecord], *, threshold: float
) -> list[SlowStep]:
    """Return steps whose mean duration is at least ``threshold`` seconds."""
    return [s for s in _slow_steps(records) if s.mean_duration >= threshold]
