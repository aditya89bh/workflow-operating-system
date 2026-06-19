"""Step status state machine and transition validation.

A step moves through a small set of states. Only the transitions declared in
:data:`STEP_TRANSITIONS` are permitted; any other move raises
:class:`StepTransitionError`.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from workflow_os.step import WorkflowStep


class StepStatus(str, Enum):
    """Execution states for a single workflow step."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"

    def __str__(self) -> str:  # pragma: no cover - convenience only
        return self.value


STEP_TRANSITIONS: dict[StepStatus, frozenset[StepStatus]] = {
    StepStatus.PENDING: frozenset({StepStatus.RUNNING, StepStatus.SKIPPED}),
    StepStatus.RUNNING: frozenset({StepStatus.COMPLETED, StepStatus.FAILED}),
    StepStatus.FAILED: frozenset({StepStatus.RUNNING}),
    StepStatus.COMPLETED: frozenset(),
    StepStatus.SKIPPED: frozenset(),
}

TERMINAL_STEP_STATES: frozenset[StepStatus] = frozenset(
    {StepStatus.COMPLETED, StepStatus.SKIPPED}
)


class StepTransitionError(ValueError):
    """Raised when an illegal step status transition is attempted."""


def available_transitions(current: StepStatus) -> frozenset[StepStatus]:
    """Return the set of states reachable from ``current``."""
    return STEP_TRANSITIONS[StepStatus(current)]


def can_transition(current: StepStatus, target: StepStatus) -> bool:
    """Return ``True`` if moving from ``current`` to ``target`` is allowed."""
    return StepStatus(target) in available_transitions(current)


def transition_step(step: WorkflowStep, target: StepStatus) -> None:
    """Move ``step`` to ``target``, validating the transition first."""
    current = StepStatus(step.status)
    target = StepStatus(target)
    if not can_transition(current, target):
        raise StepTransitionError(
            f"cannot transition step {step.id!r} from {current.value!r} "
            f"to {target.value!r}"
        )
    step.status = target
