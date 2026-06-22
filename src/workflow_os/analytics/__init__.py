"""Workflow analytics for the workflow operating system.

A deterministic, rule-based analytics layer that measures, aggregates, analyzes,
reports, and exports facts about workflow executions. It reads from the earlier
layers (memory events, approvals, exceptions) without modifying them. There is no
learning, prediction, or recommendation here - every number is computed directly
from recorded data.
"""

from workflow_os.analytics.bottlenecks import Bottleneck, detect_bottlenecks
from workflow_os.analytics.comparison import (
    WorkflowComparison,
    WorkflowComparisonRow,
    compare_workflows,
)
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
from workflow_os.analytics.execution_summary import (
    ExecutionSummary,
    execution_summaries,
)
from workflow_os.analytics.failure import (
    FailureMetrics,
    failed_workflow_ids,
    workflow_failure_metrics,
)
from workflow_os.analytics.health import HealthScore, workflow_health_score
from workflow_os.analytics.reports import (
    WorkflowStatistics,
    WorkflowSummary,
    counts_by_day,
    workflow_statistics,
    workflow_summaries,
    workflow_trends,
)
from workflow_os.analytics.scorecards import (
    Scorecard,
    agent_scorecards,
    approval_scorecards,
    workflow_scorecards,
)
from workflow_os.analytics.slow_steps import SlowStep, slow_steps, slowest_steps
from workflow_os.analytics.step_duration import (
    step_duration_metrics,
    step_durations,
)
from workflow_os.analytics.team_stats import TeamStatistics, team_statistics

__all__ = [
    "Bottleneck",
    "CompletionMetrics",
    "DurationMetrics",
    "ExecutionSummary",
    "FailureMetrics",
    "HealthScore",
    "Scorecard",
    "SlowStep",
    "TeamStatistics",
    "WorkflowComparison",
    "WorkflowComparisonRow",
    "WorkflowStatistics",
    "WorkflowSummary",
    "agent_scorecards",
    "approval_scorecards",
    "compare_workflows",
    "completed_workflow_ids",
    "counts_by_day",
    "detect_bottlenecks",
    "execution_duration_metrics",
    "execution_summaries",
    "failed_workflow_ids",
    "observed_workflow_ids",
    "slow_steps",
    "slowest_steps",
    "started_workflow_ids",
    "step_duration_metrics",
    "step_durations",
    "summarize_durations",
    "team_statistics",
    "workflow_completion_metrics",
    "workflow_durations",
    "workflow_failure_metrics",
    "workflow_health_score",
    "workflow_scorecards",
    "workflow_statistics",
    "workflow_summaries",
    "workflow_trends",
]
