"""Workflow analytics for the workflow operating system.

A deterministic, rule-based analytics layer that measures, aggregates, analyzes,
reports, and exports facts about workflow executions. It reads from the earlier
layers (memory events, approvals, exceptions) without modifying them. There is no
learning, prediction, or recommendation here - every number is computed directly
from recorded data.
"""

from workflow_os.analytics.completion import (
    CompletionMetrics,
    completed_workflow_ids,
    observed_workflow_ids,
    started_workflow_ids,
    workflow_completion_metrics,
)
from workflow_os.analytics.duration import (
    DurationMetrics,
    execution_duration_metrics,
    summarize_durations,
    workflow_durations,
)
from workflow_os.analytics.failure import (
    FailureMetrics,
    failed_workflow_ids,
    workflow_failure_metrics,
)

__all__ = [
    "CompletionMetrics",
    "DurationMetrics",
    "FailureMetrics",
    "completed_workflow_ids",
    "execution_duration_metrics",
    "failed_workflow_ids",
    "observed_workflow_ids",
    "started_workflow_ids",
    "summarize_durations",
    "workflow_completion_metrics",
    "workflow_durations",
    "workflow_failure_metrics",
]
