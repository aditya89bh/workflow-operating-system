from workflow_os import (
    StepStatus,
    Workflow,
    WorkflowStatus,
    WorkflowStep,
    workflow_from_dict,
    workflow_from_json,
    workflow_to_dict,
    workflow_to_json,
)


def make_workflow() -> Workflow:
    return Workflow(
        id="wf",
        name="Onboarding",
        description="New hire onboarding",
        status=WorkflowStatus.READY,
        metadata={"owner": "people-ops"},
        steps=[
            WorkflowStep(id="s1", name="Create account", assignee="it"),
            WorkflowStep(
                id="s2",
                name="Assign laptop",
                dependencies=["s1"],
                status=StepStatus.PENDING,
            ),
        ],
    )


def test_dict_round_trip():
    wf = make_workflow()
    restored = workflow_from_dict(workflow_to_dict(wf))
    assert restored == wf


def test_json_round_trip():
    wf = make_workflow()
    restored = workflow_from_json(workflow_to_json(wf))
    assert restored == wf


def test_status_serialized_as_plain_string():
    data = workflow_to_dict(make_workflow())
    assert data["status"] == "ready"
    assert data["steps"][0]["status"] == "pending"


def test_from_dict_applies_schema_version_default():
    wf = workflow_from_dict({"id": "wf", "name": "Minimal"})
    assert wf.schema_version
    assert wf.status is WorkflowStatus.DRAFT
