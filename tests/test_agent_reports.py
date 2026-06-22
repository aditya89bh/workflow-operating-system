from workflow_os.agents import (
    MessageBus,
    TaskDelegation,
    build_performance_report,
    workload_per_agent,
)


def setup_ledger():
    ledger = TaskDelegation()
    ledger.assign(workflow_id="wf", owner="a1", task_id="t1")
    ledger.assign(workflow_id="wf", owner="a1", task_id="t2")
    ledger.assign(workflow_id="wf", owner="a2", task_id="t3")
    ledger.transfer("t3", "a1")
    return ledger


def test_workload_per_agent():
    ledger = setup_ledger()
    counts = workload_per_agent(["a1", "a2"], ledger)
    assert counts == {"a1": 3, "a2": 0}


def test_build_performance_report():
    ledger = setup_ledger()
    bus = MessageBus()
    bus.send("a1", "a2", "status")
    report = build_performance_report(["a1", "a2"], ledger, bus)
    a1 = report.per_agent["a1"]
    assert a1.active_tasks == 3
    assert a1.transfers_in == 1
    assert a1.messages_sent == 1
    assert report.per_agent["a2"].messages_received == 1
    assert report.total_active_tasks == 3
    assert report.bottlenecks == ["a1"]


def test_no_bottleneck_when_balanced():
    ledger = TaskDelegation()
    ledger.assign(workflow_id="wf", owner="a1", task_id="t1")
    ledger.assign(workflow_id="wf", owner="a2", task_id="t2")
    report = build_performance_report(["a1", "a2"], ledger, MessageBus())
    assert report.bottlenecks == []
