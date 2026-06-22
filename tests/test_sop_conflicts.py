from workflow_os.sop import (
    SOPRecord,
    SQLiteSOPStore,
    detect_conflicts,
    detect_duplicate_sops,
    detect_ownership_conflicts,
    detect_version_conflicts,
    detect_workflow_mapping_conflicts,
)


def test_detect_duplicates():
    store = SQLiteSOPStore()
    store.add(SOPRecord.create(title="Onboarding", workflow_type="onboarding", sop_id="a"))
    store.add(SOPRecord.create(title="onboarding", workflow_type="onboarding", sop_id="b"))
    conflicts = detect_duplicate_sops(store)
    assert len(conflicts) == 1
    assert conflicts[0].sop_ids == ("a", "b")


def test_detect_version_conflicts():
    store = SQLiteSOPStore()
    store.add(SOPRecord.create(title="A", workflow_type="onboarding", version=2, sop_id="a"))
    store.add(SOPRecord.create(title="B", workflow_type="onboarding", version=2, sop_id="b"))
    conflicts = detect_version_conflicts(store)
    assert len(conflicts) == 1
    assert "version 2" in conflicts[0].detail


def test_detect_ownership_conflicts():
    store = SQLiteSOPStore()
    store.add(SOPRecord.create(
        title="A", workflow_type="onboarding", sop_id="a", metadata={"owners": ["hr"]},
    ))
    store.add(SOPRecord.create(
        title="B", workflow_type="onboarding", sop_id="b", metadata={"owners": ["it"]},
    ))
    conflicts = detect_ownership_conflicts(store)
    assert len(conflicts) == 1
    assert conflicts[0].sop_ids == ("a", "b")


def test_detect_workflow_mapping_conflicts():
    store = SQLiteSOPStore()
    store.add(SOPRecord.create(
        title="A", workflow_type="onboarding", status="active", sop_id="a",
    ))
    store.add(SOPRecord.create(
        title="B", workflow_type="onboarding", status="active", sop_id="b",
    ))
    store.add(SOPRecord.create(
        title="C", workflow_type="onboarding", status="draft", sop_id="c",
    ))
    conflicts = detect_workflow_mapping_conflicts(store)
    assert len(conflicts) == 1
    assert conflicts[0].sop_ids == ("a", "b")


def test_detect_conflicts_is_sorted_and_aggregated():
    store = SQLiteSOPStore()
    store.add(SOPRecord.create(title="A", workflow_type="onboarding", status="active", sop_id="a"))
    store.add(SOPRecord.create(title="A", workflow_type="onboarding", status="active", sop_id="b"))
    conflicts = detect_conflicts(store)
    types = [c.conflict_type for c in conflicts]
    assert types == sorted(types)
    assert "duplicate" in types
    assert "workflow_mapping" in types


def test_no_conflicts_for_clean_store():
    store = SQLiteSOPStore()
    store.add(SOPRecord.create(title="A", workflow_type="onboarding", status="active"))
    store.add(SOPRecord.create(title="B", workflow_type="incident", status="active"))
    assert detect_conflicts(store) == []
