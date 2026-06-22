"""Organizational learning demonstration.

Executes several workflows through the memory recorder, then runs the learning
pipeline over the recorded history: detect patterns, generate recommendations,
calculate organizational maturity, and produce a learning report. Everything is
deterministic and rule-based.
"""

from __future__ import annotations

from workflow_os.exception.record import ExceptionRecord
from workflow_os.learning.dashboard import organizational_dashboard
from workflow_os.learning.maturity import organizational_maturity_score
from workflow_os.learning.patterns import recurring_bottlenecks
from workflow_os.learning.reports import learning_report
from workflow_os.memory.recorder import MemoryRecorder
from workflow_os.memory.sqlite_store import SQLiteMemoryStore
from workflow_os.sop.record import SOPRecord, SOPStatus
from workflow_os.step import WorkflowStep
from workflow_os.workflow import Workflow


def _build_workflow(workflow_id: str, name: str) -> Workflow:
    return Workflow(
        id=workflow_id,
        name=name,
        steps=[
            WorkflowStep(id="collect", name="Collect documents"),
            WorkflowStep(id="review", name="Review", dependencies=["collect"]),
            WorkflowStep(id="finalize", name="Finalize", dependencies=["review"]),
        ],
    )


def _run_failing(recorder: MemoryRecorder, workflow_id: str, name: str) -> None:
    failing = _build_workflow(workflow_id, name)
    recorder.start(failing)
    first, second = failing.steps[0], failing.steps[1]
    recorder.start_step(failing, first)
    recorder.complete_step(failing, first)
    recorder.start_step(failing, second)
    recorder.fail_step(failing, second, reason="missing data")
    recorder.fail(failing, reason="review failed")


def run_demo() -> None:
    """Run the organizational learning demonstration and print a summary."""
    store = SQLiteMemoryStore(":memory:")
    recorder = MemoryRecorder(store)

    # 1. Execute workflows: "onboarding" succeeds repeatedly, "audit" struggles.
    for index in range(3):
        recorder.run(_build_workflow("onboarding", f"Onboarding run {index}"))
    recorder.run(_build_workflow("onboarding", "Onboarding run 3"))
    for index in range(3):
        _run_failing(recorder, "audit", f"Audit run {index}")

    records = store.list()
    print(f"1. executed workflows -> {len(records)} memory events recorded")

    # Supporting history from the other layers.
    sops = [
        SOPRecord.create(
            title="Onboarding SOP",
            workflow_type="onboarding",
            status=SOPStatus.ACTIVE.value,
        )
    ]
    exceptions = [
        ExceptionRecord.create(workflow_id="audit", exception_type="timeout")
        for _ in range(3)
    ]

    # 2 & 3. Analyze historical data and detect patterns.
    bottlenecks = recurring_bottlenecks(records, min_occurrences=2)
    print(
        "2-3. analyzed history; recurring bottlenecks: "
        + (", ".join(b.step_id for b in bottlenecks) or "none")
    )

    # 4. Generate recommendations and insights.
    report = learning_report(records, sops=sops, exceptions=exceptions)
    print(
        f"4. generated {len(report.insights)} insights and "
        f"{len(report.recommendations)} recommendations"
    )
    for recommendation in report.recommendations:
        print(
            f"   - [{recommendation.category}] {recommendation.title} "
            f"(severity={recommendation.severity})"
        )

    # 5. Calculate organizational maturity.
    maturity = organizational_maturity_score(records, sops=sops, exceptions=exceptions)
    print(f"5. organizational maturity: {maturity.overall:.2f} ({maturity.level})")
    for component, value in maturity.components.items():
        print(f"   - {component}: {value:.2f}")

    # 6. Generate dashboard / learning report summary.
    dashboard = organizational_dashboard(records, sops=sops, exceptions=exceptions)
    print("6. learning report summary:")
    print(f"   insights={report.summary['insight_count']}")
    print(f"   recommendations={report.summary['recommendation_count']}")
    print(f"   top successful: {dashboard['top_successful_workflows']}")
    print(f"   top failing: {dashboard['top_failing_workflows']}")


if __name__ == "__main__":  # pragma: no cover
    run_demo()
