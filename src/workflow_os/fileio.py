"""File-based import and export helpers for workflows."""

from __future__ import annotations

from pathlib import Path

from workflow_os.persistence import workflow_from_json
from workflow_os.workflow import Workflow


def import_workflow(path: str | Path) -> Workflow:
    """Load a workflow from a JSON file at ``path``."""
    text = Path(path).read_text(encoding="utf-8")
    return workflow_from_json(text)
