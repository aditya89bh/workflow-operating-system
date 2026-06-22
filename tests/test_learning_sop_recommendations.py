from workflow_os.exception.record import ExceptionRecord
from workflow_os.learning import sop_update_recommendations
from workflow_os.sop.record import SOPRecord, SOPStatus


def sop(workflow_type, status):
    return SOPRecord.create(
        title=f"{workflow_type} SOP",
        workflow_type=workflow_type,
        status=status,
    )


def exc(workflow_id):
    return ExceptionRecord.create(workflow_id=workflow_id, exception_type="timeout")


def test_update_outdated_sop():
    sops = [sop("onboarding", SOPStatus.DEPRECATED.value)]
    recs = sop_update_recommendations(sops)
    assert any(r.metadata.get("action") == "update_outdated" for r in recs)


def test_revise_exception_handling():
    sops = [sop("onboarding", SOPStatus.ACTIVE.value)]
    exceptions = [exc("onboarding"), exc("onboarding")]
    recs = sop_update_recommendations(
        sops, exceptions=exceptions, min_exception_occurrences=2
    )
    revise = [r for r in recs if r.metadata.get("action") == "revise_exceptions"]
    assert revise and revise[0].metadata["workflow_type"] == "onboarding"


def test_add_missing_guidance():
    exceptions = [exc("offboarding"), exc("offboarding")]
    recs = sop_update_recommendations(
        [], exceptions=exceptions, min_exception_occurrences=2
    )
    missing = [r for r in recs if r.metadata.get("action") == "add_missing"]
    assert missing and missing[0].metadata["workflow_type"] == "offboarding"


def test_no_recommendations_when_healthy():
    sops = [sop("onboarding", SOPStatus.ACTIVE.value)]
    assert sop_update_recommendations(sops) == []
