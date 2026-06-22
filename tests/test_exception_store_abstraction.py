import pytest

from workflow_os.exception import (
    ExceptionNotFoundError,
    ExceptionQuery,
    ExceptionRecord,
    ExceptionStore,
    InMemoryExceptionStore,
)


def make(**kwargs):
    base = dict(workflow_id="wf", message="boom")
    base.update(kwargs)
    return ExceptionRecord.create(**base)


def test_in_memory_store_is_protocol_instance():
    assert isinstance(InMemoryExceptionStore(), ExceptionStore)


def test_add_get_update_delete():
    store = InMemoryExceptionStore()
    record = make()
    store.add(record)
    assert store.get(record.exception_id) is record

    record.resolved = True
    store.update(record)
    assert store.get(record.exception_id).resolved is True

    store.delete(record.exception_id)
    with pytest.raises(ExceptionNotFoundError):
        store.get(record.exception_id)


def test_update_missing_raises():
    store = InMemoryExceptionStore()
    with pytest.raises(ExceptionNotFoundError):
        store.update(make())


def test_query_filters():
    store = InMemoryExceptionStore()
    store.add(make(exception_id="1", workflow_id="wf1", exception_type="timeout"))
    store.add(make(exception_id="2", workflow_id="wf2", severity="critical"))
    resolved = make(exception_id="3", workflow_id="wf1", resolved=True)
    store.add(resolved)

    assert len(store.list()) == 3
    assert {r.exception_id for r in store.query(ExceptionQuery(workflow_id="wf1"))} == {
        "1",
        "3",
    }
    assert {
        r.exception_id
        for r in store.query(ExceptionQuery(exception_types=("timeout",)))
    } == {"1"}
    assert {
        r.exception_id for r in store.query(ExceptionQuery(resolved=True))
    } == {"3"}
    assert {
        r.exception_id for r in store.query(ExceptionQuery(severities=("critical",)))
    } == {"2"}
