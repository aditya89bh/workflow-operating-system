from workflow_os.decision import (
    ComparisonReport,
    DecisionRecorder,
    SQLiteDecisionStore,
    compare_actors,
    compare_successful_vs_failed,
    compare_workflows,
)


def _seed() -> SQLiteDecisionStore:
    store = SQLiteDecisionStore()
    recorder = DecisionRecorder(store)
    recorder.record_decision(
        workflow_id="wf1", decision="a", actor="it", outcome="successful"
    )
    recorder.record_decision(
        workflow_id="wf1", decision="b", actor="it", outcome="failed"
    )
    recorder.record_decision(
        workflow_id="wf2", decision="c", actor="hr", outcome="successful"
    )
    return store


def test_compare_successful_vs_failed():
    report = compare_successful_vs_failed(_seed())
    assert isinstance(report, ComparisonReport)
    assert report.stats_a.total_decisions == 2  # successful
    assert report.stats_b.total_decisions == 1  # failed


def test_compare_workflows():
    report = compare_workflows(_seed(), "wf1", "wf2")
    assert report.stats_a.total_decisions == 2
    assert report.stats_b.total_decisions == 1


def test_compare_actors_as_dict():
    report = compare_actors(_seed(), "it", "hr")
    data = report.as_dict()
    assert data["label_a"] == "it"
    assert data["stats_a"]["total_decisions"] == 2
    assert data["stats_b"]["total_decisions"] == 1
