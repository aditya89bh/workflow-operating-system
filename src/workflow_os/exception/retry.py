"""Retry strategy support.

A deterministic retry strategy that decides whether an exception should be
retried and produces the next retry :class:`RecoveryAction`. The strategy caps
the number of attempts; it does not execute anything itself.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from workflow_os.exception.record import ExceptionRecord
from workflow_os.exception.recovery import RecoveryAction

_RETRY_ACTION = "retry"


def count_retries(
    recoveries: Iterable[RecoveryAction], exception_id: str
) -> int:
    """Return how many retry actions already exist for an exception."""
    return sum(
        1
        for recovery in recoveries
        if recovery.exception_id == exception_id and recovery.action == _RETRY_ACTION
    )


@dataclass
class RetryStrategy:
    """A capped, deterministic retry strategy."""

    max_attempts: int = 3

    def should_retry(self, attempts_made: int) -> bool:
        """Return ``True`` if another attempt is allowed."""
        return attempts_made < self.max_attempts

    def next_attempt(
        self,
        exception: ExceptionRecord,
        attempts_made: int,
        actor: str | None = None,
    ) -> RecoveryAction | None:
        """Return the next retry action, or ``None`` if attempts are exhausted."""
        if not self.should_retry(attempts_made):
            return None
        return RecoveryAction.create(
            exception_id=exception.exception_id,
            action=_RETRY_ACTION,
            actor=actor,
            metadata={"attempt": attempts_made + 1, "max_attempts": self.max_attempts},
        )
