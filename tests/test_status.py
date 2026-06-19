from workflow_os import WorkflowStatus


def test_status_values():
    expected = {
        "draft",
        "ready",
        "running",
        "paused",
        "completed",
        "failed",
        "cancelled",
    }
    assert {s.value for s in WorkflowStatus} == expected


def test_status_is_string_enum():
    assert WorkflowStatus.RUNNING == "running"
    assert str(WorkflowStatus.COMPLETED) == "completed"
