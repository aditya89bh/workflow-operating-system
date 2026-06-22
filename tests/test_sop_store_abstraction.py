from datetime import datetime, timedelta, timezone

from workflow_os.sop import SOPQuery, SOPRecord, apply_query, matches


def _sop(**kwargs) -> SOPRecord:
    base = dict(title="t", workflow_type="onboarding")
    base.update(kwargs)
    return SOPRecord.create(**base)


def test_empty_query_matches_everything():
    assert matches(_sop(), SOPQuery())


def test_filter_by_type_status_author_version():
    sop = _sop(status="active", author="hr", version=2)
    assert matches(sop, SOPQuery(workflow_type="onboarding"))
    assert matches(sop, SOPQuery(status="active"))
    assert matches(sop, SOPQuery(author="hr"))
    assert matches(sop, SOPQuery(version=2))
    assert not matches(sop, SOPQuery(status="draft"))


def test_tag_filter_requires_all_tags():
    sop = _sop(tags=["a", "b", "c"])
    assert matches(sop, SOPQuery(tags=("a", "b")))
    assert not matches(sop, SOPQuery(tags=("a", "z")))


def test_apply_query_orders_by_updated_at_and_limits():
    now = datetime.now(timezone.utc)
    records = [
        _sop(title="late", updated_at=now + timedelta(hours=2)),
        _sop(title="early", updated_at=now),
        _sop(title="mid", updated_at=now + timedelta(hours=1)),
    ]
    asc = apply_query(records, SOPQuery(order="asc"))
    assert [r.title for r in asc] == ["early", "mid", "late"]
    desc = apply_query(records, SOPQuery(order="desc", limit=1))
    assert [r.title for r in desc] == ["late"]
