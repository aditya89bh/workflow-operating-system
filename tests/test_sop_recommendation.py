from workflow_os.sop import (
    SOPRecord,
    SQLiteSOPStore,
    WorkflowSOPLinks,
    recommend_sop,
    recommend_sops,
)


def _store() -> SQLiteSOPStore:
    store = SQLiteSOPStore()
    store.add(SOPRecord.create(
        title="Onboarding v1", workflow_type="onboarding", version=1,
        status="active", tags=["hr"], sop_id="onb1",
    ))
    store.add(SOPRecord.create(
        title="Onboarding v2", workflow_type="onboarding", version=2,
        status="active", tags=["hr", "fast"], sop_id="onb2",
    ))
    store.add(SOPRecord.create(
        title="Generic", workflow_type="generic", version=5,
        status="active", tags=[], sop_id="gen1",
    ))
    return store


def test_recommend_prefers_type_match_then_latest_version():
    best = recommend_sop(_store(), workflow_type="onboarding")
    assert best.sop_id == "onb2"  # type match + higher version


def test_recommend_tag_match_breaks_within_type():
    ranked = recommend_sops(_store(), workflow_type="onboarding", tags=["fast"])
    assert ranked[0].sop_id == "onb2"


def test_explicit_link_outranks_type_match():
    store = _store()
    links = WorkflowSOPLinks()
    links.link("onboarding", "gen1")
    best = recommend_sop(store, workflow_type="onboarding", links=links)
    assert best.sop_id == "gen1"


def test_is_deterministic():
    store = _store()
    a = [s.sop_id for s in recommend_sops(store, workflow_type="onboarding")]
    b = [s.sop_id for s in recommend_sops(store, workflow_type="onboarding")]
    assert a == b


def test_empty_store_returns_none():
    assert recommend_sop(SQLiteSOPStore(), workflow_type="x") is None
