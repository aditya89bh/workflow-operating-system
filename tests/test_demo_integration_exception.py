from workflow_os.demos.integration_exception import run_demo


def test_run_demo_outputs_flow(capsys):
    run_demo()
    out = capsys.readouterr().out
    assert "workflow ->" in out
    assert "failure ->" in out
    assert "recovery ->" in out
    assert "reporting ->" in out
    assert "recovery success rate" in out
