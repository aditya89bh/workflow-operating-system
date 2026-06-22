from workflow_os.analytics import workflow_health_score
from workflow_os.exception.record import ExceptionRecord
from workflow_os.memory.record import MemoryRecord


def rec(workflow_id, event_type, step_id=None, duration=None):
    metadata = {"duration_seconds": duration} if duration is not None else None
    return MemoryRecord.create(
        workflow_id=workflow_id,
        event_type=event_type,
        step_id=step_id,
        metadata=metadata,
    )


def test_perfect_health():
    records = [
        rec("wf1", "workflow_started"),
        rec("wf1", "workflow_completed"),
    ]
    health = workflow_health_score(records)
    assert health.success_rate == 1.0
    assert health.failure_rate == 0.0
    assert health.recovery_rate == 1.0
    assert round(health.score, 6) == 1.0


def test_failed_workflow_lowers_score():
    records = [
        rec("wf1", "workflow_started"),
        rec("wf1", "workflow_failed"),
    ]
    health = workflow_health_score(records)
    assert health.failure_rate == 1.0
    assert health.score < 1.0


def test_recovery_rate_from_exceptions():
    records = [rec("wf1", "workflow_started"), rec("wf1", "workflow_completed")]
    exceptions = [
        ExceptionRecord.create(workflow_id="wf1", resolved=True),
        ExceptionRecord.create(workflow_id="wf1", resolved=False),
    ]
    health = workflow_health_score(records, exceptions=exceptions)
    assert health.recovery_rate == 0.5
    assert 0.0 <= health.score <= 1.0
