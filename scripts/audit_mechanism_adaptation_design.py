"""Generate the fail-closed mechanism action/intervention design audit."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from chemworld.eval.mechanism_adaptation_execution import (
    DEFAULT_GATE_A_PLAN_PATH,
    DEFAULT_PROTOCOL_PATH,
    build_action_library,
    canonical_sha256,
    load_json_object,
)
from chemworld.eval.mechanism_design_audit import audit_mechanism_design

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = (
    ROOT / "workstreams/flagship_tasks/reports/mechanism-adaptation-design-audit-freeze-rc16.json"
)


def build_report(
    protocol_path: Path = DEFAULT_PROTOCOL_PATH,
    plan_path: Path = DEFAULT_GATE_A_PLAN_PATH,
) -> dict[str, Any]:
    protocol = load_json_object(protocol_path)
    plan = load_json_object(plan_path)
    action_plan = plan["action_library"]
    action_libraries = {
        str(task_id): build_action_library(
            str(task_id),
            action_count=int(action_plan["action_count_per_task"]),
            seed=int(action_plan["design_seed"]),
        )
        for task_id in protocol["design"]["tasks"]
    }
    report = audit_mechanism_design(
        protocol,
        plan,
        action_libraries=action_libraries,
    )
    report.update(
        {
            "protocol_path": protocol_path.resolve().relative_to(ROOT).as_posix(),
            "protocol_sha256": canonical_sha256(protocol),
            "gate_a_plan_path": plan_path.resolve().relative_to(ROOT).as_posix(),
            "gate_a_plan_sha256": canonical_sha256(plan),
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
    report = build_report(args.protocol, args.plan)
    if not args.check:
        if args.output.exists():
            raise FileExistsError(
                f"refusing to overwrite immutable design audit: {args.output}; "
                "select a new versioned --output path"
            )
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    print(json.dumps({"status": report["status"], "failures": report["failures"]}))
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
