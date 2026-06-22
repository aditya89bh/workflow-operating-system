import dataclasses

from workflow_os.sop import SOPChangeLog, SOPRecord, diff_fields


def test_diff_fields_detects_changes():
    old = SOPRecord.create(title="Onboarding", workflow_type="onboarding")
    new = dataclasses.replace(
        old, version=2, status="active", title="Onboarding v2"
    )
    changed = diff_fields(old, new)
    assert set(changed) == {"title", "version", "status"}


def test_diff_fields_empty_when_identical():
    sop = SOPRecord.create(title="t", workflow_type="x")
    assert diff_fields(sop, sop) == []


def test_change_log_record_and_for_sop():
    log = SOPChangeLog()
    log.record(
        "sop1", 2,
        change_reason="promoted to active",
        changed_fields=["status"],
        changed_by="hr",
    )
    changes = log.for_sop("sop1")
    assert len(changes) == 1
    assert changes[0].change_reason == "promoted to active"
    assert changes[0].changed_by == "hr"
    assert changes[0].changed_fields == ["status"]


def test_record_change_computes_diff():
    log = SOPChangeLog()
    old = SOPRecord.create(title="t", workflow_type="x", sop_id="s1")
    new = dataclasses.replace(old, version=2, description="now documented")
    change = log.record_change(old, new, change_reason="add detail", changed_by="ops")
    assert set(change.changed_fields) == {"version", "description"}
    assert log.all() == [change]
