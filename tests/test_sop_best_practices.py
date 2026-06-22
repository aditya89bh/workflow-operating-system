from workflow_os.sop import (
    BestPracticeStore,
    BestPracticeType,
    capture_best_practice,
)


def test_capture_and_retrieve_by_sop():
    store = BestPracticeStore()
    practice = capture_best_practice(
        store,
        "Always assign a buddy on day one",
        practice_type=BestPracticeType.GUIDELINE.value,
        sop_id="onb1",
    )
    assert store.get(practice.practice_id) is practice
    assert store.for_sop("onb1") == [practice]


def test_filter_by_type():
    store = BestPracticeStore()
    capture_best_practice(store, "c", practice_type=BestPracticeType.CONVENTION.value)
    capture_best_practice(store, "s", practice_type=BestPracticeType.STANDARD.value)
    assert len(store.for_type("convention")) == 1
    assert len(store.for_type("standard")) == 1


def test_practice_type_values():
    assert {t.value for t in BestPracticeType} == {
        "practice",
        "guideline",
        "convention",
        "standard",
    }


def test_default_practice_type():
    store = BestPracticeStore()
    practice = capture_best_practice(store, "default")
    assert practice.practice_type == BestPracticeType.PRACTICE.value
