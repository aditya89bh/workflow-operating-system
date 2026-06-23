"""Standalone runner for every showcase demonstration.

Run with::

    PYTHONPATH=src python examples/run_all_demos.py
"""

from workflow_os.demos.registry import run_all_demos

if __name__ == "__main__":
    run_all_demos()
