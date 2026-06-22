"""Command-line interface for the workflow operating system.

Workflows are stored as individual JSON files inside a store directory (by
default ``./.workflow_store``). Each command loads, mutates, and saves a
workflow through the library API.

Available commands:

* ``create``   create a new workflow
* ``show``     print a workflow as JSON
* ``list``     list stored workflows
* ``start``    start a draft/ready workflow
* ``pause``    pause a running workflow
* ``resume``   resume a paused workflow
* ``complete`` complete a workflow whose required steps are done
"""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

from workflow_os.executor import WorkflowExecutor
from workflow_os.fileio import export_workflow, import_workflow
from workflow_os.operations import (
    complete_workflow,
    pause_workflow,
    resume_workflow,
    start_workflow,
)
from workflow_os.persistence import workflow_to_json
from workflow_os.step import WorkflowStep
from workflow_os.transitions import StepStatus, transition_step
from workflow_os.workflow import Workflow

DEFAULT_STORE = ".workflow_store"
DEFAULT_DEMO_WORKFLOW = "examples/employee_onboarding.json"


def _store_dir(args: argparse.Namespace) -> Path:
    path = Path(args.store)
    path.mkdir(parents=True, exist_ok=True)
    return path


def _path_for(store: Path, workflow_id: str) -> Path:
    return store / f"{workflow_id}.json"


def _parse_step(raw: str) -> WorkflowStep:
    step_id, _, name = raw.partition(":")
    step_id = step_id.strip()
    name = name.strip() or step_id
    return WorkflowStep(id=step_id, name=name)


def cmd_create(args: argparse.Namespace) -> int:
    store = _store_dir(args)
    workflow = Workflow(
        id=args.id,
        name=args.name,
        description=args.description or "",
        steps=[_parse_step(step) for step in (args.step or [])],
    )
    export_workflow(workflow, _path_for(store, workflow.id))
    print(f"created workflow {workflow.id!r} with {len(workflow.steps)} step(s)")
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    store = _store_dir(args)
    workflow = import_workflow(_path_for(store, args.id))
    print(workflow_to_json(workflow))
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    store = _store_dir(args)
    files = sorted(store.glob("*.json"))
    if not files:
        print("no workflows found")
        return 0
    for path in files:
        workflow = import_workflow(path)
        print(f"{workflow.id}\t{workflow.status.value}\t{workflow.name}")
    return 0


def _apply(args: argparse.Namespace, operation) -> int:
    store = _store_dir(args)
    path = _path_for(store, args.id)
    workflow = import_workflow(path)
    operation(workflow)
    export_workflow(workflow, path)
    print(f"workflow {workflow.id!r} is now {workflow.status.value!r}")
    return 0


def cmd_start(args: argparse.Namespace) -> int:
    return _apply(args, start_workflow)


def cmd_pause(args: argparse.Namespace) -> int:
    return _apply(args, pause_workflow)


def cmd_resume(args: argparse.Namespace) -> int:
    return _apply(args, resume_workflow)


def cmd_complete(args: argparse.Namespace) -> int:
    return _apply(args, complete_workflow)


def cmd_memory_demo(args: argparse.Namespace) -> int:
    from workflow_os.memory.demo import run_demo

    run_demo()
    return 0


def cmd_decision_demo(args: argparse.Namespace) -> int:
    from workflow_os.decision.demo import run_demo

    run_demo()
    return 0


def cmd_sop_demo(args: argparse.Namespace) -> int:
    from workflow_os.sop.demo import run_demo

    run_demo()
    return 0


def cmd_approval_demo(args: argparse.Namespace) -> int:
    from workflow_os.approval.demo import run_demo

    run_demo()
    return 0


def cmd_exception_demo(args: argparse.Namespace) -> int:
    from workflow_os.exception.demo import run_demo

    run_demo()
    return 0


def cmd_multi_agent_demo(args: argparse.Namespace) -> int:
    from workflow_os.agents.demo import run_demo

    run_demo()
    return 0


def cmd_analytics_demo(args: argparse.Namespace) -> int:
    from workflow_os.analytics.demo import run_demo

    run_demo()
    return 0


def cmd_demo(args: argparse.Namespace) -> int:
    workflow = import_workflow(args.workflow)
    print(f"running workflow {workflow.name!r} ({workflow.id})")

    order = WorkflowExecutor(workflow).execution_order()
    start_workflow(workflow)
    for step in order:
        transition_step(step, StepStatus.RUNNING)
        transition_step(step, StepStatus.COMPLETED)
        print(f"  done: {step.id} - {step.name}")

    complete_workflow(workflow)
    print(f"workflow {workflow.id!r} finished with status {workflow.status.value!r}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="workflow-os",
        description="Model, validate, and execute workflows.",
    )
    parser.add_argument(
        "--store",
        default=DEFAULT_STORE,
        help=f"directory used to store workflows (default: {DEFAULT_STORE})",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    create = sub.add_parser("create", help="create a new workflow")
    create.add_argument("--id", required=True, help="unique workflow id")
    create.add_argument("--name", required=True, help="workflow name")
    create.add_argument("--description", help="workflow description")
    create.add_argument(
        "--step",
        action="append",
        metavar="ID:NAME",
        help="add a step (repeatable)",
    )
    create.set_defaults(func=cmd_create)

    show = sub.add_parser("show", help="print a workflow as JSON")
    show.add_argument("id", help="workflow id")
    show.set_defaults(func=cmd_show)

    list_cmd = sub.add_parser("list", help="list stored workflows")
    list_cmd.set_defaults(func=cmd_list)

    for name, func, help_text in (
        ("start", cmd_start, "start a draft/ready workflow"),
        ("pause", cmd_pause, "pause a running workflow"),
        ("resume", cmd_resume, "resume a paused workflow"),
        ("complete", cmd_complete, "complete a workflow"),
    ):
        action = sub.add_parser(name, help=help_text)
        action.add_argument("id", help="workflow id")
        action.set_defaults(func=func)

    demo = sub.add_parser("demo", help="run an example workflow end to end")
    demo.add_argument(
        "--workflow",
        default=DEFAULT_DEMO_WORKFLOW,
        help=f"workflow JSON file to run (default: {DEFAULT_DEMO_WORKFLOW})",
    )
    demo.set_defaults(func=cmd_demo)

    memory_demo = sub.add_parser(
        "memory-demo", help="run the organizational memory demonstration"
    )
    memory_demo.set_defaults(func=cmd_memory_demo)

    decision_demo = sub.add_parser(
        "decision-demo", help="run the decision intelligence demonstration"
    )
    decision_demo.set_defaults(func=cmd_decision_demo)

    sop_demo = sub.add_parser(
        "sop-demo", help="run the SOP memory demonstration"
    )
    sop_demo.set_defaults(func=cmd_sop_demo)

    approval_demo = sub.add_parser(
        "approval-demo", help="run the approval system demonstration"
    )
    approval_demo.set_defaults(func=cmd_approval_demo)

    exception_demo = sub.add_parser(
        "exception-demo", help="run the exception handling demonstration"
    )
    exception_demo.set_defaults(func=cmd_exception_demo)

    multi_agent_demo = sub.add_parser(
        "multi-agent-demo", help="run the multi-agent collaboration demonstration"
    )
    multi_agent_demo.set_defaults(func=cmd_multi_agent_demo)

    analytics_demo = sub.add_parser(
        "analytics-demo", help="run the workflow analytics demonstration"
    )
    analytics_demo.set_defaults(func=cmd_analytics_demo)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
