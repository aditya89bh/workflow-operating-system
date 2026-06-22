"""Fallback strategy support.

A deterministic fallback strategy that maps an exception to an alternative
recovery action when a retry is not appropriate or has been exhausted. The
mapping is fixed per exception type and may be overridden explicitly.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from workflow_os.exception.classification import ExceptionType, normalize_type
from workflow_os.exception.record import ExceptionRecord
from workflow_os.exception.recovery import RecoveryAction

_DEFAULT_FALLBACKS: dict[str, str] = {
    ExceptionType.TIMEOUT.value: "notify_owner",
    ExceptionType.STEP_FAILURE.value: "skip_step",
    ExceptionType.WORKFLOW_FAILURE.value: "rollback_workflow",
    ExceptionType.MISSING_RESOURCE.value: "use_default_resource",
    ExceptionType.APPROVAL_FAILURE.value: "route_to_alternate_approver",
    ExceptionType.VALIDATION_FAILURE.value: "skip_with_warning",
    ExceptionType.UNKNOWN.value: "escalate_to_human",
}

_DEFAULT_FALLBACK = "escalate_to_human"


@dataclass
class FallbackStrategy:
    """A deterministic fallback strategy keyed by exception type."""

    overrides: dict[str, str] = field(default_factory=dict)

    def fallback_for(self, exception: ExceptionRecord) -> str:
        """Return the fallback action name for an exception."""
        exception_type = normalize_type(exception.exception_type)
        if exception_type in self.overrides:
            return self.overrides[exception_type]
        return _DEFAULT_FALLBACKS.get(exception_type, _DEFAULT_FALLBACK)

    def fallback_action(
        self, exception: ExceptionRecord, actor: str | None = None
    ) -> RecoveryAction:
        """Return a pending fallback :class:`RecoveryAction` for an exception."""
        return RecoveryAction.create(
            exception_id=exception.exception_id,
            action=self.fallback_for(exception),
            actor=actor,
            metadata={"strategy": "fallback", "exception_type": exception.exception_type},
        )
