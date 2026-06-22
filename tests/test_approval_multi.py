from workflow_os.approval import ApprovalRequest, MultiApproverWorkflow


def make(approvers):
    return ApprovalRequest.create(
        workflow_id="wf", requester="alice", title="t", approvers=list(approvers)
    )


def test_threshold_default_all():
    wf = MultiApproverWorkflow(make(["a", "b"]))
    assert wf.required_approvals == 2
    wf.approve("a")
    assert wf.request.state == "pending"
    wf.approve("b")
    assert wf.request.state == "approved"


def test_threshold_partial():
    wf = MultiApproverWorkflow(make(["a", "b", "c"]), required_approvals=2)
    wf.approve("a")
    assert wf.request.state == "pending"
    wf.approve("b")
    assert wf.request.state == "approved"


def test_rejection_makes_threshold_unreachable():
    wf = MultiApproverWorkflow(make(["a", "b", "c"]), required_approvals=2)
    wf.reject("a")
    assert wf.request.state == "pending"
    wf.reject("b")
    assert wf.request.state == "rejected"


def test_evaluate_does_not_mutate():
    wf = MultiApproverWorkflow(make(["a", "b"]))
    assert wf.evaluate() == "pending"
    assert wf.request.state == "pending"
