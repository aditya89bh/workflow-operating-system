# Workflow Operating System

A lightweight, dependency-free Python library to **model, validate, and execute workflows**.

Define workflows as typed entities made of ordered steps with dependencies, then drive
them through a well-defined set of state transitions (draft, ready, running, paused,
completed, failed, cancelled).

## Features

- Typed `Workflow` and `WorkflowStep` models
- Explicit workflow and step status state machines
- Validation of step ids, dependencies, and initial states
- A workflow executor that runs steps in dependency order
- JSON persistence with import/export support
- A command-line interface for creating and running workflows

## Installation

```bash
pip install -e .
```

## Project layout

```
src/workflow_os/   library source
tests/             test suite
examples/          example workflows
```

## Development

```bash
pip install -e ".[dev]"
pytest
ruff check .
python -m build
```

## License

MIT
