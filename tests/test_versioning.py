import pytest

from workflow_os import (
    CURRENT_SCHEMA_VERSION,
    SchemaVersionError,
    Workflow,
    is_supported_version,
    migrate,
    validate_schema_version,
)


def test_new_workflow_uses_current_schema_version():
    wf = Workflow(id="wf", name="Onboarding")
    assert wf.schema_version == CURRENT_SCHEMA_VERSION


def test_supported_version_checks():
    assert is_supported_version(CURRENT_SCHEMA_VERSION)
    assert not is_supported_version("99.0")


def test_validate_schema_version_rejects_unknown():
    with pytest.raises(SchemaVersionError):
        validate_schema_version("99.0")


def test_migrate_defaults_missing_version_and_upgrades():
    migrated = migrate({"id": "wf", "name": "Onboarding"})
    assert migrated["schema_version"] == CURRENT_SCHEMA_VERSION


def test_migrate_rejects_unsupported_version():
    with pytest.raises(SchemaVersionError):
        migrate({"schema_version": "99.0"})
