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
from workflow_os.analytics.failure import (
    FailureMetrics,
    failed_workflow_ids,
    workflow_failure_metrics,
)

__all__ = [
    "CompletionMetrics",
    "FailureMetrics",
    "completed_workflow_ids",
    "failed_workflow_ids",
    "observed_workflow_ids",
    "started_workflow_ids",
    "workflow_completion_metrics",
    "workflow_failure_metrics",
]
