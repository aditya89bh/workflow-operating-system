from workflow_os.learning import OrganizationalInsight


def test_create_defaults():
    insight = OrganizationalInsight.create(category="success", title="wf1 reliable")
    assert insight.insight_id
    assert insight.evidence == []
    assert insight.confidence == 1.0
    assert insight.metadata == {}


def test_create_with_evidence():
    insight = OrganizationalInsight.create(
        category="failure",
        title="wf2 unstable",
        evidence=["3 of 5 runs failed"],
        confidence=0.6,
    )
    assert insight.evidence == ["3 of 5 runs failed"]
    assert insight.confidence == 0.6


def test_evidence_isolated():
    a = OrganizationalInsight.create(category="c", title="t")
    b = OrganizationalInsight.create(category="c", title="t")
    a.evidence.append("x")
    assert b.evidence == []
