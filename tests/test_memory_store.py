from datetime import datetime, timezone

from workflow_os.memory import (
    MemoryEventType,
    MemoryQuery,
    MemoryRecord,
    apply_query,
)


def record(event_id, *, event_type, day, workflow_id="wf", actor=None, step_id=None):
    return MemoryRecord.create(
        workflow_id=workflow_id,
        event_type=event_type,
        actor=actor,
        step_id=step_id,
        event_id=event_id,
        timestamp=datetime(2026, 1, day, tzinfo=timezone.utc),
    )


def sample():
    return [
        record("e1", event_type=MemoryEventType.WORKFLOW_STARTED, day=3),
        record("e2", event_type=MemoryEventType.STEP_STARTED, day=1, step_id="s1"),
        record("e3", event_type=MemoryEventType.WORKFLOW_COMPLETED, day=2, actor="bob"),
    ]


def test_apply_query_orders_ascending_by_default():
    ids = [r.event_id for r in apply_query(sample(), MemoryQuery())]
    assert ids == ["e2", "e3", "e1"]


def test_apply_query_orders_descending():
    ids = [r.event_id for r in apply_query(sample(), MemoryQuery(order="desc"))]
    assert ids == ["e1", "e3", "e2"]


def test_apply_query_filters_by_event_type():
    q = MemoryQuery(event_types=(MemoryEventType.STEP_STARTED,))
    assert [r.event_id for r in apply_query(sample(), q)] == ["e2"]


def test_apply_query_filters_by_actor_and_step():
    assert [r.event_id for r in apply_query(sample(), MemoryQuery(actor="bob"))] == ["e3"]
    assert [r.event_id for r in apply_query(sample(), MemoryQuery(step_id="s1"))] == ["e2"]


def test_apply_query_time_window_and_limit():
    since = datetime(2026, 1, 2, tzinfo=timezone.utc)
    q = MemoryQuery(since=since, limit=1)
    assert [r.event_id for r in apply_query(sample(), q)] == ["e3"]
