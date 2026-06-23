"""Workflow + exception recovery integration demonstration.

Shows the flow ``workflow -> failure -> recovery -> reporting``: a workflow fails
at a step, the exception is recorded, a deterministic recovery is recommended and
applied successfully, and an effectiveness/risk report is produced.
"""

from __future__ import annotations

from datetime import timedelta

from workflow_os.demos.incident_management import build_workflow
from workflow_os.exception.classification import ExceptionType
from workflow_os.exception.effectiveness import compute_effectiveness
from workflow_os.exception.recommendation import recommend_recovery
from workflow_os.exception.record import ExceptionRecord, utcnow
from workflow_os.exception.recovery import RecoveryAction, RecoveryStatus
from workflow_os.exception.sqlite_store import SQLiteExceptionStore
from workflow_os.exception.trends import workflow_risk_reports
from workflow_os.memory.recorder import MemoryRecorder
from workflow_os.memory.sqlite_store import SQLiteMemoryStore


def run_demo() -> None:
    """Run the exception recovery integration demonstration and print a summary."""
    workflow = build_workflow()
    now = utcnow()

    # 1. Workflow + failure: a step fails partway through.
    print("1. workflow -> failing at the 'mitigate' step")
    recorder = MemoryRecorder(SQLiteMemoryStore(":memory:"))
    recorder.start(workflow)
    detect, triage, mitigate = workflow.steps[0], workflow.steps[1], workflow.steps[2]
    recorder.start_step(workflow, detect)
    recorder.complete_step(workflow, detect)
    recorder.start_step(workflow, triage)
    recorder.complete_step(workflow, triage)
    recorder.start_step(workflow, mitigate)
    recorder.fail_step(workflow, mitigate, reason="mitigation script timed out")
    recorder.fail(workflow, reason="incident mitigation failed")
    print(f"   {workflow.id!r} finished as {workflow.status.value!r}")

    # 2. Recovery: record the exception and apply a recommended recovery.
    print("\n2. failure -> recording exception")
    store = SQLiteExceptionStore(":memory:")
    exception = ExceptionRecord.create(
        workflow_id=workflow.id,
        exception_type=ExceptionType.TIMEOUT.value,
        severity="high",
        message="mitigation script timed out",
        step_id=mitigate.id,
        detected_at=now,
    )
    store.add(exception)
    recommendation = recommend_recovery(exception, actor="sre")
    print(f"   recommended action: {recommendation.action}")

    print("\n3. recovery -> applying recommended action")
    resolved = RecoveryAction.create(
        exception_id=exception.exception_id,
        action=recommendation.action,
        actor="sre",
        status=RecoveryStatus.SUCCEEDED.value,
        timestamp=now + timedelta(seconds=120),
    )
    exception.resolved = True
    store.update(exception)
    print(f"   recovery {resolved.action!r} -> {resolved.status}")

    # 4. Reporting: effectiveness and risk.
    print("\n4. reporting -> effectiveness and risk")
    metrics = compute_effectiveness(store.list(), [resolved])
    print(f"   recovery success rate: {metrics.recovery_success_rate:.0%}")
    risk = workflow_risk_reports(store.list())
    if risk:
        print(f"   top risk workflow: {risk[0].workflow_id} (score {risk[0].risk_score})")

    print("\ndone.")


if __name__ == "__main__":  # pragma: no cover
    run_demo()
