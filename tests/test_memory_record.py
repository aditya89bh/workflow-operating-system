from datetime import datetime, timezone

from workflow_os.memory import MemoryRecord


def test_create_fills_id_and_timestamp():
    record = MemoryRecord.create(workflow_id="wf", event_type="workflow_started")
    assert record.event_id
    assert record.workflow_id == "wf"
    assert record.event_type == "workflow_started"
    assert record.timestamp.tzinfo is not None
    assert record.step_id is None
    assert record.actor is None
    assert record.confidence == 1.0
    assert record.metadata == {}


def test_create_accepts_explicit_values():
    ts = datetime(2026, 1, 1, tzinfo=timezone.utc)
    record = MemoryRecord.create(
        workflow_id="wf",
        event_type="step_completed",
        step_id="s1",
        actor="alice",
        confidence=0.5,
        metadata={"note": "ok"},
        timestamp=ts,
        event_id="evt-1",
    )
    assert record.event_id == "evt-1"
    assert record.step_id == "s1"
    assert record.actor == "alice"
    assert record.confidence == 0.5
    assert record.metadata == {"note": "ok"}
    assert record.timestamp == ts


def test_event_ids_are_unique():
    a = MemoryRecord.create(workflow_id="wf", event_type="x")
    b = MemoryRecord.create(workflow_id="wf", event_type="x")
    assert a.event_id != b.event_id
