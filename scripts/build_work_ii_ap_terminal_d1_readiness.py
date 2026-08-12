#!/usr/bin/env python3
"""Build/check outcome-blind static readiness for the two independent A-P D1 blocks."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.eval.provenance import write_json_atomic
from chemworld.eval.work_ii_ap_terminal_d1_readiness import (
    build_independent_ap_d1_readiness,
    validate_independent_ap_d1_readiness,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PLAN = ROOT / "configs/benchmark/work_ii_ap_terminal_d1_independent_plan_v0.1.json"
DEFAULT_OUTPUT = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "work-ii-ap-independent-terminal-d1-readiness-v0.1.json"
)


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _write_or_check(path: Path, value: dict[str, object], *, check: bool) -> None:
    if check:
        if not path.is_file() or _load(path) != value:
            raise RuntimeError(f"generated artifact is missing or stale: {path}")
    elif path.exists():
        if _load(path) != value:
            raise RuntimeError(f"refusing to overwrite a different artifact: {path}")
    else:
        write_json_atomic(path, value)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    plan_path = args.plan.resolve()
    plan = _load(plan_path)
    readiness, configs = build_independent_ap_d1_readiness(ROOT, plan_path)
    observed_configs: dict[str, dict[str, object]] = {}
    rows = {str(row["task_id"]): row for row in readiness["tasks"]}
    for candidate in plan["candidates"]:
        task_id = str(candidate["task_id"])
        output_value = rows[task_id]["output_config"]
        generated = configs.get(task_id)
        if generated is None:
            if output_value is not None:
                blocked_output = (ROOT / str(output_value)).resolve()
                if blocked_output.exists():
                    raise RuntimeError(
                        f"blocked A-P D1 must not have an output config: {blocked_output}"
                    )
            continue
        output = (ROOT / str(output_value)).resolve()
        _write_or_check(output, generated, check=bool(args.check))
        observed_configs[task_id] = _load(output)
    errors = validate_independent_ap_d1_readiness(
        ROOT, plan_path, readiness, observed_configs
    )
    if errors:
        raise RuntimeError("independent A-P D1 readiness validation failed: " + "; ".join(errors))
    _write_or_check(args.output.resolve(), readiness, check=bool(args.check))
    print(
        json.dumps(
            {
                "status": readiness["status"],
                "ready_task_count": readiness["ready_task_count"],
                "blocked_task_count": readiness["blocked_task_count"],
                "provider_call_count": readiness["provider_call_count"],
                "output": str(args.output.resolve()),
                "check": bool(args.check),
            },
            sort_keys=True,
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
