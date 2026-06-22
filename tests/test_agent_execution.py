from workflow_os.agents import Agent, ExecutionAgent
from workflow_os.step import WorkflowStep
from workflow_os.workflow import Workflow


def build():
    workflow = Workflow(id="wf", name="W", steps=[WorkflowStep(id="a", name="A")])
    return workflow, workflow.steps[0]


def test_execute_task_completes_and_emits():
    workflow, step = build()
    agent = ExecutionAgent(Agent.create(name="Exec", role="executor", agent_id="ex1"))
    event = agent.execute_task(workflow, step)
    assert event.status == "completed"
    assert event.agent_id == "ex1"
    assert agent.report_status(step) == "completed"
    statuses = [e.status for e in agent.events()]
    assert statuses == ["running", "completed"]


def test_fail_task():
    workflow, step = build()
    agent = ExecutionAgent()
    from workflow_os.transitions import StepStatus, transition_step

    transition_step(step, StepStatus.RUNNING)
    event = agent.fail_task(workflow, step)
    assert event.status == "failed"
    assert agent.report_status(step) == "failed"


def test_agent_id_none_without_identity():
    workflow, step = build()
    agent = ExecutionAgent()
    event = agent.execute_task(workflow, step)
    assert event.agent_id is None
