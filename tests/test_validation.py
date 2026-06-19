import pytest

from workflow_os import (
    Workflow,
    WorkflowStatus,
    WorkflowStep,
    WorkflowValidationError,
    is_valid,
    validate,
    validate_workflow,
)


def make_valid_workflow() -> Workflow:
    return Workflow(
        id="wf",
        name="Onboarding",
        steps=[
            WorkflowStep(id="s1", name="Create account"),
            WorkflowStep(id="s2", name="Assign laptop", dependencies=["s1"]),
        ],
    )


def test_valid_workflow_has_no_errors():
    wf = make_valid_workflow()
    assert validate_workflow(wf) == []
    assert is_valid(wf)
    validate(wf)


def test_empty_name_is_rejected():
    wf = make_valid_workflow()
    wf.name = "   "
    assert any("name" in e for e in validate_workflow(wf))


def test_duplicate_step_ids_are_rejected():
    wf = make_valid_workflow()
    wf.steps.append(WorkflowStep(id="s1", name="Duplicate"))
    assert any("duplicate" in e for e in validate_workflow(wf))


def test_unknown_dependency_is_rejected():
    wf = make_valid_workflow()
    wf.steps[1].dependencies = ["does-not-exist"]
    assert any("unknown step" in e for e in validate_workflow(wf))


def test_self_dependency_is_rejected():
    wf = make_valid_workflow()
    wf.steps[0].dependencies = ["s1"]
    assert any("itself" in e for e in validate_workflow(wf))


def test_invalid_initial_state_is_rejected():
    wf = make_valid_workflow()
    wf.status = WorkflowStatus.RUNNING
    assert any("start in" in e for e in validate_workflow(wf))


def test_validate_raises_with_collected_errors():
    wf = Workflow(id="wf", name="")
    with pytest.raises(WorkflowValidationError) as excinfo:
        validate(wf)
    assert excinfo.value.errors
