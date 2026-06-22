from workflow_os.agents import (
    MessageBus,
    TaskDelegation,
    compute_collaboration_metrics,
    delegation_statistics,
    handoff_count,
    message_count,
    task_completion_rate,
)
from workflow_os.step import WorkflowStep
from workflow_os.transitions import StepStatus
from workflow_os.workflow import Workflow


def build_workflow():
    return Workflow(
        id="wf",
        name="W",
        steps=[
            WorkflowStep(id="a", name="A", status=StepStatus.COMPLETED),
            WorkflowStep(id="b", name="B", status=StepStatus.PENDING),
        ],
    )


def test_task_completion_rate():
    assert task_completion_rate(build_workflow()) == 0.5
    assert task_completion_rate(Workflow(id="e", name="empty")) == 0.0


def test_handoff_and_delegation_stats():
    ledger = TaskDelegation()
    ledger.assign(workflow_id="wf", owner="a1", task_id="t1")
    ledger.transfer("t1", "a2")
    ledger.revoke("t1")
    assert handoff_count(ledger) == 1
    assert delegation_statistics(ledger) == {"assign": 1, "transfer": 1, "revoke": 1}


def test_message_count_and_compute():
    bus = MessageBus()
    bus.send("a", "b", "1")
    bus.send("a", "c", "2")
    assert message_count(bus) == 2
    ledger = TaskDelegation()
    ledger.assign(workflow_id="wf", owner="a1", task_id="t1")
    ledger.transfer("t1", "a2")
    metrics = compute_collaboration_metrics(build_workflow(), ledger, bus)
    assert metrics.total_tasks == 2
    assert metrics.completed_tasks == 1
    assert metrics.task_completion_rate == 0.5
    assert metrics.handoff_count == 1
    assert metrics.message_count == 2
