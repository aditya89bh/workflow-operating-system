import workflow_os


def test_package_exposes_version():
    assert isinstance(workflow_os.__version__, str)
    assert workflow_os.__version__.count(".") >= 1
