"""Agent performance reports.

Deterministic per-agent reporting built from the delegation ledger and message
bus: workload per agent, completion statistics, utilization, and the bottleneck
agents carrying the most active work. These reports summarize what happened; they
do not predict or recommend.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field

from workflow_os.agents.delegation import DelegationAction, TaskDelegation
from workflow_os.agents.messaging import MessageBus


@dataclass
class AgentPerformance:
    """Performance figures for a single agent."""

    agent_id: str
    assigned_tasks: int = 0
    active_tasks: int = 0
    transfers_in: int = 0
    transfers_out: int = 0
    messages_sent: int = 0
    messages_received: int = 0
    utilization: float = 0.0


@dataclass
class PerformanceReport:
    """A collaboration-wide performance report."""

    per_agent: dict[str, AgentPerformance] = field(default_factory=dict)
    total_active_tasks: int = 0
    bottlenecks: list[str] = field(default_factory=list)


def workload_per_agent(
    agent_ids: Iterable[str], delegation: TaskDelegation
) -> dict[str, int]:
    """Return the number of currently active tasks owned by each agent."""
    counts = {agent_id: 0 for agent_id in agent_ids}
    for assignment in delegation.active_assignments():
        if assignment.owner in counts:
            counts[assignment.owner] += 1
    return counts


def build_performance_report(
    agent_ids: Iterable[str], delegation: TaskDelegation, bus: MessageBus
) -> PerformanceReport:
    """Build a :class:`PerformanceReport` for the given agents."""
    ids = list(agent_ids)
    history = delegation.history()
    active = delegation.active_assignments()
    total_active = len(active)

    per_agent: dict[str, AgentPerformance] = {}
    for agent_id in ids:
        assigned = sum(
            1
            for event in history
            if event.to_agent == agent_id
            and event.action
            in {DelegationAction.ASSIGN.value, DelegationAction.TRANSFER.value}
        )
        active_count = sum(1 for a in active if a.owner == agent_id)
        transfers_in = sum(
            1
            for event in history
            if event.action == DelegationAction.TRANSFER.value
            and event.to_agent == agent_id
        )
        transfers_out = sum(
            1
            for event in history
            if event.action == DelegationAction.TRANSFER.value
            and event.from_agent == agent_id
        )
        utilization = active_count / total_active if total_active else 0.0
        per_agent[agent_id] = AgentPerformance(
            agent_id=agent_id,
            assigned_tasks=assigned,
            active_tasks=active_count,
            transfers_in=transfers_in,
            transfers_out=transfers_out,
            messages_sent=len(bus.history(sender=agent_id)),
            messages_received=len(bus.receive(agent_id)),
            utilization=utilization,
        )

    bottlenecks = _bottlenecks(per_agent)
    return PerformanceReport(
        per_agent=per_agent,
        total_active_tasks=total_active,
        bottlenecks=bottlenecks,
    )


def _bottlenecks(per_agent: dict[str, AgentPerformance]) -> list[str]:
    """Return the agents carrying the most active tasks (when overloaded)."""
    if not per_agent:
        return []
    peak = max(perf.active_tasks for perf in per_agent.values())
    if peak < 2:
        return []
    return sorted(
        agent_id
        for agent_id, perf in per_agent.items()
        if perf.active_tasks == peak
    )
