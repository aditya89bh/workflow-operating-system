from workflow_os.agents import SharedMemory
from workflow_os.memory import MemoryQuery, MemoryRecord, SQLiteMemoryStore


def make():
    return SharedMemory(SQLiteMemoryStore(":memory:"))


def record(workflow_id="wf", event_id=None):
    return MemoryRecord.create(
        workflow_id=workflow_id, event_type="note", event_id=event_id
    )


def test_write_read_query_logged():
    shared = make()
    rec = record(event_id="e1")
    shared.write(rec, agent_id="a1")
    assert shared.read("e1", agent_id="a2").event_id == "e1"
    results = shared.query(MemoryQuery(workflow_id="wf"), agent_id="a3")
    assert len(results) == 1
    actions = [(a.agent_id, a.action) for a in shared.access_log()]
    assert actions == [("a1", "write"), ("a2", "read"), ("a3", "query")]


def test_access_log_isolated_copy():
    shared = make()
    shared.write(record(event_id="e1"))
    log = shared.access_log()
    log.clear()
    assert len(shared.access_log()) == 1
