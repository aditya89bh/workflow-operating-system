from workflow_os.cli import main
from workflow_os.decision import SQLiteDecisionStore, run_demo


def test_run_demo_populates_store_and_prints(capsys):
    store = SQLiteDecisionStore()
    returned = run_demo(store)
    assert returned is store
    assert len(store.list()) == 3

    out = capsys.readouterr().out
    assert "executing workflow" in out
    assert "replaying decisions" in out


def test_cli_decision_demo(capsys):
    assert main(["decision-demo"]) == 0
    out = capsys.readouterr().out
    assert "recording decisions" in out
