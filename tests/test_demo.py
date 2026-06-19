from pathlib import Path

from workflow_os import WorkflowStatus, import_workflow
from workflow_os.cli import main

EXAMPLE = Path(__file__).resolve().parent.parent / "examples" / "employee_onboarding.json"


def test_example_workflow_is_valid_and_importable():
    workflow = import_workflow(EXAMPLE)
    assert workflow.id == "employee-onboarding"
    assert workflow.status is WorkflowStatus.READY
    assert len(workflow.steps) == 5


def test_demo_command_runs_to_completion(capsys):
    assert main(["demo", "--workflow", str(EXAMPLE)]) == 0
    out = capsys.readouterr().out
    assert "running workflow" in out
    assert "finished with status 'completed'" in out
