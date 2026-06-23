# Workflow Operating System

A lightweight, **dependency-free** Python library to model, run, govern, and learn
from workflows. It grows from a small workflow engine into a complete,
**deterministic** operating system for organizational processes — with memory,
decisions, SOPs, approvals, exception handling, multi-agent collaboration,
analytics, and organizational learning.

No machine learning. No external services. Same input, same output, every time.

## Why

Most "workflow + AI" tools are opaque and non-deterministic. This project takes
the opposite stance: every insight, recommendation, and score is produced by a
fixed, inspectable rule from data you can see. It reads as:

```
Workflow → History → Patterns → Insights → Recommendations → Continuous Improvement
```

## Features

The system is built in layers, each an additive subpackage:

| Layer | Package | What it does |
| --- | --- | --- |
| Workflow engine | `workflow_os` | Typed models, status state machines, validation, dependency-ordered execution, JSON persistence, CLI |
| Organizational memory | `workflow_os.memory` | Records events; storage, retrieval, timelines, auditing, confidence |
| Decision intelligence | `workflow_os.decision` | Capture, store, retrieve, compare, replay decisions |
| SOP memory | `workflow_os.sop` | Versioned SOPs with search, linking, change logs |
| Approval system | `workflow_os.approval` | Requests, multi/sequential/parallel approvals, escalation, audit |
| Exception handling | `workflow_os.exception` | Detect, classify, recommend recovery, measure, report |
| Multi-agent collaboration | `workflow_os.agents` | Coordinator/planner/executor/compliance/memory agents |
| Workflow analytics | `workflow_os.analytics` | Metrics, bottlenecks, scorecards, health, trends, CSV/JSON export |
| Organizational learning | `workflow_os.learning` | Pattern mining, recommendations, maturity scoring, dashboards |

## Installation

```bash
git clone https://github.com/aditya89bh/workflow-operating-system.git
cd workflow-operating-system
python3 -m venv .venv && source .venv/bin/activate
pip install -e .
```

## Quickstart

Run the full showcase tour:

```bash
workflow-os demo-all
```

Run a single demo by name:

```bash
workflow-os demo employee-onboarding
```

Available demos: `employee-onboarding`, `procurement`, `incident-management`,
`customer-onboarding`, `workflow-memory`, `workflow-decision`,
`approval-workflow`, `exception-recovery`, `analytics`,
`organizational-learning`.

Create and drive your own workflow:

```bash
workflow-os create --id release --name "Release" --step "build:Build" --step "ship:Ship"
workflow-os start release
workflow-os show release
```

### Example output

```
workflow: Employee Onboarding (6 steps)
resolved execution order:
  1. Offer signed [recruiting] (depends on: -)
  2. Create IT account [it] (depends on: offer_signed)
  3. Provision email [it] (depends on: create_account)
  ...
workflow finished as 'completed'
recorded 14 memory events
```

More captured output lives in [`assets/screenshots/`](assets/screenshots/).

## Documentation

- [Getting started](docs/getting_started.md)
- [Tutorial: a guided walkthrough](docs/tutorial.md)
- [Architecture](docs/architecture.md)
- Per-layer guides: [memory](docs/organizational_memory.md),
  [decisions](docs/decision_intelligence.md), [SOPs](docs/sop_memory.md),
  [approvals](docs/approval_system.md), [exceptions](docs/exception_handling.md),
  [agents](docs/multi_agent_collaboration.md),
  [analytics](docs/workflow_analytics.md),
  [learning](docs/organizational_learning.md)
- [Release notes (v0.1.0)](docs/release_notes/v0.1.0.md)

## Use as a library

```python
from workflow_os.demos.employee_onboarding import build_workflow
from workflow_os.memory.recorder import MemoryRecorder
from workflow_os.memory.sqlite_store import SQLiteMemoryStore
from workflow_os.learning.maturity import organizational_maturity_score

workflow = build_workflow()
store = SQLiteMemoryStore(":memory:")
MemoryRecorder(store).run(workflow)
print("maturity:", organizational_maturity_score(store.list()).level)
```

## Project layout

```
src/workflow_os/   library source (one subpackage per layer)
tests/             test suite (~600 tests)
examples/          standalone demo runners
benchmarks/        micro-benchmarks
docs/              documentation and architecture diagrams
assets/            architecture diagrams and screenshots
```

## Development

```bash
pip install -e ".[dev]"
pytest
ruff check .
mypy src
python -m build
```

## Benchmarks

```bash
PYTHONPATH=src python -m benchmarks.runner
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Contributions should keep the system
deterministic, additive, and well-tested.

## License

[MIT](LICENSE) © Aditya
