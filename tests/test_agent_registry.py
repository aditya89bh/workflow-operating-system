import pytest

from workflow_os.agents import (
    Agent,
    AgentAlreadyRegisteredError,
    AgentNotFoundError,
    AgentRegistry,
)


def make(role="executor", agent_id=None, name="A"):
    return Agent.create(name=name, role=role, agent_id=agent_id)


def test_register_and_lookup():
    registry = AgentRegistry()
    agent = make(agent_id="a1")
    registry.register(agent)
    assert registry.lookup("a1") is agent
    assert "a1" in registry
    assert len(registry) == 1


def test_duplicate_registration_raises():
    registry = AgentRegistry()
    registry.register(make(agent_id="a1"))
    with pytest.raises(AgentAlreadyRegisteredError):
        registry.register(make(agent_id="a1"))


def test_unregister():
    registry = AgentRegistry()
    registry.register(make(agent_id="a1"))
    registry.unregister("a1")
    with pytest.raises(AgentNotFoundError):
        registry.lookup("a1")
    with pytest.raises(AgentNotFoundError):
        registry.unregister("a1")


def test_list_and_by_role():
    registry = AgentRegistry()
    registry.register(make(agent_id="a1", role="coordinator"))
    registry.register(make(agent_id="a2", role="planner"))
    registry.register(make(agent_id="a3", role="planner"))
    assert [a.agent_id for a in registry.list()] == ["a1", "a2", "a3"]
    assert [a.agent_id for a in registry.list_by_role("planner")] == ["a2", "a3"]
    assert registry.find_by_role("coordinator").agent_id == "a1"
    assert registry.find_by_role("memory") is None
