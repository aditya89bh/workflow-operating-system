from workflow_os.sop import (
    LessonStore,
    LessonType,
    capture_lesson,
)


def test_capture_and_retrieve_by_sop():
    store = LessonStore()
    lesson = capture_lesson(
        store,
        "Provision email earlier to avoid day-one delays",
        lesson_type=LessonType.POSTMORTEM.value,
        sop_id="onb1",
        author="people-ops",
    )
    assert store.get(lesson.lesson_id) is lesson
    assert store.for_sop("onb1") == [lesson]


def test_filter_by_type():
    store = LessonStore()
    capture_lesson(store, "obs", lesson_type=LessonType.OBSERVATION.value)
    capture_lesson(store, "note", lesson_type=LessonType.OPERATIONAL_NOTE.value)
    assert len(store.for_type("observation")) == 1
    assert len(store.for_type("operational_note")) == 1


def test_lesson_type_values():
    assert {t.value for t in LessonType} == {
        "lesson",
        "observation",
        "postmortem",
        "operational_note",
    }


def test_default_lesson_type():
    store = LessonStore()
    lesson = capture_lesson(store, "default note")
    assert lesson.lesson_type == LessonType.LESSON.value
