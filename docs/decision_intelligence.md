# Decision Intelligence

The decision intelligence layer captures the decisions taken during workflow
executions and makes them queryable, explainable, and replayable. It answers:

- **What** decision was made?
- **Why** was it made?
- **What alternatives** were considered?
- **Who** made the decision?
- **What was the outcome?**
- Can the decision be **replayed and analyzed** later?

It lives in the `workflow_os.decision` subpackage and is fully additive: it
builds on top of organizational memory (reusing actor attribution) without
modifying Phase 1 or Phase 2 behavior. The flow is strictly
**Capture -> Store -> Retrieve -> Replay -> Analyze**.

## Concepts

### DecisionRecord

A `DecisionRecord` is a single decision:

| Field | Meaning |
|-------|---------|
| `decision_id` | Unique id for the decision |
| `workflow_id` | Workflow the decision belongs to |
| `step_id` | Related step id (optional) |
| `actor` | Who made or owns the decision (optional) |
| `decision_type` | One of the `DecisionType` values |
| `decision` | A short statement of what was decided |
| `rationale` | Why the decision was made |
| `alternatives` | Other options that were considered |
| `timestamp` | Timezone-aware UTC time of the decision |
| `outcome` | One of the `DecisionOutcome` values |
| `confidence` | Trust score in `[0.0, 1.0]` |
| `metadata` | Free-form key/value data |

### Decision types

`DecisionType` defines the kinds of decisions recorded:
`workflow_decision`, `step_decision`, `exception_decision`, `manual_decision`,
and `system_decision`.

### Outcomes

`DecisionOutcome` is one of `pending`, `successful`, `failed`, or `unknown`.
Outcomes are validated on write and can be updated after a decision is recorded
via `set_decision_outcome` or `DecisionRecorder.update_decision_outcome`.

### Stores

`DecisionStore` is a protocol with `add`, `get`, `list`, `delete`, and `query`.
`SQLiteDecisionStore` is the standard implementation, backed by the standard
library `sqlite3` module (file-based or in-memory). It also supports `update`
for in-place record updates.

`DecisionQuery` filters by workflow, step, actor, decision types, outcome, and
time window, with ordering and an optional limit.

## Capturing decisions

`DecisionRecorder` wraps a store and offers convenient capture methods:

```python
from workflow_os.decision import DecisionRecorder, SQLiteDecisionStore

store = SQLiteDecisionStore("decisions.db")
recorder = DecisionRecorder(store)

recorder.record_workflow_decision(workflow, "Run standard onboarding",
                                   rationale="Typical role")
recorder.record_step_decision(workflow, step, "Provision SSO account",
                              rationale="Required for access")
recorder.record_exception_decision(workflow, "Retry email provisioning",
                                    step=step, reason="provider timeout")
```

Workflow and step decisions attribute the actor automatically (workflow owner
and step assignee respectively), reusing the organizational memory actor
helpers.

## Retrieval and search

- `search_by_decision_text`, `search_by_rationale`, `search_by_outcome`, and the
  combined `search_decisions` find decisions by content.
- `get_workflow_decision_timeline`, `get_actor_decision_timeline`, and
  `get_decision_timeline` return ordered timelines with per-entry offsets.

## Explanations

`explain_decision` returns a structured `DecisionExplanation` (what happened,
why, outcome); `explain_decision_text` renders it as text.

## Replay

`DecisionReplay` (and the `replay_workflow_decisions` /
`replay_actor_decisions` helpers) reconstruct decisions in order, pairing each
with an explanation and a time offset. Replay is read-only analysis; it does not
re-execute anything.

## Analysis

- `compute_decision_statistics` produces totals, per-type counts, success and
  failure rates over resolved decisions, and per-actor statistics.
- `compare_successful_vs_failed`, `compare_workflows`, and `compare_actors`
  produce side-by-side `ComparisonReport`s.

## Benchmark datasets

`load_benchmark` / `load_benchmark_into` provide ready-made datasets for
`onboarding`, `procurement`, `incidents`, and `customer_support`, useful for
demos and exploring the analysis tooling.

## Demo

Run the end-to-end demonstration:

```bash
workflow-os decision-demo
# or
python -m workflow_os decision-demo
# or
python examples/decision_demo.py
```
