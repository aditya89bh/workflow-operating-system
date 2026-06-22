from datetime import datetime

from workflow_os.exception import RecoveryAction, RecoveryStatus


def test_create_defaults():
    action = RecoveryAction.create(exception_id="e1", action="retry")
    assert action.recovery_id
    assert action.exception_id == "e1"
    assert action.action == "retry"
    assert action.status == "pending"
    assert action.actor is None
    assert isinstance(action.timestamp, datetime)
    assert action.metadata == {}


def test_create_full():
    action = RecoveryAction.create(
        exception_id="e1",
        action="fallback",
        actor="ops",
        status=RecoveryStatus.SUCCEEDED.value,
        metadata={"attempt": 2},
    )
    assert action.actor == "ops"
    assert action.status == "succeeded"
    assert action.metadata == {"attempt": 2}


def test_status_values():
    assert {s.value for s in RecoveryStatus} == {"pending", "succeeded", "failed"}
