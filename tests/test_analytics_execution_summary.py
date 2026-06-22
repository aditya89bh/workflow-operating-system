from datetime import datetime, timedelta, timezone

from workflow_os.analytics import execution_summaries
from workflow_os.memory.record import MemoryRecord


def rec(workflow_id, event_type, step_id=None, ts=None):
    return MemoryRecord.create(
        workflow_id=workflow_id, event_type=event_type, step_id=step_id, timestamp=ts
    )


def test_execution_summary_completed():
    start = datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc)
    end = start + timedelta(seconds=30)
    records = [
        rec("wf1", "workflow_started", ts=start),
        rec("wf1", "step_completed", "a", ts=start + timedelta(seconds=10)),
        rec("wf1", "step_completed", "b", ts=start + timedelta(seconds=20)),
        rec("wf1", "workflow_completed", ts=end),
    ]
    summary = execution_summaries(records)[0]
    assert summary.status == "completed"
    assert summary.duration == 30.0
    assert summary.steps_completed == 2
    assert summary.steps_failed == 0


def test_execution_summary_failed_and_running():
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    records = [
        rec("wf1", "workflow_started", ts=start),
        rec("wf1", "step_failed", "a", ts=start),
        rec("wf1", "workflow_failed", ts=start + timedelta(seconds=5)),
        rec("wf2", "workflow_started", ts=start),
    ]
    summaries = {s.workflow_id: s for s in execution_summaries(records)}
    assert summaries["wf1"].status == "failed"
    assert summaries["wf1"].steps_failed == 1
    assert summaries["wf2"].status == "running"
    assert summaries["wf2"].duration is None
