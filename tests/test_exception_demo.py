from workflow_os.exception import InMemoryExceptionStore, run_demo


def test_run_demo_completes(capsys):
    store = run_demo(InMemoryExceptionStore())
    captured = capsys.readouterr().out
    assert "triggering workflow failure" in captured
    assert "exception report" in captured
    assert "done." in captured
    assert len(store.list()) == 2
    assert all(r.exception_type == "timeout" for r in store.list())


def test_cli_exception_demo():
    from workflow_os.cli import main

    assert main(["exception-demo"]) == 0
