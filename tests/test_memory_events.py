from workflow_os.memory import (
    STEP_EVENT_TYPES,
    WORKFLOW_EVENT_TYPES,
    MemoryEventType,
)


def test_all_event_type_values():
    expected = {
        "workflow_started",
        "workflow_paused",
        "workflow_resumed",
        "workflow_completed",
        "workflow_failed",
        "step_started",
        "step_completed",
        "step_failed",
        "step_skipped",
    }
    assert {e.value for e in MemoryEventType} == expected


def test_event_type_is_string():
    assert MemoryEventType.WORKFLOW_STARTED == "workflow_started"
    assert str(MemoryEventType.STEP_FAILED) == "step_failed"


def test_event_groupings_are_disjoint_and_complete():
    assert WORKFLOW_EVENT_TYPES.isdisjoint(STEP_EVENT_TYPES)
    assert WORKFLOW_EVENT_TYPES | STEP_EVENT_TYPES == set(MemoryEventType)
