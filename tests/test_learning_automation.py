from workflow_os.approval.record import ApprovalRequest
from workflow_os.exception.recovery import RecoveryAction
from workflow_os.learning import (
    automation_opportunity_recommendations,
    repeated_approval_recommendations,
    repeated_recovery_recommendations,
    repetitive_task_recommendations,
)
from workflow_os.memory.record import MemoryRecord


def rec(workflow_id, event_type, step_id=None):
    return MemoryRecord.create(
        workflow_id=workflow_id, event_type=event_type, step_id=step_id
    )


def test_repetitive_tasks():
    records = [rec("wf", "step_completed", "notify") for _ in range(3)]
    recs = repetitive_task_recommendations(records, min_occurrences=3)
    assert recs and recs[0].metadata["step_id"] == "notify"


def test_repeated_approvals():
    approvals = [
        ApprovalRequest.create(workflow_id="wf", requester="a", title="t")
        for _ in range(3)
    ]
    recs = repeated_approval_recommendations(approvals, min_occurrences=3)
    assert recs and recs[0].metadata["workflow_id"] == "wf"


def test_repeated_recoveries():
    actions = [
        RecoveryAction.create(exception_id=f"e{i}", action="retry") for i in range(2)
    ]
    recs = repeated_recovery_recommendations(actions, min_occurrences=2)
    assert recs and recs[0].metadata["recovery_action"] == "retry"


def test_combined():
    records = [rec("wf", "step_completed", "notify") for _ in range(3)]
    recs = automation_opportunity_recommendations(records, min_task_occurrences=3)
    assert all(r.category == "automation" for r in recs)
    assert len(recs) == 1
