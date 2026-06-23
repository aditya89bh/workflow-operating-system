"""Registry of named showcase demonstrations.

Maps stable demo names to their ``run`` callables and provides helpers to run a
single demo by name or run every demo in sequence. The CLI ``demo`` and
``demo-all`` commands are built on top of this registry.
"""

from __future__ import annotations

from collections.abc import Callable

from workflow_os.demos.customer_onboarding import run_demo as _customer_onboarding
from workflow_os.demos.employee_onboarding import run_demo as _employee_onboarding
from workflow_os.demos.incident_management import run_demo as _incident_management
from workflow_os.demos.integration_analytics import run_demo as _analytics
from workflow_os.demos.integration_approval import run_demo as _approval_workflow
from workflow_os.demos.integration_decision import run_demo as _workflow_decision
from workflow_os.demos.integration_exception import run_demo as _exception_recovery
from workflow_os.demos.integration_learning import run_demo as _organizational_learning
from workflow_os.demos.integration_memory import run_demo as _workflow_memory
from workflow_os.demos.procurement import run_demo as _procurement

DEMOS: dict[str, Callable[[], object]] = {
    "employee-onboarding": _employee_onboarding,
    "procurement": _procurement,
    "incident-management": _incident_management,
    "customer-onboarding": _customer_onboarding,
    "workflow-memory": _workflow_memory,
    "workflow-decision": _workflow_decision,
    "approval-workflow": _approval_workflow,
    "exception-recovery": _exception_recovery,
    "analytics": _analytics,
    "organizational-learning": _organizational_learning,
}


def demo_names() -> list[str]:
    """Return the available demo names in their registered order."""
    return list(DEMOS)


def run_named_demo(name: str) -> None:
    """Run a single demo by name.

    Raises:
        KeyError: If ``name`` is not a registered demo.
    """
    if name not in DEMOS:
        available = ", ".join(DEMOS)
        raise KeyError(f"unknown demo {name!r}; available: {available}")
    DEMOS[name]()


def run_all_demos() -> None:
    """Run every registered demo in order, separated by headers."""
    for index, (name, run) in enumerate(DEMOS.items(), start=1):
        print(f"{'=' * 60}")
        print(f"[{index}/{len(DEMOS)}] {name}")
        print(f"{'=' * 60}")
        run()
        print()


if __name__ == "__main__":  # pragma: no cover
    run_all_demos()
