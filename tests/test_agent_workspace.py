from workflow_os.agents import SharedWorkspace
from workflow_os.workflow import Workflow


def test_shared_state():
    ws = SharedWorkspace("w1", metadata={"team": "ops"})
    ws.set_state("phase", "build")
    ws.update_state({"count": 2})
    assert ws.get_state("phase") == "build"
    assert ws.get_state("count") == 2
    assert ws.get_state("missing", "x") == "x"
    assert ws.metadata == {"team": "ops"}


def test_workflow_context():
    ws = SharedWorkspace("w1")
    assert ws.workflow is None
    workflow = Workflow(id="wf", name="W")
    ws.attach_workflow(workflow)
    assert ws.workflow is workflow


def test_agent_context_isolated():
    ws = SharedWorkspace("w1")
    ws.set_agent_context("a1", "task", "design")
    ws.set_agent_context("a2", "task", "build")
    assert ws.agent_context("a1") == {"task": "design"}
    assert ws.agent_context("a2") == {"task": "build"}
