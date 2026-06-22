from workflow_os.analytics import workflow_completion_metrics
from workflow_os.memory.record import MemoryRecord


def rec(workflow_id, event_type):
    return MemoryRecord.create(workflow_id=workflow_id, event_type=event_type)


def test_completion_metrics_basic():
    records = [
        rec("wf1", "workflow_started"),
        rec("wf1", "workflow_completed"),
        rec("wf2", "workflow_started"),
        rec("wf2", "workflow_failed"),
        rec("wf3", "workflow_started"),
    ]
    metrics = workflow_completion_metrics(records)
    assert metrics.total_workflows == 3
    assert metrics.completed_workflows == 1
    assert round(metrics.completion_rate, 3) == round(1 / 3, 3)


def test_completion_metrics_empty():
    metrics = workflow_completion_metrics([])
    assert metrics.total_workflows == 0
    assert metrics.completion_rate == 0.0
