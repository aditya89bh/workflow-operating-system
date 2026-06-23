from workflow_os.demos.integration_analytics import run_demo


def test_run_demo_outputs_flow(capsys):
    run_demo()
    out = capsys.readouterr().out
    assert "workflow ->" in out
    assert "metrics ->" in out
    assert "reports ->" in out
    assert "exports ->" in out
    assert "csv export" in out
    assert "json export" in out
