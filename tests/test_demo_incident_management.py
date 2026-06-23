from workflow_os.demos.incident_management import build_workflow, run_demo
from workflow_os.status import WorkflowStatus


def test_build_workflow_has_steps():
    workflow = build_workflow()
    assert workflow.id == "incident-management"
    assert len(workflow.steps) == 6


def test_run_demo_completes(capsys):
    workflow = run_demo()
    assert workflow.status == WorkflowStatus.COMPLETED
    out = capsys.readouterr().out
    assert "Incident Management" in out
    assert "recorded" in out
