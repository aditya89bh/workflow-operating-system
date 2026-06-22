import json

from workflow_os.exception.record import ExceptionRecord
from workflow_os.learning import organizational_dashboard
from workflow_os.memory.record import MemoryRecord


def rec(workflow_id, event_type, step_id=None, duration=None):
    metadata = {"duration_seconds": duration} if duration is not None else None
    return MemoryRecord.create(
        workflow_id=workflow_id,
        event_type=event_type,
        step_id=step_id,
        metadata=metadata,
    )


def build():
    return [
        rec("good", "workflow_completed"),
        rec("good", "workflow_completed"),
        rec("bad", "workflow_failed"),
        rec("bad", "workflow_failed"),
        rec("bad", "step_completed", "slow", 5.0),
        rec("bad", "step_completed", "slow", 6.0),
    ]


def test_dashboard_structure():
    data = organizational_dashboard(build())
    assert set(data) >= {
        "maturity",
        "totals",
        "top_successful_workflows",
        "top_failing_workflows",
        "recurring_bottlenecks",
        "trends",
    }
    assert data["totals"]["workflows"] == 2


def test_dashboard_is_json_serializable():
    exceptions = [ExceptionRecord.create(workflow_id="bad", exception_type="timeout")]
    data = organizational_dashboard(build(), exceptions=exceptions)
    encoded = json.dumps(data)
    assert isinstance(encoded, str)


def test_dashboard_top_failing():
    data = organizational_dashboard(build())
    failing_ids = {row["workflow_id"] for row in data["top_failing_workflows"]}
    assert "bad" in failing_ids


def test_empty_dashboard():
    data = organizational_dashboard()
    assert data["totals"]["workflows"] == 0
    assert data["maturity"]["overall"] == 0.0
