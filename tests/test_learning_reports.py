from workflow_os.exception.record import ExceptionRecord
from workflow_os.learning import (
    learning_report,
    organizational_insights,
)
from workflow_os.memory.record import MemoryRecord


def rec(workflow_id, event_type):
    return MemoryRecord.create(workflow_id=workflow_id, event_type=event_type)


def build():
    return [
        rec("good", "workflow_completed"),
        rec("good", "workflow_completed"),
        rec("bad", "workflow_failed"),
        rec("bad", "workflow_failed"),
    ]


def test_organizational_insights():
    exceptions = [
        ExceptionRecord.create(workflow_id="bad", exception_type="timeout")
        for _ in range(2)
    ]
    insights = organizational_insights(build(), exceptions=exceptions)
    categories = {i.category for i in insights}
    assert {"success", "failure", "exception"} <= categories


def test_learning_report_summary():
    report = learning_report(build())
    assert report.summary["insight_count"] == len(report.insights)
    assert report.summary["recommendation_count"] == len(report.recommendations)
    assert report.recommendations


def test_empty_learning_report():
    report = learning_report()
    assert report.insights == []
    assert report.summary["insight_count"] == 0
