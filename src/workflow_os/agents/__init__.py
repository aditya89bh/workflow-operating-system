"""Multi-agent collaboration for the workflow operating system.

This subpackage provides a deterministic, rule-based multi-agent layer on top of
the workflow, memory, decision, SOP, approval, and exception layers. Agents are
service objects (coordinator, planner, execution, compliance, memory) - not LLM
wrappers - that assign, delegate, communicate, coordinate, audit, and measure
collaboration. It builds on the earlier layers without modifying them.
"""

from workflow_os.agents.compliance import ComplianceAgent, ComplianceResult
from workflow_os.agents.coordinator import CoordinationError, CoordinatorAgent
from workflow_os.agents.execution import ExecutionAgent, ExecutionEvent
from workflow_os.agents.memory_agent import MemoryAgent
from workflow_os.agents.planner import PlannerAgent
from workflow_os.agents.record import Agent, new_agent_id
from workflow_os.agents.registry import (
    AgentAlreadyRegisteredError,
    AgentNotFoundError,
    AgentRegistry,
)
from workflow_os.agents.roles import ALL_AGENT_ROLES, AgentRole, normalize_role
from workflow_os.agents.shared_memory import MemoryAccess, SharedMemory
from workflow_os.agents.workspace import SharedWorkspace

__all__ = [
    "ALL_AGENT_ROLES",
    "Agent",
    "AgentAlreadyRegisteredError",
    "AgentNotFoundError",
    "AgentRegistry",
    "AgentRole",
    "ComplianceAgent",
    "ComplianceResult",
    "CoordinationError",
    "CoordinatorAgent",
    "ExecutionAgent",
    "ExecutionEvent",
    "MemoryAccess",
    "MemoryAgent",
    "PlannerAgent",
    "SharedMemory",
    "SharedWorkspace",
    "new_agent_id",
    "normalize_role",
]
