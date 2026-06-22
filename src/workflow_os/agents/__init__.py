"""Multi-agent collaboration for the workflow operating system.

This subpackage provides a deterministic, rule-based multi-agent layer on top of
the workflow, memory, decision, SOP, approval, and exception layers. Agents are
service objects (coordinator, planner, execution, compliance, memory) - not LLM
wrappers - that assign, delegate, communicate, coordinate, audit, and measure
collaboration. It builds on the earlier layers without modifying them.
"""

from workflow_os.agents.record import Agent, new_agent_id

__all__ = [
    "Agent",
    "new_agent_id",
]
