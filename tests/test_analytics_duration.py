from workflow_os.analytics import (
    execution_duration_metrics,
    summarize_durations,
    workflow_durations,
)
from workflow_os.memory.record import MemoryRecord


def rec(workflow_id, event_type, duration=None):
    metadata = {"duration_seconds": duration} if duration is not None else None
    return MemoryRecord.create(
        workflow_id=workflow_id, event_type=event_type, metadata=metadata
    )


def test_workflow_durations():
    records = [
        rec("wf1", "workflow_completed", 10.0),
        rec("wf2", "workflow_failed", 20.0),
        rec("wf3", "workflow_completed"),  # no duration metadata
    ]
    durations = workflow_durations(records)
    assert durations == {"wf1": 10.0, "wf2": 20.0}


def test_execution_duration_metrics():
    records = [
        rec("wf1", "workflow_completed", 10.0),
        rec("wf2", "workflow_completed", 30.0),
    ]
    metrics = execution_duration_metrics(records)
    assert metrics.count == 2
    assert metrics.total == 40.0
    assert metrics.mean == 20.0
    assert metrics.minimum == 10.0
    assert metrics.maximum == 30.0


def test_summarize_empty():
    metrics = summarize_durations([])
    assert metrics.count == 0
    assert metrics.mean == 0.0
