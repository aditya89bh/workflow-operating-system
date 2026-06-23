"""Showcase demonstrations for the workflow operating system.

This package bundles runnable, end-to-end demonstrations: realistic domain
workflows (employee onboarding, procurement, incident management, customer
onboarding) and integration demos that thread a workflow through the memory,
decision, approval, exception, analytics, and learning layers. They are meant
for exploration and presentation and only use the public library APIs.
"""

from workflow_os.demos.employee_onboarding import (
    build_workflow as build_employee_onboarding_workflow,
)
from workflow_os.demos.employee_onboarding import (
    run_demo as run_employee_onboarding_demo,
)
from workflow_os.demos.procurement import (
    build_workflow as build_procurement_workflow,
)
from workflow_os.demos.procurement import (
    run_demo as run_procurement_demo,
)

__all__ = [
    "build_employee_onboarding_workflow",
    "build_procurement_workflow",
    "run_employee_onboarding_demo",
    "run_procurement_demo",
]
