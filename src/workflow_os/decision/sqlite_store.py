"""A :class:`~workflow_os.decision.store.DecisionStore` backed by SQLite.

Uses only the standard library ``sqlite3`` module. Records are stored in a
single table; ``alternatives`` and ``metadata`` are serialised as JSON and
timestamps are stored as ISO-8601 strings.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime

from workflow_os.decision.record import DecisionRecord
from workflow_os.decision.store import (
    DecisionList,
    DecisionNotFoundError,
    DecisionQuery,
    apply_query,
)

_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS decision_records (
    decision_id TEXT PRIMARY KEY,
    workflow_id TEXT NOT NULL,
    step_id TEXT,
    actor TEXT,
    decision_type TEXT NOT NULL,
    decision TEXT NOT NULL,
    rationale TEXT NOT NULL,
    alternatives TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    outcome TEXT NOT NULL,
    confidence REAL NOT NULL,
    metadata TEXT NOT NULL
)
"""

_COLUMNS = (
    "decision_id",
    "workflow_id",
    "step_id",
    "actor",
    "decision_type",
    "decision",
    "rationale",
    "alternatives",
    "timestamp",
    "outcome",
    "confidence",
    "metadata",
)

_INSERT = f"""
INSERT OR REPLACE INTO decision_records ({", ".join(_COLUMNS)})
VALUES ({", ".join("?" for _ in _COLUMNS)})
"""

_UPDATE = """
UPDATE decision_records SET
    workflow_id = ?, step_id = ?, actor = ?, decision_type = ?, decision = ?,
    rationale = ?, alternatives = ?, timestamp = ?, outcome = ?,
    confidence = ?, metadata = ?
WHERE decision_id = ?
"""


class SQLiteDecisionStore:
    """A decision store persisted to a SQLite database (file or in-memory)."""

    def __init__(self, path: str = ":memory:") -> None:
        self.path = path
        self._conn = sqlite3.connect(path)
        self._conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self) -> None:
        self._conn.execute(_CREATE_TABLE)
        self._conn.commit()

    @staticmethod
    def _values(record: DecisionRecord) -> tuple[object, ...]:
        return (
            record.decision_id,
            record.workflow_id,
            record.step_id,
            record.actor,
            record.decision_type,
            record.decision,
            record.rationale,
            json.dumps(record.alternatives),
            record.timestamp.isoformat(),
            record.outcome,
            record.confidence,
            json.dumps(record.metadata),
        )

    def add(self, record: DecisionRecord) -> None:
        self._conn.execute(_INSERT, self._values(record))
        self._conn.commit()

    def update(self, record: DecisionRecord) -> None:
        """Update an existing record, raising if its id is not present."""
        values = self._values(record)
        cursor = self._conn.execute(_UPDATE, (*values[1:], record.decision_id))
        self._conn.commit()
        if cursor.rowcount == 0:
            raise DecisionNotFoundError(record.decision_id)

    def get(self, decision_id: str) -> DecisionRecord:
        cursor = self._conn.execute(
            "SELECT * FROM decision_records WHERE decision_id = ?", (decision_id,)
        )
        row = cursor.fetchone()
        if row is None:
            raise DecisionNotFoundError(decision_id)
        return self._row_to_record(row)

    def list(self) -> DecisionList:
        return apply_query(self._all_records(), DecisionQuery())

    def delete(self, decision_id: str) -> None:
        cursor = self._conn.execute(
            "DELETE FROM decision_records WHERE decision_id = ?", (decision_id,)
        )
        self._conn.commit()
        if cursor.rowcount == 0:
            raise DecisionNotFoundError(decision_id)

    def query(self, query: DecisionQuery) -> DecisionList:
        return apply_query(self._all_records(), query)

    def close(self) -> None:
        self._conn.close()

    def __enter__(self) -> SQLiteDecisionStore:
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()

    def _all_records(self) -> DecisionList:
        cursor = self._conn.execute("SELECT * FROM decision_records")
        return [self._row_to_record(row) for row in cursor.fetchall()]

    @staticmethod
    def _row_to_record(row: sqlite3.Row) -> DecisionRecord:
        return DecisionRecord(
            decision_id=str(row["decision_id"]),
            workflow_id=str(row["workflow_id"]),
            decision_type=str(row["decision_type"]),
            decision=str(row["decision"]),
            timestamp=datetime.fromisoformat(str(row["timestamp"])),
            step_id=row["step_id"],
            actor=row["actor"],
            rationale=str(row["rationale"]),
            alternatives=list(json.loads(row["alternatives"])),
            outcome=str(row["outcome"]),
            confidence=float(row["confidence"]),
            metadata=json.loads(row["metadata"]),
        )
