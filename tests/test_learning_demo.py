from workflow_os.learning.demo import run_demo


def test_run_demo_outputs_summary(capsys):
    run_demo()
    out = capsys.readouterr().out
    assert "executed workflows" in out
    assert "organizational maturity" in out
    assert "recommendations=" in out


def test_cli_learning_demo():
    from workflow_os.cli import main

    assert main(["learning-demo"]) == 0
