import dataclasses

from workflow_os.sop import SOPRecord, SOPVersionHistory


def _versioned(sop: SOPRecord, version: int, **changes) -> SOPRecord:
    return dataclasses.replace(sop, version=version, **changes)


def test_record_and_history_is_ordered():
    history = SOPVersionHistory()
    sop = SOPRecord.create(title="Onboarding", workflow_type="onboarding")
    history.record(sop)
    history.record(_versioned(sop, 2, status="active"))
    history.record(_versioned(sop, 3, status="active"))

    assert history.versions(sop.sop_id) == [1, 2, 3]
    assert history.current_version(sop.sop_id).version == 3
    assert history.previous_version(sop.sop_id).version == 2


def test_no_previous_for_single_version():
    history = SOPVersionHistory()
    sop = SOPRecord.create(title="t", workflow_type="x")
    history.record(sop)
    assert history.previous_version(sop.sop_id) is None
    assert history.current_version(sop.sop_id).version == 1


def test_unknown_sop_returns_empty():
    history = SOPVersionHistory()
    assert history.history("nope") == []
    assert history.current_version("nope") is None
    assert history.previous_version("nope") is None


def test_out_of_order_recording_is_sorted():
    history = SOPVersionHistory()
    sop = SOPRecord.create(title="t", workflow_type="x")
    history.record(_versioned(sop, 3))
    history.record(_versioned(sop, 1))
    history.record(_versioned(sop, 2))
    assert history.versions(sop.sop_id) == [1, 2, 3]
    assert history.current_version(sop.sop_id).version == 3
