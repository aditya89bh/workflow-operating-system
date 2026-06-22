from workflow_os.sop import SOPRecord, SQLiteSOPStore, score_sop, score_sops


def _store() -> SQLiteSOPStore:
    store = SQLiteSOPStore()
    store.add(SOPRecord.create(
        title="Onboarding v2", workflow_type="onboarding", version=2,
        tags=["hr", "fast"], sop_id="onb2",
    ))
    store.add(SOPRecord.create(
        title="Generic", workflow_type="generic", version=1, tags=[], sop_id="gen1",
    ))
    return store


def test_score_components_and_range():
    store = _store()
    scores = {s.sop_id: s for s in score_sops(
        store, workflow_type="onboarding", tags=["hr", "fast"],
        usage_counts={"onb2": 10, "gen1": 0},
    )}
    onb = scores["onb2"]
    assert onb.components["workflow_match"] == 1.0
    assert onb.components["tag_match"] == 1.0
    assert onb.components["version_recency"] == 1.0  # max version
    assert onb.components["usage_frequency"] == 1.0  # max usage
    assert onb.score == 1.0
    assert 0.0 <= scores["gen1"].score <= 1.0


def test_ranking_is_deterministic():
    store = _store()
    a = [s.sop_id for s in score_sops(store, workflow_type="onboarding")]
    b = [s.sop_id for s in score_sops(store, workflow_type="onboarding")]
    assert a == b
    assert a[0] == "onb2"


def test_score_sop_no_criteria():
    sop = SOPRecord.create(title="t", workflow_type="x", version=1)
    result = score_sop(sop, max_version=1)
    # Only version recency contributes (version == max_version).
    assert result.score == 0.2
    assert result.components["workflow_match"] == 0.0
    assert result.components["version_recency"] == 1.0
    assert result.components["tag_match"] == 0.0
    assert result.components["usage_frequency"] == 0.0
