from workflow_os.learning import (
    all_examples,
    improvement_journey,
    organizational_maturity_score,
    struggling_organization,
    successful_organization,
)


def _maturity(example):
    return organizational_maturity_score(
        example.records,
        sops=example.sops,
        exceptions=example.exceptions,
        approvals=example.approvals,
        recoveries=example.recoveries,
    ).overall


def test_all_examples_present():
    names = {e.name for e in all_examples()}
    assert names == {"successful", "struggling", "improvement_journey"}


def test_successful_more_mature_than_struggling():
    assert _maturity(successful_organization()) > _maturity(struggling_organization())


def test_improvement_journey_has_mixed_history():
    example = improvement_journey()
    types = {r.event_type for r in example.records}
    assert "workflow_failed" in types
    assert "workflow_completed" in types


def test_examples_have_records():
    for example in all_examples():
        assert example.records
