"""Collaboration efficiency metrics.

Deterministic, rule-based measures of how a collaboration ran: task completion
rate, the number of handoffs, message volume, and delegation statistics. All
metrics are computed directly from the workflow, delegation ledger, and message
bus - there is no learning or estimation.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from workflow_os.agents.delegation import DelegationAction, TaskDelegation
from workflow_os.agents.messaging import MessageBus
from workflow_os.transitions import StepStatus
from workflow_os.workflow import Workflow


@dataclass
class CollaborationMetrics:
    """Aggregate efficiency metrics for a collaboration."""

    total_tasks: int = 0
    completed_tasks: int = 0
    task_completion_rate: float = 0.0
    handoff_count: int = 0
    message_count: int = 0
    delegation_stats: dict[str, int] = field(default_factory=dict)


def task_completion_rate(workflow: Workflow) -> float:
    """Return the fraction of workflow steps that are completed, in ``[0, 1]``."""
    total = len(workflow.steps)
    if total == 0:
        return 0.0
    completed = sum(
        1 for step in workflow.steps if StepStatus(step.status) == StepStatus.COMPLETED
    )
    return completed / total


def handoff_count(delegation: TaskDelegation) -> int:
    """Return the number of task transfers (handoffs) recorded."""
    return sum(
        1
        for event in delegation.history()
        if event.action == DelegationAction.TRANSFER.value
    )


def message_count(bus: MessageBus) -> int:
    """Return the total number of messages exchanged."""
    return len(bus.all())


def delegation_statistics(delegation: TaskDelegation) -> dict[str, int]:
    """Return counts of each delegation action."""
    stats = {action.value: 0 for action in DelegationAction}
    for event in delegation.history():
        stats[event.action] = stats.get(event.action, 0) + 1
    return stats


def compute_collaboration_metrics(
    workflow: Workflow, delegation: TaskDelegation, bus: MessageBus
) -> CollaborationMetrics:
    """Compute aggregate :class:`CollaborationMetrics`."""
    total = len(workflow.steps)
    completed = sum(
        1 for step in workflow.steps if StepStatus(step.status) == StepStatus.COMPLETED
    )
    return CollaborationMetrics(
        total_tasks=total,
        completed_tasks=completed,
        task_completion_rate=task_completion_rate(workflow),
        handoff_count=handoff_count(delegation),
        message_count=message_count(bus),
        delegation_stats=delegation_statistics(delegation),
    )
