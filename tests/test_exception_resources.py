from workflow_os.exception import detect_missing_resources, find_missing_resources


def test_find_missing_resources():
    missing = find_missing_resources(["db", "api", "cache"], ["api"])
    assert missing == ["db", "cache"]


def test_find_missing_deduplicates():
    assert find_missing_resources(["db", "db"], []) == ["db"]


def test_detect_missing_resources():
    records = detect_missing_resources(
        required=["db", "api"],
        available=["api"],
        workflow_id="wf",
        step_id="s1",
    )
    assert len(records) == 1
    assert records[0].exception_type == "missing_resource"
    assert records[0].metadata["resource"] == "db"
    assert records[0].step_id == "s1"


def test_no_missing_returns_empty():
    assert detect_missing_resources(["db"], ["db"], workflow_id="wf") == []
