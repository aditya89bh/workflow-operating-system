# Approval System

The approval system adds a deterministic, rule-based governance layer on top of
the workflow, memory, decision, and SOP layers. It answers questions such as:

- Who needs to approve this workflow?
- Who approved or rejected it?
- What approvals are still pending?
- How long do approvals take?
- Where are the approval bottlenecks?
- Can approvals be audited later?

The lifecycle is **Request → Review → Approve → Escalate → Audit → Analyze**.
Everything is deterministic; there are no agents, no LLM calls, and no learning.

## Concepts

### ApprovalRequest

An `ApprovalRequest` (`workflow_os.approval.record`) captures a single governance
ask: a `requester` wants a `workflow_id` (optionally a `step_id`) approved by a
list of `approvers`. It carries a `title`, `description`, timestamps, the overall
`state`, the per-approver `decisions`, and arbitrary `metadata`.

```python
from workflow_os.approval import ApprovalRequest

request = ApprovalRequest.create(
    workflow_id="wf-budget-001",
    requester="alice",
    title="Approve Q3 budget",
    approvers=["manager", "finance"],
)
```

### ApprovalState

`ApprovalState` defines the lifecycle states: `pending`, `approved`, `rejected`,
`cancelled`, and `expired`. `is_active` and `is_terminal` classify a state, and
`set_state` / `record_response` update a request.

### ApprovalPolicy

An `ApprovalPolicy` describes how an approval is conducted: its `policy_type`
(one of `PolicyType`: single, multi, sequential, parallel), the number of
`required_approvals`, and an optional `escalation_timeout` (seconds).

## Storage

`ApprovalStore` is a structural protocol supporting `add`, `get`, `update`,
`delete`, `list`, and `query` (via `ApprovalQuery`). Two implementations ship:

- `InMemoryApprovalStore` — a dictionary-backed store for tests and demos.
- `SQLiteApprovalStore` — persistence using the standard-library `sqlite3`.

## Workflows

Four workflows drive a request through its approvers:

- **Single** (`SingleApproverWorkflow`) — one approver approves or rejects.
- **Multi** (`MultiApproverWorkflow`) — several approvers, approved once a
  threshold of approvals is reached, rejected once the threshold is unreachable.
- **Sequential** (`SequentialApprovalWorkflow`) — approvers act in a fixed order
  (for example Requester → Manager → Finance → Operations).
- **Parallel** (`ParallelApprovalWorkflow`) — approvers act simultaneously; by
  default all must approve, and any rejection rejects the request.

## Timeouts, escalation, reminders, delegation

- **Timeouts** (`workflow_os.approval.timeout`) — `is_overdue`, `find_overdue`,
  and `expire_overdue` detect and expire requests past their deadline.
- **Escalation** (`escalate`, `EscalationRule`, `escalate_if_overdue`) — route a
  stalled request to an escalation target and record the escalation history.
- **Reminders** (`generate_reminders`) — produce pending and overdue reminders
  for approvers who still need to act.
- **Delegation** (`delegate`, `active_delegations`) — an approver delegates to
  another person, permanently or temporarily (with an expiry).

## Auditing and analysis

- **Audit log** (`ApprovalAuditLog`) — an append-only trail of requests,
  approvals, rejections, escalations, and delegations.
- **History** (`workflow_approvals`, `actor_approvals`, `pending_approvals`,
  `completed_approvals`) — convenience retrieval over a store.
- **Workload metrics** (`compute_workload_metrics`) — approvals by actor,
  average response time, pending counts, and overdue counts.
- **Bottleneck analysis** (`analyze_bottlenecks`) — slowest approvers, workflow
  bottlenecks, and escalation hotspots.

## Demo

Run the end-to-end demonstration:

```bash
python examples/approval_demo.py
# or
workflow-os approval-demo
```

It creates a request, runs a sequential workflow, escalates, delegates,
generates an audit report, and prints a bottleneck analysis.
