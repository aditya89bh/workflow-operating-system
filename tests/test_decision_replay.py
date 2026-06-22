from datetime import datetime, timedelta, timezone

from workflow_os.decision import (
    DecisionRecord,
    DecisionReplay,
    SQLiteDecisionStore,
    reconstruct_decision_timeline,
    replay_actor_decisions,
    replay_workflow_decisions,
)


def _seed() -> SQLiteDecisionStore:
    store = SQLiteDecisionStore()
    base = datetime(2026, 1, 1, tzinfo=timezone.utc)
    for index, (decision, actor) in enumerate(
        [("first", "it"), ("second", "hr"), ("third", "it")]
    ):
        store.add(
            DecisionRecord.create(
                workflow_id="wf",
                decision_type="workflow_decision",
                decision=decision,
                actor=actor,
                rationale="because",
                timestamp=base + timedelta(seconds=index * 10),
            )
        )
    return store


def test_replay_workflow_is_ordered_with_explanations():
    events = replay_workflow_decisions(_seed(), "wf")
    assert [e.decision.decision for e in events] == ["first", "second", "third"]
    assert [e.sequence for e in events] == [0, 1, 2]
    assert events[2].offset_seconds == 20.0
    assert "because" in events[0].explanation.why


def test_replay_actor_filters_by_actor():
    events = replay_actor_decisions(_seed(), "it")
    assert [e.decision.decision for e in events] == ["first", "third"]


def test_reconstruct_timeline():
    timeline = reconstruct_decision_timeline(_seed())
    assert [entry.decision for entry in timeline] == ["first", "second", "third"]


def test_replay_engine_class():
    replay = DecisionReplay(_seed())
    assert len(replay.replay_workflow("wf")) == 3
    assert replay.replay_actor("hr")[0].decision.decision == "second"
