"""Organizational learning for the workflow operating system.

A deterministic, rule-based learning layer that turns the history captured by the
earlier layers - memory events, decisions, SOPs, approvals, exceptions, and
analytics - into organizational knowledge: patterns, insights, recommendations,
and maturity scores. It only consumes the outputs of those layers; there is no
machine learning, prediction, autonomous optimization, or external service here.
"""

from workflow_os.learning.recommendation import (
    Recommendation,
    new_recommendation_id,
)

__all__ = [
    "Recommendation",
    "new_recommendation_id",
]
