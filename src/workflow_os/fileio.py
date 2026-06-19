"""File-based import and export helpers for workflows."""

from __future__ import annotations

from pathlib import Path

from workflow_os.persistence import workflow_from_json, workflow_to_json
from workflow_os.workflow import Workflow


def import_workflow(path: str | Path) -> Workflow:
    """Load a workflow from a JSON file at ``path``."""
    text = Path(path).read_text(encoding="utf-8")
    return workflow_from_json(text)


def export_workflow(workflow: Workflow, path: str | Path, *, indent: int = 2) -> Path:
    """Write ``workflow`` to a JSON file at ``path`` and return the path.

    Parent directories are created if they do not already exist.
    """
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(workflow_to_json(workflow, indent=indent), encoding="utf-8")
    return target
