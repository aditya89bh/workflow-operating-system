from datetime import datetime, timezone

import pytest

from workflow_os.memory import (
    MemoryEventType,
    MemoryNotFoundError,
    MemoryQuery,
    MemoryRecord,
    MemoryStore,
    SQLiteMemoryStore,
)


def make_record(event_id, *, day, event_type=MemoryEventType.WORKFLOW_STARTED, **kw):
    return MemoryRecord.create(
        workflow_id=kw.get("workflow_id", "wf"),
        event_type=event_type,
        step_id=kw.get("step_id"),
        actor=kw.get("actor"),
        confidence=kw.get("confidence", 1.0),
        metadata=kw.get("metadata"),
        event_id=event_id,
        timestamp=datetime(2026, 1, day, tzinfo=timezone.utc),
    )


def test_satisfies_protocol():
    store = SQLiteMemoryStore()
    assert isinstance(store, MemoryStore)


def test_add_get_round_trip():
    store = SQLiteMemoryStore()
    record = make_record("e1", day=1, actor="alice", metadata={"k": "v"})
    store.add(record)
    loaded = store.get("e1")
    assert loaded == record


def test_list_is_ordered_by_timestamp():
    store = SQLiteMemoryStore()
    store.add(make_record("e2", day=2))
    store.add(make_record("e1", day=1))
    assert [r.event_id for r in store.list()] == ["e1", "e2"]


def test_query_filters():
    store = SQLiteMemoryStore()
    store.add(make_record("e1", day=1, event_type=MemoryEventType.WORKFLOW_STARTED))
    store.add(make_record("e2", day=2, event_type=MemoryEventType.STEP_COMPLETED))
    q = MemoryQuery(event_types=(MemoryEventType.STEP_COMPLETED,))
    assert [r.event_id for r in store.query(q)] == ["e2"]


def test_delete_and_missing():
    store = SQLiteMemoryStore()
    store.add(make_record("e1", day=1))
    store.delete("e1")
    assert store.list() == []
    with pytest.raises(MemoryNotFoundError):
        store.get("e1")
    with pytest.raises(MemoryNotFoundError):
        store.delete("e1")


def test_persists_to_file(tmp_path):
    db = str(tmp_path / "memory.db")
    with SQLiteMemoryStore(db) as store:
        store.add(make_record("e1", day=1, metadata={"x": 1}))
    with SQLiteMemoryStore(db) as reopened:
        loaded = reopened.get("e1")
        assert loaded.metadata == {"x": 1}
        assert loaded.timestamp.tzinfo is not None
