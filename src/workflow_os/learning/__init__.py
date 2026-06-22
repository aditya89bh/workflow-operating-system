"""Organizational learning for the workflow operating system.

A deterministic, rule-based learning layer that turns the history captured by the
earlier layers - memory events, decisions, SOPs, approvals, exceptions, and
analytics - into organizational knowledge: patterns, insights, recommendations,
and maturity scores. It only consumes the outputs of those layers; there is no
machine learning, prediction, autonomous optimization, or external service here.
"""

from workflow_os.learning.exception_patterns import (
    chronic_workflow_problems,
    recurring_exception_insights,
    recurring_recovery_actions,
    repeated_exceptions,
)
from workflow_os.learning.failure_patterns import (
    failure_hotspots,
    failure_pattern_insights,
    frequently_failing_workflows,
    unstable_workflows,
)
from workflow_os.learning.insight import (
    OrganizationalInsight,
    new_insight_id,
)
from workflow_os.learning.patterns import (
    WorkflowRunStats,
    recurring_bottlenecks,
    recurring_exceptions,
    recurring_workflows,
    workflow_run_stats,
)
from workflow_os.learning.recommendation import (
    Recommendation,
    new_recommendation_id,
)
from workflow_os.learning.success import (
    consistently_healthy_workflows,
    highest_success_rate_workflows,
    most_reliable_workflows,
    successful_workflow_insights,
)

__all__ = [
    "OrganizationalInsight",
    "Recommendation",
    "WorkflowRunStats",
    "chronic_workflow_problems",
    "consistently_healthy_workflows",
    "failure_hotspots",
    "failure_pattern_insights",
    "frequently_failing_workflows",
    "highest_success_rate_workflows",
    "most_reliable_workflows",
    "new_insight_id",
    "new_recommendation_id",
    "recurring_bottlenecks",
    "recurring_exception_insights",
    "recurring_exceptions",
    "recurring_recovery_actions",
    "recurring_workflows",
    "repeated_exceptions",
    "successful_workflow_insights",
    "unstable_workflows",
    "workflow_run_stats",
]
