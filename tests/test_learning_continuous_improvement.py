from workflow_os.exception.record import ExceptionRecord
from workflow_os.learning import (
    continuous_improvement_report,
    improvement_opportunities,
)
from workflow_os.memory.record import MemoryRecord


def rec(workflow_id, event_type, step_id=None):
    return MemoryRecord.create(
        workflow_id=workflow_id, event_type=event_type, step_id=step_id
    )


def build_records():
    return [
        rec("bad", "workflow_failed"),
        rec("bad", "workflow_failed"),
        rec("bad", "workflow_completed"),
    ]


def test_improvement_opportunities_collects_categories():
    exceptions = [
        ExceptionRecord.create(workflow_id="bad", exception_type="timeout")
        for _ in range(2)
    ]
    opps = improvement_opportunities(build_records(), exceptions=exceptions)
    categories = {o.category for o in opps}
    assert "workflow" in categories
    assert "sop" in categories


def test_continuous_improvement_report():
    report = continuous_improvement_report(build_records())
    assert report.maturity is not None
    assert report.trends.failure_trends
    assert isinstance(report.opportunities, list)


def test_empty_report():
    report = continuous_improvement_report()
    assert report.opportunities == []
    assert report.maturity.overall == 0.0
