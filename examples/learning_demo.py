"""Standalone runner for the organizational learning demonstration.

Run with::

    PYTHONPATH=src python examples/learning_demo.py
"""

from workflow_os.learning.demo import run_demo

if __name__ == "__main__":
    run_demo()
