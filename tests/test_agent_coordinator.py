import pytest

from workflow_os.agents import CoordinationError, CoordinatorAgent
from workflow_os.status import WorkflowStatus
from workflow_os.step import WorkflowStep
from workflow_os.workflow import Workflow


def build_workflow():
    return Workflow(
        id="wf",
        name="Onboard",
        steps=[
            WorkflowStep(id="a", name="A"),
            WorkflowStep(id="b", name="B", dependencies=["a"]),
        ],
    )


def test_assign_tasks_sets_assignee():
    workflow = build_workflow()
    coordinator = CoordinatorAgent()
    result = coordinator.assign_tasks(workflow, {"a": "agent-1", "b": "agent-2"})
    assert result == {"a": "agent-1", "b": "agent-2"}
    assert workflow.steps[0].assignee == "agent-1"
    assert workflow.steps[1].assignee == "agent-2"


def test_assign_unknown_step_raises():
    workflow = build_workflow()
    coordinator = CoordinatorAgent()
    with pytest.raises(CoordinationError):
        coordinator.assign_tasks(workflow, {"missing": "agent-1"})


def test_coordinate_execution_order():
    workflow = build_workflow()
    order = CoordinatorAgent().coordinate_execution(workflow)
    assert [step.id for step in order] == ["a", "b"]


def test_manage_state():
    workflow = build_workflow()
    coordinator = CoordinatorAgent()
    coordinator.start(workflow)
    assert workflow.status == WorkflowStatus.RUNNING
