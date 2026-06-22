from workflow_os.sop import (
    SOPRecord,
    SQLiteSOPStore,
    search_by_tags,
    search_by_title,
    search_by_workflow_type,
    search_sops,
    text_search,
)


def _seed() -> SQLiteSOPStore:
    store = SQLiteSOPStore()
    store.add(SOPRecord.create(
        title="Employee Onboarding", workflow_type="onboarding",
        description="How we welcome new hires", tags=["hr", "people"],
    ))
    store.add(SOPRecord.create(
        title="Incident Response", workflow_type="incident",
        description="Handling production incidents", tags=["sre", "oncall"],
    ))
    return store


def test_search_by_title_case_insensitive():
    results = search_by_title(_seed(), "onboarding")
    assert [s.title for s in results] == ["Employee Onboarding"]


def test_search_by_workflow_type():
    results = search_by_workflow_type(_seed(), "incident")
    assert [s.title for s in results] == ["Incident Response"]


def test_search_by_tags_all_and_any():
    store = _seed()
    assert len(search_by_tags(store, ["hr", "people"])) == 1
    assert len(search_by_tags(store, ["hr", "sre"])) == 0
    assert len(search_by_tags(store, ["hr", "sre"], match_all=False)) == 2


def test_text_search_matches_description():
    results = text_search(_seed(), "production")
    assert [s.title for s in results] == ["Incident Response"]


def test_search_sops_combines_criteria():
    store = _seed()
    results = search_sops(store, workflow_type="onboarding", tags=["hr"])
    assert len(results) == 1
    assert search_sops(store, workflow_type="onboarding", tags=["sre"]) == []
