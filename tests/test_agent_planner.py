from workflow_os.agents import PlannerAgent
from workflow_os.step import WorkflowStep
from workflow_os.workflow import Workflow


def build_workflow():
    return Workflow(
        id="wf",
        name="Build",
        steps=[
            WorkflowStep(id="design", name="Design"),
            WorkflowStep(id="build", name="Build", dependencies=["design"]),
            WorkflowStep(id="test", name="Test", dependencies=["build"]),
        ],
    )


def test_create_plan_orders_by_dependency():
    plan = PlannerAgent().create_plan(build_workflow())
    assert plan == ["design", "build", "test"]


def test_determine_ordering_returns_steps():
    order = PlannerAgent().determine_ordering(build_workflow())
    assert [s.id for s in order] == ["design", "build", "test"]


def test_identify_dependencies():
    deps = PlannerAgent().identify_dependencies(build_workflow())
    assert deps == {
        "design": [],
        "build": ["design"],
        "test": ["build"],
    }
