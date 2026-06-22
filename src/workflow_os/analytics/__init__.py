"""Workflow analytics for the workflow operating system.

A deterministic, rule-based analytics layer that measures, aggregates, analyzes,
reports, and exports facts about workflow executions. It reads from the earlier
layers (memory events, approvals, exceptions) without modifying them. There is no
learning, prediction, or recommendation here - every number is computed directly
from recorded data.
"""

from workflow_os.analytics.bottlenecks import Bottleneck, detect_bottlenecks
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
from workflow_os.analytics.step_duration import (
    step_duration_metrics,
    step_durations,
)

__all__ = [
    "Bottleneck",
    "CompletionMetrics",
    "DurationMetrics",
    "FailureMetrics",
    "completed_workflow_ids",
    "detect_bottlenecks",
    "execution_duration_metrics",
    "failed_workflow_ids",
    "observed_workflow_ids",
    "started_workflow_ids",
    "step_duration_metrics",
    "step_durations",
    "summarize_durations",
    "workflow_completion_metrics",
    "workflow_durations",
    "workflow_failure_metrics",
]
