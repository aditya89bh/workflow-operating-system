"""Standalone entry point for the approval system demonstration.

Run with::

    python examples/approval_demo.py

or via the CLI::

    workflow-os approval-demo
"""

from __future__ import annotations

from workflow_os.approval.demo import run_demo

if __name__ == "__main__":
    run_demo()
