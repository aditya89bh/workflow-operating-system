import pytest

from workflow_os import (
    StepStatus,
    Workflow,
    WorkflowExecutor,
    WorkflowOperationError,
    WorkflowStatus,
    WorkflowStep,
    WorkflowValidationError,
    complete_workflow,
    pause_workflow,
    resume_workflow,
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


def test_pause_running_workflow():
    wf = make_workflow(WorkflowStatus.DRAFT)
    start_workflow(wf)
    pause_workflow(wf)
    assert wf.status is WorkflowStatus.PAUSED


def test_cannot_pause_non_running_workflow():
    wf = make_workflow(WorkflowStatus.DRAFT)
    with pytest.raises(WorkflowOperationError):
        pause_workflow(wf)


def test_resume_paused_workflow():
    wf = make_workflow(WorkflowStatus.DRAFT)
    start_workflow(wf)
    pause_workflow(wf)
    resume_workflow(wf)
    assert wf.status is WorkflowStatus.RUNNING


def test_cannot_resume_non_paused_workflow():
    wf = make_workflow(WorkflowStatus.DRAFT)
    start_workflow(wf)
    with pytest.raises(WorkflowOperationError):
        resume_workflow(wf)


def test_complete_when_all_required_steps_done():
    wf = make_workflow(WorkflowStatus.DRAFT)
    WorkflowExecutor(wf).run()
    complete_workflow(wf)
    assert wf.status is WorkflowStatus.COMPLETED


def test_cannot_complete_with_pending_required_step():
    wf = make_workflow(WorkflowStatus.DRAFT)
    start_workflow(wf)
    with pytest.raises(WorkflowOperationError):
        complete_workflow(wf)


def test_optional_steps_do_not_block_completion():
    wf = Workflow(
        id="wf",
        name="Onboarding",
        status=WorkflowStatus.RUNNING,
        steps=[
            WorkflowStep(id="s1", name="Required", status=StepStatus.COMPLETED),
            WorkflowStep(
                id="s2",
                name="Optional",
                status=StepStatus.PENDING,
                metadata={"optional": True},
            ),
        ],
    )
    complete_workflow(wf)
    assert wf.status is WorkflowStatus.COMPLETED
