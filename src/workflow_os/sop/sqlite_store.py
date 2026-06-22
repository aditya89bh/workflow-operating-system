"""A :class:`~workflow_os.sop.store.SOPStore` backed by SQLite.

Uses only the standard library ``sqlite3`` module. Records are stored in a
single table; ``tags`` and ``metadata`` are serialised as JSON and timestamps
are stored as ISO-8601 strings.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime

from workflow_os.sop.record import SOPRecord
from workflow_os.sop.store import (
    SOPList,
    SOPNotFoundError,
    SOPQuery,
    apply_query,
)

_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS sop_records (
    sop_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    workflow_type TEXT NOT NULL,
    description TEXT NOT NULL,
    version INTEGER NOT NULL,
    status TEXT NOT NULL,
    author TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    tags TEXT NOT NULL,
    metadata TEXT NOT NULL
)
"""

_COLUMNS = (
    "sop_id",
    "title",
    "workflow_type",
    "description",
    "version",
    "status",
    "author",
    "created_at",
    "updated_at",
    "tags",
    "metadata",
)

_INSERT = f"""
INSERT OR REPLACE INTO sop_records ({", ".join(_COLUMNS)})
VALUES ({", ".join("?" for _ in _COLUMNS)})
"""

_UPDATE = """
UPDATE sop_records SET
    title = ?, workflow_type = ?, description = ?, version = ?, status = ?,
    author = ?, created_at = ?, updated_at = ?, tags = ?, metadata = ?
WHERE sop_id = ?
"""


class SQLiteSOPStore:
    """A SOP store persisted to a SQLite database (file or in-memory)."""

    def __init__(self, path: str = ":memory:") -> None:
        self.path = path
        self._conn = sqlite3.connect(path)
        self._conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self) -> None:
        self._conn.execute(_CREATE_TABLE)
        self._conn.commit()

    @staticmethod
    def _values(record: SOPRecord) -> tuple[object, ...]:
        return (
            record.sop_id,
            record.title,
            record.workflow_type,
            record.description,
            record.version,
            record.status,
            record.author,
            record.created_at.isoformat(),
            record.updated_at.isoformat(),
            json.dumps(record.tags),
            json.dumps(record.metadata),
        )

    def add(self, record: SOPRecord) -> None:
        self._conn.execute(_INSERT, self._values(record))
        self._conn.commit()

    def update(self, record: SOPRecord) -> None:
        values = self._values(record)
        cursor = self._conn.execute(_UPDATE, (*values[1:], record.sop_id))
        self._conn.commit()
        if cursor.rowcount == 0:
            raise SOPNotFoundError(record.sop_id)

    def get(self, sop_id: str) -> SOPRecord:
        cursor = self._conn.execute(
            "SELECT * FROM sop_records WHERE sop_id = ?", (sop_id,)
        )
        row = cursor.fetchone()
        if row is None:
            raise SOPNotFoundError(sop_id)
        return self._row_to_record(row)

    def delete(self, sop_id: str) -> None:
        cursor = self._conn.execute(
            "DELETE FROM sop_records WHERE sop_id = ?", (sop_id,)
        )
        self._conn.commit()
        if cursor.rowcount == 0:
            raise SOPNotFoundError(sop_id)

    def list(self) -> SOPList:
        return apply_query(self._all_records(), SOPQuery())

    def query(self, query: SOPQuery) -> SOPList:
        return apply_query(self._all_records(), query)

    def close(self) -> None:
        self._conn.close()

    def __enter__(self) -> SQLiteSOPStore:
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()

    def _all_records(self) -> SOPList:
        cursor = self._conn.execute("SELECT * FROM sop_records")
        return [self._row_to_record(row) for row in cursor.fetchall()]

    @staticmethod
    def _row_to_record(row: sqlite3.Row) -> SOPRecord:
        return SOPRecord(
            sop_id=str(row["sop_id"]),
            title=str(row["title"]),
            workflow_type=str(row["workflow_type"]),
            description=str(row["description"]),
            version=int(row["version"]),
            status=str(row["status"]),
            author=row["author"],
            created_at=datetime.fromisoformat(str(row["created_at"])),
            updated_at=datetime.fromisoformat(str(row["updated_at"])),
            tags=list(json.loads(row["tags"])),
            metadata=json.loads(row["metadata"]),
        )
