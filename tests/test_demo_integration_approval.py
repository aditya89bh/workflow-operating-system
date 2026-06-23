from workflow_os.demos.integration_approval import run_demo


def test_run_demo_outputs_flow(capsys):
    run_demo()
    out = capsys.readouterr().out
    assert "workflow ->" in out
    assert "approval ->" in out
    assert "audit ->" in out
    assert "approved" in out
