from workflow_os.exception.record import ExceptionRecord
from workflow_os.exception.recovery import RecoveryAction
from workflow_os.learning import (
    chronic_workflow_problems,
    recurring_exception_insights,
    recurring_recovery_actions,
    repeated_exceptions,
)


def exc(workflow_id, exception_type="timeout"):
    return ExceptionRecord.create(workflow_id=workflow_id, exception_type=exception_type)


def test_repeated_exceptions():
    exceptions = [exc("wf1"), exc("wf1"), exc("wf2")]
    assert repeated_exceptions(exceptions, min_occurrences=2) == {"wf1:timeout": 2}


def test_chronic_workflow_problems():
    exceptions = [exc("wf1"), exc("wf1"), exc("wf1"), exc("wf2")]
    assert chronic_workflow_problems(exceptions, min_occurrences=3) == ["wf1"]


def test_recurring_recovery_actions():
    actions = [
        RecoveryAction.create(exception_id="e1", action="retry"),
        RecoveryAction.create(exception_id="e2", action="retry"),
        RecoveryAction.create(exception_id="e3", action="escalate"),
    ]
    assert recurring_recovery_actions(actions, min_occurrences=2) == {"retry": 2}


def test_recurring_exception_insights():
    exceptions = [exc("wf1"), exc("wf1")]
    insights = recurring_exception_insights(exceptions, min_occurrences=2)
    assert len(insights) == 1
    assert insights[0].category == "exception"
    assert insights[0].metadata["workflow_id"] == "wf1"
