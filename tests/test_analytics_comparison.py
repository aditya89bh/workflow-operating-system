from workflow_os.analytics import compare_workflows
from workflow_os.memory.record import MemoryRecord


def rec(workflow_id, event_type, step_id=None, duration=None):
    metadata = {"duration_seconds": duration} if duration is not None else None
    return MemoryRecord.create(
        workflow_id=workflow_id,
        event_type=event_type,
        step_id=step_id,
        metadata=metadata,
    )


def build_records():
    return [
        rec("wf1", "workflow_started"),
        rec("wf1", "step_completed", "a", 2.0),
        rec("wf1", "workflow_completed", duration=5.0),
        rec("wf2", "workflow_started"),
        rec("wf2", "step_failed", "a", 1.0),
        rec("wf2", "workflow_failed", duration=12.0),
    ]


def test_comparison_rows():
    report = compare_workflows(build_records())
    rows = {r.workflow_id: r for r in report.rows}
    assert rows["wf1"].completed is True
    assert rows["wf1"].duration == 5.0
    assert rows["wf1"].step_count == 1
    assert rows["wf2"].failed is True
    assert rows["wf2"].duration == 12.0


def test_fastest_and_slowest():
    report = compare_workflows(build_records())
    assert report.fastest == "wf1"
    assert report.slowest == "wf2"


def test_empty_comparison():
    report = compare_workflows([])
    assert report.rows == []
    assert report.fastest is None
