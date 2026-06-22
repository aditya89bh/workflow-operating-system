import pytest

from workflow_os.decision import (
    SQLiteDecisionStore,
    UnknownBenchmarkError,
    list_benchmarks,
    load_all_benchmarks_into,
    load_benchmark,
    load_benchmark_into,
)


def test_list_benchmarks_covers_required_scenarios():
    names = set(list_benchmarks())
    assert names == {"onboarding", "procurement", "incidents", "customer_support"}


def test_load_benchmark_returns_records():
    records = load_benchmark("onboarding")
    assert len(records) == 5
    assert all(r.workflow_id == "onboarding" for r in records)
    # stable ids and deterministic ordering
    assert records[0].decision_id == "onboarding-01"


def test_load_unknown_benchmark_raises():
    with pytest.raises(UnknownBenchmarkError):
        load_benchmark("does-not-exist")


def test_load_benchmark_into_store():
    store = SQLiteDecisionStore()
    count = load_benchmark_into(store, "procurement")
    assert count == len(store.list())
    assert count > 0


def test_load_all_benchmarks_into_store():
    store = SQLiteDecisionStore()
    total = load_all_benchmarks_into(store)
    assert total == len(store.list())
    assert total == sum(len(load_benchmark(name)) for name in list_benchmarks())
