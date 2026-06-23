from workflow_os.demos.integration_decision import run_demo


def test_run_demo_outputs_flow(capsys):
    run_demo()
    out = capsys.readouterr().out
    assert "workflow ->" in out
    assert "decisions ->" in out
    assert "replay ->" in out
    assert "stored 3 decisions" in out
