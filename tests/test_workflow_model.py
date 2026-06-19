from workflow_os import Workflow


def test_create_workflow_with_defaults():
    wf = Workflow(id="wf-1", name="Onboarding")
    assert wf.id == "wf-1"
    assert wf.name == "Onboarding"
    assert wf.description == ""
    assert wf.steps == []
    assert wf.status == "draft"
    assert wf.metadata == {}


def test_workflow_metadata_and_steps_are_independent():
    a = Workflow(id="a", name="A")
    b = Workflow(id="b", name="B")
    a.metadata["owner"] = "ops"
    a.steps.append("s1")
    assert b.metadata == {}
    assert b.steps == []
