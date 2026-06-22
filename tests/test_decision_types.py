from workflow_os.decision import ALL_DECISION_TYPES, DecisionType


def test_decision_type_values():
    expected = {
        "workflow_decision",
        "step_decision",
        "exception_decision",
        "manual_decision",
        "system_decision",
    }
    assert {t.value for t in DecisionType} == expected


def test_decision_type_is_string_enum():
    assert DecisionType.WORKFLOW_DECISION == "workflow_decision"
    assert str(DecisionType.EXCEPTION_DECISION) == "exception_decision"


def test_all_decision_types_contains_every_member():
    assert ALL_DECISION_TYPES == frozenset(DecisionType)
    assert len(ALL_DECISION_TYPES) == 5
