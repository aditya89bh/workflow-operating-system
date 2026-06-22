from workflow_os.analytics import execution_summaries, to_csv, write_csv
from workflow_os.memory.record import MemoryRecord


def rec(workflow_id, event_type):
    return MemoryRecord.create(workflow_id=workflow_id, event_type=event_type)


def test_to_csv_from_dicts():
    rows = [{"a": 1, "b": True}, {"a": 2, "b": False}]
    csv_text = to_csv(rows)
    lines = csv_text.strip().splitlines()
    assert lines[0] == "a,b"
    assert lines[1] == "1,true"
    assert lines[2] == "2,false"


def test_to_csv_empty():
    assert to_csv([]) == ""


def test_to_csv_from_dataclasses():
    records = [rec("wf1", "workflow_started"), rec("wf1", "workflow_completed")]
    summaries = execution_summaries(records)
    csv_text = to_csv(summaries, fieldnames=["workflow_id", "status"])
    lines = csv_text.strip().splitlines()
    assert lines[0] == "workflow_id,status"
    assert "wf1,completed" in lines[1]


def test_write_csv(tmp_path):
    rows = [{"x": 1}]
    target = write_csv(tmp_path / "out.csv", rows)
    assert target.exists()
    assert "x" in target.read_text()
