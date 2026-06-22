from workflow_os.approval import ApprovalRequest, ParallelApprovalWorkflow


def make():
    return ApprovalRequest.create(
        workflow_id="wf",
        requester="alice",
        title="t",
        approvers=["manager", "finance", "legal"],
    )


def test_all_must_approve():
    wf = ParallelApprovalWorkflow(make())
    wf.approve("finance")
    wf.approve("legal")
    assert wf.request.state == "pending"
    wf.approve("manager")
    assert wf.request.state == "approved"


def test_any_rejection_rejects():
    wf = ParallelApprovalWorkflow(make())
    wf.approve("manager")
    wf.reject("legal")
    assert wf.request.state == "rejected"


def test_pending_approvers_tracks_responses():
    wf = ParallelApprovalWorkflow(make())
    wf.approve("manager")
    assert set(wf.pending_approvers) == {"finance", "legal"}


def test_threshold_allows_partial_approval():
    wf = ParallelApprovalWorkflow(make(), required_approvals=2)
    wf.approve("manager")
    wf.approve("finance")
    assert wf.request.state == "approved"
