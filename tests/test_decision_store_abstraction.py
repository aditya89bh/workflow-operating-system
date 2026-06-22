from datetime import datetime, timedelta, timezone

from workflow_os.decision import DecisionQuery, DecisionRecord, apply_query, matches


def _record(**kwargs) -> DecisionRecord:
    base = dict(
        workflow_id="wf",
        decision_type="workflow_decision",
        decision="decide",
    )
    base.update(kwargs)
    return DecisionRecord.create(**base)


def test_empty_query_matches_everything():
    record = _record()
    assert matches(record, DecisionQuery())


def test_filter_by_workflow_and_actor_and_type():
    record = _record(actor="it", decision_type="step_decision", step_id="s1")
    assert matches(record, DecisionQuery(workflow_id="wf"))
    assert matches(record, DecisionQuery(actor="it"))
    assert matches(record, DecisionQuery(step_id="s1"))
    assert matches(record, DecisionQuery(decision_types=("step_decision",)))
    assert not matches(record, DecisionQuery(actor="hr"))
    assert not matches(record, DecisionQuery(decision_types=("workflow_decision",)))


def test_filter_by_outcome():
    record = _record(outcome="successful")
    assert matches(record, DecisionQuery(outcome="successful"))
    assert not matches(record, DecisionQuery(outcome="failed"))


def test_apply_query_orders_and_limits():
    now = datetime.now(timezone.utc)
    records = [
        _record(timestamp=now + timedelta(seconds=2), decision="late"),
        _record(timestamp=now, decision="early"),
        _record(timestamp=now + timedelta(seconds=1), decision="mid"),
    ]
    asc = apply_query(records, DecisionQuery(order="asc"))
    assert [r.decision for r in asc] == ["early", "mid", "late"]

    desc = apply_query(records, DecisionQuery(order="desc", limit=1))
    assert [r.decision for r in desc] == ["late"]
