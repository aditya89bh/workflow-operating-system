"""Standalone organizational memory demonstration.

Run directly with::

    python examples/memory_demo.py

or through the CLI::

    workflow-os memory-demo

It executes a workflow, generates and stores memory events, retrieves the
workflow history, and prints an audit report.
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))

from workflow_os.memory.demo import run_demo  # noqa: E402


def main() -> int:
    run_demo()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
