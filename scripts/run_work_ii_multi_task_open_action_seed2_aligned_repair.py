#!/usr/bin/env python3
"""Run the isolated seed-2 aligned open-action repair cell.

The original formal result is never overwritten. This launcher copies the frozen cell config,
reuses its truth/terminal contract, and records a separate repair result for sensitivity analysis.
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any

import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from work_ii_longitudinal_runtime import Progress, _run_one_cell  # noqa: E402
from chemworld.eval.provenance import canonical_json_sha256, write_json_atomic  # noqa: E402
from chemworld.eval.work_ii_longitudinal_action_readout import summarize_results  # noqa: E402


SOURCE_ROOT = ROOT / "runs/formal/work-ii-deepseek-multi-task-open-action-five-world-v0.1-20260817-formal2"
SOURCE_CELL_ID = "A_S_MULTI_TASK_OAD--reaction-to-crystallization--seed2--aligned_nominal"
REPAIR_CELL_ID = SOURCE_CELL_ID + "--repair1"


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def run(output_root: Path) -> dict[str, Any]:
    if output_root.exists() and any(output_root.iterdir()):
        raise RuntimeError(f"repair output already exists and will not be overwritten: {output_root}")
    output_root.mkdir(parents=True, exist_ok=True)

    manifest = _load(SOURCE_ROOT / "input_manifest.json")
    source_cell = next(
        (dict(cell) for cell in manifest["cells"] if cell["cell_id"] == SOURCE_CELL_ID),
        None,
    )
    if source_cell is None:
        raise RuntimeError(f"source cell not found: {SOURCE_CELL_ID}")

    source_config = SOURCE_ROOT / str(source_cell["campaign_config_path"])
    target_config = output_root / "input" / "campaign-config.json"
    target_config.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_config, target_config)

    cell = dict(source_cell)
    cell["cell_id"] = REPAIR_CELL_ID
    cell["campaign_config_path"] = target_config.relative_to(output_root).as_posix()
    write_json_atomic(
        output_root / "repair_manifest.json",
        {
            "schema_version": "chemworld-work-ii-open-action-seed2-aligned-repair-0.1",
            "source_root": SOURCE_ROOT.relative_to(ROOT).as_posix(),
            "source_cell_id": SOURCE_CELL_ID,
            "repair_cell_id": REPAIR_CELL_ID,
            "resource_profile": "resource_recovery_v2",
            "formal_preflight_sha256": manifest["formal_preflight_sha256"],
            "tested_commit": manifest["tested_commit"],
            "protocol_reused_without_change": True,
            "cell": cell,
        },
    )

    progress = Progress(output_root / "progress.jsonl")
    result = _run_one_cell(
        cell,
        output_root=output_root,
        phase="repair",
        progress=progress,
        cell_index=1,
        total_cells=1,
    )
    summary = summarize_results([result])
    summary.update(
        {
            "schema_version": "chemworld-work-ii-open-action-seed2-aligned-repair-summary-0.1",
            "source_cell_id": SOURCE_CELL_ID,
            "repair_cell_id": REPAIR_CELL_ID,
            "original_result_retained": True,
            "original_result_path": (
                SOURCE_ROOT / "formal/cells" / f"{SOURCE_CELL_ID}.json"
            ).relative_to(ROOT).as_posix(),
            "repair_result_path": (
                output_root / "repair/cells" / f"{REPAIR_CELL_ID}.json"
            ).relative_to(ROOT).as_posix(),
            "formal_preflight_sha256": manifest["formal_preflight_sha256"],
            "tested_commit": manifest["tested_commit"],
        }
    )
    summary["summary_sha256"] = canonical_json_sha256(summary)
    write_json_atomic(output_root / "repair_summary.json", summary)
    progress.emit(
        {
            "stage": "repair_complete",
            "source_cell_id": SOURCE_CELL_ID,
            "repair_cell_id": REPAIR_CELL_ID,
            "status": result.get("status"),
        }
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        type=Path,
        default=ROOT / "runs/formal/work-ii-multi-task-open-action-repair-v0.1-seed2-aligned-20260817",
    )
    args = parser.parse_args()
    output_root = args.output_root if args.output_root.is_absolute() else ROOT / args.output_root
    run(output_root.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

