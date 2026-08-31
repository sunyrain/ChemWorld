#!/usr/bin/env python3
"""Materialize the deterministic W2-59 cross-model execution configs."""

from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from chemworld.eval.provenance import write_json_atomic

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PLAN = (
    ROOT / "configs/benchmark/work_ii_cross_model_main_evidence_completion_v0.1.json"
)


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def _resolve(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def _openai_runtime_provider(
    source: dict[str, Any], provider: dict[str, Any]
) -> dict[str, Any]:
    result = deepcopy(source)
    for key in (
        "api_key_file",
        "model_catalog_json",
        "preferred_auth_method",
        "forced_login_method",
        "experimental_bearer_token",
    ):
        result.pop(key, None)
    result.update(deepcopy(provider))
    result["base_url"] = None
    result["env_key"] = None
    result["auth_mode"] = "none"
    return result


def build_outputs(plan_path: Path) -> dict[Path, dict[str, Any]]:
    plan = _load(plan_path)
    if (
        plan.get("schema_version")
        != "chemworld-work-ii-cross-model-main-evidence-completion-0.1"
        or plan.get("status") != "participant_execution_authorized"
    ):
        raise ValueError("W2-59 plan is not execution-authorized")
    note = _resolve(str(plan["experiment_note"]))
    if not note.is_file():
        raise ValueError("W2-59 experiment note is missing")
    provider = deepcopy(plan["providers"]["openai"])
    blocks = plan["blocks"]
    c2_block = blocks["public_c2_openai"]
    source_c2 = _load(_resolve(c2_block["source_plan"]))
    runtime_root = _resolve(c2_block["target_runtime_root"])
    outputs: dict[Path, dict[str, Any]] = {}
    target_c2 = deepcopy(source_c2)
    target_c2.update(
        {
            "schema_version": "chemworld-work-ii-c2-cross-model-replication-0.1",
            "cohort_id": "work-ii-c2-gpt56-sol-medium-replication-v0.1",
            "status": "public_execution_authorized",
            "provider": deepcopy(provider),
            "experiment_note": plan["experiment_note"],
        }
    )
    target_c2["private_block"] = None
    target_c2["expected_complete_totals"] = deepcopy(target_c2["expected_public_totals"])
    runtime_by_source: dict[Path, Path] = {}
    for block in target_c2["public_blocks"]:
        for task in block["tasks"]:
            source_path = _resolve(task["config"])
            source_runtime = _load(source_path)
            target_path = runtime_root / source_path.name
            target_runtime = deepcopy(source_runtime)
            target_runtime["provider"] = _openai_runtime_provider(
                source_runtime["provider"], provider
            )
            target_runtime["cross_model_replication"] = {
                "study_id": plan["study_id"],
                "source_runtime": source_path.relative_to(ROOT).as_posix(),
                "participant_provider": "openai",
                "model": provider["model"],
                "reasoning_effort": provider["reasoning_effort"],
            }
            outputs[target_path] = target_runtime
            runtime_by_source[source_path] = target_path
            task["config"] = target_path.relative_to(ROOT).as_posix()
    outputs[_resolve(c2_block["target_plan"])] = target_c2

    ap_block = blocks["matched_ap_openai"]
    ap = _load(_resolve(ap_block["source_protocol"]))
    ap.update(
        {
            "schema_version": (
                "chemworld-work-ii-study-b-matched-evidence-replication-protocol-0.1"
            ),
            "study_id": "work-ii-study-b-ap-gpt56-sol-medium-replication-v0.1",
            "status": "provider_execution_authorized",
            "experiment_note": plan["experiment_note"],
            "source_cohort": _resolve(c2_block["target_plan"]).relative_to(ROOT).as_posix(),
            "provider": deepcopy(provider),
        }
    )
    ap["loci"] = [deepcopy(ap["loci"][0])]
    ap_runtime_source = _resolve(ap["loci"][0]["runtime_config"])
    ap["loci"][0]["runtime_config"] = runtime_by_source[ap_runtime_source].relative_to(
        ROOT
    ).as_posix()
    ap["execution"]["formal_sessions"] = 15
    outputs[_resolve(ap_block["target_protocol"])] = ap

    b2_block = blocks["matched_as_b2_openai"]
    b2 = _load(_resolve(b2_block["source_protocol"]))
    b2.update(
        {
            "study_id": "work-ii-as-study-b2-gpt56-sol-medium-replication-v0.1",
            "status": "provider_execution_authorized",
            "experiment_note": plan["experiment_note"],
            "provider": deepcopy(provider),
        }
    )
    b2_runtime_source = _resolve(b2["runtime_config"])
    b2["runtime_config"] = runtime_by_source[b2_runtime_source].relative_to(ROOT).as_posix()
    outputs[_resolve(b2_block["target_protocol"])] = b2

    b3_block = blocks["b3_paired_successor"]
    for provider_name in ("deepseek", "openai"):
        source_key = f"source_{provider_name}_protocol"
        target_key = f"target_{provider_name}_protocol"
        b3 = _load(_resolve(b3_block[source_key]))
        b3.update(
            {
                "study_id": (
                    "work-ii-as-study-b3-main-evidence-successor-"
                    + ("deepseek" if provider_name == "deepseek" else "gpt56-sol-medium")
                    + "-v0.1"
                ),
                "status": "participant_execution_authorized",
                "experiment_note": plan["experiment_note"],
            }
        )
        b3["execution"]["canary_execution_authorized"] = True
        b3["execution"]["formal_execution_authorized"] = True
        outputs[_resolve(b3_block[target_key])] = b3

    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    plan_path = args.plan if args.plan.is_absolute() else ROOT / args.plan
    outputs = build_outputs(plan_path.resolve())
    mismatches: list[str] = []
    for path, payload in sorted(outputs.items(), key=lambda item: item[0].as_posix()):
        if args.write:
            path.parent.mkdir(parents=True, exist_ok=True)
            write_json_atomic(path, payload)
        elif not path.is_file() or _load(path) != payload:
            mismatches.append(path.relative_to(ROOT).as_posix())
    report = {
        "status": "written" if args.write else "passed" if not mismatches else "failed",
        "output_count": len(outputs),
        "mismatches": mismatches,
    }
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    return 0 if not mismatches else 1


if __name__ == "__main__":
    raise SystemExit(main())
