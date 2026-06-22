# Organizational Learning

The organizational learning layer (`workflow_os.learning`) turns the history
captured by the earlier layers into actionable organizational knowledge. It is
deterministic and rule-based: there is no machine learning, prediction,
autonomous optimization, or external service. Every output is derived by fixed
rules from data that already exists.

The flow is:

```
Workflow → History → Patterns → Insights → Recommendations → Continuous Improvement
```

It consumes the outputs of the other layers:

- **memory** – `MemoryRecord` events (workflow and step lifecycle)
- **decisions** – decision records
- **SOPs** – `SOPRecord` documents and their status
- **approvals** – `ApprovalRequest` records and escalation history
- **exceptions** – `ExceptionRecord` and `RecoveryAction` records
- **analytics** – bottlenecks, trends, and health primitives

## Schemas

### `Recommendation`

A deterministic improvement suggestion.

| Field | Meaning |
| --- | --- |
| `recommendation_id` | Unique id |
| `category` | `workflow`, `sop`, `automation`, or `approval` |
| `title` | Short title |
| `description` | Longer description |
| `severity` | `low` / `medium` / `high` |
| `confidence` | Strength of supporting evidence, `[0.0, 1.0]` |
| `created_at` | Timestamp (UTC) |
| `metadata` | Free-form key/value data |

### `OrganizationalInsight`

A deterministic, evidence-backed observation.

| Field | Meaning |
| --- | --- |
| `insight_id` | Unique id |
| `category` | `success`, `failure`, `exception`, ... |
| `title` | Short title |
| `description` | Longer description |
| `evidence` | Supporting facts |
| `confidence` | Strength of evidence, `[0.0, 1.0]` |
| `created_at` | Timestamp (UTC) |
| `metadata` | Free-form key/value data |

## Patterns

- `workflow_run_stats` – per-workflow run / success / failure counts
- `recurring_workflows` – workflows that run repeatedly
- `recurring_bottlenecks` – steps that are repeatedly bottlenecks
- `recurring_exceptions` – exception signatures that repeat

## Success and failure detection

- `highest_success_rate_workflows`, `most_reliable_workflows`,
  `consistently_healthy_workflows`, `successful_workflow_insights`
- `frequently_failing_workflows`, `failure_hotspots`, `unstable_workflows`,
  `failure_pattern_insights`
- `repeated_exceptions`, `chronic_workflow_problems`,
  `recurring_recovery_actions`, `recurring_exception_insights`

## Recommendations

- `workflow_improvement_recommendations` – simplify, split, remove bottleneck
- `sop_update_recommendations` – update outdated, revise exception handling, add
  missing guidance
- `automation_opportunity_recommendations` – repetitive tasks, repeated
  approvals, repeated recoveries
- `approval_improvement_recommendations` – reduce approvers, adjust escalation,
  eliminate bottlenecks

## Maturity and reports

- `organizational_maturity_score` – composite score (workflow health,
  documentation coverage, exception rate, approval efficiency, recovery
  effectiveness) and a named maturity level
- `continuous_improvement_report` – opportunities, trends, and maturity together
- `learning_report` – insights, recommendations, and a numeric summary
- `organizational_dashboard` – JSON-serializable summary for dashboards

## Examples and demo

`workflow_os.learning.examples` provides built-in datasets
(`successful_organization`, `struggling_organization`, `improvement_journey`).
Run the end-to-end demonstration with:

```bash
workflow-os learning-demo
```
