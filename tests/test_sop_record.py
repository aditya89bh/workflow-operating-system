from datetime import datetime

from workflow_os.sop import SOPRecord, SOPStatus


def test_create_fills_id_and_timestamps():
    sop = SOPRecord.create(title="Onboarding", workflow_type="onboarding")
    assert sop.sop_id
    assert isinstance(sop.created_at, datetime)
    assert sop.created_at == sop.updated_at
    assert sop.version == 1
    assert sop.status == SOPStatus.DRAFT.value
    assert sop.tags == []
    assert sop.metadata == {}
    assert sop.author is None


def test_create_with_full_fields():
    sop = SOPRecord.create(
        title="Incident Response",
        workflow_type="incident",
        description="How we handle incidents",
        version=3,
        status=SOPStatus.ACTIVE.value,
        author="sre-lead",
        tags=["oncall", "sev"],
        metadata={"owner": "sre"},
    )
    assert sop.version == 3
    assert sop.status == "active"
    assert sop.author == "sre-lead"
    assert sop.tags == ["oncall", "sev"]
    assert sop.metadata == {"owner": "sre"}


def test_status_values():
    assert {s.value for s in SOPStatus} == {
        "draft",
        "active",
        "deprecated",
        "archived",
    }


def test_tags_independent_between_records():
    a = SOPRecord.create(title="A", workflow_type="x")
    b = SOPRecord.create(title="B", workflow_type="y")
    a.tags.append("t")
    assert b.tags == []
