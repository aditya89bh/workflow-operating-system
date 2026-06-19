from workflow_os import Workflow, WorkflowStep
from workflow_os.memory import (
    HIGH_CONFIDENCE,
    MEDIUM_CONFIDENCE,
    MemoryQuery,
    MemoryRecorder,
    SQLiteMemoryStore,
    confidence_for,
)


def test_completed_event_is_high_confidence():
    assert confidence_for("workflow_completed") == HIGH_CONFIDENCE


def test_failure_event_is_medium_confidence():
    assert confidence_for("step_failed") == MEDIUM_CONFIDENCE


def test_manual_event_uses_configurable_confidence():
    assert confidence_for("note", manual=True, manual_confidence=0.42) == 0.42


def test_overrides_take_precedence():
    assert confidence_for("step_failed", overrides={"step_failed": 0.1}) == 0.1


def test_unknown_event_uses_default():
    assert 0.0 <= confidence_for("something_unmapped") <= 1.0


def test_recorder_applies_confidence_scores():
    store = SQLiteMemoryStore()
    wf = Workflow(id="wf", name="WF", steps=[WorkflowStep(id="s1", name="A")])
    recorder = MemoryRecorder(store)
    recorder.start(wf)
    recorder.start_step(wf, wf.steps[0])
    recorder.fail_step(wf, wf.steps[0], reason="boom")

    completed = store.query(MemoryQuery(event_types=("workflow_started",)))
    failed = store.query(MemoryQuery(event_types=("step_failed",)))
    assert completed[0].confidence == HIGH_CONFIDENCE
    assert failed[0].confidence == MEDIUM_CONFIDENCE
