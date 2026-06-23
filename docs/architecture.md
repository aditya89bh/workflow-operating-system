# Architecture

The workflow operating system is a layered, deterministic library. Each layer is
an additive subpackage that consumes the outputs of the layers beneath it; there
is no machine learning, prediction, or external service anywhere in the stack.

Diagram sources live in [`assets/architecture/`](../assets/architecture/) as
Mermaid (`.mmd`) files and are embedded below.

## System architecture

The core workflow engine feeds a knowledge layer (memory, decisions, SOPs), a
governance layer (approvals, exceptions), and an intelligence layer (analytics,
organizational learning). Multi-agent collaboration coordinates execution on top
of the engine.

```mermaid
graph TD
    subgraph Core
        WF[Workflow Engine]
    end
    subgraph Knowledge
        MEM[Organizational Memory]
        DEC[Decision Intelligence]
        SOP[SOP Memory]
    end
    subgraph Governance
        APP[Approval System]
        EXC[Exception Handling]
    end
    subgraph Intelligence
        AGT[Multi-Agent Collaboration]
        ANA[Workflow Analytics]
        LRN[Organizational Learning]
    end

    WF --> MEM
    WF --> DEC
    WF --> SOP
    WF --> APP
    WF --> EXC
    MEM --> ANA
    APP --> ANA
    EXC --> ANA
    MEM --> LRN
    DEC --> LRN
    SOP --> LRN
    APP --> LRN
    EXC --> LRN
    ANA --> LRN
    AGT --> WF
```

## Module relationships

How the Python subpackages depend on each other. Dependencies only point
"downward" toward more fundamental modules, keeping the layering clean.

```mermaid
graph LR
    workflow[workflow_os.workflow] --> executor[workflow_os.executor]
    executor --> memory[workflow_os.memory]
    memory --> decision[workflow_os.decision]
    memory --> sop[workflow_os.sop]
    memory --> approval[workflow_os.approval]
    memory --> exception[workflow_os.exception]
    memory --> analytics[workflow_os.analytics]
    approval --> analytics
    exception --> analytics
    analytics --> learning[workflow_os.learning]
    decision --> learning
    sop --> learning
    approval --> learning
    exception --> learning
    agents[workflow_os.agents] --> executor
    agents --> memory
    demos[workflow_os.demos] --> workflow
    demos --> memory
    demos --> learning
    cli[workflow_os.cli] --> demos
```

## Data flow

A workflow definition becomes an execution order, which produces lifecycle events
recorded in the memory store. Those events fan out to decisions, SOPs, approvals,
exceptions, and analytics, and finally converge in the learning layer as
patterns, insights, recommendations, and a maturity score.

```mermaid
flowchart LR
    A[Workflow definition] --> B[Execution order]
    B --> C[Lifecycle events]
    C --> D[(Memory store)]
    D --> E[Decisions / SOPs]
    D --> F[Approvals / Exceptions]
    D --> G[Analytics: metrics, reports, exports]
    E --> H[Patterns]
    F --> H
    G --> H
    H --> I[Insights]
    I --> J[Recommendations]
    J --> K[Maturity & Continuous Improvement]
```

## Design principles

- **Deterministic and rule-based.** Same input, same output, every time.
- **Additive layering.** New phases add subpackages without modifying existing
  ones, preserving backward compatibility.
- **Plain data + small functions.** Schemas are dataclasses; behavior lives in
  focused, well-tested functions.
- **Storage behind protocols.** Stores share a common interface with in-memory
  and SQLite implementations.
