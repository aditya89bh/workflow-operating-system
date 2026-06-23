from benchmarks import (
    benchmark_analytics_generation,
    benchmark_memory_retrieval,
    benchmark_workflow_execution,
    run_all_benchmarks,
)


def test_individual_benchmarks_run():
    for benchmark in (
        benchmark_workflow_execution,
        benchmark_memory_retrieval,
        benchmark_analytics_generation,
    ):
        result = benchmark(iterations=3)
        assert result.iterations == 3
        assert result.seconds >= 0.0


def test_run_all_benchmarks():
    results = run_all_benchmarks(iterations=2)
    names = {r.name for r in results}
    assert names == {
        "workflow_execution",
        "memory_retrieval",
        "analytics_generation",
    }


def test_ops_per_second_non_negative():
    result = benchmark_workflow_execution(iterations=2)
    assert result.ops_per_second >= 0.0
    assert "workflow_execution" in str(result)
