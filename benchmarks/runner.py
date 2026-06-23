"""Run the full benchmark suite and print the results."""

from __future__ import annotations

from benchmarks.analytics_generation import benchmark_analytics_generation
from benchmarks.common import BenchmarkResult
from benchmarks.memory_retrieval import benchmark_memory_retrieval
from benchmarks.workflow_execution import benchmark_workflow_execution


def run_all_benchmarks(iterations: int = 200) -> list[BenchmarkResult]:
    """Run every benchmark and return the list of results."""
    return [
        benchmark_workflow_execution(iterations),
        benchmark_memory_retrieval(iterations),
        benchmark_analytics_generation(iterations),
    ]


def main(iterations: int = 200) -> None:
    """Run the benchmark suite and print a table of results."""
    print(f"workflow-operating-system benchmarks ({iterations} iterations each)")
    print("-" * 70)
    for result in run_all_benchmarks(iterations):
        print(result)


if __name__ == "__main__":  # pragma: no cover
    main()
