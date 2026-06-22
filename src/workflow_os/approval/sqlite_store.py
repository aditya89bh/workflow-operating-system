"""An :class:`~workflow_os.approval.store.ApprovalStore` backed by SQLite.

Uses only the standard library ``sqlite3`` module. Requests are stored in a
single table; ``approvers``, ``decisions``, and ``metadata`` are serialised as
JSON and timestamps are stored as ISO-8601 strings.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime

from workflow_os.approval.record import ApprovalRequest
from workflow_os.approval.store import (
    ApprovalList,
    ApprovalNotFoundError,
    ApprovalQuery,
    apply_query,
)

_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS approval_requests (
    approval_id TEXT PRIMARY KEY,
    workflow_id TEXT NOT NULL,
    step_id TEXT,
    requester TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    state TEXT NOT NULL,
    approvers TEXT NOT NULL,
    decisions TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    metadata TEXT NOT NULL
)
"""

_COLUMNS = (
    "approval_id",
    "workflow_id",
    "step_id",
    "requester",
    "title",
    "description",
    "state",
    "approvers",
    "decisions",
    "created_at",
    "updated_at",
    "metadata",
)

_INSERT = f"""
INSERT OR REPLACE INTO approval_requests ({", ".join(_COLUMNS)})
VALUES ({", ".join("?" for _ in _COLUMNS)})
"""

_UPDATE = """
UPDATE approval_requests SET
    workflow_id = ?, step_id = ?, requester = ?, title = ?, description = ?,
    state = ?, approvers = ?, decisions = ?, created_at = ?, updated_at = ?,
    metadata = ?
WHERE approval_id = ?
"""


class SQLiteApprovalStore:
    """An approval store persisted to a SQLite database (file or in-memory)."""

    def __init__(self, path: str = ":memory:") -> None:
        self.path = path
        self._conn = sqlite3.connect(path)
        self._conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self) -> None:
        self._conn.execute(_CREATE_TABLE)
        self._conn.commit()

    @staticmethod
    def _values(request: ApprovalRequest) -> tuple[object, ...]:
        return (
            request.approval_id,
            request.workflow_id,
            request.step_id,
            request.requester,
            request.title,
            request.description,
            request.state,
            json.dumps(request.approvers),
            json.dumps(request.decisions),
            request.created_at.isoformat(),
            request.updated_at.isoformat(),
            json.dumps(request.metadata),
        )

    def add(self, request: ApprovalRequest) -> None:
        self._conn.execute(_INSERT, self._values(request))
        self._conn.commit()

    def update(self, request: ApprovalRequest) -> None:
        """Update an existing request, raising if its id is not present."""
        values = self._values(request)
        cursor = self._conn.execute(_UPDATE, (*values[1:], request.approval_id))
        self._conn.commit()
        if cursor.rowcount == 0:
            raise ApprovalNotFoundError(request.approval_id)

    def get(self, approval_id: str) -> ApprovalRequest:
        cursor = self._conn.execute(
            "SELECT * FROM approval_requests WHERE approval_id = ?", (approval_id,)
        )
        row = cursor.fetchone()
        if row is None:
            raise ApprovalNotFoundError(approval_id)
        return self._row_to_request(row)

    def delete(self, approval_id: str) -> None:
        cursor = self._conn.execute(
            "DELETE FROM approval_requests WHERE approval_id = ?", (approval_id,)
        )
        self._conn.commit()
        if cursor.rowcount == 0:
            raise ApprovalNotFoundError(approval_id)

    def list(self) -> ApprovalList:
        return apply_query(self._all_requests(), ApprovalQuery())

    def query(self, query: ApprovalQuery) -> ApprovalList:
        return apply_query(self._all_requests(), query)

    def close(self) -> None:
        self._conn.close()

    def __enter__(self) -> SQLiteApprovalStore:
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()

    def _all_requests(self) -> ApprovalList:
        cursor = self._conn.execute("SELECT * FROM approval_requests")
        return [self._row_to_request(row) for row in cursor.fetchall()]

    @staticmethod
    def _row_to_request(row: sqlite3.Row) -> ApprovalRequest:
        return ApprovalRequest(
            approval_id=str(row["approval_id"]),
            workflow_id=str(row["workflow_id"]),
            requester=str(row["requester"]),
            title=str(row["title"]),
            approvers=list(json.loads(row["approvers"])),
            step_id=row["step_id"],
            description=str(row["description"]),
            state=str(row["state"]),
            created_at=datetime.fromisoformat(str(row["created_at"])),
            updated_at=datetime.fromisoformat(str(row["updated_at"])),
            decisions=dict(json.loads(row["decisions"])),
            metadata=json.loads(row["metadata"]),
        )
