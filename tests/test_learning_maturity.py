from workflow_os.approval.record import ApprovalRequest
from workflow_os.exception.recovery import RecoveryAction, RecoveryStatus
from workflow_os.learning import (
    maturity_level,
    organizational_maturity_score,
)
from workflow_os.memory.record import MemoryRecord
from workflow_os.sop.record import SOPRecord, SOPStatus


def rec(workflow_id, event_type):
    return MemoryRecord.create(workflow_id=workflow_id, event_type=event_type)


def test_maturity_level_bands():
    assert maturity_level(0.1) == "initial"
    assert maturity_level(0.5) == "developing"
    assert maturity_level(0.7) == "defined"
    assert maturity_level(0.9) == "managed"
    assert maturity_level(1.0) == "optimizing"


def test_perfect_organization():
    records = [rec("onboarding", "workflow_completed")]
    sops = [
        SOPRecord.create(
            title="t", workflow_type="onboarding", status=SOPStatus.ACTIVE.value
        )
    ]
    approvals = [
        ApprovalRequest.create(
            workflow_id="onboarding", requester="r", title="t", state="approved"
        )
    ]
    recoveries = [
        RecoveryAction.create(
            exception_id="e", action="retry", status=RecoveryStatus.SUCCEEDED.value
        )
    ]
    score = organizational_maturity_score(
        records, sops=sops, approvals=approvals, recoveries=recoveries
    )
    assert round(score.overall, 6) == 1.0
    assert score.level == "optimizing"
    assert "workflow_health" in score.components


def test_empty_inputs():
    score = organizational_maturity_score()
    assert score.overall == 0.0
    assert score.components == {}


def test_failing_organization_low_score():
    records = [rec("bad", "workflow_failed")]
    score = organizational_maturity_score(records)
    assert score.components["workflow_health"] == 0.0
