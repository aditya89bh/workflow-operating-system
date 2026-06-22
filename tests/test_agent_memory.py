from workflow_os.agents import MemoryAgent
from workflow_os.memory import MemoryQuery, SQLiteMemoryStore


def make_agent():
    return MemoryAgent(SQLiteMemoryStore(":memory:"))


def test_write_and_retrieve():
    agent = make_agent()
    record = agent.write(
        workflow_id="wf", event_type="note", actor="alice", metadata={"k": "v"}
    )
    assert record.workflow_id == "wf"
    results = agent.retrieve(MemoryQuery(workflow_id="wf"))
    assert len(results) == 1
    assert results[0].metadata == {"k": "v"}


def test_workflow_and_actor_history():
    agent = make_agent()
    agent.write(workflow_id="wf1", event_type="note", actor="alice")
    agent.write(workflow_id="wf1", event_type="note", actor="bob")
    agent.write(workflow_id="wf2", event_type="note", actor="alice")
    assert len(agent.workflow_history("wf1")) == 2
    assert len(agent.actor_history("alice")) == 2
