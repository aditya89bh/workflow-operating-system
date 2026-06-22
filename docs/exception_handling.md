# Exception Handling

The exception handling layer adds deterministic, rule-based exception
intelligence on top of the workflow, memory, decision, SOP, and approval layers.
It can:

- detect workflow failures,
- classify and score exceptions,
- recommend recovery actions,
- measure recovery effectiveness,
- identify recurring failures, and
- generate exception reports.

There is no autonomous recovery, no organizational learning, and no LLM
involvement. The same inputs always produce the same outputs.

## Concepts

### ExceptionRecord

An `ExceptionRecord` (`workflow_os.exception.record`) captures a detected
failure: the `workflow_id` (and optional `step_id`), its `exception_type`,
`severity`, a `message`, the detecting `source`, `detected_at`, a `resolved`
flag, and arbitrary `metadata`.

```python
from workflow_os.exception import ExceptionRecord

record = ExceptionRecord.create(
    workflow_id="wf-1",
    exception_type="timeout",
    severity="high",
    message="deadline missed",
)
```

### Classification and severity

`ExceptionType` defines the categories: `workflow_failure`, `step_failure`,
`timeout`, `missing_resource`, `approval_failure`, `validation_failure`, and
`unknown`. `ExceptionSeverity` defines `low`, `medium`, `high`, and `critical`,
and `severity_rank` provides a deterministic ordering.

## Storage

`ExceptionStore` is a structural protocol supporting `add`, `get`, `update`,
`delete`, `list`, and `query` (via `ExceptionQuery`). Two implementations ship:
`InMemoryExceptionStore` and `SQLiteExceptionStore` (standard-library `sqlite3`).

## Detection

Detectors turn observed conditions into exception records:

- **Deadline failures** (`detect_deadline_failures`) — workflows/steps that
  passed their deadline (`timeout`).
- **Missing approvals** (`detect_missing_approvals`) — approval requests that
  were rejected, expired, or (optionally) still pending (`approval_failure`).
- **Missing resources** (`detect_missing_resources`) — required resources that
  are unavailable (`missing_resource`).
- **Workflow stalls** (`detect_stalled_workflows`) — workflows idle beyond a
  threshold (`workflow_failure`).

## Recovery

- **RecoveryAction** (`workflow_os.exception.recovery`) — a recorded recovery
  attempt with `recovery_id`, `exception_id`, `action`, `actor`, `status`,
  `timestamp`, and `metadata`.
- **Recommendation engine** (`recommend_recovery`) — a fixed mapping from
  exception type to a recommended action (deterministic).
- **Retry strategy** (`RetryStrategy`) — caps attempts and produces the next
  retry action.
- **Fallback strategy** (`FallbackStrategy`) — a deterministic alternative
  action per exception type, with optional overrides.

## Analysis

- **Clustering** (`cluster_by_type`, `cluster_by_workflow`,
  `cluster_by_severity`, `cluster_by_recovery_outcome`) — group related
  exceptions.
- **Trend reports** (`failures_over_time`, `recurring_failures`,
  `workflow_risk_reports`) — failures over time, recurring failures, and
  per-workflow risk.
- **Effectiveness metrics** (`compute_effectiveness`) — recovery success rate,
  retry success rate, and mean recovery time.

## Demo

Run the end-to-end demonstration:

```bash
python examples/exception_demo.py
# or
workflow-os exception-demo
```

It triggers a workflow failure, records the exception, generates a recovery
recommendation, retries the workflow, and prints an exception report.
