from workflow_os.analytics import run_demo


def test_run_demo_outputs_summary(capsys):
    run_demo()
    out = capsys.readouterr().out
    assert "recorded" in out
    assert "metrics:" in out
    assert "health score:" in out
    assert "csv export" in out
    assert "json export:" in out


def test_run_demo_reports_one_failure(capsys):
    run_demo()
    out = capsys.readouterr().out
    assert "failed=1" in out
