from workflow_os.exception import (
    ExceptionRecord,
    RetryStrategy,
    count_retries,
)


def make():
    return ExceptionRecord.create(workflow_id="wf", exception_type="timeout")


def test_should_retry_caps_attempts():
    strategy = RetryStrategy(max_attempts=2)
    assert strategy.should_retry(0)
    assert strategy.should_retry(1)
    assert not strategy.should_retry(2)


def test_next_attempt_increments():
    strategy = RetryStrategy(max_attempts=3)
    exception = make()
    action = strategy.next_attempt(exception, attempts_made=1)
    assert action is not None
    assert action.action == "retry"
    assert action.metadata["attempt"] == 2


def test_next_attempt_exhausted():
    strategy = RetryStrategy(max_attempts=1)
    assert strategy.next_attempt(make(), attempts_made=1) is None


def test_count_retries():
    exception = make()
    strategy = RetryStrategy()
    recoveries = [
        strategy.next_attempt(exception, 0),
        strategy.next_attempt(exception, 1),
    ]
    recoveries = [r for r in recoveries if r is not None]
    assert count_retries(recoveries, exception.exception_id) == 2
    assert count_retries(recoveries, "other") == 0
