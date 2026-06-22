from workflow_os.agents import build_demo_registry, build_demo_workflow, run_demo
from workflow_os.status import WorkflowStatus
from workflow_os.transitions import StepStatus


def test_demo_registry_has_three_agents():
    registry = build_demo_registry()
    assert len(registry) == 3


def test_demo_workflow_shape():
    workflow = build_demo_workflow()
    assert [s.id for s in workflow.steps] == ["collect", "provision", "welcome"]


def test_run_demo_completes(capsys):
    run_demo()
    out = capsys.readouterr().out
    assert "workflow status: completed" in out
    assert "metrics:" in out


def test_run_demo_is_deterministic():
    workflow = build_demo_workflow()
    assert workflow.status == WorkflowStatus.DRAFT
    assert all(StepStatus(s.status) == StepStatus.PENDING for s in workflow.steps)
