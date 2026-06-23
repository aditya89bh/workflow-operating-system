from workflow_os.demos.integration_learning import run_demo


def test_run_demo_outputs_flow(capsys):
    run_demo()
    out = capsys.readouterr().out
    assert "workflow ->" in out
    assert "insights ->" in out
    assert "recommendations ->" in out
    assert "maturity ->" in out
    assert "maturity:" in out
