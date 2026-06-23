"""Benchmark: workflow execution (order resolution + recorded run)."""

from __future__ import annotations

from benchmarks.common import BenchmarkResult, timed
from workflow_os.demos.employee_onboarding import build_workflow
from workflow_os.memory.recorder import MemoryRecorder
from workflow_os.memory.sqlite_store import SQLiteMemoryStore


def _run_once() -> None:
    workflow = build_workflow()
    MemoryRecorder(SQLiteMemoryStore(":memory:")).run(workflow)


def benchmark_workflow_execution(iterations: int = 200) -> BenchmarkResult:
    """Benchmark running a workflow end to end through the memory recorder."""
    return timed("workflow_execution", iterations, _run_once)


if __name__ == "__main__":  # pragma: no cover
    print(benchmark_workflow_execution())
