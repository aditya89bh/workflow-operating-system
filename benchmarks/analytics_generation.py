"""Benchmark: analytics generation over recorded history."""

from __future__ import annotations

from benchmarks.common import BenchmarkResult, timed
from workflow_os.analytics.completion import workflow_completion_metrics
from workflow_os.analytics.duration import execution_duration_metrics
from workflow_os.analytics.failure import workflow_failure_metrics
from workflow_os.analytics.reports import workflow_statistics
from workflow_os.demos.employee_onboarding import build_workflow
from workflow_os.memory.record import MemoryRecord
from workflow_os.memory.recorder import MemoryRecorder
from workflow_os.memory.sqlite_store import SQLiteMemoryStore


def _recorded_events(runs: int = 25) -> list[MemoryRecord]:
    store = SQLiteMemoryStore(":memory:")
    recorder = MemoryRecorder(store)
    for index in range(runs):
        workflow = build_workflow()
        workflow.id = f"employee-onboarding-{index}"
        recorder.run(workflow)
    return store.list()


def benchmark_analytics_generation(iterations: int = 200) -> BenchmarkResult:
    """Benchmark computing the core analytics metrics and statistics."""
    records = _recorded_events()

    def _generate() -> None:
        workflow_completion_metrics(records)
        workflow_failure_metrics(records)
        execution_duration_metrics(records)
        workflow_statistics(records)

    return timed("analytics_generation", iterations, _generate)


if __name__ == "__main__":  # pragma: no cover
    print(benchmark_analytics_generation())
