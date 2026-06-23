# Tutorial: A Guided Walkthrough

This tutorial walks through the layers of the workflow operating system in the
order they build on each other. Each section is runnable; paste the snippets into
a Python shell (with the package installed) or follow along with the matching
`workflow-os` demo command.

The layers form a pipeline:

```
Workflow → Memory → Decisions → SOPs → Approvals → Exceptions → Agents → Analytics → Learning
```

## 1. Model and run a workflow

A `Workflow` is a named set of `WorkflowStep`s with dependencies. The
`WorkflowExecutor` resolves a valid execution order (topological sort).

```python
from workflow_os.demos.employee_onboarding import build_workflow
from workflow_os.executor import WorkflowExecutor

workflow = build_workflow()
order = WorkflowExecutor(workflow).execution_order()
print([step.id for step in order])
```

## 2. Record organizational memory

`MemoryRecorder` runs a workflow while persisting every lifecycle event.

```python
from workflow_os.memory.recorder import MemoryRecorder
from workflow_os.memory.sqlite_store import SQLiteMemoryStore
from workflow_os.memory.retrieval import get_workflow_history

store = SQLiteMemoryStore(":memory:")
MemoryRecorder(store).run(workflow)
print(len(get_workflow_history(store, workflow.id)), "events")
```

CLI: `workflow-os demo workflow-memory`

## 3. Capture decisions and replay them

```python
from workflow_os.decision.recorder import DecisionRecorder
from workflow_os.decision.sqlite_store import SQLiteDecisionStore
from workflow_os.decision.replay import replay_workflow_decisions

decisions = SQLiteDecisionStore(":memory:")
DecisionRecorder(decisions).record_workflow_decision(
    workflow, "Run standard track", rationale="typical role", outcome="successful"
)
for event in replay_workflow_decisions(decisions, workflow.id):
    print(event.explanation.what_happened)
```

CLI: `workflow-os demo workflow-decision`

## 4. Govern with approvals

```python
from workflow_os.approval.audit import ApprovalAuditLog
from workflow_os.approval.multi import MultiApproverWorkflow
from workflow_os.approval.record import ApprovalRequest

request = ApprovalRequest.create(
    workflow_id=workflow.id, requester="alice", title="Approve", approvers=["m", "f"]
)
flow = MultiApproverWorkflow(request, required_approvals=2)
flow.approve("m")
flow.approve("f")
print(request.state)
```

CLI: `workflow-os demo approval-workflow`

## 5. Handle exceptions and recover

```python
from workflow_os.exception.record import ExceptionRecord
from workflow_os.exception.recommendation import recommend_recovery

exception = ExceptionRecord.create(
    workflow_id=workflow.id, exception_type="timeout", severity="high"
)
print(recommend_recovery(exception, actor="ops").action)
```

CLI: `workflow-os demo exception-recovery`

## 6. Measure with analytics

```python
from workflow_os.analytics.completion import workflow_completion_metrics

metrics = workflow_completion_metrics(store.list())
print(f"completion rate: {metrics.completion_rate:.0%}")
```

CLI: `workflow-os demo analytics`

## 7. Learn and improve

```python
from workflow_os.learning.reports import learning_report
from workflow_os.learning.maturity import organizational_maturity_score

report = learning_report(store.list())
print(len(report.recommendations), "recommendations")
print("maturity:", organizational_maturity_score(store.list()).level)
```

CLI: `workflow-os demo organizational-learning`

## Putting it together

Run the whole showcase to see every layer in sequence:

```bash
workflow-os demo-all
```
