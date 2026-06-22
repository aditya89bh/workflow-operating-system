from workflow_os.cli import main
from workflow_os.memory import AuditReport, SQLiteMemoryStore, run_demo


def test_run_demo_returns_report(capsys):
    store = SQLiteMemoryStore()
    report = run_demo(store)
    out = capsys.readouterr().out

    assert isinstance(report, AuditReport)
    assert report.total_events > 0
    assert report.workflow_count == 1
    assert "Audit report" in out
    assert "Workflow history" in out


def test_cli_memory_demo_command(capsys):
    assert main(["memory-demo"]) == 0
    out = capsys.readouterr().out
    assert "Executing workflow" in out
    assert "total events" in out
