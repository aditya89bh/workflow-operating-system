# Contributing

Thanks for your interest in improving the workflow operating system. This project
is deterministic and dependency-free by design; please keep contributions in that
spirit.

## Development setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Checks

Run the full validation suite before opening a pull request:

```bash
pytest
ruff check .
mypy src
python -m build
```

All four must pass. New code should come with tests.

## Guidelines

- **Deterministic and rule-based.** No machine learning, prediction, autonomous
  optimization, or external services.
- **Additive layering.** Prefer adding focused modules over modifying existing
  layers; preserve backward compatibility.
- **Plain data + small functions.** Use dataclasses for schemas and keep behavior
  in small, well-tested functions.
- **Style.** Code is formatted and linted with `ruff` (line length 100) and type
  checked with `mypy`. Imports are sorted.
- **Commits.** Use [Conventional Commits](https://www.conventionalcommits.org/)
  (`feat:`, `fix:`, `docs:`, `test:`, `chore:`, ...).

## Project layout

```
src/workflow_os/   library source (one subpackage per layer)
tests/             test suite
examples/          standalone demo runners
benchmarks/        micro-benchmarks
docs/              documentation
assets/            architecture diagrams and screenshots
```
