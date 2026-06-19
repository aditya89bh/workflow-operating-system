from datetime import datetime, timedelta, timezone

from workflow_os.memory import (
    MemoryRecord,
    SQLiteMemoryStore,
    prune_by_max_age,
    prune_to_max_count,
    prune_workflow,
)

BASE = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)


def populate(workflow_id: str = "wf", count: int = 5) -> SQLiteMemoryStore:
    store = SQLiteMemoryStore()
    for minute in range(count):
        store.add(
            MemoryRecord.create(
                workflow_id=workflow_id,
                event_type="step_completed",
                timestamp=BASE + timedelta(minutes=minute),
            )
        )
    return store


def test_prune_by_max_age():
    store = populate()
    now = BASE + timedelta(minutes=4)
    removed = prune_by_max_age(store, timedelta(minutes=2), now=now)
    assert removed == 2
    remaining = store.list()
    assert all(r.timestamp >= now - timedelta(minutes=2) for r in remaining)


def test_prune_to_max_count_keeps_newest():
    store = populate()
    removed = prune_to_max_count(store, 2)
    assert removed == 3
    remaining = sorted(store.list(), key=lambda r: r.timestamp)
    assert len(remaining) == 2
    assert remaining[0].timestamp == BASE + timedelta(minutes=3)


def test_prune_to_max_count_zero_removes_all():
    store = populate()
    assert prune_to_max_count(store, 0) == 5
    assert store.list() == []


def test_prune_workflow_scoped():
    store = populate("wf-a", 3)
    for minute in range(2):
        store.add(
            MemoryRecord.create(
                workflow_id="wf-b",
                event_type="step_completed",
                timestamp=BASE + timedelta(minutes=minute),
            )
        )
    removed = prune_workflow(store, "wf-a")
    assert removed == 3
    assert all(r.workflow_id == "wf-b" for r in store.list())
