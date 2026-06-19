import pytest

from workflow_os import (
    InMemoryWorkflowRepository,
    Workflow,
    WorkflowNotFoundError,
    WorkflowRepository,
)


def test_in_memory_repository_satisfies_protocol():
    repo = InMemoryWorkflowRepository()
    assert isinstance(repo, WorkflowRepository)


def test_save_and_load():
    repo = InMemoryWorkflowRepository()
    wf = Workflow(id="wf", name="Onboarding")
    repo.save(wf)
    assert repo.load("wf") is wf


def test_list_returns_all():
    repo = InMemoryWorkflowRepository()
    repo.save(Workflow(id="a", name="A"))
    repo.save(Workflow(id="b", name="B"))
    assert {wf.id for wf in repo.list()} == {"a", "b"}


def test_delete_removes_workflow():
    repo = InMemoryWorkflowRepository()
    repo.save(Workflow(id="wf", name="Onboarding"))
    repo.delete("wf")
    assert repo.list() == []


def test_load_missing_raises():
    repo = InMemoryWorkflowRepository()
    with pytest.raises(WorkflowNotFoundError):
        repo.load("missing")


def test_delete_missing_raises():
    repo = InMemoryWorkflowRepository()
    with pytest.raises(WorkflowNotFoundError):
        repo.delete("missing")
