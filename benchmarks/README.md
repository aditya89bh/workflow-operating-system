# Benchmarks

Small, deterministic micro-benchmarks for the hot paths of the workflow operating
system.

## Run

```bash
PYTHONPATH=src python -m benchmarks.runner
```

This runs every benchmark and prints a table:

```
workflow-operating-system benchmarks (200 iterations each)
----------------------------------------------------------------------
workflow_execution            200 iters  ...
memory_retrieval              200 iters  ...
analytics_generation          200 iters  ...
```

## What is measured

- **workflow_execution** – resolving execution order and running a workflow end
  to end through the memory recorder.
- **memory_retrieval** – querying workflow and actor history from a populated
  store.
- **analytics_generation** – computing the core completion, failure, duration,
  and statistics metrics over recorded events.

## Use from code

```python
from benchmarks import run_all_benchmarks

for result in run_all_benchmarks(iterations=50):
    print(result.name, result.ops_per_second)
```
