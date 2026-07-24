"""Generate the fail-closed mechanism action/intervention design audit."""

from __future__ import annotations

import argparse
import json
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any

from chemworld.agents.task_recipes import DIAGNOSTIC_RECIPE_DESIGN_V1
from chemworld.eval.mechanism_adaptation_execution import (
    DEFAULT_GATE_A_PLAN_PATH,
    DEFAULT_PROTOCOL_PATH,
    build_action_library,
    canonical_sha256,
    load_json_object,
    load_protocol_object,
)
from chemworld.eval.mechanism_design_audit import audit_mechanism_design
from chemworld.eval.mechanism_relation_graph import (
    validate_diagnostic_relation_graph,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = (
    ROOT / "workstreams/flagship_tasks/reports/mechanism-adaptation-design-audit-freeze-rc23.json"
)


def build_report(
    protocol_path: Path = DEFAULT_PROTOCOL_PATH,
    plan_path: Path = DEFAULT_GATE_A_PLAN_PATH,
    *,
    progress_callback: Callable[[Mapping[str, Any]], None] | None = None,
) -> dict[str, Any]:
    protocol = load_protocol_object(protocol_path)
    plan = load_json_object(plan_path)
    relation_graph_path = ROOT / plan["diagnostic_relation_graph"]["report"]
    relation_graph = load_json_object(relation_graph_path)
    relation_graph_errors = validate_diagnostic_relation_graph(
        protocol,
        plan,
        relation_graph,
    )
    if relation_graph_errors:
        raise ValueError(
            "invalid diagnostic relation graph: "
            + "; ".join(relation_graph_errors)
        )
    action_plan = plan["action_library"]
    action_libraries = {
        str(task_id): build_action_library(
            str(task_id),
            action_count=int(action_plan["action_count_per_task"]),
            seed=int(action_plan["design_seed"]),
            design_id=str(
                action_plan.get("design", DIAGNOSTIC_RECIPE_DESIGN_V1)
            ),
        )
        for task_id in protocol["design"]["tasks"]
    }
    report = audit_mechanism_design(
        protocol,
        plan,
        action_libraries=action_libraries,
        progress_callback=progress_callback,
    )
    report.update(
        {
            "protocol_path": protocol_path.resolve().relative_to(ROOT).as_posix(),
            "protocol_sha256": canonical_sha256(protocol),
            "gate_a_plan_path": plan_path.resolve().relative_to(ROOT).as_posix(),
            "gate_a_plan_sha256": canonical_sha256(plan),
            "diagnostic_relation_graph_path": (
                relation_graph_path.resolve().relative_to(ROOT).as_posix()
            ),
            "diagnostic_relation_graph_sha256": relation_graph[
                "graph_sha256"
            ],
        }
    )
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL_PATH)
    parser.add_argument("--plan", type=Path, default=DEFAULT_GATE_A_PLAN_PATH)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Run the audit without rewriting its report.",
    )
    args = parser.parse_args()
    report = build_report(
        args.protocol,
        args.plan,
        progress_callback=lambda event: print(
            json.dumps(dict(event), sort_keys=True),
            flush=True,
        ),
    )
    if args.output.exists():
        recorded = json.loads(args.output.read_text(encoding="utf-8"))
        if recorded != report:
            raise FileExistsError(
                f"immutable design audit differs from current execution: "
                f"{args.output}; select a new versioned --output path"
            )
    elif not args.check:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    else:
        raise FileNotFoundError(f"missing immutable design audit: {args.output}")
    print(json.dumps({"status": report["status"], "failures": report["failures"]}))
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
