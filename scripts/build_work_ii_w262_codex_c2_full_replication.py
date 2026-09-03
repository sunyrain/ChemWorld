#!/usr/bin/env python3
"""Build the W2-62 full-cohort Codex C2 replication inputs."""

from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from chemworld.eval.provenance import write_json_atomic

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PLAN = ROOT / "configs/benchmark/work_ii_deepseek_c2_prospective_v0.2.json"
SOURCE_PROVIDER_PLAN = (
    ROOT / "configs/benchmark/work_ii_cross_model_main_evidence_completion_v0.1.json"
)
TARGET_PLAN = ROOT / "configs/benchmark/work_ii_c2_codex_full_replication_v0.1.json"
TARGET_RUNTIME_ROOT = (
    ROOT / "configs/benchmark/work_ii_c2_codex_full_replication_runtime_v0.1"
)
NOTE_PATH = (
    "workstreams/flagship_tasks/"
    "WORK_II_W262_CODEX_C2_FULL_REPLICATION_EXPERIMENT_NOTE.md"
)
STUDY_ID = "work-ii-w2-62-codex-c2-full-replication-v0.1"
COHORT_ID = "work-ii-c2-codex-full-replication-v0.1"


def _load(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected JSON object: {path}")
    return payload


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


def build_outputs() -> dict[Path, dict[str, Any]]:
    if not (ROOT / NOTE_PATH).is_file():
        raise FileNotFoundError("W2-62 experiment note is missing")
    source_plan = _load(SOURCE_PLAN)
    provider_plan = _load(SOURCE_PROVIDER_PLAN)
    provider = deepcopy(provider_plan["providers"]["openai"])
    if (
        provider.get("model") != "gpt-5.6-sol"
        or provider.get("reasoning_effort") != "medium"
    ):
        raise ValueError("W2-62 provider surface drifted")

    target_plan = deepcopy(source_plan)
    target_plan.update(
        {
            "schema_version": "chemworld-work-ii-c2-cross-model-replication-0.1",
            "cohort_id": COHORT_ID,
            "status": "public_execution_authorized",
            "provider": provider,
            "experiment_note": NOTE_PATH,
            "full_cohort_successor": {
                "study_id": STUDY_ID,
                "source_deepseek_plan": SOURCE_PLAN.relative_to(ROOT).as_posix(),
                "historical_w2_59_canary_reused": False,
                "fresh_sessions": 135,
                "planned_complete_experiments": 1260,
            },
        }
    )
    target_plan["private_block"] = None
    target_plan["expected_complete_totals"] = deepcopy(
        target_plan["expected_public_totals"]
    )

    outputs: dict[Path, dict[str, Any]] = {}
    for block in target_plan["public_blocks"]:
        for task in block["tasks"]:
            source_path = ROOT / str(task["config"])
            source_runtime = _load(source_path)
            target_path = TARGET_RUNTIME_ROOT / source_path.name
            target_runtime = deepcopy(source_runtime)
            target_runtime["provider"] = _openai_runtime_provider(
                source_runtime["provider"], provider
            )
            target_runtime["cross_model_replication"] = {
                "study_id": STUDY_ID,
                "cohort_id": COHORT_ID,
                "source_runtime": source_path.relative_to(ROOT).as_posix(),
                "participant_provider": "openai",
                "model": "gpt-5.6-sol",
                "reasoning_effort": "medium",
                "historical_w2_59_canary_reused": False,
            }
            task["config"] = target_path.relative_to(ROOT).as_posix()
            outputs[target_path] = target_runtime
    outputs[TARGET_PLAN] = target_plan
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    outputs = build_outputs()
    mismatches = []
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
