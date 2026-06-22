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
from workflow_os.analytics.csv_export import rows_to_dicts, to_csv, write_csv
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
from workflow_os.analytics.json_export import to_json, write_json
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
from workflow_os.analytics.trends import (
    TrendReport,
    approval_trends,
    exception_trends,
    failure_trends,
    trend_report,
    workflow_completion_trends,
)

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
    "TrendReport",
    "WorkflowComparison",
    "WorkflowComparisonRow",
    "WorkflowStatistics",
    "WorkflowSummary",
    "agent_scorecards",
    "approval_scorecards",
    "approval_trends",
    "compare_workflows",
    "completed_workflow_ids",
    "counts_by_day",
    "detect_bottlenecks",
    "exception_trends",
    "execution_duration_metrics",
    "execution_summaries",
    "failed_workflow_ids",
    "failure_trends",
    "observed_workflow_ids",
    "rows_to_dicts",
    "slow_steps",
    "slowest_steps",
    "started_workflow_ids",
    "step_duration_metrics",
    "step_durations",
    "summarize_durations",
    "team_statistics",
    "to_csv",
    "to_json",
    "trend_report",
    "workflow_completion_metrics",
    "workflow_completion_trends",
    "workflow_durations",
    "workflow_failure_metrics",
    "workflow_health_score",
    "workflow_scorecards",
    "workflow_statistics",
    "workflow_summaries",
    "workflow_trends",
    "write_csv",
    "write_json",
]
