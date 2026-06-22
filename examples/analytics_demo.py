"""Standalone runner for the workflow analytics demonstration.

Run with::

    PYTHONPATH=src python examples/analytics_demo.py
"""

from workflow_os.analytics.demo import run_demo

if __name__ == "__main__":
    run_demo()
