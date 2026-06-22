"""Multi-agent collaboration demonstration.

Wires the agents together end to end: register agents, plan and assign a
workflow, exchange messages, execute the steps, and print collaboration reports.
Everything here is deterministic and rule-based.
"""

from __future__ import annotations

from workflow_os.agents.accountability import build_accountability
from workflow_os.agents.coordinator import CoordinatorAgent
from workflow_os.agents.delegation import TaskDelegation
from workflow_os.agents.execution import ExecutionAgent
from workflow_os.agents.logs import CollaborationLog
from workflow_os.agents.messaging import MessageBus
from workflow_os.agents.metrics import compute_collaboration_metrics
from workflow_os.agents.planner import PlannerAgent
from workflow_os.agents.record import Agent
from workflow_os.agents.registry import AgentRegistry
from workflow_os.agents.reports import build_performance_report
from workflow_os.agents.roles import AgentRole
from workflow_os.agents.workspace import SharedWorkspace
from workflow_os.step import WorkflowStep
from workflow_os.workflow import Workflow


def build_demo_registry() -> AgentRegistry:
    """Return a registry populated with one agent per role."""
    registry = AgentRegistry()
    registry.register(
        Agent.create(
            name="Coordinator", role=AgentRole.COORDINATOR.value, agent_id="coordinator"
        )
    )
    registry.register(
        Agent.create(name="Planner", role=AgentRole.PLANNER.value, agent_id="planner")
    )
    registry.register(
        Agent.create(name="Executor", role=AgentRole.EXECUTOR.value, agent_id="executor")
    )
    return registry


def build_demo_workflow() -> Workflow:
    """Return a small onboarding workflow with linear dependencies."""
    return Workflow(
        id="onboarding",
        name="Employee Onboarding",
        steps=[
            WorkflowStep(id="collect", name="Collect documents"),
            WorkflowStep(id="provision", name="Provision accounts", dependencies=["collect"]),
            WorkflowStep(id="welcome", name="Send welcome", dependencies=["provision"]),
        ],
    )


def run_demo() -> None:
    """Run the multi-agent collaboration demonstration and print a summary."""
    registry = build_demo_registry()
    workflow = build_demo_workflow()
    workspace = SharedWorkspace("onboarding-ws", workflow=workflow)
    log = CollaborationLog()
    bus = MessageBus()
    delegation = TaskDelegation()

    coordinator = CoordinatorAgent(registry.lookup("coordinator"))
    planner = PlannerAgent(registry.lookup("planner"))
    execution = ExecutionAgent(registry.lookup("executor"))

    print(f"registered agents: {[a.agent_id for a in registry.list()]}")

    plan = planner.create_plan(workflow)
    workspace.set_state("plan", plan)
    print(f"plan: {plan}")

    coordinator.assign_tasks(workflow, dict.fromkeys(plan, "executor"))
    for step_id in plan:
        task = delegation.assign(
            workflow_id=workflow.id,
            owner="executor",
            step_id=step_id,
            assigned_by="coordinator",
        )
        log.record_assignment(workflow.id, "executor", task.task_id)

    kickoff = bus.send("coordinator", "executor", "begin onboarding", subject="kickoff")
    log.record_message(kickoff, workflow_id=workflow.id)
    print(f"message: {kickoff.sender} -> {kickoff.recipient}: {kickoff.body}")

    coordinator.start(workflow)
    for step in coordinator.coordinate_execution(workflow):
        execution.execute_task(workflow, step)
        log.record_participation(workflow.id, "executor")
        print(f"  executed {step.id}: {execution.report_status(step)}")
    coordinator.complete(workflow)
    print(f"workflow status: {workflow.status.value}")

    metrics = compute_collaboration_metrics(workflow, delegation, bus)
    print(
        "metrics: "
        f"completion={metrics.task_completion_rate:.2f} "
        f"messages={metrics.message_count} "
        f"handoffs={metrics.handoff_count}"
    )

    accountability = build_accountability(log, "executor")
    print(f"executor actions: {accountability.action_counts}")

    report = build_performance_report(["coordinator", "executor"], delegation, bus)
    for agent_id, perf in report.per_agent.items():
        print(
            f"  {agent_id}: active={perf.active_tasks} "
            f"utilization={perf.utilization:.2f}"
        )


if __name__ == "__main__":  # pragma: no cover
    run_demo()
