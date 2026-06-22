"""Multi-agent collaboration for the workflow operating system.

This subpackage provides a deterministic, rule-based multi-agent layer on top of
the workflow, memory, decision, SOP, approval, and exception layers. Agents are
service objects (coordinator, planner, execution, compliance, memory) - not LLM
wrappers - that assign, delegate, communicate, coordinate, audit, and measure
collaboration. It builds on the earlier layers without modifying them.
"""

from workflow_os.agents.accountability import (
    AgentAccountability,
    actions_performed,
    build_accountability,
    ownership_history,
    responsibility_chain,
)
from workflow_os.agents.compliance import ComplianceAgent, ComplianceResult
from workflow_os.agents.coordinator import CoordinationError, CoordinatorAgent
from workflow_os.agents.delegation import (
    DelegationAction,
    DelegationError,
    DelegationEvent,
    TaskAssignment,
    TaskDelegation,
    TaskNotFoundError,
    new_task_id,
)
from workflow_os.agents.execution import ExecutionAgent, ExecutionEvent
from workflow_os.agents.logs import (
    CollaborationEntry,
    CollaborationEventType,
    CollaborationLog,
)
from workflow_os.agents.memory_agent import MemoryAgent
from workflow_os.agents.messaging import Message, MessageBus, new_message_id
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
    "AgentAccountability",
    "AgentAlreadyRegisteredError",
    "AgentNotFoundError",
    "AgentRegistry",
    "AgentRole",
    "CollaborationEntry",
    "CollaborationEventType",
    "CollaborationLog",
    "ComplianceAgent",
    "ComplianceResult",
    "CoordinationError",
    "CoordinatorAgent",
    "DelegationAction",
    "DelegationError",
    "DelegationEvent",
    "ExecutionAgent",
    "ExecutionEvent",
    "MemoryAccess",
    "MemoryAgent",
    "Message",
    "MessageBus",
    "PlannerAgent",
    "SharedMemory",
    "SharedWorkspace",
    "TaskAssignment",
    "TaskDelegation",
    "TaskNotFoundError",
    "actions_performed",
    "build_accountability",
    "new_agent_id",
    "new_message_id",
    "new_task_id",
    "normalize_role",
    "ownership_history",
    "responsibility_chain",
]
