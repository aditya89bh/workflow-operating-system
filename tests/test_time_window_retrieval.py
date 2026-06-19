from datetime import datetime, timedelta, timezone

from workflow_os.memory import (
    MemoryRecord,
    SQLiteMemoryStore,
    get_events_between,
    get_events_since,
)

BASE = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)


def populate() -> SQLiteMemoryStore:
    store = SQLiteMemoryStore()
    for minute in range(5):
        store.add(
            MemoryRecord.create(
                workflow_id="wf",
                event_type="step_completed",
                timestamp=BASE + timedelta(minutes=minute),
            )
        )
    return store


def test_get_events_since_is_inclusive():
    store = populate()
    since = BASE + timedelta(minutes=2)
    events = get_events_since(store, since)
    assert len(events) == 3
    assert all(record.timestamp >= since for record in events)


def test_get_events_between_inclusive_window():
    store = populate()
    start = BASE + timedelta(minutes=1)
    end = BASE + timedelta(minutes=3)
    events = get_events_between(store, start, end)
    assert len(events) == 3
    assert events[0].timestamp == start
    assert events[-1].timestamp == end


def test_window_with_no_matches():
    store = populate()
    start = BASE + timedelta(hours=1)
    end = BASE + timedelta(hours=2)
    assert get_events_between(store, start, end) == []
