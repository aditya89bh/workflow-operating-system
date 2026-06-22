from workflow_os.agents import Agent


def test_create_fills_id():
    agent = Agent.create(name="Coordinator")
    assert agent.agent_id
    assert agent.name == "Coordinator"
    assert agent.role == "executor"
    assert agent.capabilities == []
    assert agent.metadata == {}


def test_create_full():
    agent = Agent.create(
        name="Planner",
        role="planner",
        description="Builds plans",
        capabilities=["plan", "order"],
        metadata={"team": "ops"},
    )
    assert agent.role == "planner"
    assert agent.description == "Builds plans"
    assert agent.has_capability("plan")
    assert not agent.has_capability("execute")
    assert agent.metadata == {"team": "ops"}


def test_capabilities_independent():
    a = Agent.create(name="A")
    b = Agent.create(name="B")
    a.capabilities.append("x")
    assert b.capabilities == []
