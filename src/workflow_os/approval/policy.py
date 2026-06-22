"""The :class:`ApprovalPolicy` schema.

A policy describes how an approval should be conducted: what kind of workflow it
uses (single, multi, sequential, parallel), how many approvals are required, and
how long to wait before escalation.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


def new_policy_id() -> str:
    """Return a fresh, unique policy id."""
    return uuid.uuid4().hex


class PolicyType(str, Enum):
    """The supported approval policy types."""

    SINGLE = "single"
    MULTI = "multi"
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"

    def __str__(self) -> str:  # pragma: no cover - convenience only
        return self.value


@dataclass
class ApprovalPolicy:
    """A rule set describing how an approval is conducted.

    Attributes:
        policy_id: Unique identifier for the policy.
        name: Human-readable policy name.
        policy_type: One of the :class:`PolicyType` values.
        required_approvals: Number of approvals required to approve.
        escalation_timeout: Seconds before the request should escalate, or
            ``None`` to disable escalation.
        metadata: Arbitrary key/value data attached to the policy.
    """

    policy_id: str
    name: str
    policy_type: str = PolicyType.SINGLE.value
    required_approvals: int = 1
    escalation_timeout: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        *,
        name: str,
        policy_type: str = PolicyType.SINGLE.value,
        required_approvals: int = 1,
        escalation_timeout: float | None = None,
        metadata: dict[str, Any] | None = None,
        policy_id: str | None = None,
    ) -> ApprovalPolicy:
        """Build an :class:`ApprovalPolicy`, filling in the id if needed."""
        return cls(
            policy_id=policy_id or new_policy_id(),
            name=name,
            policy_type=str(policy_type),
            required_approvals=int(required_approvals),
            escalation_timeout=escalation_timeout,
            metadata=dict(metadata or {}),
        )
