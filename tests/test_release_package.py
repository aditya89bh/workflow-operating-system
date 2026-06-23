"""Package-level release validation: version, metadata, and public API."""

import importlib

import workflow_os


def test_version_is_0_1_0():
    assert workflow_os.__version__ == "0.1.0"


def test_top_level_public_api_importable():
    for name in workflow_os.__all__:
        assert hasattr(workflow_os, name), name


def test_subpackages_import():
    for module in (
        "workflow_os.memory",
        "workflow_os.decision",
        "workflow_os.sop",
        "workflow_os.approval",
        "workflow_os.exception",
        "workflow_os.agents",
        "workflow_os.analytics",
        "workflow_os.learning",
        "workflow_os.demos",
        "workflow_os.cli",
    ):
        assert importlib.import_module(module) is not None


def test_console_entry_point_target_callable():
    from workflow_os.cli import main

    assert callable(main)
