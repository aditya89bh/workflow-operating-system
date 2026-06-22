"""A runnable demonstration of the SOP memory layer.

The demo walks through the full loop: it creates a SOP, versions it, links it to
a workflow, searches for it, recommends it deterministically, and generates a
lifecycle report.
"""

from __future__ import annotations

import dataclasses

from workflow_os.sop.change_history import SOPChangeLog
from workflow_os.sop.linking import WorkflowSOPLinks, get_sops_for_workflow
from workflow_os.sop.recommendation import recommend_sop
from workflow_os.sop.record import SOPRecord, SOPStatus
from workflow_os.sop.reports import generate_lifecycle_report
from workflow_os.sop.search import search_sops
from workflow_os.sop.sqlite_store import SQLiteSOPStore
from workflow_os.sop.store import SOPStore
from workflow_os.sop.versioning import SOPVersionHistory
from workflow_os.workflow import Workflow


def run_demo(store: SOPStore | None = None) -> SOPStore:
    """Run the SOP memory demonstration, printing each stage."""
    store = store if store is not None else SQLiteSOPStore()
    history = SOPVersionHistory()
    changes = SOPChangeLog()

    # 1. Create a SOP.
    print("1. creating SOP")
    sop = SOPRecord.create(
        title="Employee Onboarding",
        workflow_type="onboarding",
        description="How we normally onboard a new hire",
        author="people-ops",
        status=SOPStatus.ACTIVE.value,
        tags=["hr", "people"],
        sop_id="onboarding-sop",
    )
    store.add(sop)
    history.record(sop)
    print(f"   created {sop.sop_id!r} v{sop.version} ({sop.status})")

    # 2. Version the SOP.
    print("\n2. versioning SOP")
    revised = dataclasses.replace(
        sop,
        version=2,
        description="How we normally onboard a new hire (now with a buddy)",
        updated_at=sop.updated_at,
    )
    store.update(revised)
    history.record(revised)
    change = changes.record_change(
        sop, revised, change_reason="add buddy step", changed_by="people-ops"
    )
    current = history.current_version(sop.sop_id)
    previous = history.previous_version(sop.sop_id)
    assert current is not None and previous is not None
    print(f"   current v{current.version}, previous v{previous.version}")
    print(f"   changed fields: {', '.join(change.changed_fields)}")

    # 3. Link the SOP to a workflow.
    print("\n3. linking SOP to workflow")
    links = WorkflowSOPLinks()
    links.link("new_hire", sop.sop_id)
    workflow = Workflow(
        id="wf-onboard-001",
        name="Onboard Dana",
        metadata={"workflow_type": "onboarding"},
    )
    linked = get_sops_for_workflow(store, workflow, links)
    print(f"   workflow {workflow.id!r} maps to {[s.sop_id for s in linked]}")

    # 4. Search for the SOP.
    print("\n4. searching SOPs")
    found = search_sops(store, text="onboard", tags=["hr"])
    print(f"   text+tag search found: {[s.title for s in found]}")

    # 5. Recommend a SOP (deterministic).
    print("\n5. recommending SOP")
    best = recommend_sop(store, workflow_type="onboarding", tags=["hr"], links=links)
    if best is not None:
        print(f"   recommended {best.sop_id!r} v{best.version}")

    # 6. Generate a lifecycle report.
    print("\n6. lifecycle report")
    report = generate_lifecycle_report(store)
    print(f"   total SOPs: {report.total_sops}")
    print(f"   active: {report.active_count}  inactive: {report.inactive_count}")
    print(f"   workflow coverage: {report.workflow_coverage_count} type(s)")
    print(f"   max version: {report.version_statistics['max_version']:.0f}")

    print("\ndone.")
    return store


if __name__ == "__main__":  # pragma: no cover
    run_demo()
