"""Workflow schema versioning and lightweight migration support.

Persisted workflows carry a ``schema_version`` so that older payloads can be
recognised and upgraded to the current shape before being loaded.
"""

from __future__ import annotations

from typing import Any

CURRENT_SCHEMA_VERSION = "1.0"

SUPPORTED_SCHEMA_VERSIONS: frozenset[str] = frozenset({"1.0"})


class SchemaVersionError(ValueError):
    """Raised when a workflow payload uses an unsupported schema version."""


def is_supported_version(version: str) -> bool:
    """Return ``True`` if ``version`` can be loaded by this library."""
    return version in SUPPORTED_SCHEMA_VERSIONS


def validate_schema_version(version: str) -> None:
    """Raise :class:`SchemaVersionError` if ``version`` is not supported."""
    if not is_supported_version(version):
        supported = ", ".join(sorted(SUPPORTED_SCHEMA_VERSIONS))
        raise SchemaVersionError(
            f"unsupported schema version {version!r}; supported: [{supported}]"
        )


def migrate(data: dict[str, Any]) -> dict[str, Any]:
    """Upgrade a raw workflow payload to the current schema version.

    Payloads without a ``schema_version`` are assumed to predate versioning and
    are tagged as the earliest known version before validation.
    """
    payload = dict(data)
    payload.setdefault("schema_version", "1.0")
    validate_schema_version(payload["schema_version"])
    payload["schema_version"] = CURRENT_SCHEMA_VERSION
    return payload
