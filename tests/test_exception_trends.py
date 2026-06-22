from datetime import datetime, timezone

from workflow_os.exception import (
    ExceptionRecord,
    failures_over_time,
    recurring_failures,
    workflow_risk_reports,
)


def at(day, exception_id, workflow_id="wf", exception_type="timeout", severity="high"):
    return ExceptionRecord.create(
        workflow_id=workflow_id,
        exception_type=exception_type,
        severity=severity,
        detected_at=datetime(2026, 1, day, 12, 0, tzinfo=timezone.utc),
        exception_id=exception_id,
    )


def test_failures_over_time_by_day():
    exceptions = [at(1, "1"), at(1, "2"), at(3, "3")]
    assert failures_over_time(exceptions) == {"2026-01-01": 2, "2026-01-03": 1}


def test_recurring_failures():
    exceptions = [
        at(1, "1", workflow_id="wf1", exception_type="timeout"),
        at(2, "2", workflow_id="wf1", exception_type="timeout"),
        at(3, "3", workflow_id="wf2", exception_type="step_failure"),
    ]
    recurring = recurring_failures(exceptions, min_count=2)
    assert recurring == {"wf1:timeout": 2}


def test_workflow_risk_reports_ordered():
    exceptions = [
        at(1, "1", workflow_id="risky", severity="critical"),
        at(2, "2", workflow_id="risky", severity="high"),
        at(3, "3", workflow_id="calm", severity="low"),
    ]
    reports = workflow_risk_reports(exceptions)
    assert reports[0].workflow_id == "risky"
    assert reports[0].total == 2
    assert reports[0].risk_score > reports[1].risk_score
    assert reports[1].workflow_id == "calm"
