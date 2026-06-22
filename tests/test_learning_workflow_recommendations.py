from workflow_os.learning import workflow_improvement_recommendations
from workflow_os.memory.record import MemoryRecord


def rec(workflow_id, event_type, step_id=None, duration=None):
    metadata = {"duration_seconds": duration} if duration is not None else None
    return MemoryRecord.create(
        workflow_id=workflow_id,
        event_type=event_type,
        step_id=step_id,
        metadata=metadata,
    )


def test_simplify_recommendation_for_failing_workflow():
    records = [
        rec("bad", "workflow_failed"),
        rec("bad", "workflow_failed"),
    ]
    recs = workflow_improvement_recommendations(records, min_failures=2)
    actions = {r.metadata.get("action") for r in recs}
    assert "simplify" in actions
    simplify = next(r for r in recs if r.metadata.get("action") == "simplify")
    assert simplify.severity == "high"


def test_split_recommendation_for_large_workflow():
    records = [
        rec("big", "step_completed", f"s{i}") for i in range(5)
    ]
    recs = workflow_improvement_recommendations(records, large_workflow_steps=5)
    split = [r for r in recs if r.metadata.get("action") == "split"]
    assert len(split) == 1
    assert split[0].metadata["step_count"] == 5


def test_bottleneck_recommendation():
    records = [
        rec("wf", "step_completed", "slow", 5.0),
        rec("wf", "step_completed", "slow", 6.0),
    ]
    recs = workflow_improvement_recommendations(records, bottleneck_min_occurrences=2)
    bottleneck = [r for r in recs if r.metadata.get("action") == "remove_bottleneck"]
    assert bottleneck and bottleneck[0].metadata["step_id"] == "slow"


def test_no_recommendations_for_clean_history():
    records = [rec("wf", "workflow_completed")]
    assert workflow_improvement_recommendations(records) == []
