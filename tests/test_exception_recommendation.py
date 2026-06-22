import pytest

from workflow_os.exception import (
    ExceptionRecord,
    recommend_action,
    recommend_recovery,
)


def make(exception_type):
    return ExceptionRecord.create(workflow_id="wf", exception_type=exception_type)


@pytest.mark.parametrize(
    "exception_type,expected",
    [
        ("timeout", "retry"),
        ("step_failure", "retry_step"),
        ("workflow_failure", "restart_workflow"),
        ("missing_resource", "provision_resource"),
        ("approval_failure", "escalate_approval"),
        ("validation_failure", "fix_and_resubmit"),
        ("unknown", "manual_review"),
    ],
)
def test_recommend_action(exception_type, expected):
    assert recommend_action(make(exception_type)) == expected


def test_unknown_type_defaults_to_manual_review():
    assert recommend_action(make("nonsense")) == "manual_review"


def test_recommend_recovery_is_deterministic():
    exception = make("timeout")
    a = recommend_recovery(exception, actor="ops")
    b = recommend_recovery(exception, actor="ops")
    assert a.action == b.action == "retry"
    assert a.status == "pending"
    assert a.exception_id == exception.exception_id
    assert a.metadata["exception_type"] == "timeout"
