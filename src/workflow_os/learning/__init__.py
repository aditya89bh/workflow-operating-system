"""Organizational learning for the workflow operating system.

A deterministic, rule-based learning layer that turns the history captured by the
earlier layers - memory events, decisions, SOPs, approvals, exceptions, and
analytics - into organizational knowledge: patterns, insights, recommendations,
and maturity scores. It only consumes the outputs of those layers; there is no
machine learning, prediction, autonomous optimization, or external service here.
"""

from workflow_os.learning.approval_recommendations import (
    approval_improvement_recommendations,
    approver_bottleneck_recommendations,
    escalation_recommendations,
    reduce_approver_recommendations,
)
from workflow_os.learning.automation import (
    automation_opportunity_recommendations,
    repeated_approval_recommendations,
    repeated_recovery_recommendations,
    repetitive_task_recommendations,
)
from workflow_os.learning.continuous_improvement import (
    ContinuousImprovementReport,
    continuous_improvement_report,
    improvement_opportunities,
)
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
from workflow_os.learning.maturity import (
    MaturityScore,
    maturity_level,
    organizational_maturity_score,
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
from workflow_os.learning.sop_recommendations import sop_update_recommendations
from workflow_os.learning.success import (
    consistently_healthy_workflows,
    highest_success_rate_workflows,
    most_reliable_workflows,
    successful_workflow_insights,
)
from workflow_os.learning.workflow_recommendations import (
    workflow_improvement_recommendations,
)

__all__ = [
    "ContinuousImprovementReport",
    "MaturityScore",
    "OrganizationalInsight",
    "Recommendation",
    "WorkflowRunStats",
    "approval_improvement_recommendations",
    "approver_bottleneck_recommendations",
    "automation_opportunity_recommendations",
    "chronic_workflow_problems",
    "consistently_healthy_workflows",
    "continuous_improvement_report",
    "escalation_recommendations",
    "failure_hotspots",
    "failure_pattern_insights",
    "frequently_failing_workflows",
    "highest_success_rate_workflows",
    "improvement_opportunities",
    "maturity_level",
    "most_reliable_workflows",
    "new_insight_id",
    "organizational_maturity_score",
    "new_recommendation_id",
    "recurring_bottlenecks",
    "recurring_exception_insights",
    "recurring_exceptions",
    "recurring_recovery_actions",
    "recurring_workflows",
    "reduce_approver_recommendations",
    "repeated_approval_recommendations",
    "repeated_exceptions",
    "repeated_recovery_recommendations",
    "repetitive_task_recommendations",
    "sop_update_recommendations",
    "successful_workflow_insights",
    "unstable_workflows",
    "workflow_improvement_recommendations",
    "workflow_run_stats",
]
