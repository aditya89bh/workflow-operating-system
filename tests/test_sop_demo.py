from workflow_os.cli import main
from workflow_os.sop import SQLiteSOPStore, run_demo


def test_run_demo_populates_store_and_prints(capsys):
    store = SQLiteSOPStore()
    returned = run_demo(store)
    assert returned is store
    assert len(store.list()) == 1
    assert store.get("onboarding-sop").version == 2

    out = capsys.readouterr().out
    assert "creating SOP" in out
    assert "lifecycle report" in out


def test_cli_sop_demo(capsys):
    assert main(["sop-demo"]) == 0
    out = capsys.readouterr().out
    assert "recommending SOP" in out
