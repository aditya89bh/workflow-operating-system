from workflow_os.sop import (
    SOPRecord,
    SQLiteSOPStore,
    WorkflowSOPLinks,
    get_sops_for_workflow,
    get_sops_for_workflow_type,
    get_workflow_types_for_sop,
    workflow_type_of,
)
from workflow_os.workflow import Workflow


def test_workflow_type_of_prefers_metadata():
    wf = Workflow(id="wf1", name="x", metadata={"workflow_type": "onboarding"})
    assert workflow_type_of(wf) == "onboarding"
    assert workflow_type_of(Workflow(id="incident", name="x")) == "incident"


def test_implicit_link_by_workflow_type():
    store = SQLiteSOPStore()
    sop = SOPRecord.create(title="Onboarding", workflow_type="onboarding")
    store.add(sop)
    wf = Workflow(id="wf1", name="x", metadata={"workflow_type": "onboarding"})
    results = get_sops_for_workflow(store, wf)
    assert [s.sop_id for s in results] == [sop.sop_id]


def test_explicit_links_extend_results():
    store = SQLiteSOPStore()
    sop = SOPRecord.create(title="General", workflow_type="general", sop_id="s1")
    store.add(sop)
    links = WorkflowSOPLinks()
    links.link("onboarding", "s1")

    results = get_sops_for_workflow_type(store, "onboarding", links)
    assert [s.sop_id for s in results] == ["s1"]
    assert get_workflow_types_for_sop(sop, links) == {"general", "onboarding"}


def test_unlink_removes_association():
    links = WorkflowSOPLinks()
    links.link("onboarding", "s1")
    links.unlink("onboarding", "s1")
    assert links.sop_ids_for_workflow_type("onboarding") == set()
    assert links.workflow_types_for_sop("s1") == set()
