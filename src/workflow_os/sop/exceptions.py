"""Exception-to-SOP capture.

Captures the workflow exceptions and exception decisions that change how a
procedure is run, together with documentation explaining the exception. Entries
can be created directly or derived from a Phase 3
:class:`~workflow_os.decision.record.DecisionRecord` exception decision, linking
institutional knowledge back to the decision that produced it.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from workflow_os.decision.record import DecisionRecord
from workflow_os.sop.record import utcnow


def new_exception_id() -> str:
    """Return a fresh, unique exception id."""
    return uuid.uuid4().hex


SOPExceptionList = list["SOPExceptionRecord"]


@dataclass
class SOPExceptionRecord:
    """A documented workflow exception that may inform a SOP."""

    exception_id: str
    workflow_id: str
    description: str
    sop_id: str | None = None
    workflow_type: str | None = None
    decision_id: str | None = None
    reason: str | None = None
    author: str | None = None
    created_at: datetime = field(default_factory=utcnow)
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        *,
        workflow_id: str,
        description: str,
        sop_id: str | None = None,
        workflow_type: str | None = None,
        decision_id: str | None = None,
        reason: str | None = None,
        author: str | None = None,
        metadata: dict[str, Any] | None = None,
        created_at: datetime | None = None,
        exception_id: str | None = None,
    ) -> SOPExceptionRecord:
        """Build a record, filling in id and timestamp by default."""
        return cls(
            exception_id=exception_id or new_exception_id(),
            workflow_id=workflow_id,
            description=description,
            sop_id=sop_id,
            workflow_type=workflow_type,
            decision_id=decision_id,
            reason=reason,
            author=author,
            created_at=created_at or utcnow(),
            metadata=dict(metadata or {}),
        )


class SOPExceptionStore:
    """An in-memory collection of documented workflow exceptions."""

    def __init__(self) -> None:
        self._records: dict[str, SOPExceptionRecord] = {}

    def add(self, record: SOPExceptionRecord) -> None:
        """Store an exception record."""
        self._records[record.exception_id] = record

    def get(self, exception_id: str) -> SOPExceptionRecord:
        """Return an exception by id or raise ``KeyError`` if missing."""
        return self._records[exception_id]

    def list(self) -> SOPExceptionList:
        """Return all exceptions ordered by creation time."""
        return sorted(self._records.values(), key=lambda record: record.created_at)

    def for_sop(self, sop_id: str) -> SOPExceptionList:
        """Return exceptions linked to a SOP."""
        return [record for record in self.list() if record.sop_id == sop_id]

    def for_workflow(self, workflow_id: str) -> SOPExceptionList:
        """Return exceptions recorded for a workflow."""
        return [record for record in self.list() if record.workflow_id == workflow_id]


def capture_exception(
    store: SOPExceptionStore,
    *,
    workflow_id: str,
    description: str,
    sop_id: str | None = None,
    workflow_type: str | None = None,
    reason: str | None = None,
    author: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> SOPExceptionRecord:
    """Capture a documented workflow exception into ``store``."""
    record = SOPExceptionRecord.create(
        workflow_id=workflow_id,
        description=description,
        sop_id=sop_id,
        workflow_type=workflow_type,
        reason=reason,
        author=author,
        metadata=metadata,
    )
    store.add(record)
    return record


def capture_exception_from_decision(
    store: SOPExceptionStore,
    decision: DecisionRecord,
    *,
    sop_id: str | None = None,
    workflow_type: str | None = None,
    documentation: str | None = None,
) -> SOPExceptionRecord:
    """Capture an exception derived from a Phase 3 exception decision.

    The decision's text becomes the description (unless ``documentation``
    overrides it), and the decision id, actor, and recorded reason are carried
    over so the exception remains traceable to the decision that produced it.
    """
    reason = decision.metadata.get("reason")
    record = SOPExceptionRecord.create(
        workflow_id=decision.workflow_id,
        description=documentation or decision.decision,
        sop_id=sop_id,
        workflow_type=workflow_type,
        decision_id=decision.decision_id,
        reason=str(reason) if reason is not None else None,
        author=decision.actor,
        metadata={"decision_type": decision.decision_type},
    )
    store.add(record)
    return record
