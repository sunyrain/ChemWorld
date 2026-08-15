#!/usr/bin/env python3
"""Materialize the finite DeepSeek A-S crystallization recovery inputs."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any

from chemworld.eval.provenance import write_json_atomic
from chemworld.eval.work_ii_constitutive_structural_qualification import (
    CRYSTALLIZATION_RESOURCE_DESIGN_VERSION,
    apply_crystallization_recovery_resource_design,
)

ROOT = Path(__file__).resolve().parents[1]
SOURCE_CONFIG = ROOT / (
    "workstreams/flagship_tasks/reports/"
    "work-ii-w2-26-deepseek-runtime-configs-v0.1/"
    "a_s--reaction-to-crystallization--r12.json"
)
SOURCE_PLAN = ROOT / "configs/benchmark/work_ii_deepseek_c2_prospective_v0.2.json"
EXPERIMENT_NOTE = (
    "workstreams/flagship_tasks/"
    "WORK_II_DEEPSEEK_AS_CRYSTALLIZATION_RESOURCE_RECOVERY_EXPERIMENT_NOTE.md"
)
DEFAULT_ROOT = ROOT / (
    "runs/formal_inputs/"
    "work-ii-deepseek-c2-as-crystallization-resource-recovery-v0.2"
)
DEFAULT_CONFIG = DEFAULT_ROOT / "a_s--reaction-to-crystallization--r12.json"
DEFAULT_PLAN = DEFAULT_ROOT / "execution_plan.json"


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def materialize(
    *,
    output_config: Path = DEFAULT_CONFIG,
) -> tuple[dict[str, Any], dict[str, Any]]:
    config = apply_crystallization_recovery_resource_design(_load(SOURCE_CONFIG))
    config["pilot_id"] = (
        "work-ii-reaction-to-crystallization-deepseek-v4-flash-"
        "thermal-resource-recovery-v0.1"
    )
    config["resource_design"] = {
        "version": CRYSTALLIZATION_RESOURCE_DESIGN_VERSION,
        "source_runtime_config": SOURCE_CONFIG.relative_to(ROOT).as_posix(),
        "scope": "participant_lab_resources_only",
        "provider_budget_semantics": "report_only_unlimited",
    }

    plan = copy.deepcopy(_load(SOURCE_PLAN))
    plan["cohort_id"] = (
        "work-ii-deepseek-c2-crystallization-resource-recovery-v0.3"
    )
    plan["experiment_note"] = EXPERIMENT_NOTE
    execution = plan.setdefault("execution", {})
    execution["resource_design_version"] = CRYSTALLIZATION_RESOURCE_DESIGN_VERSION
    execution["batch_replacement_semantics"] = (
        "participant_controlled_within_session_up_to_15_started_batches"
    )
    relative_config = output_config.resolve().relative_to(ROOT.resolve()).as_posix()
    matches = 0
    for block in plan.get("public_blocks", []):
        if block.get("block") != "A_S":
            continue
        for task in block.get("tasks", []):
            if task.get("task_id") == "reaction-to-crystallization":
                task["config"] = relative_config
                matches += 1
    if matches != 1:
        raise ValueError("source plan lacks one A-S crystallization task")
    return config, plan


def _write_once_or_same(path: Path, payload: dict[str, Any]) -> None:
    if path.is_file():
        if _load(path) != payload:
            raise FileExistsError(f"refusing to overwrite differing input: {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    write_json_atomic(path, payload)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    parser.add_argument("--output-config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--output-plan", type=Path, default=DEFAULT_PLAN)
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    output_config = args.output_config.resolve()
    output_plan = args.output_plan.resolve()
    for path in (output_config, output_plan):
        path.relative_to(ROOT.resolve())
    config, plan = materialize(output_config=output_config)
    if args.write:
        _write_once_or_same(output_config, config)
        _write_once_or_same(output_plan, plan)
    campaign = config["campaign"]
    print(
        json.dumps(
            {
                "status": "written" if args.write else "valid",
                "config": output_config.relative_to(ROOT).as_posix(),
                "plan": output_plan.relative_to(ROOT).as_posix(),
                "cohort_id": plan["cohort_id"],
                "complete_experiments_per_session": campaign["complete_experiments"],
                "maximum_started_batches_per_session": campaign[
                    "vessel_start_limit"
                ],
                "heat_limit": campaign["operation_repeat_limits"]["heat"],
                "cool_limit": campaign["operation_repeat_limits"][
                    "cool_crystallize"
                ],
                "provider_budget": plan["provider"]["resource_limits"],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
