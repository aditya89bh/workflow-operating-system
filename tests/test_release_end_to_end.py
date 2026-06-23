"""End-to-end release validation across every layer.

Threads a single body of workflow history through memory, analytics, and
organizational learning, asserting the full pipeline holds together.
"""

from workflow_os.analytics.completion import workflow_completion_metrics
from workflow_os.analytics.reports import workflow_statistics
from workflow_os.demos.employee_onboarding import build_workflow
from workflow_os.learning.maturity import organizational_maturity_score
from workflow_os.learning.reports import learning_report
from workflow_os.memory.recorder import MemoryRecorder
from workflow_os.memory.retrieval import get_workflow_history
from workflow_os.memory.sqlite_store import SQLiteMemoryStore
from workflow_os.status import WorkflowStatus


def _record_history():
    store = SQLiteMemoryStore(":memory:")
    recorder = MemoryRecorder(store)
    for index in range(3):
        workflow = build_workflow()
        workflow.id = f"employee-onboarding-{index}"
        recorder.run(workflow)
    return store


def test_workflow_to_memory_to_analytics_to_learning():
    store = _record_history()
    records = store.list()

    # Memory retrieval works.
    assert get_workflow_history(store, "employee-onboarding-0")

    # Analytics aggregates the recorded history.
    completion = workflow_completion_metrics(records)
    assert completion.completion_rate == 1.0
    stats = workflow_statistics(records)
    assert stats.total_workflows == 3
    assert stats.completed_workflows == 3

    # Learning derives a report and maturity from the same history.
    report = learning_report(records)
    assert isinstance(report.recommendations, list)
    maturity = organizational_maturity_score(records)
    assert 0.0 <= maturity.overall <= 1.0


def test_single_run_completes():
    workflow = build_workflow()
    MemoryRecorder(SQLiteMemoryStore(":memory:")).run(workflow)
    assert workflow.status == WorkflowStatus.COMPLETED
