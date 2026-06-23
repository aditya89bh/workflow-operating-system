from workflow_os.demos.integration_memory import run_demo


def test_run_demo_outputs_flow(capsys):
    run_demo()
    out = capsys.readouterr().out
    assert "workflow ->" in out
    assert "memory ->" in out
    assert "retrieval ->" in out
    assert "execution timeline" in out
