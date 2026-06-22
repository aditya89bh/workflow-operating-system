from workflow_os.exception import (
    ALL_SEVERITIES,
    ExceptionSeverity,
    normalize_severity,
    severity_rank,
)


def test_severity_values():
    assert {s.value for s in ExceptionSeverity} == {
        "low",
        "medium",
        "high",
        "critical",
    }


def test_all_severities_complete():
    assert len(ALL_SEVERITIES) == 4


def test_severity_rank_ordering():
    assert severity_rank("low") < severity_rank("medium")
    assert severity_rank("medium") < severity_rank("high")
    assert severity_rank("high") < severity_rank("critical")


def test_normalize_severity():
    assert normalize_severity("critical") == "critical"
    assert normalize_severity("nonsense") == "medium"
