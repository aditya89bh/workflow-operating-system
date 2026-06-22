"""Analytics CSV export.

Serializes analytics rows (plain mappings or dataclass instances such as
``ExecutionSummary`` and ``Scorecard``) to CSV text or a file. Values that are
not simple scalars are stringified so the output stays flat and deterministic.
"""

from __future__ import annotations

import csv
import io
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import asdict, is_dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


def _to_mapping(row: Any) -> dict[str, Any]:
    if isinstance(row, Mapping):
        return dict(row)
    if is_dataclass(row) and not isinstance(row, type):
        return asdict(row)
    raise TypeError(f"cannot convert {type(row)!r} to a CSV row")


def _cell(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (dict, list, tuple)):
        return str(value)
    return str(value)


def rows_to_dicts(rows: Iterable[Any]) -> list[dict[str, Any]]:
    """Normalize an iterable of mappings/dataclasses into a list of dicts."""
    return [_to_mapping(row) for row in rows]


def to_csv(rows: Iterable[Any], *, fieldnames: Sequence[str] | None = None) -> str:
    """Return CSV text for ``rows``.

    ``fieldnames`` fixes the column order; when omitted, the keys of the first
    row are used. An empty input produces an empty string.
    """
    dict_rows = rows_to_dicts(rows)
    if not dict_rows:
        return ""
    columns = list(fieldnames) if fieldnames is not None else list(dict_rows[0].keys())
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=columns, extrasaction="ignore")
    writer.writeheader()
    for row in dict_rows:
        writer.writerow({key: _cell(row.get(key)) for key in columns})
    return buffer.getvalue()


def write_csv(
    path: str | Path,
    rows: Iterable[Any],
    *,
    fieldnames: Sequence[str] | None = None,
) -> Path:
    """Write ``rows`` as CSV to ``path`` and return the path."""
    target = Path(path)
    target.write_text(to_csv(rows, fieldnames=fieldnames), encoding="utf-8")
    return target
