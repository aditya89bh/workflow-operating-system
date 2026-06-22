from datetime import timedelta

from workflow_os.exception import detect_stalled_workflows, is_stalled, utcnow


def test_is_stalled():
    now = utcnow()
    assert is_stalled(now - timedelta(hours=2), 3600, now=now)
    assert not is_stalled(now - timedelta(minutes=5), 3600, now=now)


def test_detect_stalled_workflows():
    now = utcnow()
    activities = {
        "wf1": now - timedelta(hours=2),
        "wf2": now - timedelta(minutes=1),
        "wf3": now - timedelta(hours=5),
    }
    records = detect_stalled_workflows(activities, max_idle_seconds=3600, now=now)
    assert {r.workflow_id for r in records} == {"wf1", "wf3"}
    assert all(r.exception_type == "workflow_failure" for r in records)
    assert all(r.severity == "medium" for r in records)


def test_no_stall_returns_empty():
    now = utcnow()
    assert detect_stalled_workflows({"wf": now}, 3600, now=now) == []
