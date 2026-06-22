from datetime import timedelta

from workflow_os.exception import (
    Deadline,
    detect_deadline_failure,
    detect_deadline_failures,
    utcnow,
)


def test_detect_passed_deadline():
    now = utcnow()
    deadline = Deadline(workflow_id="wf", deadline=now - timedelta(hours=1))
    record = detect_deadline_failure(deadline, now=now)
    assert record is not None
    assert record.exception_type == "timeout"
    assert record.severity == "high"
    assert record.workflow_id == "wf"


def test_future_deadline_returns_none():
    now = utcnow()
    deadline = Deadline(workflow_id="wf", deadline=now + timedelta(hours=1))
    assert detect_deadline_failure(deadline, now=now) is None


def test_detect_batch():
    now = utcnow()
    deadlines = [
        Deadline("wf1", now - timedelta(minutes=5)),
        Deadline("wf2", now + timedelta(minutes=5)),
        Deadline("wf3", now - timedelta(minutes=1), step_id="s3"),
    ]
    records = detect_deadline_failures(deadlines, now=now)
    assert {r.workflow_id for r in records} == {"wf1", "wf3"}
