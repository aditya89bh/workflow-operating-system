from workflow_os.analytics import step_duration_metrics, step_durations
from workflow_os.memory.record import MemoryRecord


def rec(workflow_id, event_type, step_id=None, duration=None):
    metadata = {"duration_seconds": duration} if duration is not None else None
    return MemoryRecord.create(
        workflow_id=workflow_id,
        event_type=event_type,
        step_id=step_id,
        metadata=metadata,
    )


def test_step_durations_grouped():
    records = [
        rec("wf1", "step_completed", "review", 5.0),
        rec("wf2", "step_completed", "review", 7.0),
        rec("wf1", "step_failed", "build", 3.0),
        rec("wf1", "step_started", "review"),  # ignored
    ]
    durations = step_durations(records)
    assert durations == {"review": [5.0, 7.0], "build": [3.0]}


def test_step_duration_metrics():
    records = [
        rec("wf1", "step_completed", "review", 5.0),
        rec("wf2", "step_completed", "review", 7.0),
    ]
    metrics = step_duration_metrics(records)
    assert metrics["review"].count == 2
    assert metrics["review"].mean == 6.0
    assert metrics["review"].maximum == 7.0
