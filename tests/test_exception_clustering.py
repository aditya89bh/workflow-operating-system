from workflow_os.exception import (
    ExceptionRecord,
    RecoveryAction,
    cluster_by_recovery_outcome,
    cluster_by_severity,
    cluster_by_type,
    cluster_by_workflow,
    recovery_outcome,
)


def make(exception_id, workflow_id="wf", exception_type="timeout", severity="high"):
    return ExceptionRecord.create(
        workflow_id=workflow_id,
        exception_type=exception_type,
        severity=severity,
        exception_id=exception_id,
    )


def test_cluster_by_type():
    exceptions = [
        make("1", exception_type="timeout"),
        make("2", exception_type="timeout"),
        make("3", exception_type="step_failure"),
    ]
    clusters = cluster_by_type(exceptions)
    assert {k: len(v) for k, v in clusters.items()} == {"timeout": 2, "step_failure": 1}


def test_cluster_by_workflow_and_severity():
    exceptions = [
        make("1", workflow_id="wf1", severity="low"),
        make("2", workflow_id="wf2", severity="critical"),
    ]
    assert set(cluster_by_workflow(exceptions)) == {"wf1", "wf2"}
    assert set(cluster_by_severity(exceptions)) == {"low", "critical"}


def test_recovery_outcome():
    recoveries = [
        RecoveryAction.create(exception_id="1", action="retry", status="failed"),
        RecoveryAction.create(exception_id="1", action="retry", status="succeeded"),
        RecoveryAction.create(exception_id="2", action="retry", status="failed"),
    ]
    assert recovery_outcome("1", recoveries) == "succeeded"
    assert recovery_outcome("2", recoveries) == "failed"
    assert recovery_outcome("3", recoveries) == "none"


def test_cluster_by_recovery_outcome():
    exceptions = [make("1"), make("2"), make("3")]
    recoveries = [
        RecoveryAction.create(exception_id="1", action="retry", status="succeeded"),
        RecoveryAction.create(exception_id="2", action="retry", status="failed"),
    ]
    clusters = cluster_by_recovery_outcome(exceptions, recoveries)
    assert {e.exception_id for e in clusters["succeeded"]} == {"1"}
    assert {e.exception_id for e in clusters["failed"]} == {"2"}
    assert {e.exception_id for e in clusters["none"]} == {"3"}
