"""Benchmark: memory retrieval queries over a populated store."""

from __future__ import annotations

from benchmarks.common import BenchmarkResult, timed
from workflow_os.demos.employee_onboarding import build_workflow
from workflow_os.memory.recorder import MemoryRecorder
from workflow_os.memory.retrieval import get_actor_history, get_workflow_history
from workflow_os.memory.sqlite_store import SQLiteMemoryStore


def _populated_store(runs: int = 25) -> SQLiteMemoryStore:
    store = SQLiteMemoryStore(":memory:")
    recorder = MemoryRecorder(store)
    for index in range(runs):
        workflow = build_workflow()
        workflow.id = f"employee-onboarding-{index}"
        recorder.run(workflow)
    return store


def benchmark_memory_retrieval(iterations: int = 200) -> BenchmarkResult:
    """Benchmark retrieving workflow and actor history from a populated store."""
    store = _populated_store()

    def _query() -> None:
        get_workflow_history(store, "employee-onboarding-0")
        get_actor_history(store, "it")

    return timed("memory_retrieval", iterations, _query)


if __name__ == "__main__":  # pragma: no cover
    print(benchmark_memory_retrieval())
