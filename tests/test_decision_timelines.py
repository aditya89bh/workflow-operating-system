from datetime import datetime, timedelta, timezone

from workflow_os.decision import (
    DecisionRecord,
    SQLiteDecisionStore,
    get_actor_decision_timeline,
    get_decision_timeline,
    get_workflow_decision_timeline,
)


def _seed() -> SQLiteDecisionStore:
    store = SQLiteDecisionStore()
    base = datetime(2026, 1, 1, tzinfo=timezone.utc)
    store.add(
        DecisionRecord.create(
            workflow_id="wf",
            decision_type="workflow_decision",
            decision="start",
            actor="ops",
            timestamp=base,
        )
    )
    store.add(
        DecisionRecord.create(
            workflow_id="wf",
            decision_type="step_decision",
            decision="middle",
            actor="it",
            timestamp=base + timedelta(seconds=30),
        )
    )
    store.add(
        DecisionRecord.create(
            workflow_id="other",
            decision_type="workflow_decision",
            decision="elsewhere",
            actor="ops",
            timestamp=base + timedelta(seconds=60),
        )
    )
    return store


def test_workflow_timeline_is_ordered_with_offsets():
    timeline = get_workflow_decision_timeline(_seed(), "wf")
    assert [entry.decision for entry in timeline] == ["start", "middle"]
    assert timeline[0].offset_seconds == 0.0
    assert timeline[1].offset_seconds == 30.0


def test_actor_timeline_spans_workflows():
    timeline = get_actor_decision_timeline(_seed(), "ops")
    assert [entry.decision for entry in timeline] == ["start", "elsewhere"]


def test_full_decision_timeline():
    timeline = get_decision_timeline(_seed())
    assert [entry.decision for entry in timeline] == ["start", "middle", "elsewhere"]
    assert timeline[-1].offset_seconds == 60.0
