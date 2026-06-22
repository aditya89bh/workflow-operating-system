# Multi-Agent Collaboration

The multi-agent collaboration layer (`workflow_os.agents`) coordinates work across
a small set of deterministic service agents. It builds on the workflow, memory,
decision, SOP, approval, and exception layers without changing them.

The agents are plain service objects, not LLM wrappers. There is no autonomous
planning, no self-improvement, and no external framework integration. Every output
is derived by rule from the workflow, the delegation ledger, the message bus, and
the collaboration log.

## Architecture

```
Workflow
  ↓
Coordinator Agent   (assigns work, manages workflow state)
  ↓
Planner Agent       (derives execution order and dependencies)
  ↓
Execution Agent     (runs steps, emits execution events)
  ↓
Compliance Agent    (verifies policies, approvals, SOP compliance)
  ↓
Memory Agent        (reads/writes organizational memory)
  ↓
Reports             (accountability, efficiency, performance)
```

## Agents and roles

An `Agent` is a data record: `agent_id`, `name`, `role`, `description`,
`capabilities`, and `metadata`. `AgentRole` enumerates the fixed roles:
`coordinator`, `planner`, `executor`, `compliance`, and `memory`.

The `AgentRegistry` registers, unregisters, looks up, and lists agents, and can
filter by role.

```python
from workflow_os.agents import Agent, AgentRegistry, AgentRole

registry = AgentRegistry()
registry.register(Agent.create(name="Coord", role=AgentRole.COORDINATOR.value))
```

### Service agents

- `CoordinatorAgent` — `assign_tasks`, `coordinate_execution`, and lifecycle
  control (`start`, `pause`, `resume`, `complete`).
- `PlannerAgent` — `create_plan`, `determine_ordering`, `identify_dependencies`.
- `ExecutionAgent` — `execute_task`, `report_status`, and emitted `events`.
- `ComplianceAgent` — `verify_policies`, `verify_approvals`,
  `validate_sop_compliance`, each returning a `ComplianceResult`.
- `MemoryAgent` — `write`, `retrieve`, `workflow_history`, `actor_history` over a
  `MemoryStore`.

## Shared workspace and memory

`SharedWorkspace` holds shared state, the workflow context, per-agent context, and
workspace metadata. `SharedMemory` is the auditable access layer over a memory
store: every `read`, `write`, and `query` is captured in an `access_log`.

## Delegation

`TaskDelegation` is the ledger of task ownership. Tasks can be assigned,
transferred, and revoked, and the full `history` is retained. `TaskAssignment`
holds the current owner and active flag.

```python
from workflow_os.agents import TaskDelegation

ledger = TaskDelegation()
task = ledger.assign(workflow_id="wf", owner="exec")
ledger.transfer(task.task_id, "backup")
```

## Messaging

`MessageBus` lets agents `send` and `receive` messages and query the full
`history` by sender and recipient. Messages carry a subject and metadata.

## Collaboration logs

`CollaborationLog` is the append-only record of assignments, messages, task
transfers, and workflow participation. It powers accountability and reporting and
exposes the `participants` of a workflow.

## Accountability

- `actions_performed(log, agent_id)` — every action attributed to an agent.
- `ownership_history(delegation, task_id)` — how a task's ownership changed.
- `responsibility_chain(delegation, task_id)` — the ordered chain of owners.
- `build_accountability(log, agent_id)` — a per-agent summary with action counts.

## Collaboration efficiency metrics

`compute_collaboration_metrics(workflow, delegation, bus)` returns
`CollaborationMetrics`: task completion rate, handoff count, message count, and
delegation statistics. The individual functions (`task_completion_rate`,
`handoff_count`, `message_count`, `delegation_statistics`) are available too.

## Performance reports

`build_performance_report(agent_ids, delegation, bus)` returns a
`PerformanceReport` with per-agent workload, active tasks, transfers, message
counts, utilization, and the bottleneck agents carrying the most active work.

## Demo

Run the end-to-end demonstration:

```bash
workflow-os multi-agent-demo
```

or:

```bash
PYTHONPATH=src python examples/multi_agent_demo.py
```
