from workflow_os.exception import ALL_EXCEPTION_TYPES, ExceptionType, normalize_type


def test_type_values():
    assert {t.value for t in ExceptionType} == {
        "workflow_failure",
        "step_failure",
        "timeout",
        "missing_resource",
        "approval_failure",
        "validation_failure",
        "unknown",
    }


def test_all_exception_types_complete():
    assert len(ALL_EXCEPTION_TYPES) == 7


def test_normalize_type():
    assert normalize_type("timeout") == "timeout"
    assert normalize_type("nonsense") == "unknown"
