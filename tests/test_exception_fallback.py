from workflow_os.exception import ExceptionRecord, FallbackStrategy


def make(exception_type):
    return ExceptionRecord.create(workflow_id="wf", exception_type=exception_type)


def test_default_fallbacks():
    strategy = FallbackStrategy()
    assert strategy.fallback_for(make("timeout")) == "notify_owner"
    assert strategy.fallback_for(make("missing_resource")) == "use_default_resource"
    assert strategy.fallback_for(make("unknown")) == "escalate_to_human"


def test_override():
    strategy = FallbackStrategy(overrides={"timeout": "page_oncall"})
    assert strategy.fallback_for(make("timeout")) == "page_oncall"


def test_fallback_action():
    strategy = FallbackStrategy()
    exception = make("approval_failure")
    action = strategy.fallback_action(exception, actor="ops")
    assert action.action == "route_to_alternate_approver"
    assert action.status == "pending"
    assert action.metadata["strategy"] == "fallback"
    assert action.exception_id == exception.exception_id
