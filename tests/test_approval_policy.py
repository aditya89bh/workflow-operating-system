from workflow_os.approval import ApprovalPolicy, PolicyType


def test_create_defaults():
    policy = ApprovalPolicy.create(name="default")
    assert policy.policy_id
    assert policy.name == "default"
    assert policy.policy_type == "single"
    assert policy.required_approvals == 1
    assert policy.escalation_timeout is None
    assert policy.metadata == {}


def test_create_full():
    policy = ApprovalPolicy.create(
        name="budget",
        policy_type=PolicyType.MULTI.value,
        required_approvals=2,
        escalation_timeout=3600.0,
        metadata={"tier": "high"},
    )
    assert policy.policy_type == "multi"
    assert policy.required_approvals == 2
    assert policy.escalation_timeout == 3600.0
    assert policy.metadata == {"tier": "high"}


def test_policy_type_values():
    assert {t.value for t in PolicyType} == {
        "single",
        "multi",
        "sequential",
        "parallel",
    }
