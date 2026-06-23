"""Workflow + organizational learning integration demonstration.

Shows the flow ``workflow -> insights -> recommendations -> maturity``: a body of
workflow history is built (reliable and struggling workflows), then insights,
improvement recommendations, and an organizational maturity score are derived.
"""

from __future__ import annotations

from workflow_os.demos.procurement import build_workflow
from workflow_os.learning.maturity import organizational_maturity_score
from workflow_os.learning.reports import learning_report
from workflow_os.memory.recorder import MemoryRecorder
from workflow_os.memory.sqlite_store import SQLiteMemoryStore


def _run_failing(recorder: MemoryRecorder, workflow_id: str) -> None:
    workflow = build_workflow()
    workflow.id = workflow_id
    recorder.start(workflow)
    first = workflow.steps[0]
    recorder.start_step(workflow, first)
    recorder.fail_step(workflow, first, reason="budget rejected")
    recorder.fail(workflow, reason="request denied")


def run_demo() -> None:
    """Run the workflow-learning integration demonstration and print a summary."""
    store = SQLiteMemoryStore(":memory:")
    recorder = MemoryRecorder(store)

    # 1. Workflow: build a body of history (a reliable and a struggling workflow).
    print("1. workflow -> building history")
    for _ in range(4):
        workflow = build_workflow()
        workflow.id = "procurement-reliable"
        recorder.run(workflow)
    for _ in range(3):
        _run_failing(recorder, "procurement-flaky")
    records = store.list()
    print(f"   recorded {len(records)} events")

    # 2. Insights: observe what the history reveals.
    report = learning_report(records)
    print("\n2. insights -> observations")
    for insight in report.insights:
        print(f"   [{insight.category}] {insight.title}")

    # 3. Recommendations: deterministic improvement suggestions.
    print("\n3. recommendations -> improvements")
    for recommendation in report.recommendations:
        print(
            f"   [{recommendation.category}] {recommendation.title} "
            f"(severity={recommendation.severity})"
        )

    # 4. Maturity: a single composite score.
    print("\n4. maturity -> composite score")
    maturity = organizational_maturity_score(records)
    print(f"   maturity: {maturity.overall:.2f} ({maturity.level})")
    for component, value in maturity.components.items():
        print(f"     - {component}: {value:.2f}")

    print("\ndone.")


if __name__ == "__main__":  # pragma: no cover
    run_demo()
