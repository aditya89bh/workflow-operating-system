from workflow_os.sop import (
    SOPRecord,
    add_contributor,
    add_owner,
    add_reviewer,
    get_authorship,
    set_owners,
    set_reviewers,
)


def test_get_authorship_defaults_empty():
    sop = SOPRecord.create(title="t", workflow_type="x", author="hr")
    authorship = get_authorship(sop)
    assert authorship.author == "hr"
    assert authorship.reviewers == []
    assert authorship.owners == []
    assert authorship.contributors == []


def test_set_and_get_people():
    sop = SOPRecord.create(title="t", workflow_type="x")
    set_reviewers(sop, ["alice", "bob", "alice"])  # dedups
    set_owners(sop, ["people-ops"])
    authorship = get_authorship(sop)
    assert authorship.reviewers == ["alice", "bob"]
    assert authorship.owners == ["people-ops"]


def test_add_people_is_idempotent():
    sop = SOPRecord.create(title="t", workflow_type="x")
    add_reviewer(sop, "carol")
    add_reviewer(sop, "carol")
    add_owner(sop, "team")
    add_contributor(sop, "dan")
    authorship = get_authorship(sop)
    assert authorship.reviewers == ["carol"]
    assert authorship.owners == ["team"]
    assert authorship.contributors == ["dan"]


def test_authorship_does_not_clobber_other_metadata():
    sop = SOPRecord.create(title="t", workflow_type="x", metadata={"keep": 1})
    add_owner(sop, "team")
    assert sop.metadata["keep"] == 1
    assert sop.metadata["owners"] == ["team"]
