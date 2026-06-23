"""Benchmark suite for the workflow operating system.

Small, deterministic micro-benchmarks for the hot paths: workflow execution,
memory retrieval, and analytics generation. Each benchmark returns a
:class:`BenchmarkResult` so the timings can be printed or collected.
"""

from benchmarks.analytics_generation import benchmark_analytics_generation
from benchmarks.common import BenchmarkResult, timed
from benchmarks.memory_retrieval import benchmark_memory_retrieval
from benchmarks.runner import run_all_benchmarks
from benchmarks.workflow_execution import benchmark_workflow_execution

__all__ = [
    "BenchmarkResult",
    "benchmark_analytics_generation",
    "benchmark_memory_retrieval",
    "benchmark_workflow_execution",
    "run_all_benchmarks",
    "timed",
]
