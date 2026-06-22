from workflow_os.agents import MessageBus


def test_send_and_receive():
    bus = MessageBus()
    msg = bus.send("coord", "exec", "do task", subject="assign", metadata={"task": "t1"})
    assert msg.sender == "coord"
    assert msg.recipient == "exec"
    assert msg.metadata == {"task": "t1"}
    inbox = bus.receive("exec")
    assert len(inbox) == 1
    assert inbox[0].body == "do task"


def test_receive_only_addressed():
    bus = MessageBus()
    bus.send("a", "b", "1")
    bus.send("a", "c", "2")
    assert len(bus.receive("b")) == 1
    assert len(bus.receive("c")) == 1
    assert bus.receive("d") == []


def test_history_filters():
    bus = MessageBus()
    bus.send("a", "b", "1")
    bus.send("a", "c", "2")
    bus.send("b", "a", "3")
    assert len(bus.history(sender="a")) == 2
    assert len(bus.history(recipient="a")) == 1
    assert len(bus.history(sender="a", recipient="b")) == 1
    assert len(bus.all()) == 3
