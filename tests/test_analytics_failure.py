from workflow_os.analytics import workflow_failure_metrics
from workflow_os.memory.record import MemoryRecord


def rec(workflow_id, event_type):
    return MemoryRecord.create(workflow_id=workflow_id, event_type=event_type)


def test_failure_metrics_basic():
    records = [
        rec("wf1", "workflow_started"),
        rec("wf1", "workflow_completed"),
        rec("wf2", "workflow_started"),
        rec("wf2", "workflow_failed"),
    ]
    metrics = workflow_failure_metrics(records)
    assert metrics.total_workflows == 2
    assert metrics.failed_workflows == 1
    assert metrics.failure_rate == 0.5


def test_failure_metrics_empty():
    metrics = workflow_failure_metrics([])
    assert metrics.failed_workflows == 0
    assert metrics.failure_rate == 0.0
