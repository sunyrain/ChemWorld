#!/usr/bin/env python3
# ruff: noqa: RUF001
"""Build a matched DeepSeek-Codex C2 current-composite analysis."""

from __future__ import annotations

import argparse
import json
import random
from collections import Counter, defaultdict
from collections.abc import Mapping, Sequence
from pathlib import Path
from statistics import mean
from typing import Any

from chemworld.eval.provenance import canonical_json_sha256, write_json_atomic

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DEEPSEEK_REPORT = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "work-ii-deepseek-c2-current-composite-evaluation-v0.2.json"
)
DEFAULT_DEEPSEEK_DATASET = (
    ROOT
    / "runs/formal/"
    "work-ii-deepseek-c2-current-composite-evaluator-v0.2-20260815/analysis_dataset.json"
)
DEFAULT_CODEX_REPORT = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "work-ii-w2-62-codex-c2-current-composite-evaluation-v0.1.json"
)
DEFAULT_CODEX_DATASET = (
    ROOT
    / "runs/development/"
    "work-ii-w2-62-codex-c2-current-composite-evaluator-v0.1-20260902/analysis_dataset.json"
)
DEFAULT_OUTPUT = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "work-ii-w2-62-c2-cross-model-current-composite-v0.1.json"
)
DEFAULT_MARKDOWN = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "WORK_II_W2_62_C2_CROSS_MODEL_CURRENT_COMPOSITE_ZH.md"
)
EXPECTED_CELLS = 135
EXPECTED_CLUSTERS = 45
EXPECTED_TASKS = 9
ARMS = ("opaque", "aligned_nominal", "misindexed_nominal")
LOCI = ("A_E", "A_P", "A_S")


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def _self_hash_valid(value: Mapping[str, Any], field: str) -> bool:
    expected = value.get(field)
    payload = dict(value)
    payload.pop(field, None)
    return isinstance(expected, str) and canonical_json_sha256(payload) == expected


def _coordinate(row: Mapping[str, Any]) -> tuple[str, str, int, str]:
    return (
        str(row["locus_id"]),
        str(row["task_id"]),
        int(row["world_seed"]),
        str(row["prior_arm"]),
    )


def _load_bundle(report_path: Path, dataset_path: Path) -> dict[str, Any]:
    report = _load(report_path)
    dataset = _load(dataset_path)
    if (
        report.get("status") != "completed"
        or int(report.get("provider_call_count", -1)) != 0
        or not _self_hash_valid(report, "report_sha256")
    ):
        raise ValueError(f"current-composite report is incomplete or drifted: {report_path}")
    if (
        int(dataset.get("provider_call_count", -1)) != 0
        or not _self_hash_valid(dataset, "dataset_sha256")
        or report.get("analysis_dataset_sha256") != dataset.get("dataset_sha256")
    ):
        raise ValueError(f"current-composite dataset is incomplete or drifted: {dataset_path}")
    rows = dataset.get("cell_rows")
    if not isinstance(rows, list) or len(rows) != EXPECTED_CELLS:
        raise ValueError("current-composite dataset must contain 135 cell rows")
    by_coordinate = {_coordinate(row): row for row in rows}
    if len(by_coordinate) != EXPECTED_CELLS:
        raise ValueError("current-composite dataset contains duplicate coordinates")
    clusters = {
        (row["locus_id"], row["task_id"], row["world_seed"]) for row in rows
    }
    task_surfaces = {(row["locus_id"], row["task_id"]) for row in rows}
    if len(clusters) != EXPECTED_CLUSTERS or len(task_surfaces) != EXPECTED_TASKS:
        raise ValueError("current-composite task/world denominator differs from 9/45")
    return {"report": report, "dataset": dataset, "rows": by_coordinate}


def _numeric(value: Any) -> float | None:
    if isinstance(value, bool) or not isinstance(value, int | float):
        return None
    return float(value)


def _metrics(row: Mapping[str, Any]) -> dict[str, Any]:
    checkpoint = row.get("checkpoint_error")
    checkpoint = checkpoint if isinstance(checkpoint, Mapping) else {}
    law = row.get("law_summary")
    law = law if isinstance(law, Mapping) else {}
    blind = row.get("blind")
    blind = blind if isinstance(blind, Mapping) else {}
    return {
        "terminal_completed": row.get("terminal_state") == "completed",
        "prediction_improvement": _numeric(checkpoint.get("primary_improvement")),
        "effective_final_error": _numeric(checkpoint.get("effective_final_error")),
        "law_mae": _numeric(law.get("normalized_mae")),
        "law_compression_loss": _numeric(
            law.get("summary_minus_effective_final_error")
        ),
        "blind_gain": _numeric(blind.get("recommendation_gain_over_incumbent")),
        "blind_launched": int(blind.get("launched_execution_count", 0) or 0) > 0,
    }


def _available_mean(rows: Sequence[Mapping[str, Any]], field: str) -> float | None:
    values = [float(row[field]) for row in rows if row.get(field) is not None]
    return mean(values) if values else None


def _metric_summary(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    terminal = Counter(
        "completed" if row["terminal_completed"] else "not_completed" for row in rows
    )
    blind = [row for row in rows if row["blind_gain"] is not None]
    return {
        "scheduled_cell_count": len(rows),
        "terminal_state_counts": dict(sorted(terminal.items())),
        "terminal_completion_rate": mean(
            float(row["terminal_completed"]) for row in rows
        ),
        "prediction_scored_count": sum(
            row["prediction_improvement"] is not None for row in rows
        ),
        "mean_prediction_improvement": _available_mean(
            rows, "prediction_improvement"
        ),
        "mean_effective_final_error": _available_mean(rows, "effective_final_error"),
        "law_evaluated_count": sum(row["law_mae"] is not None for row in rows),
        "mean_law_mae": _available_mean(rows, "law_mae"),
        "mean_law_compression_loss": _available_mean(rows, "law_compression_loss"),
        "blind_gain_evaluable_count": len(blind),
        "mean_blind_gain": _available_mean(blind, "blind_gain"),
        "blind_better_count": sum(float(row["blind_gain"]) > 1.0e-12 for row in blind),
        "blind_equivalent_count": sum(
            abs(float(row["blind_gain"])) <= 1.0e-12 for row in blind
        ),
        "blind_worse_count": sum(float(row["blind_gain"]) < -1.0e-12 for row in blind),
    }


def _percentile(values: Sequence[float], probability: float) -> float:
    ordered = sorted(values)
    position = (len(ordered) - 1) * probability
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    weight = position - lower
    return ordered[lower] * (1.0 - weight) + ordered[upper] * weight


def _task_stratified_cluster_bootstrap(
    left: Mapping[tuple[str, str, int, str], Mapping[str, Any]],
    right: Mapping[tuple[str, str, int, str], Mapping[str, Any]],
    *,
    field: str,
    replicates: int = 10_000,
    seed: int = 262,
) -> dict[str, Any]:
    common = [
        coordinate
        for coordinate in left
        if left[coordinate].get(field) is not None and right[coordinate].get(field) is not None
    ]
    all_task_surfaces = {(coordinate[0], coordinate[1]) for coordinate in left}
    if not common:
        return {
            "paired_cell_count": 0,
            "task_count": 0,
            "cluster_count": 0,
            "replicate_count": 0,
            "seed": seed,
            "estimate": None,
            "interval_95": None,
            "missing_task_surfaces": [
                f"{locus_id}/{task_id}"
                for locus_id, task_id in sorted(all_task_surfaces)
            ],
        }
    tasks: dict[tuple[str, str], list[int]] = defaultdict(list)
    for locus_id, task_id, world_seed, _ in common:
        task_surface = (locus_id, task_id)
        if world_seed not in tasks[task_surface]:
            tasks[task_surface].append(world_seed)
    missing_task_surfaces = all_task_surfaces - set(tasks)
    for seeds in tasks.values():
        seeds.sort()
    estimate = mean(
        float(right[coordinate][field]) - float(left[coordinate][field])
        for coordinate in common
    )
    rng = random.Random(seed)
    draws: list[float] = []
    for _ in range(replicates):
        deltas: list[float] = []
        for (locus_id, task_id), seeds in sorted(tasks.items()):
            for _ in seeds:
                sampled_seed = rng.choice(seeds)
                for arm in ARMS:
                    coordinate = (locus_id, task_id, sampled_seed, arm)
                    if (
                        coordinate in left
                        and left[coordinate].get(field) is not None
                        and right[coordinate].get(field) is not None
                    ):
                        deltas.append(
                            float(right[coordinate][field])
                            - float(left[coordinate][field])
                        )
        draws.append(mean(deltas))
    return {
        "paired_cell_count": len(common),
        "task_count": len(tasks),
        "cluster_count": sum(len(seeds) for seeds in tasks.values()),
        "replicate_count": replicates,
        "seed": seed,
        "estimate": estimate,
        "interval_95": [_percentile(draws, 0.025), _percentile(draws, 0.975)],
        "missing_task_surfaces": [
            f"{locus_id}/{task_id}"
            for locus_id, task_id in sorted(missing_task_surfaces)
        ],
    }


def _paired_summary(
    left: Mapping[tuple[str, str, int, str], Mapping[str, Any]],
    right: Mapping[tuple[str, str, int, str], Mapping[str, Any]],
    *,
    bootstrap: bool,
) -> dict[str, Any]:
    if set(left) != set(right):
        raise ValueError("current-composite paired coordinates differ")
    coordinates = sorted(left)
    result: dict[str, Any] = {
        "orientation": "codex_minus_deepseek",
        "paired_scheduled_cell_count": len(coordinates),
        "terminal_completion_rate_difference": mean(
            float(right[key]["terminal_completed"])
            - float(left[key]["terminal_completed"])
            for key in coordinates
        ),
    }
    for field in (
        "prediction_improvement",
        "effective_final_error",
        "law_mae",
        "law_compression_loss",
        "blind_gain",
    ):
        common = [
            key
            for key in coordinates
            if left[key].get(field) is not None and right[key].get(field) is not None
        ]
        result[field] = {
            "paired_cell_count": len(common),
            "mean_difference": (
                mean(float(right[key][field]) - float(left[key][field]) for key in common)
                if common
                else None
            ),
        }
        if bootstrap and field != "blind_gain":
            result[field]["task_stratified_world_cluster_bootstrap"] = (
                _task_stratified_cluster_bootstrap(left, right, field=field)
            )
    return result


def build_summary(
    deepseek_report: Path,
    deepseek_dataset: Path,
    codex_report: Path,
    codex_dataset: Path,
) -> dict[str, Any]:
    deepseek = _load_bundle(deepseek_report, deepseek_dataset)
    codex = _load_bundle(codex_report, codex_dataset)
    if set(deepseek["rows"]) != set(codex["rows"]):
        raise ValueError("DeepSeek and Codex C2 cell coordinates differ")
    for coordinate in deepseek["rows"]:
        left = deepseek["rows"][coordinate]
        right = codex["rows"][coordinate]
        shared = ("locus_id", "task_id", "world_seed", "prior_arm", "scheduled_experiment_count")
        if any(left[field] != right[field] for field in shared):
            raise ValueError(f"C2 scientific coordinate drifted: {coordinate}")
    raw = {
        "deepseek": {
            coordinate: _metrics(row) for coordinate, row in deepseek["rows"].items()
        },
        "codex": {
            coordinate: _metrics(row) for coordinate, row in codex["rows"].items()
        },
    }
    result: dict[str, Any] = {
        "schema_version": "chemworld-work-ii-w2-62-c2-cross-model-current-composite-0.1",
        "status": "terminal_complete",
        "provider_call_count": 0,
        "models": {
            model: {
                "overall": _metric_summary(list(rows.values())),
                "by_locus": {
                    locus: _metric_summary(
                        [
                            rows[coordinate]
                            for coordinate in rows
                            if deepseek["rows"][coordinate]["locus_id"] == locus
                        ]
                    )
                    for locus in LOCI
                },
                "by_arm": {
                    arm: _metric_summary(
                        [rows[coordinate] for coordinate in rows if coordinate[3] == arm]
                    )
                    for arm in ARMS
                },
            }
            for model, rows in raw.items()
        },
        "paired_descriptive_differences": {
            "overall": _paired_summary(raw["deepseek"], raw["codex"], bootstrap=True),
            "by_locus": {
                locus: _paired_summary(
                    {
                        key: value
                        for key, value in raw["deepseek"].items()
                        if deepseek["rows"][key]["locus_id"] == locus
                    },
                    {
                        key: value
                        for key, value in raw["codex"].items()
                        if deepseek["rows"][key]["locus_id"] == locus
                    },
                    bootstrap=False,
                )
                for locus in LOCI
            },
        },
        "integrity": {
            "paired_cell_count": len(raw["deepseek"]),
            "paired_cluster_count": EXPECTED_CLUSTERS,
            "paired_task_count": EXPECTED_TASKS,
            "same_task_world_prior_coordinates": True,
            "deepseek_dataset_sha256": deepseek["dataset"]["dataset_sha256"],
            "codex_dataset_sha256": codex["dataset"]["dataset_sha256"],
        },
        "claim_boundaries": {
            "model_stratified_c2_results_supported": True,
            "paired_descriptive_differences_supported": True,
            "model_superiority_ranking_supported": False,
            "causal_provider_effect_supported": False,
        },
    }
    result["summary_sha256"] = canonical_json_sha256(result)
    return result


def _show(value: Any, digits: int = 4) -> str:
    return "—" if value is None else f"{float(value):.{digits}f}"


def _write_markdown(summary: Mapping[str, Any], path: Path) -> None:
    lines = [
        "# Work II W2-62 C2 双模型 current-composite 收束",
        "",
        "两个模型均使用同一 135-cell、45-world-cluster、9-task C2 evaluator surface。"
        "差值方向固定为 Codex − DeepSeek，仅作 matched descriptive analysis。",
        "",
        "| 模型 | completed | prediction Δ | final error | law MAE | "
        "compression loss | blind gain |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for model in ("deepseek", "codex"):
        row = summary["models"][model]["overall"]
        lines.append(
            f"| {model} | {row['terminal_state_counts'].get('completed', 0)}/135 | "
            f"{_show(row['mean_prediction_improvement'])} | "
            f"{_show(row['mean_effective_final_error'])} | {_show(row['mean_law_mae'])} | "
            f"{_show(row['mean_law_compression_loss'])} | {_show(row['mean_blind_gain'])} |"
        )
    paired = summary["paired_descriptive_differences"]["overall"]
    lines.extend(["", "## 配对差值", ""])
    for field in (
        "prediction_improvement",
        "effective_final_error",
        "law_mae",
        "law_compression_loss",
        "blind_gain",
    ):
        row = paired[field]
        text = f"- {field}: n=`{row['paired_cell_count']}`, Δ=`{_show(row['mean_difference'])}`"
        bootstrap = row.get("task_stratified_world_cluster_bootstrap")
        if isinstance(bootstrap, Mapping):
            interval = bootstrap["interval_95"]
            text += f", 95% cluster interval=`[{_show(interval[0])}, {_show(interval[1])}]`"
        lines.append(text + "。")
    lines.extend(["", "不执行模型优劣检验，也不解释为 provider 因果效应。"])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deepseek-report", type=Path, default=DEFAULT_DEEPSEEK_REPORT)
    parser.add_argument("--deepseek-dataset", type=Path, default=DEFAULT_DEEPSEEK_DATASET)
    parser.add_argument("--codex-report", type=Path, default=DEFAULT_CODEX_REPORT)
    parser.add_argument("--codex-dataset", type=Path, default=DEFAULT_CODEX_DATASET)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown", type=Path, default=DEFAULT_MARKDOWN)
    args = parser.parse_args()
    summary = build_summary(
        args.deepseek_report.resolve(),
        args.deepseek_dataset.resolve(),
        args.codex_report.resolve(),
        args.codex_dataset.resolve(),
    )
    write_json_atomic(args.output.resolve(), summary)
    _write_markdown(summary, args.markdown.resolve())
    print(
        json.dumps(
            {
                "status": summary["status"],
                "paired_cell_count": summary["integrity"]["paired_cell_count"],
                "provider_call_count": summary["provider_call_count"],
            },
            ensure_ascii=False,
            sort_keys=True,
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
