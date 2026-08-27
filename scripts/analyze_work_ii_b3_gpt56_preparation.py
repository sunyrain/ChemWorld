#!/usr/bin/env python
# ruff: noqa: RUF001
"""Verify and close out provider-free GPT-5.6-sol B3 preparation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from chemworld.eval.provenance import canonical_json_sha256, write_json_atomic

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DEEPSEEK_ROOT = ROOT / (
    "runs/formal/"
    "work-ii-as-study-b3-identifiable-law-action-v0.2-20260827-restart1"
)
DEFAULT_GPT_ROOT = ROOT / (
    "runs/formal/"
    "work-ii-as-study-b3-gpt56-sol-medium-replication-v0.1-20260827-restart1"
)
DEFAULT_JSON_OUTPUT = ROOT / (
    "workstreams/flagship_tasks/reports/"
    "work-ii-as-study-b3-gpt56-sol-medium-preparation-v0.1.json"
)
DEFAULT_REPORT_OUTPUT = ROOT / (
    "workstreams/flagship_tasks/reports/"
    "WORK_II_AS_STUDY_B3_GPT56_SOL_MEDIUM_PREPARATION_ZH.md"
)


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected a JSON object: {path}")
    return value


def _without(value: dict[str, Any], *keys: str) -> dict[str, Any]:
    return {key: item for key, item in value.items() if key not in keys}


def _truth_file_roster(root: Path) -> list[str]:
    truth_root = root / "truth"
    return [
        path.relative_to(truth_root).as_posix()
        for path in sorted(truth_root.rglob("*.json"))
    ]


def _scientific_cells(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    return sorted(
        (_without(dict(cell), "study_id") for cell in manifest["cells"]),
        key=lambda cell: str(cell["cell_id"]),
    )


def _has_participant_results(root: Path) -> bool:
    return any(
        path.is_file()
        for directory in (root / "canary", root / "cells")
        if directory.is_dir()
        for path in directory.rglob("*.json")
    )


def _write_report(summary: dict[str, Any], path: Path) -> None:
    counts = summary["preparation_counts"]
    checks = summary["cross_provider_equivalence"]
    static = summary["gpt_static_harness"]
    lines = [
        "# Work II A-S Study B3 GPT-5.6-sol medium provider-free 准备收束",
        "",
        f"状态：`{summary['status']}`。GPT participant calls 为 `0`，physical experiments "
        "为 `0`；canary 与 formal session 均未启动。",
        "",
        "## 已准备的冻结表面",
        "",
        f"- 5 个 development worlds；candidate-grid truth executions "
        f"`{counts['candidate_grid_truth_execution_count']}`。",
        f"- exponent-grid 共评估 `{counts['exponent_grid_evaluated_target_count']}` 个 target，"
        f"其中 `{counts['exponent_grid_truth_execution_count']}` 个新 truth executions、"
        f"`{counts['exponent_grid_reused_target_truth_count']}` 个复用 target truth。",
        f"- 5 个 public worlds；public truth executions "
        f"`{counts['public_truth_execution_count']}`；action-opportunity eligible "
        f"`{counts['action_opportunity_eligible_world_count']}/5`。",
        f"- input manifest 为 `{counts['cell_count']}` cells = 5 worlds × 3 arms × "
        f"{counts['replicates_per_arm']} independent sessions；replicate blocks "
        f"`{counts['replicate_block_count']}`。",
        "",
        "## 与 DeepSeek v0.2 的等价性",
        "",
        "| surface | exact scientific match |",
        "|---|---:|",
        f"| frozen roster | {checks['roster_exact']} |",
        f"| qualification science fields | {checks['qualification_science_exact']} |",
        f"| public worlds and truth | {checks['public_truth_exact']} |",
        f"| truth file roster | {checks['truth_file_roster_exact']} |",
        f"| cluster packets | {checks['cluster_packets_exact']} |",
        f"| cell packets, scoring truth and hidden ranks | {checks['cells_science_exact']} |",
        "",
        "## GPT harness",
        "",
        f"模型固定为 `{static['model']}`、reasoning effort `{static['reasoning_effort']}`；"
        f"Responses transport、cached ChatGPT login、Codex CLI 与 disabled-tool command "
        f"contract 均 ready=`{static['ready']}`。static provider calls=`0`。",
        "",
        "## 执行边界",
        "",
        "本工作包只授权 provider-free preparation。当前 participant execution 保持 blocked："
        "不运行 canary，不运行 30-session formal block，也不把 DeepSeek canary 的单个 completed "
        "cell 作为跨模型科学结果。未来如单独授权 GPT participant execution，必须从这套冻结的 "
        "30-cell manifest 开始，并保留独立 provider receipts 与所有失败。",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--deepseek-root", type=Path, default=DEFAULT_DEEPSEEK_ROOT)
    parser.add_argument("--gpt-root", type=Path, default=DEFAULT_GPT_ROOT)
    parser.add_argument("--json-output", type=Path, default=DEFAULT_JSON_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT_OUTPUT)
    args = parser.parse_args()

    deepseek_root = args.deepseek_root.resolve()
    gpt_root = args.gpt_root.resolve()
    deepseek = {
        name: _load(deepseek_root / name)
        for name in (
            "frozen_roster.json",
            "qualification_summary.json",
            "public_truth_manifest.json",
            "input_manifest.json",
            "provider_static_check.json",
        )
    }
    gpt = {
        name: _load(gpt_root / name)
        for name in (
            "frozen_roster.json",
            "qualification_summary.json",
            "public_truth_manifest.json",
            "input_manifest.json",
            "provider_static_check.json",
        )
    }

    deepseek_manifest = deepseek["input_manifest.json"]
    gpt_manifest = gpt["input_manifest.json"]
    deepseek_qualification = deepseek["qualification_summary.json"]
    gpt_qualification = gpt["qualification_summary.json"]
    deepseek_public = deepseek["public_truth_manifest.json"]
    gpt_public = gpt["public_truth_manifest.json"]
    gpt_static = gpt["provider_static_check.json"]

    equivalence = {
        "roster_exact": deepseek["frozen_roster.json"] == gpt["frozen_roster.json"],
        "qualification_science_exact": _without(
            deepseek_qualification, "study_id", "qualification_sha256"
        )
        == _without(gpt_qualification, "study_id", "qualification_sha256"),
        "public_truth_exact": _without(
            deepseek_public, "study_id", "public_truth_sha256"
        )
        == _without(gpt_public, "study_id", "public_truth_sha256"),
        "truth_file_roster_exact": _truth_file_roster(deepseek_root)
        == _truth_file_roster(gpt_root),
        "cluster_packets_exact": deepseek_manifest["cluster_packets"]
        == gpt_manifest["cluster_packets"],
        "cells_science_exact": _scientific_cells(deepseek_manifest)
        == _scientific_cells(gpt_manifest),
    }
    static_ready = (
        gpt_static.get("ready") is True
        and gpt_static.get("model") == "gpt-5.6-sol"
        and gpt_static.get("reasoning_effort") == "medium"
        and gpt_static.get("wire_api") == "responses"
        and gpt_static.get("cached_chatgpt_login_verified") is True
        and gpt_static.get("command_contract_ready") is True
        and int(gpt_static.get("provider_calls", -1)) == 0
    )
    expected_counts = (
        int(gpt_manifest["cell_count"]) == 30
        and int(gpt_manifest["cluster_count"]) == 5
        and int(gpt_manifest["replicates_per_arm"]) == 2
        and int(gpt_qualification["provider_call_count"]) == 0
        and int(gpt_public["provider_call_count"]) == 0
        and not _has_participant_results(gpt_root)
    )
    if not all(equivalence.values()):
        mismatches = sorted(key for key, matched in equivalence.items() if not matched)
        raise ValueError(
            "GPT and DeepSeek scientific preparation surfaces differ: "
            + ", ".join(mismatches)
        )
    if not static_ready or not expected_counts:
        raise ValueError("GPT preparation is not ready, zero-call, and participant-free")

    exponent_truth = int(gpt_qualification["exponent_grid_truth_execution_count"])
    exponent_reused = int(
        gpt_qualification["exponent_grid_reused_target_truth_count"]
    )
    summary: dict[str, Any] = {
        "schema_version": "chemworld-work-ii-b3-gpt56-preparation-closeout-0.1",
        "status": "provider_free_ready_participant_execution_blocked",
        "formal_result": False,
        "participant_execution_authorized": False,
        "provider_call_count": 0,
        "participant_session_count": 0,
        "participant_physical_experiment_count": 0,
        "gpt_static_harness": {
            "provider_id": gpt_static["provider_id"],
            "model": gpt_static["model"],
            "reasoning_effort": gpt_static["reasoning_effort"],
            "wire_api": gpt_static["wire_api"],
            "auth_mode": gpt_static["auth_mode"],
            "cached_chatgpt_login_verified": gpt_static[
                "cached_chatgpt_login_verified"
            ],
            "codex_cli_available": gpt_static["codex_cli_available"],
            "command_contract_ready": gpt_static["command_contract_ready"],
            "ready": gpt_static["ready"],
        },
        "preparation_counts": {
            "development_world_count": int(
                gpt_qualification["development_world_count"]
            ),
            "candidate_grid_truth_execution_count": int(
                gpt_qualification["linear_and_power_truth_execution_count"]
            ),
            "exponent_grid_truth_execution_count": exponent_truth,
            "exponent_grid_reused_target_truth_count": exponent_reused,
            "exponent_grid_evaluated_target_count": exponent_truth + exponent_reused,
            "public_world_count": int(gpt_public["public_world_count"]),
            "public_truth_execution_count": int(
                gpt_public["linear_and_power_truth_execution_count"]
            ),
            "action_opportunity_eligible_world_count": int(
                gpt_public["action_opportunity_eligible_world_count"]
            ),
            "failed_public_world_count": int(
                gpt_public["failed_public_world_count"]
            ),
            "cell_count": int(gpt_manifest["cell_count"]),
            "cluster_count": int(gpt_manifest["cluster_count"]),
            "replicate_block_count": int(gpt_manifest["replicate_block_count"]),
            "replicates_per_arm": int(gpt_manifest["replicates_per_arm"]),
            "scoring_term_count": int(gpt_manifest["scoring_term_count"]),
        },
        "cross_provider_equivalence": equivalence,
        "deepseek_static_ready": deepseek["provider_static_check.json"].get("ready")
        is True,
        "canary_session_count": 0,
        "formal_session_count": 0,
        "scheduled_future_formal_session_count": int(gpt_manifest["cell_count"]),
    }
    summary["summary_sha256"] = canonical_json_sha256(summary)
    write_json_atomic(args.json_output.resolve(), summary)
    _write_report(summary, args.report_output.resolve())
    print(
        json.dumps(
            {
                "status": summary["status"],
                "cell_count": summary["preparation_counts"]["cell_count"],
                "equivalence_checks": sum(equivalence.values()),
                "provider_calls": summary["provider_call_count"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
