"""CLI release validation: core commands and every demo subcommand."""

import pytest

from workflow_os.cli import main


def test_create_show_list_roundtrip(tmp_path, capsys):
    store = str(tmp_path)
    assert main(["--store", store, "create", "--id", "wf", "--name", "WF",
                 "--step", "a:Step A", "--step", "b:Step B"]) == 0
    assert main(["--store", store, "list"]) == 0
    assert main(["--store", store, "show", "wf"]) == 0
    assert "wf" in capsys.readouterr().out


@pytest.mark.parametrize(
    "command",
    [
        "memory-demo",
        "decision-demo",
        "sop-demo",
        "approval-demo",
        "exception-demo",
        "multi-agent-demo",
        "analytics-demo",
        "learning-demo",
    ],
)
def test_subsystem_demos_run(command):
    assert main([command]) == 0


@pytest.mark.parametrize(
    "name",
    [
        "employee-onboarding",
        "procurement",
        "incident-management",
        "customer-onboarding",
        "workflow-memory",
        "workflow-decision",
        "approval-workflow",
        "exception-recovery",
        "analytics",
        "organizational-learning",
    ],
)
def test_named_demos_run(name):
    assert main(["demo", name]) == 0


def test_demo_all_runs():
    assert main(["demo-all"]) == 0


def test_unknown_demo_returns_error_code():
    assert main(["demo", "not-a-demo"]) == 2
