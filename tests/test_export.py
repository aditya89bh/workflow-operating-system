from workflow_os import (
    Workflow,
    WorkflowStatus,
    WorkflowStep,
    export_workflow,
    import_workflow,
)


def make_workflow() -> Workflow:
    return Workflow(
        id="wf",
        name="Onboarding",
        status=WorkflowStatus.READY,
        steps=[WorkflowStep(id="s1", name="Create account")],
    )


def test_export_then_import_round_trip(tmp_path):
    wf = make_workflow()
    path = export_workflow(wf, tmp_path / "wf.json")
    assert path.exists()
    assert import_workflow(path) == wf


def test_export_creates_parent_directories(tmp_path):
    wf = make_workflow()
    target = tmp_path / "nested" / "dir" / "wf.json"
    export_workflow(wf, target)
    assert target.exists()
