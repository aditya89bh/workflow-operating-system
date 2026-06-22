# Workflow Analytics

The analytics layer (`workflow_os.analytics`) measures, aggregates, analyzes,
reports, and exports facts about workflow executions. It reads from the earlier
layers - organizational memory events, approvals, and exceptions - and never
modifies them.

Everything here is deterministic and rule-based. There is no organizational
learning, no recommendations, no predictive analytics, no machine learning, and
no LLM-generated reporting. Every number is computed directly from recorded data.

## Pipeline

```
Measure → Aggregate → Analyze → Report → Visualize
```

The primary input is a list of `MemoryRecord` events produced by the memory
recorder (`workflow_os.memory`). Workflow and step durations come from the
`duration_seconds` metadata the recorder attaches to terminal events.

## Measure

- `workflow_completion_metrics(records)` → `CompletionMetrics` (total, completed,
  completion rate).
- `workflow_failure_metrics(records)` → `FailureMetrics` (total, failed, failure
  rate).
- `execution_duration_metrics(records)` → `DurationMetrics` (count, total, mean,
  min, max) for whole-workflow durations.
- `step_duration_metrics(records)` → per-step `DurationMetrics`.

## Analyze

- `detect_bottlenecks(records, limit=...)` → steps ranked by total time consumed.
- `slowest_steps(records, limit=...)` / `slow_steps(records, threshold=...)` →
  steps ranked by mean duration, or those above a threshold.
- `compare_workflows(records)` → a `WorkflowComparison` with per-workflow rows and
  the fastest/slowest finished workflows.

## Report

- `workflow_summaries(records)` → a `WorkflowSummary` per workflow.
- `workflow_statistics(records)` → aggregate `WorkflowStatistics`.
- `workflow_trends(records)` → completions per UTC day.
- `execution_summaries(records)` → per-run `ExecutionSummary` (start/end, status,
  duration, steps completed/failed).

## Scorecards and team statistics

- `workflow_scorecards(records)` → `Scorecard` per workflow (1.0 completed, 0.0
  failed, 0.5 running).
- `agent_scorecards(records)` → `Scorecard` per actor by step success ratio.
- `approval_scorecards(approvals)` → `Scorecard` per approver by approval ratio.
- `team_statistics(records)` → per-actor workload, throughput, and utilization.

## Health scores

`workflow_health_score(records, exceptions=...)` returns a `HealthScore` in
`[0, 1]` from a fixed weighted blend of:

- success rate (weight 0.4)
- inverse failure rate (weight 0.3)
- exception recovery rate (weight 0.2)
- bottleneck health, `1 / (1 + bottleneck_count)` (weight 0.1)

## Trend analysis

`trend_report(records, approvals=..., exceptions=...)` returns a `TrendReport`
with day-bucketed `workflow_trends`, `failure_trends`, `approval_trends`, and
`exception_trends`. The individual functions are available separately.

## Export

- `to_csv(rows, fieldnames=...)` / `write_csv(path, rows)` for CSV.
- `to_json(data)` / `write_json(path, data)` for JSON. Dataclasses are expanded
  recursively and datetimes are rendered as ISO strings.

## Demo

```bash
workflow-os analytics-demo
```

or:

```bash
PYTHONPATH=src python examples/analytics_demo.py
```
