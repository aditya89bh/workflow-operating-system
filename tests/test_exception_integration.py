from datetime import timedelta

from workflow_os.exception import (
    Deadline,
    RecoveryAction,
    RetryStrategy,
    SQLiteExceptionStore,
    cluster_by_type,
    compute_effectiveness,
    detect_deadline_failures,
    recommend_recovery,
    recurring_failures,
    utcnow,
    workflow_risk_reports,
)


def test_end_to_end_exception_flow():
    now = utcnow()
    store = SQLiteExceptionStore()

    # 1. Detect failures from passed deadlines.
    deadlines = [
        Deadline("wf1", now - timedelta(hours=1)),
        Deadline("wf1", now - timedelta(hours=2)),
        Deadline("wf2", now + timedelta(hours=1)),
    ]
    detected = detect_deadline_failures(deadlines, now=now)
    assert len(detected) == 2
    for record in detected:
        store.add(record)

    # 2. Recommend and run recovery for the first exception.
    exception = store.list()[0]
    recommendation = recommend_recovery(exception, actor="ops")
    assert recommendation.action == "retry"

    strategy = RetryStrategy(max_attempts=2)
    retry = strategy.next_attempt(exception, attempts_made=0, actor="ops")
    assert retry is not None
    succeeded = RecoveryAction.create(
        exception_id=exception.exception_id,
        action="retry",
        status="succeeded",
        timestamp=now + timedelta(seconds=45),
    )
    recoveries = [retry, succeeded]

    # 3. Analyse.
    clusters = cluster_by_type(store.list())
    assert "timeout" in clusters
    assert recurring_failures(store.list()) == {"wf1:timeout": 2}

    reports = workflow_risk_reports(store.list())
    assert reports[0].workflow_id == "wf1"

    metrics = compute_effectiveness(store.list(), recoveries)
    assert metrics.successful_recoveries == 1
    assert metrics.mean_recovery_seconds == 45.0
    store.close()
