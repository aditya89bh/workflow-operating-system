from workflow_os.approval import InMemoryApprovalStore, run_demo


def test_run_demo_completes(capsys):
    store = run_demo(InMemoryApprovalStore())
    captured = capsys.readouterr().out
    assert "creating approval request" in captured
    assert "bottleneck analysis" in captured
    assert "done." in captured
    request = store.get("budget-approval")
    assert request.state == "approved"


def test_cli_approval_demo():
    from workflow_os.cli import main

    assert main(["approval-demo"]) == 0
