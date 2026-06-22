from datetime import datetime, timezone

from workflow_os.analytics import (
    approval_trends,
    exception_trends,
    failure_trends,
    trend_report,
    workflow_completion_trends,
)
from workflow_os.approval import ApprovalRequest
from workflow_os.exception.record import ExceptionRecord
from workflow_os.memory.record import MemoryRecord


def day(d):
    return datetime(2026, 1, d, tzinfo=timezone.utc)


def test_workflow_and_failure_trends():
    records = [
        MemoryRecord.create(workflow_id="wf1", event_type="workflow_completed", timestamp=day(1)),
        MemoryRecord.create(workflow_id="wf2", event_type="workflow_completed", timestamp=day(1)),
        MemoryRecord.create(workflow_id="wf3", event_type="workflow_failed", timestamp=day(2)),
    ]
    assert workflow_completion_trends(records) == {"2026-01-01": 2}
    assert failure_trends(records) == {"2026-01-02": 1}


def test_approval_and_exception_trends():
    approvals = [
        ApprovalRequest.create(workflow_id="wf", requester="r", title="t", created_at=day(1)),
        ApprovalRequest.create(workflow_id="wf", requester="r", title="t", created_at=day(1)),
    ]
    exceptions = [
        ExceptionRecord.create(workflow_id="wf", detected_at=day(3)),
    ]
    assert approval_trends(approvals) == {"2026-01-01": 2}
    assert exception_trends(exceptions) == {"2026-01-03": 1}


def test_trend_report_combines():
    records = [
        MemoryRecord.create(workflow_id="wf1", event_type="workflow_completed", timestamp=day(1)),
    ]
    report = trend_report(records)
    assert report.workflow_trends == {"2026-01-01": 1}
    assert report.approval_trends == {}
    assert report.exception_trends == {}
