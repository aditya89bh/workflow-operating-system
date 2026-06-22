"""End-to-end integration tests for the SOP memory layer.

These exercise the full Capture -> Version -> Search -> Retrieve -> Link ->
Analyze loop across the SOP modules working together, including integration with
Phase 3 decisions.
"""

from __future__ import annotations

import dataclasses

from workflow_os.decision import DecisionRecorder, SQLiteDecisionStore
from workflow_os.sop import (
    SOPChangeLog,
    SOPRecord,
    SOPVersionHistory,
    SQLiteSOPStore,
    WorkflowSOPLinks,
    capture_best_practice,
    capture_exception_from_decision,
    capture_lesson,
    detect_conflicts,
    generate_lifecycle_report,
    get_sops_for_workflow,
    recommend_sop,
    score_sops,
    search_sops,
)
from workflow_os.sop.best_practices import BestPracticeStore
from workflow_os.sop.exceptions import SOPExceptionStore
from workflow_os.sop.lessons import LessonStore
from workflow_os.workflow import Workflow


def test_capture_version_search_retrieve_link_analyze():
    store = SQLiteSOPStore()
    history = SOPVersionHistory()
    changes = SOPChangeLog()

    # Capture
    sop = SOPRecord.create(
        title="Employee Onboarding",
        workflow_type="onboarding",
        description="How we onboard new hires",
        author="people-ops",
        tags=["hr"],
        status="active",
        sop_id="onb",
    )
    store.add(sop)
    history.record(sop)

    # Version
    updated = dataclasses.replace(
        sop, version=2, description="How we onboard new hires (revised)"
    )
    store.update(updated)
    history.record(updated)
    changes.record_change(sop, updated, change_reason="clarify steps", changed_by="hr")

    assert history.current_version("onb").version == 2
    assert history.previous_version("onb").version == 1
    assert set(changes.for_sop("onb")[0].changed_fields) == {"description", "version"}

    # Search
    assert search_sops(store, workflow_type="onboarding", tags=["hr"])[0].sop_id == "onb"

    # Link + Retrieve
    links = WorkflowSOPLinks()
    links.link("new_hire", "onb")
    workflow = Workflow(id="wf1", name="x", metadata={"workflow_type": "onboarding"})
    assert [s.sop_id for s in get_sops_for_workflow(store, workflow)] == ["onb"]

    # Analyze: recommend + score + report + conflicts
    assert recommend_sop(store, workflow_type="onboarding").sop_id == "onb"
    assert score_sops(store, workflow_type="onboarding")[0].sop_id == "onb"
    report = generate_lifecycle_report(store)
    assert report.total_sops == 1
    assert report.active_count == 1
    assert detect_conflicts(store) == []


def test_knowledge_capture_integration():
    lessons = LessonStore()
    practices = BestPracticeStore()
    exceptions = SOPExceptionStore()

    capture_lesson(lessons, "Provision email earlier", sop_id="onb")
    capture_best_practice(practices, "Assign a buddy on day one", sop_id="onb")

    decisions = SQLiteDecisionStore()
    recorder = DecisionRecorder(decisions)
    workflow = Workflow(id="wf1", name="Onboarding", metadata={"owner": "people-ops"})
    decision = recorder.record_exception_decision(
        workflow, "Use backup mail provider", reason="primary timeout"
    )
    exc = capture_exception_from_decision(exceptions, decision, sop_id="onb")

    assert lessons.for_sop("onb")[0].text == "Provision email earlier"
    assert practices.for_sop("onb")[0].text == "Assign a buddy on day one"
    assert exc.decision_id == decision.decision_id
    assert exc.reason == "primary timeout"
