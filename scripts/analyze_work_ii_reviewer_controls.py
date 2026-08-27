#!/usr/bin/env python
"""Generate provider-free Work II reviewer control analyses."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

from chemworld.eval.provenance import canonical_json_sha256, write_json_atomic
from chemworld.eval.work_ii_reviewer_controls import (
    CONTROL_SCHEMA_VERSION,
    analyze_schema_capacity,
    analyze_w2_50,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_W2 = ROOT / (
    "runs/formal/work-ii-deepseek-multi-task-open-action-five-world-v0.1-"
    "20260817-formal2/summary.json"
)
DEFAULT_EVALUATOR = ROOT / (
    "runs/formal/work-ii-deepseek-c2-current-composite-evaluator-v0.2-20260815"
)
DEFAULT_JSON = ROOT / (
    "workstreams/flagship_tasks/reports/work-ii-reviewer-control-analyses-v0.1.json"
)
DEFAULT_MD = ROOT / (
    "workstreams/flagship_tasks/reports/WORK_II_REVIEWER_CONTROL_ANALYSES_ZH.md"
)


def _read(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def _report(payload: dict[str, Any]) -> str:
    action = payload["w2_50_continuous_action"]
    schema = payload["typed_law_schema_capacity"]
    aggregate = schema["aggregate"]
    means = aggregate["cell_weighted_mean"]
    lines = [
        "# Work II reviewer control analyses",
        "",
        "## Denominators",
        "",
        f"- W2-50: {action['eligible_cell_count']}/{action['scheduled_cell_count']} eligible; "
        f"{action['retained_failure_count']} retained failures.",
        f"- Typed-law capacity: {schema['completed_cell_count']}/{schema['scheduled_cell_count']} "
        f"cells completed; {schema['failed_cell_count']} analysis failures; provider calls 0.",
        "",
        "## Continuous law--action relation",
        "",
    ]
    overall = action["overall"]
    lines.append(
        "Pooled law MAE versus normalized regret: Spearman "
        f"{overall['normalized_regret']['spearman']['coefficient']:.4f}; versus selected rank: "
        f"{overall['selected_rank']['spearman']['coefficient']:.4f}."
    )
    lines.extend(["", "| task | n | Spearman law MAE vs rank |", "|---|---:|---:|"])
    for task_id, row in action["by_task"].items():
        coefficient = row["selected_rank"]["spearman"]["coefficient"]
        lines.append(f"| {task_id} | {row['cell_count']} | {coefficient:.4f} |")
    lines.extend(
        [
            "",
            "## Typed-law capacity",
            "",
            "Participant law to final prediction MAE: "
            f"{means['participant_law_to_final_prediction_mae']:.6f}.",
            f"Best full-schema MAE: {means['full_schema_to_final_prediction_mae']:.6g}; "
            f"near-exact cells {aggregate['full_schema_near_exact_cell_count']}/"
            f"{schema['completed_cell_count']}.",
            f"Term-matched MAE: {means['term_matched_to_final_prediction_mae']:.6f}; "
            f"near-exact cells {aggregate['term_matched_near_exact_cell_count']}/"
            f"{schema['completed_cell_count']}.",
            f"Leave-one-query-out MAE: {means['leave_one_query_out_to_final_prediction_mae']:.6f}.",
            "",
            "The full-schema result is an in-domain representation-capacity control. It does not "
            "claim that the fitted oracle is a globally identified mechanism.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--w2-summary", type=Path, default=DEFAULT_W2)
    parser.add_argument("--evaluator-root", type=Path, default=DEFAULT_EVALUATOR)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_MD)
    parser.add_argument("--bootstrap-replicates", type=int, default=10_000)
    args = parser.parse_args()
    w2_path = args.w2_summary.resolve()
    evaluator_root = args.evaluator_root.resolve()
    dataset_path = evaluator_root / "analysis_dataset.json"
    manifest_path = evaluator_root / "input_manifest.json"
    started = time.perf_counter()

    def progress(event: dict[str, Any]) -> None:
        print(
            json.dumps(
                {**event, "elapsed_s": round(time.perf_counter() - started, 1)},
                ensure_ascii=False,
                sort_keys=True,
            ),
            flush=True,
        )

    payload: dict[str, Any] = {
        "schema_version": CONTROL_SCHEMA_VERSION,
        "formal_result": False,
        "analysis_role": "provider_free_reviewer_control",
        "provider_call_count": 0,
        "participant_physical_experiment_count": 0,
        "source_artifacts": {
            "w2_50_summary": w2_path.relative_to(ROOT).as_posix(),
            "c2_analysis_dataset": dataset_path.relative_to(ROOT).as_posix(),
            "c2_input_manifest": manifest_path.relative_to(ROOT).as_posix(),
        },
        "w2_50_continuous_action": analyze_w2_50(
            _read(w2_path),
            bootstrap_replicates=args.bootstrap_replicates,
            progress=progress,
        ),
        "typed_law_schema_capacity": analyze_schema_capacity(
            _read(dataset_path),
            _read(manifest_path),
            evaluator_root,
            progress=progress,
        ),
    }
    payload["summary_sha256"] = canonical_json_sha256(payload)
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    write_json_atomic(args.output_json, payload)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(_report(payload), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
