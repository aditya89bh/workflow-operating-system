import pytest

from workflow_os import (
    StepStatus,
    StepTransitionError,
    WorkflowStep,
    can_transition,
    transition_step,
)


def test_pending_can_start_or_skip():
    assert can_transition(StepStatus.PENDING, StepStatus.RUNNING)
    assert can_transition(StepStatus.PENDING, StepStatus.SKIPPED)
    assert not can_transition(StepStatus.PENDING, StepStatus.COMPLETED)


def test_running_can_complete_or_fail():
    assert can_transition(StepStatus.RUNNING, StepStatus.COMPLETED)
    assert can_transition(StepStatus.RUNNING, StepStatus.FAILED)


def test_failed_can_retry():
    assert can_transition(StepStatus.FAILED, StepStatus.RUNNING)


def test_completed_is_terminal():
    assert not can_transition(StepStatus.COMPLETED, StepStatus.RUNNING)
    assert not can_transition(StepStatus.COMPLETED, StepStatus.FAILED)


def test_transition_step_updates_status():
    step = WorkflowStep(id="s1", name="A")
    transition_step(step, StepStatus.RUNNING)
    assert step.status is StepStatus.RUNNING
    transition_step(step, StepStatus.COMPLETED)
    assert step.status is StepStatus.COMPLETED


def test_invalid_transition_raises():
    step = WorkflowStep(id="s1", name="A")
    with pytest.raises(StepTransitionError):
        transition_step(step, StepStatus.COMPLETED)
