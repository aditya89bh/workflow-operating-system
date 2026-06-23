# Getting Started

This guide gets you from a clone to a running demo in a few minutes.

## Requirements

- Python 3.10+
- `pip` and (recommended) a virtual environment

## Install

```bash
git clone https://github.com/aditya89bh/workflow-operating-system.git
cd workflow-operating-system
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

Verify the install:

```bash
workflow-os --help
```

## Your first workflow

Create a workflow, inspect it, and run it end to end:

```bash
workflow-os create --id hello --name "Hello Workflow" \
    --step collect:"Collect input" --step process:"Process" --step finish:"Finish"
workflow-os show hello
workflow-os start hello
```

## Run the showcase demos

The project ships runnable demonstrations. Run a single one by name:

```bash
workflow-os demo employee-onboarding
```

Available demo names:

- `employee-onboarding`
- `procurement`
- `incident-management`
- `customer-onboarding`
- `workflow-memory`
- `workflow-decision`
- `approval-workflow`
- `exception-recovery`
- `analytics`
- `organizational-learning`

Run all of them in sequence:

```bash
workflow-os demo-all
```

## Use it as a library

```python
from workflow_os.demos.employee_onboarding import build_workflow
from workflow_os.executor import WorkflowExecutor
from workflow_os.memory.recorder import MemoryRecorder
from workflow_os.memory.sqlite_store import SQLiteMemoryStore

workflow = build_workflow()
for step in WorkflowExecutor(workflow).execution_order():
    print(step.id, "->", step.name)

store = SQLiteMemoryStore(":memory:")
MemoryRecorder(store).run(workflow)
print("recorded", len(store.list()), "events")
```

## Where to next

- Follow the [tutorial](tutorial.md) for a guided, layer-by-layer walkthrough.
- Read the [architecture overview](architecture.md).
- Explore the per-layer docs in this `docs/` directory.
