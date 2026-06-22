"""Agent role definitions.

Defines the fixed set of roles an agent can take in a collaboration. Roles are
deterministic labels used to look agents up and to decide which service object
acts on a task.
"""

from __future__ import annotations

from enum import Enum


class AgentRole(str, Enum):
    """The roles an agent can take."""

    COORDINATOR = "coordinator"
    PLANNER = "planner"
    EXECUTOR = "executor"
    COMPLIANCE = "compliance"
    MEMORY = "memory"

    def __str__(self) -> str:  # pragma: no cover - convenience only
        return self.value


ALL_AGENT_ROLES: frozenset[AgentRole] = frozenset(AgentRole)


def normalize_role(value: str) -> str:
    """Return a known role string, defaulting to ``executor``."""
    text = str(value)
    if text in {member.value for member in AgentRole}:
        return text
    return AgentRole.EXECUTOR.value
