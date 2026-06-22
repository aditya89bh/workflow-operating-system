from datetime import datetime

from workflow_os.exception import ExceptionRecord


def test_create_fills_id_and_timestamp():
    record = ExceptionRecord.create(workflow_id="wf", message="boom")
    assert record.exception_id
    assert isinstance(record.detected_at, datetime)
    assert record.exception_type == "unknown"
    assert record.severity == "medium"
    assert record.resolved is False
    assert record.step_id is None
    assert record.metadata == {}


def test_create_full_fields():
    record = ExceptionRecord.create(
        workflow_id="wf",
        exception_type="timeout",
        severity="high",
        message="missed deadline",
        step_id="s1",
        source="deadline-detector",
        metadata={"deadline": "2026-01-01"},
    )
    assert record.exception_type == "timeout"
    assert record.severity == "high"
    assert record.step_id == "s1"
    assert record.source == "deadline-detector"
    assert record.metadata == {"deadline": "2026-01-01"}


def test_metadata_independent_between_records():
    a = ExceptionRecord.create(workflow_id="a")
    b = ExceptionRecord.create(workflow_id="b")
    a.metadata["x"] = 1
    assert b.metadata == {}
