"""Showcase demonstrations for the workflow operating system.

This package bundles runnable, end-to-end demonstrations: realistic domain
workflows (employee onboarding, procurement, incident management, customer
onboarding) and integration demos that thread a workflow through the memory,
decision, approval, exception, analytics, and learning layers. They are meant
for exploration and presentation and only use the public library APIs.
"""

from workflow_os.demos.customer_onboarding import (
    build_workflow as build_customer_onboarding_workflow,
)
from workflow_os.demos.customer_onboarding import (
    run_demo as run_customer_onboarding_demo,
)
from workflow_os.demos.employee_onboarding import (
    build_workflow as build_employee_onboarding_workflow,
)
from workflow_os.demos.employee_onboarding import (
    run_demo as run_employee_onboarding_demo,
)
from workflow_os.demos.incident_management import (
    build_workflow as build_incident_management_workflow,
)
from workflow_os.demos.incident_management import (
    run_demo as run_incident_management_demo,
)
from workflow_os.demos.integration_analytics import (
    run_demo as run_analytics_demo,
)
from workflow_os.demos.integration_approval import (
    run_demo as run_approval_workflow_demo,
)
from workflow_os.demos.integration_decision import (
    run_demo as run_workflow_decision_demo,
)
from workflow_os.demos.integration_exception import (
    run_demo as run_exception_recovery_demo,
)
from workflow_os.demos.integration_learning import (
    run_demo as run_organizational_learning_demo,
)
from workflow_os.demos.integration_memory import (
    run_demo as run_workflow_memory_demo,
)
from workflow_os.demos.procurement import (
    build_workflow as build_procurement_workflow,
)
from workflow_os.demos.procurement import (
    run_demo as run_procurement_demo,
)

__all__ = [
    "build_customer_onboarding_workflow",
    "build_employee_onboarding_workflow",
    "build_incident_management_workflow",
    "build_procurement_workflow",
    "run_analytics_demo",
    "run_approval_workflow_demo",
    "run_customer_onboarding_demo",
    "run_employee_onboarding_demo",
    "run_exception_recovery_demo",
    "run_incident_management_demo",
    "run_organizational_learning_demo",
    "run_procurement_demo",
    "run_workflow_decision_demo",
    "run_workflow_memory_demo",
]
