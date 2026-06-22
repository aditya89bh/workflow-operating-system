from workflow_os.learning import Recommendation


def test_create_fills_id_and_timestamp():
    rec = Recommendation.create(category="workflow", title="Simplify onboarding")
    assert rec.recommendation_id
    assert rec.category == "workflow"
    assert rec.severity == "medium"
    assert rec.confidence == 1.0
    assert rec.created_at is not None
    assert rec.metadata == {}


def test_create_full():
    rec = Recommendation.create(
        category="approval",
        title="Reduce approvers",
        description="Two approvers is enough",
        severity="high",
        confidence=0.8,
        metadata={"workflow_id": "wf1"},
    )
    assert rec.severity == "high"
    assert rec.confidence == 0.8
    assert rec.metadata == {"workflow_id": "wf1"}


def test_metadata_isolated():
    a = Recommendation.create(category="c", title="t")
    b = Recommendation.create(category="c", title="t")
    a.metadata["x"] = 1
    assert b.metadata == {}
