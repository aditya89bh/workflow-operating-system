from workflow_os.decision import (
    DecisionRecord,
    explain_decision,
    explain_decision_text,
)


def test_explain_decision_structure():
    record = DecisionRecord.create(
        workflow_id="wf",
        decision_type="step_decision",
        decision="Issue laptop",
        rationale="Role requires it",
        alternatives=["Defer", "Refurbished unit"],
        step_id="assign_laptop",
        actor="it",
        outcome="successful",
    )
    explanation = explain_decision(record)
    assert "it made a step_decision" in explanation.what_happened
    assert "assign_laptop" in explanation.what_happened
    assert "Role requires it" in explanation.why
    assert "alternatives considered: Defer, Refurbished unit" in explanation.why
    assert "successful" in explanation.outcome


def test_explain_decision_handles_missing_fields():
    record = DecisionRecord.create(
        workflow_id="wf",
        decision_type="workflow_decision",
        decision="Proceed",
    )
    explanation = explain_decision(record)
    assert "an unspecified actor" in explanation.what_happened
    assert "the workflow" in explanation.what_happened
    assert "no rationale was recorded" in explanation.why


def test_explain_decision_text_renders_all_sections():
    record = DecisionRecord.create(
        workflow_id="wf", decision_type="manual_decision", decision="Do it"
    )
    text = explain_decision_text(record)
    assert "What happened:" in text
    assert "Why:" in text
    assert "Outcome:" in text
