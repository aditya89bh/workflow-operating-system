from datetime import datetime, timezone

from workflow_os.analytics import (
    counts_by_day,
    workflow_statistics,
    workflow_summaries,
    workflow_trends,
)
from workflow_os.memory.record import MemoryRecord


def rec(workflow_id, event_type, step_id=None, duration=None, ts=None):
    metadata = {"duration_seconds": duration} if duration is not None else None
    return MemoryRecord.create(
        workflow_id=workflow_id,
        event_type=event_type,
        step_id=step_id,
        metadata=metadata,
        timestamp=ts,
    )


def build_records():
    return [
        rec("wf1", "workflow_started"),
        rec("wf1", "step_completed", "a", 2.0),
        rec("wf1", "workflow_completed", duration=5.0),
        rec("wf2", "workflow_started"),
        rec("wf2", "workflow_failed", duration=8.0),
    ]


def test_workflow_summaries():
    summaries = {s.workflow_id: s for s in workflow_summaries(build_records())}
    assert summaries["wf1"].status == "completed"
    assert summaries["wf1"].step_count == 1
    assert summaries["wf2"].status == "failed"


def test_workflow_statistics():
    stats = workflow_statistics(build_records())
    assert stats.total_workflows == 2
    assert stats.completed_workflows == 1
    assert stats.failed_workflows == 1
    assert stats.duration.count == 2


def test_counts_by_day_and_trends():
    day1 = datetime(2026, 1, 1, tzinfo=timezone.utc)
    day2 = datetime(2026, 1, 2, tzinfo=timezone.utc)
    records = [
        rec("wf1", "workflow_completed", ts=day1),
        rec("wf2", "workflow_completed", ts=day1),
        rec("wf3", "workflow_completed", ts=day2),
    ]
    trends = workflow_trends(records)
    assert trends == {"2026-01-01": 2, "2026-01-02": 1}
    assert counts_by_day(records, "workflow_completed") == trends
