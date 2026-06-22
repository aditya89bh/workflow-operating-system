"""Organizational learning for the workflow operating system.

A deterministic, rule-based learning layer that turns the history captured by the
earlier layers - memory events, decisions, SOPs, approvals, exceptions, and
analytics - into organizational knowledge: patterns, insights, recommendations,
and maturity scores. It only consumes the outputs of those layers; there is no
machine learning, prediction, autonomous optimization, or external service here.
"""

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
    "consistently_healthy_workflows",
    "highest_success_rate_workflows",
    "most_reliable_workflows",
    "new_insight_id",
    "new_recommendation_id",
    "recurring_bottlenecks",
    "recurring_exceptions",
    "recurring_workflows",
    "successful_workflow_insights",
    "workflow_run_stats",
]
