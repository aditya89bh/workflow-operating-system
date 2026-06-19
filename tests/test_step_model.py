from workflow_os import WorkflowStep


def test_create_step_with_defaults():
    step = WorkflowStep(id="s1", name="Collect documents")
    assert step.id == "s1"
    assert step.name == "Collect documents"
    assert step.description == ""
    assert step.status == "pending"
    assert step.dependencies == []
    assert step.assignee is None
    assert step.metadata == {}


def test_step_with_dependencies_and_assignee():
    step = WorkflowStep(
        id="s2",
        name="Approve",
        dependencies=["s1"],
        assignee="manager",
    )
    assert step.dependencies == ["s1"]
    assert step.assignee == "manager"
