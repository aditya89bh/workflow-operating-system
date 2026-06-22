"""Analytics JSON export.

Serializes analytics structures (dataclasses, lists, and dicts) to JSON text or
a file. Dataclasses are expanded recursively and datetimes are rendered as ISO
strings, so the output is deterministic and round-trippable.
"""

from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


def _default(value: Any) -> Any:
    if is_dataclass(value) and not isinstance(value, type):
        return asdict(value)
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, (set, frozenset)):
        return sorted(value)
    raise TypeError(f"cannot serialize {type(value)!r} to JSON")


def to_json(data: Any, *, indent: int = 2, sort_keys: bool = True) -> str:
    """Return JSON text for ``data`` (dataclasses and datetimes supported)."""
    return json.dumps(data, default=_default, indent=indent, sort_keys=sort_keys)


def write_json(path: str | Path, data: Any, *, indent: int = 2) -> Path:
    """Write ``data`` as JSON to ``path`` and return the path."""
    target = Path(path)
    target.write_text(to_json(data, indent=indent), encoding="utf-8")
    return target
