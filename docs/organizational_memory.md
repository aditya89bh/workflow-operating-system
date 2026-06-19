# Organizational Memory

The organizational memory system turns workflow executions into a queryable,
auditable history. Every lifecycle change a workflow goes through can be
recorded as a structured **memory record**, stored durably, and later
retrieved, analyzed, and pruned.

It lives in the `workflow_os.memory` subpackage and is fully additive: Phase 1
workflow modelling and execution behave exactly as before.

## Concepts

### MemoryRecord

A `MemoryRecord` is a single fact about something that happened:

| Field | Meaning |
|-------|---------|
| `event_id` | Unique id for the event |
| `workflow_id` | Workflow the event belongs to |
| `step_id` | Related step id (optional) |
| `actor` | Who the event is attributed to (optional) |
| `event_type` | One of the `MemoryEventType` values |
| `timestamp` | Timezone-aware UTC time of the event |
| `confidence` | Trust score in `[0.0, 1.0]` |
| `metadata` | Free-form key/value data (e.g. `duration_seconds`) |

### Event types

`MemoryEventType` defines the recorded events:

- workflow: `workflow_started`, `workflow_paused`, `workflow_resumed`,
  `workflow_completed`, `workflow_failed`
- step: `step_started`, `step_completed`, `step_failed`, `step_skipped`

### Stores

`MemoryStore` is a protocol with `add`, `get`, `list`, `delete`, and `query`.
`SQLiteMemoryStore` is the standard implementation, backed by the standard
library `sqlite3` module (file-based or in-memory).

## Recording memory

`MemoryRecorder` wraps a store and the Phase 1 lifecycle operations so each
state change automatically produces a record (with actor attribution,
confidence, and duration metadata):

```python
from workflow_os import Workflow, WorkflowStep
from workflow_os.memory import MemoryRecorder, SQLiteMemoryStore

workflow = Workflow(
    id="onboarding",
    name="Onboarding",
    metadata={"owner": "people-ops"},
    steps=[WorkflowStep(id="s1", name="Create account", assignee="it")],
)

store = SQLiteMemoryStore()
MemoryRecorder(store).run(workflow)
```

## Retrieval

```python
from workflow_os.memory import (
    get_workflow_history,
    get_actor_history,
    get_events_since,
    get_events_between,
    get_execution_timeline,
    get_step_timeline,
)

history = get_workflow_history(store, "onboarding")
by_actor = get_actor_history(store, "it")
timeline = get_execution_timeline(store, "onboarding")
```

Time-window helpers `get_events_since(store, since)` and
`get_events_between(store, start, end)` filter by timestamp.

## Confidence scoring

`confidence_for(event_type)` returns a default score: observed lifecycle events
are high confidence, failures are medium confidence, and manually recorded
events accept a configurable score via `manual=True, manual_confidence=...`.

## Pruning

Keep a store bounded with:

- `prune_by_max_age(store, max_age)`
- `prune_to_max_count(store, max_count)`
- `prune_workflow(store, workflow_id)`

Each returns the number of records removed.

## Auditing

`generate_audit_report(store)` returns an `AuditReport` with total events,
per-type / per-workflow / per-actor counts, and the oldest and newest event
timestamps. Call `report.as_dict()` for a JSON-serialisable view.
