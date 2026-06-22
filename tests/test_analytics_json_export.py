import json

from workflow_os.analytics import (
    execution_summaries,
    to_json,
    workflow_statistics,
    write_json,
)
from workflow_os.memory.record import MemoryRecord


def rec(workflow_id, event_type, duration=None):
    metadata = {"duration_seconds": duration} if duration is not None else None
    return MemoryRecord.create(
        workflow_id=workflow_id, event_type=event_type, metadata=metadata
    )


def test_to_json_dataclass():
    records = [rec("wf1", "workflow_started"), rec("wf1", "workflow_completed", duration=5.0)]
    stats = workflow_statistics(records)
    payload = json.loads(to_json(stats))
    assert payload["total_workflows"] == 1
    assert payload["duration"]["count"] == 1


def test_to_json_list_of_dataclasses():
    records = [rec("wf1", "workflow_started"), rec("wf1", "workflow_completed")]
    summaries = execution_summaries(records)
    payload = json.loads(to_json(summaries))
    assert isinstance(payload, list)
    assert payload[0]["workflow_id"] == "wf1"


def test_write_json(tmp_path):
    target = write_json(tmp_path / "out.json", {"a": 1})
    assert json.loads(target.read_text()) == {"a": 1}
