from workflow_os.agents import ALL_AGENT_ROLES, AgentRole, normalize_role


def test_role_values():
    assert {r.value for r in AgentRole} == {
        "coordinator",
        "planner",
        "executor",
        "compliance",
        "memory",
    }


def test_all_roles_complete():
    assert len(ALL_AGENT_ROLES) == 5


def test_normalize_role():
    assert normalize_role("planner") == "planner"
    assert normalize_role("nonsense") == "executor"
