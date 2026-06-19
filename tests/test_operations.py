import pytest

from workflow_os import (
    Workflow,
    WorkflowOperationError,
    WorkflowStatus,
    WorkflowStep,
    WorkflowValidationError,
    start_workflow,
)


def make_workflow(status: WorkflowStatus = WorkflowStatus.DRAFT) -> Workflow:
    return Workflow(
        id="wf",
        name="Onboarding",
        status=status,
        steps=[WorkflowStep(id="s1", name="Create account")],
    )


def test_start_from_draft():
    wf = start_workflow(make_workflow(WorkflowStatus.DRAFT))
    assert wf.status is WorkflowStatus.RUNNING


def test_start_from_ready():
    wf = start_workflow(make_workflow(WorkflowStatus.READY))
    assert wf.status is WorkflowStatus.RUNNING


def test_cannot_start_running_workflow():
    wf = make_workflow(WorkflowStatus.DRAFT)
    start_workflow(wf)
    with pytest.raises(WorkflowOperationError):
        start_workflow(wf)


def test_cannot_start_invalid_workflow():
    wf = Workflow(id="wf", name="")
    with pytest.raises(WorkflowValidationError):
        start_workflow(wf)
