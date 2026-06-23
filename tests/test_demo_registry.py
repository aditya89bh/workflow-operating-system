import pytest

from workflow_os.cli import main
from workflow_os.demos.registry import (
    DEMOS,
    demo_names,
    run_all_demos,
    run_named_demo,
)


def test_registry_has_ten_demos():
    assert len(DEMOS) == 10
    assert "employee-onboarding" in demo_names()
    assert "organizational-learning" in demo_names()


def test_run_named_demo(capsys):
    run_named_demo("employee-onboarding")
    assert "Employee Onboarding" in capsys.readouterr().out


def test_run_named_demo_unknown():
    with pytest.raises(KeyError):
        run_named_demo("does-not-exist")


def test_run_all_demos(capsys):
    run_all_demos()
    out = capsys.readouterr().out
    for name in demo_names():
        assert name in out


def test_cli_demo_all():
    assert main(["demo-all"]) == 0


def test_cli_demo_named():
    assert main(["demo", "procurement"]) == 0


def test_cli_demo_unknown():
    assert main(["demo", "nope"]) == 2
