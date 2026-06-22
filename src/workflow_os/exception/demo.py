"""A runnable demonstration of the exception handling layer.

The demo walks through the loop: it triggers a workflow failure, records the
exception, generates a deterministic recovery recommendation, retries the
workflow, and prints an exception report.
"""

from __future__ import annotations

from datetime import timedelta

from workflow_os.exception.classification import ExceptionType
from workflow_os.exception.deadline import Deadline, detect_deadline_failures
from workflow_os.exception.effectiveness import compute_effectiveness
from workflow_os.exception.recommendation import recommend_recovery
from workflow_os.exception.record import utcnow
from workflow_os.exception.recovery import RecoveryAction, RecoveryStatus
from workflow_os.exception.retry import RetryStrategy
from workflow_os.exception.sqlite_store import SQLiteExceptionStore
from workflow_os.exception.store import ExceptionStore
from workflow_os.exception.trends import recurring_failures, workflow_risk_reports


def run_demo(store: ExceptionStore | None = None) -> ExceptionStore:
    """Run the exception handling demonstration, printing each stage."""
    store = store if store is not None else SQLiteExceptionStore()
    now = utcnow()

    # 1. Trigger a workflow failure (a missed deadline).
    print("1. triggering workflow failure")
    deadlines = [
        Deadline("wf-invoice-001", now - timedelta(hours=2), step_id="approve"),
        Deadline("wf-invoice-001", now - timedelta(hours=5), step_id="pay"),
    ]
    detected = detect_deadline_failures(deadlines, now=now)
    print(f"   detected {len(detected)} failure(s) of type {ExceptionType.TIMEOUT}")

    # 2. Record the exceptions.
    print("\n2. recording exceptions")
    for record in detected:
        store.add(record)
    exception = store.list()[0]
    print(f"   recorded {exception.exception_id[:8]} ({exception.severity})")

    # 3. Generate a recovery recommendation.
    print("\n3. generating recovery recommendation")
    recommendation = recommend_recovery(exception, actor="ops")
    print(f"   recommended action: {recommendation.action}")

    # 4. Retry the workflow.
    print("\n4. retrying workflow")
    strategy = RetryStrategy(max_attempts=2)
    attempt = strategy.next_attempt(exception, attempts_made=0, actor="ops")
    assert attempt is not None
    resolved = RecoveryAction.create(
        exception_id=exception.exception_id,
        action="retry",
        actor="ops",
        status=RecoveryStatus.SUCCEEDED.value,
        timestamp=now + timedelta(seconds=90),
    )
    exception.resolved = True
    store.update(exception)
    recoveries = [attempt, resolved]
    print(f"   retry attempt {attempt.metadata['attempt']} -> {resolved.status}")

    # 5. Generate an exception report.
    print("\n5. exception report")
    print(f"   recurring failures: {recurring_failures(store.list())}")
    risk = workflow_risk_reports(store.list())
    if risk:
        top = risk[0]
        print(f"   top risk workflow: {top.workflow_id} (score {top.risk_score})")
    metrics = compute_effectiveness(store.list(), recoveries)
    print(f"   recovery success rate: {metrics.recovery_success_rate:.0%}")
    if metrics.mean_recovery_seconds is not None:
        print(f"   mean recovery time: {metrics.mean_recovery_seconds:.0f}s")

    print("\ndone.")
    return store


if __name__ == "__main__":  # pragma: no cover
    run_demo()
