import pytest

from workflow_os.exception import (
    ExceptionNotFoundError,
    ExceptionQuery,
    ExceptionRecord,
    ExceptionStore,
    SQLiteExceptionStore,
)


def make(**kwargs):
    base = dict(workflow_id="wf", message="boom")
    base.update(kwargs)
    return ExceptionRecord.create(**base)


def test_is_protocol_instance():
    store = SQLiteExceptionStore()
    assert isinstance(store, ExceptionStore)
    store.close()


def test_round_trip_preserves_fields():
    store = SQLiteExceptionStore()
    record = make(
        exception_type="timeout",
        severity="high",
        step_id="s1",
        source="detector",
        metadata={"k": "v"},
    )
    store.add(record)
    loaded = store.get(record.exception_id)
    assert loaded.exception_type == "timeout"
    assert loaded.severity == "high"
    assert loaded.step_id == "s1"
    assert loaded.source == "detector"
    assert loaded.resolved is False
    assert loaded.metadata == {"k": "v"}
    assert loaded.detected_at == record.detected_at
    store.close()


def test_update_and_delete():
    store = SQLiteExceptionStore()
    record = make()
    store.add(record)
    record.resolved = True
    store.update(record)
    assert store.get(record.exception_id).resolved is True

    store.delete(record.exception_id)
    with pytest.raises(ExceptionNotFoundError):
        store.get(record.exception_id)
    store.close()


def test_query(tmp_path):
    db = tmp_path / "exceptions.db"
    store = SQLiteExceptionStore(str(db))
    store.add(make(exception_id="1", workflow_id="wf1"))
    store.add(make(exception_id="2", workflow_id="wf2"))
    assert {r.exception_id for r in store.query(ExceptionQuery(workflow_id="wf1"))} == {
        "1"
    }
    assert len(store.list()) == 2
    store.close()
