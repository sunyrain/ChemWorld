#!/usr/bin/env python3
"""Run the independent Codex autonomous donor cohort for W2-61."""

from __future__ import annotations

import argparse
import json
import time
from collections.abc import Mapping
from copy import deepcopy
from pathlib import Path
from typing import Any

from work_ii_longitudinal_runtime import Progress, _run_one_cell

from chemworld.eval.provenance import canonical_json_sha256, write_json_atomic
from chemworld.eval.work_ii_longitudinal_action_readout import summarize_results

ROOT = Path(__file__).resolve().parents[1]
CURRENT_PATH = ROOT / "configs/current.json"
NOTE_PATH = (
    "workstreams/flagship_tasks/"
    "WORK_II_W250_ACTION_ALIGNED_CAUSAL_EXTENSION_EXPERIMENT_NOTE.md"
)
DEFAULT_OUTPUT = (
    ROOT
    / "runs/development/"
    "work-ii-w2-61-codex-open-action-donors-v0.1-20260902"
)
EXPECTED_CELLS = 45
EXPECTED_EXPERIMENTS_PER_CELL = 12
MATCHED_CELL_KEYS = (
    "cell_id",
    "cluster_id",
    "task_id",
    "world_seed",
    "arm",
    "candidate_truth",
    "presented_candidate_ranks",
    "candidate_pool_ranks",
    "candidate_action_plan_sha256",
    "checkpoint_truth",
)


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain one object")
    return value


def _sha256_file(path: Path) -> str:
    import hashlib

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _binding(name: str) -> dict[str, Any]:
    current = _load(CURRENT_PATH)
    work_ii = current.get("work_ii")
    work_ii = work_ii if isinstance(work_ii, Mapping) else {}
    value = work_ii.get(name)
    if not isinstance(value, Mapping):
        raise ValueError(f"configs/current.json lacks Work II binding {name}")
    return deepcopy(dict(value))


def _validate_source_preparation() -> tuple[Path, dict[str, Any], dict[str, Any]]:
    codex_binding = _binding("w2_61_codex_open_action_preparation")
    source_root = ROOT / str(codex_binding["root"])
    source_manifest_path = ROOT / str(codex_binding["input_manifest"])
    if _sha256_file(source_manifest_path) != codex_binding.get("input_manifest_sha256"):
        raise RuntimeError("Codex provider-free preparation binding drifted")
    source = _load(source_manifest_path)
    if (
        source.get("cell_count") != EXPECTED_CELLS
        or source.get("participant") != "openai"
    ):
        raise ValueError("Codex provider-free preparation denominator drifted")
    source_cells = source.get("cells")
    if not isinstance(source_cells, list) or len(source_cells) != EXPECTED_CELLS:
        raise ValueError("Codex provider-free preparation lacks 45 cells")

    deepseek_binding = _binding("w2_50_open_action")
    deepseek = _load(ROOT / str(deepseek_binding["input_manifest"]))
    deepseek_cells = deepseek.get("cells")
    if not isinstance(deepseek_cells, list) or len(deepseek_cells) != EXPECTED_CELLS:
        raise ValueError("DeepSeek matched manifest lacks 45 cells")
    for codex_cell, deepseek_cell in zip(source_cells, deepseek_cells, strict=True):
        if not isinstance(codex_cell, Mapping) or not isinstance(deepseek_cell, Mapping):
            raise ValueError("matched manifest contains a malformed cell")
        for key in MATCHED_CELL_KEYS:
            if codex_cell.get(key) != deepseek_cell.get(key):
                raise ValueError(
                    "Codex and DeepSeek science surfaces differ for "
                    f"{codex_cell.get('cell_id')}: {key}"
                )
        codex_terminal = deepcopy(dict(codex_cell["terminal_action_readout"]))
        deepseek_terminal = deepcopy(dict(deepseek_cell["terminal_action_readout"]))
        for terminal in (codex_terminal, deepseek_terminal):
            terminal.pop("contract_sha256", None)
            terminal.pop("readout_id", None)
        if codex_terminal != deepseek_terminal:
            raise ValueError(
                "Codex and DeepSeek executable terminal contracts differ for "
                f"{codex_cell.get('cell_id')}"
            )
        codex_checkpoint_plan = deepcopy(dict(codex_cell["checkpoint_truth_plan"]))
        deepseek_checkpoint_plan = deepcopy(dict(deepseek_cell["checkpoint_truth_plan"]))
        for checkpoint_plan in (codex_checkpoint_plan, deepseek_checkpoint_plan):
            checkpoint_plan.pop("campaign_config_sha256", None)
            checkpoint_plan.pop("plan_sha256", None)
        if codex_checkpoint_plan != deepseek_checkpoint_plan:
            raise ValueError(
                "Codex and DeepSeek checkpoint truth plans differ for "
                f"{codex_cell.get('cell_id')}"
            )
        config_path = source_root / str(codex_cell["campaign_config_path"])
        config = _load(config_path)
        provider = config.get("provider")
        if not isinstance(provider, Mapping) or (
            provider.get("model") != "gpt-5.6-sol"
            or provider.get("reasoning_effort") != "medium"
        ):
            raise ValueError(f"{codex_cell['cell_id']}: Codex provider configuration drifted")
    return source_root, source, codex_binding


def materialize() -> dict[str, Any]:
    source_root, source, binding = _validate_source_preparation()
    cells = []
    for raw_cell in source["cells"]:
        cell = deepcopy(dict(raw_cell))
        cell["campaign_config_path"] = str(
            (source_root / str(raw_cell["campaign_config_path"])).resolve()
        )
        cells.append(cell)
    payload = {
        "schema_version": "chemworld-work-ii-w2-61-codex-donor-manifest-0.1",
        "study_id": "work-ii-w2-61-codex-open-action-donors-v0.1",
        "formal_result": False,
        "prospective_development_experiment": True,
        "experiment_note": NOTE_PATH,
        "participant": "openai",
        "model": "gpt-5.6-sol",
        "reasoning_effort": "medium",
        "scheduled_cell_count": EXPECTED_CELLS,
        "campaign_experiment_count_per_cell": EXPECTED_EXPERIMENTS_PER_CELL,
        "scheduled_participant_physical_experiments": (
            EXPECTED_CELLS * EXPECTED_EXPERIMENTS_PER_CELL
        ),
        "provider_free_truth_reused": True,
        "new_provider_free_truth_executions": 0,
        "source_preparation_binding": binding,
        "source_preparation_manifest_sha256": source["manifest_sha256"],
        "matched_deepseek_science_surface": True,
        "execution_order": [str(cell["cell_id"]) for cell in cells],
        "cells": cells,
    }
    payload["manifest_sha256"] = canonical_json_sha256(payload)
    return payload


def _write_once_or_match(path: Path, payload: Mapping[str, Any]) -> None:
    normalized = deepcopy(dict(payload))
    if path.is_file():
        if _load(path) != normalized:
            raise RuntimeError(f"retained W2-61 artifact differs: {path}")
        return
    write_json_atomic(path, normalized)


def _result_path(output_root: Path, cell_id: str) -> Path:
    return output_root / "formal/cells" / f"{cell_id}.json"


def _attempt_path(output_root: Path, cell_id: str) -> Path:
    return output_root / "attempts" / f"{cell_id}.json"


def _interrupted_result(cell: Mapping[str, Any], *, message: str) -> dict[str, Any]:
    result = {
        "schema_version": "chemworld-work-ii-w2-61-codex-donor-failure-0.1",
        "cell_id": str(cell["cell_id"]),
        "cluster_id": str(cell["cluster_id"]),
        "task_id": str(cell["task_id"]),
        "world_seed": int(cell["world_seed"]),
        "arm": str(cell["arm"]),
        "phase": "formal",
        "status": "failed_retained_process_or_platform",
        "failure_message": message,
        "campaign_complete_experiment_count": 0,
        "provider_call_count": 0,
    }
    result["result_sha256"] = canonical_json_sha256(result)
    return result


def execute(
    *,
    manifest: Mapping[str, Any],
    output_root: Path,
    progress: Progress,
) -> None:
    cells = manifest["cells"]
    completed = sum(_result_path(output_root, str(cell["cell_id"])).is_file() for cell in cells)
    started = time.perf_counter()
    for index, raw_cell in enumerate(cells, start=1):
        cell = dict(raw_cell)
        cell_id = str(cell["cell_id"])
        result_path = _result_path(output_root, cell_id)
        if result_path.is_file():
            continue
        attempt_path = _attempt_path(output_root, cell_id)
        if attempt_path.is_file():
            _write_once_or_match(
                result_path,
                _interrupted_result(
                    cell,
                    message="attempt marker exists without a terminal result; donor not relaunched",
                ),
            )
            completed += 1
            continue
        _write_once_or_match(
            attempt_path,
            {
                "schema_version": "chemworld-work-ii-w2-61-codex-donor-attempt-0.1",
                "manifest_sha256": manifest["manifest_sha256"],
                "cell_id": cell_id,
                "cell_index": index,
            },
        )
        try:
            _run_one_cell(
                cell,
                output_root=output_root,
                phase="formal",
                progress=progress,
                cell_index=index,
                total_cells=EXPECTED_CELLS,
            )
        except Exception as error:
            _write_once_or_match(
                result_path,
                _interrupted_result(
                    cell,
                    message=f"{type(error).__name__}: {error}",
                ),
            )
            progress.emit(
                {
                    "stage": "w2_61_codex_donor_failed_retained",
                    "cell_id": cell_id,
                    "cell": index,
                    "total_cells": EXPECTED_CELLS,
                    "failure_type": type(error).__name__,
                }
            )
        completed += 1
        elapsed = max(time.perf_counter() - started, 1.0e-9)
        rate = completed / elapsed
        progress.emit(
            {
                "stage": "w2_61_codex_donor_progress",
                "completed_cells": completed,
                "total_cells": EXPECTED_CELLS,
                "throughput_cells_per_hour": round(rate * 3600.0, 3),
                "eta_minutes": round((EXPECTED_CELLS - completed) / rate / 60.0, 1),
            }
        )


def analyze(*, manifest: Mapping[str, Any], output_root: Path) -> dict[str, Any]:
    results = []
    for cell in manifest["cells"]:
        path = _result_path(output_root, str(cell["cell_id"]))
        if path.is_file():
            results.append(_load(path))
    summary = summarize_results(results)
    summary.update(
        {
            "study_id": manifest["study_id"],
            "formal_result": False,
            "prospective_development_experiment": True,
            "experiment_note": NOTE_PATH,
            "participant": "openai",
            "model": "gpt-5.6-sol",
            "reasoning_effort": "medium",
            "execution_status": (
                "terminal_complete" if len(results) == EXPECTED_CELLS else "partial_retained"
            ),
            "scheduled_cell_count": EXPECTED_CELLS,
            "retained_cell_count": len(results),
            "scheduled_participant_physical_experiments": (
                EXPECTED_CELLS * EXPECTED_EXPERIMENTS_PER_CELL
            ),
            "new_provider_free_truth_executions": 0,
            "source_preparation_manifest_sha256": manifest[
                "source_preparation_manifest_sha256"
            ],
            "manifest_sha256": manifest["manifest_sha256"],
        }
    )
    summary["summary_sha256"] = canonical_json_sha256(
        {key: value for key, value in summary.items() if key != "summary_sha256"}
    )
    write_json_atomic(output_root / "summary.json", summary)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--materialize", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--analyze", action="store_true")
    parser.add_argument("--allow-provider-execution", action="store_true")
    args = parser.parse_args()
    if not (args.materialize or args.execute or args.analyze):
        parser.error("select at least one action")
    if args.execute and not args.allow_provider_execution:
        parser.error("provider execution requires --allow-provider-execution")
    output_root = args.output_root if args.output_root.is_absolute() else ROOT / args.output_root
    output_root.mkdir(parents=True, exist_ok=True)
    manifest = materialize()
    _write_once_or_match(output_root / "input_manifest.json", manifest)
    progress = Progress(output_root / "progress.jsonl")
    progress.emit(
        {
            "stage": "w2_61_codex_donors_materialized",
            "cells": EXPECTED_CELLS,
            "scheduled_physical_experiments": EXPECTED_CELLS
            * EXPECTED_EXPERIMENTS_PER_CELL,
            "provider_calls": 0,
            "new_truth_executions": 0,
        }
    )
    if args.execute:
        execute(manifest=manifest, output_root=output_root, progress=progress)
    if args.execute or args.analyze:
        summary = analyze(manifest=manifest, output_root=output_root)
        progress.emit(
            {
                "stage": "w2_61_codex_donors_analysis_complete",
                "execution_status": summary["execution_status"],
                "retained_cells": summary["retained_cell_count"],
                "eligible_cells": summary["eligible_cell_count"],
                "failed_or_ineligible_cells": summary["failed_or_ineligible_cell_count"],
                "physical_experiments": summary["participant_physical_experiment_count"],
            }
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
