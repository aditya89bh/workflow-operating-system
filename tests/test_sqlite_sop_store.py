import pytest

from workflow_os.sop import (
    SOPNotFoundError,
    SOPQuery,
    SOPRecord,
    SQLiteSOPStore,
)


def _sop(**kwargs) -> SOPRecord:
    base = dict(title="Onboarding", workflow_type="onboarding")
    base.update(kwargs)
    return SOPRecord.create(**base)


def test_add_get_round_trip():
    store = SQLiteSOPStore()
    sop = _sop(
        description="how we onboard",
        author="hr",
        tags=["people", "hr"],
        metadata={"owner": "people-ops"},
        status="active",
    )
    store.add(sop)
    assert store.get(sop.sop_id) == sop


def test_update_existing():
    store = SQLiteSOPStore()
    sop = _sop()
    store.add(sop)
    sop.version = 2
    sop.status = "active"
    store.update(sop)
    loaded = store.get(sop.sop_id)
    assert loaded.version == 2
    assert loaded.status == "active"


def test_update_missing_raises():
    store = SQLiteSOPStore()
    with pytest.raises(SOPNotFoundError):
        store.update(_sop())


def test_get_and_delete_missing_raise():
    store = SQLiteSOPStore()
    with pytest.raises(SOPNotFoundError):
        store.get("missing")
    with pytest.raises(SOPNotFoundError):
        store.delete("missing")


def test_list_and_query():
    store = SQLiteSOPStore()
    store.add(_sop(title="a", workflow_type="onboarding"))
    store.add(_sop(title="b", workflow_type="incident"))
    assert len(store.list()) == 2
    incidents = store.query(SOPQuery(workflow_type="incident"))
    assert [s.title for s in incidents] == ["b"]


def test_delete_removes_record():
    store = SQLiteSOPStore()
    sop = _sop()
    store.add(sop)
    store.delete(sop.sop_id)
    assert store.list() == []
