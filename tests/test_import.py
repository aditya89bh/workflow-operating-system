import json

from workflow_os import WorkflowStatus, import_workflow


def test_import_workflow_from_file(tmp_path):
    payload = {
        "schema_version": "1.0",
        "id": "wf",
        "name": "Onboarding",
        "description": "New hire",
        "status": "ready",
        "metadata": {},
        "steps": [
            {
                "id": "s1",
                "name": "Create account",
                "description": "",
                "status": "pending",
                "dependencies": [],
                "assignee": "it",
                "metadata": {},
            }
        ],
    }
    path = tmp_path / "workflow.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    wf = import_workflow(path)
    assert wf.id == "wf"
    assert wf.name == "Onboarding"
    assert wf.status is WorkflowStatus.READY
    assert wf.steps[0].assignee == "it"


def test_import_minimal_workflow(tmp_path):
    path = tmp_path / "min.json"
    path.write_text(json.dumps({"id": "wf", "name": "Minimal"}), encoding="utf-8")
    wf = import_workflow(str(path))
    assert wf.id == "wf"
    assert wf.schema_version
