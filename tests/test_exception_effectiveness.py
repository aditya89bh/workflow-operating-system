from datetime import timedelta

from workflow_os.exception import (
    ExceptionRecord,
    RecoveryAction,
    compute_effectiveness,
    mean_recovery_time,
    recovery_success_rate,
    retry_success_rate,
    utcnow,
)


def make_exception(exception_id, detected_at):
    return ExceptionRecord.create(
        workflow_id="wf", exception_id=exception_id, detected_at=detected_at
    )


def test_recovery_success_rate_ignores_pending():
    recoveries = [
        RecoveryAction.create(exception_id="1", action="retry", status="succeeded"),
        RecoveryAction.create(exception_id="2", action="retry", status="failed"),
        RecoveryAction.create(exception_id="3", action="retry", status="pending"),
    ]
    assert recovery_success_rate(recoveries) == 0.5


def test_retry_success_rate_only_retries():
    recoveries = [
        RecoveryAction.create(exception_id="1", action="retry", status="succeeded"),
        RecoveryAction.create(exception_id="2", action="fallback", status="failed"),
    ]
    assert retry_success_rate(recoveries) == 1.0


def test_mean_recovery_time():
    now = utcnow()
    exceptions = [make_exception("1", now), make_exception("2", now)]
    recoveries = [
        RecoveryAction.create(
            exception_id="1",
            action="retry",
            status="succeeded",
            timestamp=now + timedelta(seconds=60),
        ),
        RecoveryAction.create(
            exception_id="2",
            action="retry",
            status="succeeded",
            timestamp=now + timedelta(seconds=120),
        ),
    ]
    assert mean_recovery_time(exceptions, recoveries) == 90.0


def test_compute_effectiveness():
    now = utcnow()
    exceptions = [make_exception("1", now)]
    recoveries = [
        RecoveryAction.create(
            exception_id="1",
            action="retry",
            status="succeeded",
            timestamp=now + timedelta(seconds=30),
        )
    ]
    metrics = compute_effectiveness(exceptions, recoveries)
    assert metrics.total_recoveries == 1
    assert metrics.successful_recoveries == 1
    assert metrics.recovery_success_rate == 1.0
    assert metrics.mean_recovery_seconds == 30.0


def test_empty_rates_are_zero():
    assert recovery_success_rate([]) == 0.0
    assert mean_recovery_time([], []) is None
