# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [0.1.0] - 2026-06-23

The first release. A complete, deterministic, dependency-free workflow operating
system built up across ten phases.

### Added

- **Workflow engine** – typed `Workflow`/`WorkflowStep` models, status state
  machines, validation, dependency-ordered execution, JSON persistence, and a
  CLI.
- **Organizational memory** – structured event recording with SQLite-backed
  storage, retrieval, history/timelines, auditing, and confidence scoring.
- **Decision intelligence** – capture, store, retrieve, compare, and replay
  workflow decisions with deterministic explanations.
- **SOP memory** – versioned standard operating procedures with search,
  retrieval, linking, and change logs.
- **Approval system** – requests, single/multi/sequential/parallel approval
  workflows, escalation, delegation, reminders, audit trail, and metrics.
- **Exception handling** – detection, classification, severity, deterministic
  recovery recommendations, retries, effectiveness, and risk reporting.
- **Multi-agent collaboration** – agent registry, coordinator/planner/executor/
  compliance/memory agents, shared workspace, messaging, delegation, and
  accountability.
- **Workflow analytics** – completion/failure/duration metrics, bottlenecks,
  comparisons, scorecards, health, trends, and CSV/JSON export.
- **Organizational learning** – pattern mining, success/failure detection,
  recommendations, maturity scoring, continuous improvement, and dashboards.
- **Productization** – ten showcase demos (domain and integration), a
  `demo`/`demo-all` CLI, getting-started and tutorial docs, architecture
  diagrams, a benchmark suite, and release validation tests.

[0.1.0]: https://github.com/aditya89bh/workflow-operating-system/releases/tag/v0.1.0
