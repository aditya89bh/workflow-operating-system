"""Shared workspace.

A :class:`SharedWorkspace` is the deterministic collaboration surface agents use
to share state. It holds shared key/value state, the workflow context being
worked on, per-agent context, and workspace-level metadata.
"""

from __future__ import annotations

from typing import Any

from workflow_os.workflow import Workflow


class SharedWorkspace:
    """A shared context object that agents read from and write to."""

    def __init__(
        self,
        workspace_id: str,
        workflow: Workflow | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        self.workspace_id = workspace_id
        self.workflow = workflow
        self.state: dict[str, Any] = {}
        self._agent_context: dict[str, dict[str, Any]] = {}
        self.metadata: dict[str, Any] = dict(metadata or {})

    def attach_workflow(self, workflow: Workflow) -> None:
        """Attach the workflow context being collaborated on."""
        self.workflow = workflow

    def set_state(self, key: str, value: Any) -> None:
        """Set a shared state value."""
        self.state[key] = value

    def get_state(self, key: str, default: Any = None) -> Any:
        """Return a shared state value, or ``default`` if missing."""
        return self.state.get(key, default)

    def update_state(self, values: dict[str, Any]) -> None:
        """Merge ``values`` into the shared state."""
        self.state.update(values)

    def agent_context(self, agent_id: str) -> dict[str, Any]:
        """Return the per-agent context dict, creating it on first access."""
        return self._agent_context.setdefault(agent_id, {})

    def set_agent_context(self, agent_id: str, key: str, value: Any) -> None:
        """Set a value in a specific agent's context."""
        self.agent_context(agent_id)[key] = value
