"""Team statistics.

Aggregates activity per actor (treated as a team member) from the memory event
stream: workload (events attributed to them), throughput (steps they completed),
and utilization (the share of their activity that produced completed steps). All
figures are deterministic ratios over recorded events.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from workflow_os.memory.events import MemoryEventType
from workflow_os.memory.record import MemoryRecord


@dataclass
class TeamStatistics:
    """Workload, throughput, and utilization for one actor."""

    actor: str
    workload: int
    throughput: int
    utilization: float


def team_statistics(records: Iterable[MemoryRecord]) -> list[TeamStatistics]:
    """Return per-actor :class:`TeamStatistics`, ordered by actor."""
    workload: dict[str, int] = {}
    throughput: dict[str, int] = {}
    for record in records:
        if record.actor is None:
            continue
        workload[record.actor] = workload.get(record.actor, 0) + 1
        if record.event_type == str(MemoryEventType.STEP_COMPLETED):
            throughput[record.actor] = throughput.get(record.actor, 0) + 1

    stats: list[TeamStatistics] = []
    for actor in sorted(workload):
        load = workload[actor]
        done = throughput.get(actor, 0)
        stats.append(
            TeamStatistics(
                actor=actor,
                workload=load,
                throughput=done,
                utilization=done / load if load else 0.0,
            )
        )
    return stats
