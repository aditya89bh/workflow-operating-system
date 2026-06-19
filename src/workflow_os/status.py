"""Lifecycle status for workflows."""

from __future__ import annotations

from enum import Enum


class WorkflowStatus(str, Enum):
    """The lifecycle states a workflow can be in.

    The values are plain strings so workflows serialize cleanly to JSON.
    """

    DRAFT = "draft"
    READY = "ready"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

    def __str__(self) -> str:  # pragma: no cover - convenience only
        return self.value
