"""A :class:`~workflow_os.memory.store.MemoryStore` backed by SQLite.

Uses only the standard library ``sqlite3`` module. Records are stored in a
single table; ``metadata`` is serialised as JSON and timestamps are stored as
ISO-8601 strings.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime

from workflow_os.memory.record import MemoryRecord
from workflow_os.memory.store import (
    MemoryNotFoundError,
    MemoryQuery,
    RecordList,
    apply_query,
)

_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS memory_records (
    event_id TEXT PRIMARY KEY,
    workflow_id TEXT NOT NULL,
    step_id TEXT,
    actor TEXT,
    event_type TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    confidence REAL NOT NULL,
    metadata TEXT NOT NULL
)
"""

_INSERT = """
INSERT OR REPLACE INTO memory_records
    (event_id, workflow_id, step_id, actor, event_type, timestamp, confidence, metadata)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
"""


class SQLiteMemoryStore:
    """A memory store persisted to a SQLite database (file or in-memory)."""

    def __init__(self, path: str = ":memory:") -> None:
        self.path = path
        self._conn = sqlite3.connect(path)
        self._conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self) -> None:
        self._conn.execute(_CREATE_TABLE)
        self._conn.commit()

    def add(self, record: MemoryRecord) -> None:
        self._conn.execute(
            _INSERT,
            (
                record.event_id,
                record.workflow_id,
                record.step_id,
                record.actor,
                record.event_type,
                record.timestamp.isoformat(),
                record.confidence,
                json.dumps(record.metadata),
            ),
        )
        self._conn.commit()

    def get(self, event_id: str) -> MemoryRecord:
        cursor = self._conn.execute(
            "SELECT * FROM memory_records WHERE event_id = ?", (event_id,)
        )
        row = cursor.fetchone()
        if row is None:
            raise MemoryNotFoundError(event_id)
        return self._row_to_record(row)

    def list(self) -> RecordList:
        return apply_query(self._all_records(), MemoryQuery())

    def delete(self, event_id: str) -> None:
        cursor = self._conn.execute(
            "DELETE FROM memory_records WHERE event_id = ?", (event_id,)
        )
        self._conn.commit()
        if cursor.rowcount == 0:
            raise MemoryNotFoundError(event_id)

    def query(self, query: MemoryQuery) -> RecordList:
        return apply_query(self._all_records(), query)

    def close(self) -> None:
        self._conn.close()

    def __enter__(self) -> SQLiteMemoryStore:
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()

    def _all_records(self) -> RecordList:
        cursor = self._conn.execute("SELECT * FROM memory_records")
        return [self._row_to_record(row) for row in cursor.fetchall()]

    @staticmethod
    def _row_to_record(row: sqlite3.Row) -> MemoryRecord:
        return MemoryRecord(
            event_id=str(row["event_id"]),
            workflow_id=str(row["workflow_id"]),
            event_type=str(row["event_type"]),
            timestamp=datetime.fromisoformat(str(row["timestamp"])),
            step_id=row["step_id"],
            actor=row["actor"],
            confidence=float(row["confidence"]),
            metadata=json.loads(row["metadata"]),
        )
