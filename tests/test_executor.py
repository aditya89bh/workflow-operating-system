import pytest

from workflow_os import (
    CycleError,
    Workflow,
    WorkflowExecutor,
    WorkflowStatus,
    WorkflowStep,
)


def test_execution_order_respects_dependencies():
    wf = Workflow(
        id="wf",
        name="Build",
        steps=[
            WorkflowStep(id="c", name="C", dependencies=["b"]),
            WorkflowStep(id="b", name="B", dependencies=["a"]),
            WorkflowStep(id="a", name="A"),
        ],
    )
    order = [step.id for step in WorkflowExecutor(wf).execution_order()]
    assert order == ["a", "b", "c"]


def test_independent_steps_keep_definition_order():
    wf = Workflow(
        id="wf",
        name="Parallel",
        steps=[
            WorkflowStep(id="x", name="X"),
            WorkflowStep(id="y", name="Y"),
        ],
    )
    order = [step.id for step in WorkflowExecutor(wf).execution_order()]
    assert order == ["x", "y"]


def test_run_completes_all_steps():
    wf = Workflow(
        id="wf",
        name="Run",
        steps=[
            WorkflowStep(id="a", name="A"),
            WorkflowStep(id="b", name="B", dependencies=["a"]),
        ],
    )
    result = WorkflowExecutor(wf).run()
    assert result.status is WorkflowStatus.RUNNING
    assert all(step.status == "completed" for step in result.steps)


def test_cycle_is_detected():
    wf = Workflow(
        id="wf",
        name="Cycle",
        steps=[
            WorkflowStep(id="a", name="A", dependencies=["b"]),
            WorkflowStep(id="b", name="B", dependencies=["a"]),
        ],
    )
    with pytest.raises(CycleError):
        WorkflowExecutor(wf).execution_order()
