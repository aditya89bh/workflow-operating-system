from workflow_os.agents import (
    Agent,
    AgentRegistry,
    AgentRole,
    CollaborationLog,
    CoordinatorAgent,
    ExecutionAgent,
    MessageBus,
    PlannerAgent,
    SharedWorkspace,
    TaskDelegation,
    build_accountability,
    build_performance_report,
    compute_collaboration_metrics,
    responsibility_chain,
)
from workflow_os.status import WorkflowStatus
from workflow_os.step import WorkflowStep
from workflow_os.transitions import StepStatus
from workflow_os.workflow import Workflow


def build_registry():
    registry = AgentRegistry()
    registry.register(
        Agent.create(name="Coord", role=AgentRole.COORDINATOR.value, agent_id="coord")
    )
    registry.register(
        Agent.create(name="Plan", role=AgentRole.PLANNER.value, agent_id="plan")
    )
    registry.register(
        Agent.create(name="Exec", role=AgentRole.EXECUTOR.value, agent_id="exec")
    )
    return registry


def build_workflow():
    return Workflow(
        id="wf",
        name="Onboarding",
        steps=[
            WorkflowStep(id="collect", name="Collect"),
            WorkflowStep(id="review", name="Review", dependencies=["collect"]),
        ],
    )


def test_end_to_end_multi_agent_flow():
    registry = build_registry()
    workflow = build_workflow()
    workspace = SharedWorkspace("ws", workflow=workflow)
    log = CollaborationLog()
    bus = MessageBus()
    delegation = TaskDelegation()

    coordinator = CoordinatorAgent(registry.lookup("coord"))
    planner = PlannerAgent(registry.lookup("plan"))
    execution = ExecutionAgent(registry.lookup("exec"))

    plan = planner.create_plan(workflow)
    assert plan == ["collect", "review"]
    workspace.set_state("plan", plan)

    coordinator.assign_tasks(workflow, {"collect": "exec", "review": "exec"})
    for step_id in plan:
        task = delegation.assign(
            workflow_id=workflow.id, owner="exec", step_id=step_id, assigned_by="coord"
        )
        log.record_assignment(workflow.id, "exec", task.task_id)

    msg = bus.send("coord", "exec", "begin", subject="kickoff")
    log.record_message(msg, workflow_id=workflow.id)

    coordinator.start(workflow)
    order = coordinator.coordinate_execution(workflow)
    for step in order:
        execution.execute_task(workflow, step)
        log.record_participation(workflow.id, "exec")
    coordinator.complete(workflow)

    assert workflow.status == WorkflowStatus.COMPLETED
    assert all(StepStatus(s.status) == StepStatus.COMPLETED for s in workflow.steps)

    metrics = compute_collaboration_metrics(workflow, delegation, bus)
    assert metrics.task_completion_rate == 1.0
    assert metrics.message_count == 1
    assert metrics.delegation_stats["assign"] == 2

    accountability = build_accountability(log, "exec")
    assert accountability.action_counts["assignment"] == 2
    assert accountability.action_counts["participation"] == 2

    report = build_performance_report(["coord", "exec"], delegation, bus)
    assert report.per_agent["exec"].assigned_tasks == 2
    assert workspace.get_state("plan") == ["collect", "review"]


def test_responsibility_chain_after_transfer():
    delegation = TaskDelegation()
    delegation.assign(workflow_id="wf", owner="exec", task_id="t1")
    delegation.transfer("t1", "backup")
    assert responsibility_chain(delegation, "t1") == ["exec", "backup"]
