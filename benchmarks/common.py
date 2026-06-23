"""Shared helpers for the benchmark suite."""

from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass


@dataclass
class BenchmarkResult:
    """The result of running a benchmark.

    Attributes:
        name: Human-readable benchmark name.
        iterations: How many times the workload ran.
        seconds: Total wall-clock time spent, in seconds.
    """

    name: str
    iterations: int
    seconds: float

    @property
    def ops_per_second(self) -> float:
        """Return iterations per second (0.0 if no time elapsed)."""
        return self.iterations / self.seconds if self.seconds else 0.0

    def __str__(self) -> str:
        return (
            f"{self.name:<28} {self.iterations:>6} iters  "
            f"{self.seconds * 1000:8.2f} ms  {self.ops_per_second:10.0f} ops/s"
        )


def timed(name: str, iterations: int, workload: Callable[[], object]) -> BenchmarkResult:
    """Run ``workload`` ``iterations`` times and return a :class:`BenchmarkResult`."""
    start = time.perf_counter()
    for _ in range(iterations):
        workload()
    elapsed = time.perf_counter() - start
    return BenchmarkResult(name=name, iterations=iterations, seconds=elapsed)
