"""Recovery recommendation engine.

Maps an exception to a recommended recovery action using a fixed, deterministic
rule table keyed by exception type. There is no learning and no LLM involvement:
the same exception type always yields the same recommendation.
"""

from __future__ import annotations

from workflow_os.exception.classification import ExceptionType, normalize_type
from workflow_os.exception.record import ExceptionRecord
from workflow_os.exception.recovery import RecoveryAction

_RECOMMENDATIONS: dict[str, str] = {
    ExceptionType.TIMEOUT.value: "retry",
    ExceptionType.STEP_FAILURE.value: "retry_step",
    ExceptionType.WORKFLOW_FAILURE.value: "restart_workflow",
    ExceptionType.MISSING_RESOURCE.value: "provision_resource",
    ExceptionType.APPROVAL_FAILURE.value: "escalate_approval",
    ExceptionType.VALIDATION_FAILURE.value: "fix_and_resubmit",
    ExceptionType.UNKNOWN.value: "manual_review",
}

_DEFAULT_ACTION = "manual_review"


def recommend_action(exception: ExceptionRecord) -> str:
    """Return the recommended recovery action name for an exception."""
    return _RECOMMENDATIONS.get(normalize_type(exception.exception_type), _DEFAULT_ACTION)


def recommend_recovery(
    exception: ExceptionRecord, actor: str | None = None
) -> RecoveryAction:
    """Return a pending :class:`RecoveryAction` for an exception."""
    return RecoveryAction.create(
        exception_id=exception.exception_id,
        action=recommend_action(exception),
        actor=actor,
        metadata={"exception_type": exception.exception_type},
    )
