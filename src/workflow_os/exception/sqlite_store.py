"""An :class:`~workflow_os.exception.store.ExceptionStore` backed by SQLite.

Uses only the standard library ``sqlite3`` module. Records are stored in a single
table; ``metadata`` is serialised as JSON, ``detected_at`` as an ISO-8601 string,
and ``resolved`` as an integer flag.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime

from workflow_os.exception.record import ExceptionRecord
from workflow_os.exception.store import (
    ExceptionList,
    ExceptionNotFoundError,
    ExceptionQuery,
    apply_query,
)

_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS exception_records (
    exception_id TEXT PRIMARY KEY,
    workflow_id TEXT NOT NULL,
    step_id TEXT,
    exception_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    message TEXT NOT NULL,
    source TEXT,
    detected_at TEXT NOT NULL,
    resolved INTEGER NOT NULL,
    metadata TEXT NOT NULL
)
"""

_COLUMNS = (
    "exception_id",
    "workflow_id",
    "step_id",
    "exception_type",
    "severity",
    "message",
    "source",
    "detected_at",
    "resolved",
    "metadata",
)

_INSERT = f"""
INSERT OR REPLACE INTO exception_records ({", ".join(_COLUMNS)})
VALUES ({", ".join("?" for _ in _COLUMNS)})
"""

_UPDATE = """
UPDATE exception_records SET
    workflow_id = ?, step_id = ?, exception_type = ?, severity = ?, message = ?,
    source = ?, detected_at = ?, resolved = ?, metadata = ?
WHERE exception_id = ?
"""


class SQLiteExceptionStore:
    """An exception store persisted to a SQLite database (file or in-memory)."""

    def __init__(self, path: str = ":memory:") -> None:
        self.path = path
        self._conn = sqlite3.connect(path)
        self._conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self) -> None:
        self._conn.execute(_CREATE_TABLE)
        self._conn.commit()

    @staticmethod
    def _values(record: ExceptionRecord) -> tuple[object, ...]:
        return (
            record.exception_id,
            record.workflow_id,
            record.step_id,
            record.exception_type,
            record.severity,
            record.message,
            record.source,
            record.detected_at.isoformat(),
            int(record.resolved),
            json.dumps(record.metadata),
        )

    def add(self, record: ExceptionRecord) -> None:
        self._conn.execute(_INSERT, self._values(record))
        self._conn.commit()

    def update(self, record: ExceptionRecord) -> None:
        """Update an existing record, raising if its id is not present."""
        values = self._values(record)
        cursor = self._conn.execute(_UPDATE, (*values[1:], record.exception_id))
        self._conn.commit()
        if cursor.rowcount == 0:
            raise ExceptionNotFoundError(record.exception_id)

    def get(self, exception_id: str) -> ExceptionRecord:
        cursor = self._conn.execute(
            "SELECT * FROM exception_records WHERE exception_id = ?", (exception_id,)
        )
        row = cursor.fetchone()
        if row is None:
            raise ExceptionNotFoundError(exception_id)
        return self._row_to_record(row)

    def delete(self, exception_id: str) -> None:
        cursor = self._conn.execute(
            "DELETE FROM exception_records WHERE exception_id = ?", (exception_id,)
        )
        self._conn.commit()
        if cursor.rowcount == 0:
            raise ExceptionNotFoundError(exception_id)

    def list(self) -> ExceptionList:
        return apply_query(self._all_records(), ExceptionQuery())

    def query(self, query: ExceptionQuery) -> ExceptionList:
        return apply_query(self._all_records(), query)

    def close(self) -> None:
        self._conn.close()

    def __enter__(self) -> SQLiteExceptionStore:
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()

    def _all_records(self) -> ExceptionList:
        cursor = self._conn.execute("SELECT * FROM exception_records")
        return [self._row_to_record(row) for row in cursor.fetchall()]

    @staticmethod
    def _row_to_record(row: sqlite3.Row) -> ExceptionRecord:
        return ExceptionRecord(
            exception_id=str(row["exception_id"]),
            workflow_id=str(row["workflow_id"]),
            exception_type=str(row["exception_type"]),
            severity=str(row["severity"]),
            message=str(row["message"]),
            step_id=row["step_id"],
            source=row["source"],
            detected_at=datetime.fromisoformat(str(row["detected_at"])),
            resolved=bool(row["resolved"]),
            metadata=json.loads(row["metadata"]),
        )
