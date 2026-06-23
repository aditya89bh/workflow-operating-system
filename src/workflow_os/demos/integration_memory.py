"""Workflow + memory integration demonstration.

Shows the flow ``workflow -> memory -> retrieval``: a workflow is executed through
the memory recorder, every lifecycle event is persisted, and the history is then
retrieved by workflow, by actor, and as an execution timeline.
"""

from __future__ import annotations

from workflow_os.demos.employee_onboarding import build_workflow
from workflow_os.memory.history import get_execution_timeline
from workflow_os.memory.recorder import MemoryRecorder
from workflow_os.memory.retrieval import get_actor_history, get_workflow_history
from workflow_os.memory.sqlite_store import SQLiteMemoryStore


def run_demo() -> None:
    """Run the workflow-memory integration demonstration and print a summary."""
    workflow = build_workflow()

    # 1. Execute the workflow, recording organizational memory.
    print("1. workflow -> executing with the memory recorder")
    store = SQLiteMemoryStore(":memory:")
    MemoryRecorder(store).run(workflow)
    print(f"   {workflow.id!r} finished as {workflow.status.value!r}")

    # 2. Memory: every lifecycle change is persisted.
    print("\n2. memory -> events persisted")
    print(f"   total events stored: {len(store.list())}")

    # 3. Retrieval: query the recorded history different ways.
    print("\n3. retrieval -> querying the recorded history")
    history = get_workflow_history(store, workflow.id)
    print(f"   workflow history: {len(history)} events")

    it_history = get_actor_history(store, "it")
    print(f"   events attributed to 'it': {len(it_history)}")

    print("   execution timeline:")
    for entry in get_execution_timeline(store, workflow.id):
        step = entry.step_id or "-"
        print(f"     +{entry.offset_seconds:6.2f}s  {entry.event_type:<18} {step}")

    print("\ndone.")


if __name__ == "__main__":  # pragma: no cover
    run_demo()
