from workflow_os.cli import main


def run(args, store):
    return main(["--store", str(store), *args])


def test_create_show_and_list(tmp_path, capsys):
    create_args = ["create", "--id", "wf", "--name", "Onboarding", "--step", "s1:Setup"]
    assert run(create_args, tmp_path) == 0
    assert (tmp_path / "wf.json").exists()

    assert run(["list"], tmp_path) == 0
    listed = capsys.readouterr().out
    assert "wf" in listed
    assert "draft" in listed

    assert run(["show", "wf"], tmp_path) == 0
    shown = capsys.readouterr().out
    assert '"id": "wf"' in shown


def test_lifecycle_commands(tmp_path, capsys):
    run(["create", "--id", "wf", "--name", "Onboarding"], tmp_path)
    capsys.readouterr()

    assert run(["start", "wf"], tmp_path) == 0
    assert "running" in capsys.readouterr().out

    assert run(["pause", "wf"], tmp_path) == 0
    assert "paused" in capsys.readouterr().out

    assert run(["resume", "wf"], tmp_path) == 0
    assert "running" in capsys.readouterr().out

    assert run(["complete", "wf"], tmp_path) == 0
    assert "completed" in capsys.readouterr().out


def test_list_empty_store(tmp_path, capsys):
    assert run(["list"], tmp_path) == 0
    assert "no workflows found" in capsys.readouterr().out
