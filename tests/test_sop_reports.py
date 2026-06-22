from workflow_os.sop import (
    SOPRecord,
    SQLiteSOPStore,
    generate_lifecycle_report,
)


def _store() -> SQLiteSOPStore:
    store = SQLiteSOPStore()
    store.add(SOPRecord.create(
        title="Onboarding", workflow_type="onboarding", version=2,
        status="active", author="hr",
    ))
    store.add(SOPRecord.create(
        title="Incident", workflow_type="incident", version=1,
        status="draft", author="sre",
    ))
    store.add(SOPRecord.create(
        title="Procurement", workflow_type="procurement", version=3,
        status="deprecated", author="hr",
    ))
    return store


def test_lifecycle_report_counts():
    report = generate_lifecycle_report(_store())
    assert report.total_sops == 3
    assert report.active_count == 1
    assert report.inactive_count == 2
    assert report.status_counts["active"] == 1
    assert report.status_counts["draft"] == 1
    assert report.status_counts["deprecated"] == 1


def test_version_and_coverage_and_author_stats():
    report = generate_lifecycle_report(_store())
    assert report.version_statistics["max_version"] == 3.0
    assert report.version_statistics["average_version"] == 2.0
    assert report.workflow_coverage_count == 3
    assert report.author_statistics["hr"] == 2
    assert report.author_statistics["sre"] == 1


def test_empty_report():
    report = generate_lifecycle_report(SQLiteSOPStore())
    assert report.total_sops == 0
    assert report.as_dict()["workflow_coverage_count"] == 0
