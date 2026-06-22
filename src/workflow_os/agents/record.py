"""The :class:`Agent` schema.

An agent is a deterministic service identity: a named participant with a role and
a set of capabilities. Agents are plain data records; the behaviour lives in the
dedicated service classes (coordinator, planner, execution, compliance, memory).
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any


def new_agent_id() -> str:
    """Return a fresh, unique agent id."""
    return uuid.uuid4().hex


@dataclass
class Agent:
    """A participant in a multi-agent collaboration.

    Attributes:
        agent_id: Unique identifier for the agent.
        name: Human-readable agent name.
        role: The agent's role (see ``AgentRole`` values).
        description: Optional longer description of the agent.
        capabilities: The capabilities the agent provides.
        metadata: Arbitrary key/value data attached to the agent.
    """

    agent_id: str
    name: str
    role: str = "executor"
    description: str = ""
    capabilities: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        *,
        name: str,
        role: str = "executor",
        description: str = "",
        capabilities: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        agent_id: str | None = None,
    ) -> Agent:
        """Build an :class:`Agent`, filling in the id if not supplied."""
        return cls(
            agent_id=agent_id or new_agent_id(),
            name=name,
            role=str(role),
            description=description,
            capabilities=list(capabilities or []),
            metadata=dict(metadata or {}),
        )

    def has_capability(self, capability: str) -> bool:
        """Return ``True`` if the agent declares ``capability``."""
        return capability in self.capabilities
