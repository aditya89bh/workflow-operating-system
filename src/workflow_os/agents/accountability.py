"""Agent accountability tracking.

Deterministic accountability built from the collaboration log and the delegation
ledger: which actions an agent performed, how ownership of a task changed over
time, and the ordered chain of agents responsible for a task.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from workflow_os.agents.delegation import DelegationEvent, TaskDelegation
from workflow_os.agents.logs import CollaborationEntry, CollaborationLog


@dataclass
class AgentAccountability:
    """A summary of one agent's accountable activity."""

    agent_id: str
    actions: list[CollaborationEntry] = field(default_factory=list)
    action_counts: dict[str, int] = field(default_factory=dict)


def actions_performed(log: CollaborationLog, agent_id: str) -> list[CollaborationEntry]:
    """Return all collaboration entries attributed to ``agent_id``."""
    return log.entries(agent_id=agent_id)


def ownership_history(
    delegation: TaskDelegation, task_id: str
) -> list[DelegationEvent]:
    """Return the full delegation history for a task, oldest first."""
    return delegation.history(task_id)


def responsibility_chain(delegation: TaskDelegation, task_id: str) -> list[str]:
    """Return the ordered chain of agents who have owned a task."""
    chain: list[str] = []
    for event in delegation.history(task_id):
        if event.to_agent is not None and (not chain or chain[-1] != event.to_agent):
            chain.append(event.to_agent)
    return chain


def build_accountability(log: CollaborationLog, agent_id: str) -> AgentAccountability:
    """Return an :class:`AgentAccountability` summary for ``agent_id``."""
    actions = actions_performed(log, agent_id)
    counts: dict[str, int] = {}
    for entry in actions:
        counts[entry.event_type] = counts.get(entry.event_type, 0) + 1
    return AgentAccountability(
        agent_id=agent_id, actions=actions, action_counts=counts
    )
