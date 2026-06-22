"""Agent registry.

A deterministic, in-memory registry of agents. Agents can be registered,
unregistered, looked up by id, listed, and filtered by role.
"""

from __future__ import annotations

from workflow_os.agents.record import Agent

AgentList = list[Agent]


class AgentNotFoundError(KeyError):
    """Raised when an agent id cannot be found in the registry."""


class AgentAlreadyRegisteredError(ValueError):
    """Raised when registering an agent id that already exists."""


class AgentRegistry:
    """A registry mapping agent ids to :class:`Agent` records."""

    def __init__(self) -> None:
        self._agents: dict[str, Agent] = {}

    def register(self, agent: Agent) -> Agent:
        """Register ``agent``, raising if its id is already registered."""
        if agent.agent_id in self._agents:
            raise AgentAlreadyRegisteredError(agent.agent_id)
        self._agents[agent.agent_id] = agent
        return agent

    def unregister(self, agent_id: str) -> None:
        """Remove an agent by id, raising if it is not registered."""
        if agent_id not in self._agents:
            raise AgentNotFoundError(agent_id)
        del self._agents[agent_id]

    def lookup(self, agent_id: str) -> Agent:
        """Return the agent with ``agent_id`` or raise if missing."""
        try:
            return self._agents[agent_id]
        except KeyError as exc:
            raise AgentNotFoundError(agent_id) from exc

    def list(self) -> AgentList:
        """Return all registered agents ordered by id."""
        return [self._agents[key] for key in sorted(self._agents)]

    def list_by_role(self, role: str) -> AgentList:
        """Return all registered agents with a given role, ordered by id."""
        return [agent for agent in self.list() if agent.role == str(role)]

    def find_by_role(self, role: str) -> Agent | None:
        """Return the first registered agent with ``role``, or ``None``."""
        agents = self.list_by_role(role)
        return agents[0] if agents else None

    def __contains__(self, agent_id: object) -> bool:
        return agent_id in self._agents

    def __len__(self) -> int:
        return len(self._agents)
