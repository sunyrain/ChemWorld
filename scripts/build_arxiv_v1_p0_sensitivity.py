"""Build the frozen P0 sensitivity supplement for the ChemWorld arXiv paper."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import statistics
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from chemworld.eval.autonomous_material_campaign_audit import (
    _discovery_retention_recovery_metrics,
)

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "chemworld-arxiv-v1-p0-sensitivity-0.1"
CORE_METRICS = (
    "global_best_discovery_fraction",
    "online_incumbent_retention_rate",
    "maximum_absolute_incumbent_drawdown",
    "terminal_to_global_best_ratio",
)
ENDPOINT_METRICS = ("best_final_score", "final_score_mean")
ALL_METRICS = (*CORE_METRICS, *ENDPOINT_METRICS)
RAW_TRAJECTORY_METRIC_KEYS = {
    "global_best_discovery_fraction": "global_best_discovery_fraction",
    "online_incumbent_retention_rate": "online_retention_rate",
    "maximum_absolute_incumbent_drawdown": "maximum_absolute_drawdown_from_prior_incumbent",
    "terminal_to_global_best_ratio": "terminal_to_global_best_ratio",
}


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _canonical_sha256(value: Any) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def _portable(path: Path) -> str:
    resolved = path.resolve()
    for base in (ROOT, ROOT.parent / "ChemWorld"):
        try:
            return resolved.relative_to(base.resolve()).as_posix()
        except ValueError:
            continue
    return resolved.name


def _source(path: Path) -> dict[str, Any]:
    return {
        "path": _portable(path),
        "bytes": path.stat().st_size,
        "sha256": _file_sha256(path),
    }


def _sign_summary(values: Sequence[float]) -> dict[str, Any]:
    numeric = [float(value) for value in values]
    positive = sum(value > 0.0 for value in numeric)
    negative = sum(value < 0.0 for value in numeric)
    zero = len(numeric) - positive - negative
    nonzero = positive + negative
    if nonzero:
        tail = sum(math.comb(nonzero, k) for k in range(max(positive, negative), nonzero + 1)) / (
            2**nonzero
        )
        exact_two_sided = min(1.0, 2.0 * tail)
    else:
        exact_two_sided = 1.0
    leave_one_out = [
        statistics.fmean(numeric[:index] + numeric[index + 1 :]) for index in range(len(numeric))
    ]
    return {
        "n": len(numeric),
        "mean": statistics.fmean(numeric),
        "median": statistics.median(numeric),
        "sample_standard_deviation": statistics.stdev(numeric) if len(numeric) > 1 else 0.0,
        "positive_count": positive,
        "negative_count": negative,
        "zero_count": zero,
        "exact_two_sided_sign_p": exact_two_sided,
        "leave_one_world_out_mean_min": min(leave_one_out),
        "leave_one_world_out_mean_max": max(leave_one_out),
        "leave_one_world_out_means": leave_one_out,
    }


def _g0_sensitivity(g0_v10: Mapping[str, Any], g0_v12: Mapping[str, Any]) -> dict[str, Any]:
    information_rows: list[dict[str, Any]] = []
    baseline_rows: list[dict[str, Any]] = []
    for task_key in ("electrochemical", "crystallization"):
        triarm = g0_v12["tasks"][task_key]
        task_id = str(triarm["task_id"])
        worlds = list(triarm["worlds"])
        for contrast_id, left, right in (
            ("nominal_minus_opaque", "nominal", "opaque"),
            ("misindexed_minus_opaque", "misindexed", "opaque"),
            ("misindexed_minus_nominal", "misindexed", "nominal"),
        ):
            differences = [
                {
                    "world_seed": int(row["world_seed"]),
                    "difference": float(row[left]["primary_score"])
                    - float(row[right]["primary_score"]),
                }
                for row in worlds
            ]
            information_rows.append(
                {
                    "task_id": task_id,
                    "contrast_id": contrast_id,
                    "analysis_unit": "paired physical world",
                    "world_differences": differences,
                    "summary": _sign_summary([row["difference"] for row in differences]),
                }
            )
        for comparison in g0_v10["tasks"][task_key]["paired_comparisons"]:
            differences = [
                {
                    "world_seed": int(row["world_seed"]),
                    "difference": float(row["difference"]),
                }
                for row in comparison["world_differences"]
            ]
            baseline_rows.append(
                {
                    "task_id": task_id,
                    "algorithm_id": comparison["algorithm_id"],
                    "role": comparison["role"],
                    "analysis_unit": "paired physical world",
                    "world_differences": differences,
                    "summary": _sign_summary([row["difference"] for row in differences]),
                }
            )
    return {
        "information_contrasts": information_rows,
        "all_baseline_contrasts": baseline_rows,
        "interpretation": (
            "Execution counts quantify simulator use. Information and baseline contrasts are "
            "summarized over ten paired physical worlds per task. Exact sign statistics and "
            "leave-one-world-out ranges are descriptive robustness checks."
        ),
    }


def _classify(
    values: Sequence[float],
    *,
    threshold: float,
    zero_mode: str,
    tolerance: float = 1e-12,
) -> str:
    numeric = [float(value) for value in values]
    if zero_mode == "exclude_zeros":
        directional = [value for value in numeric if abs(value) > tolerance]
        if not directional:
            return "stable_zero"
        denominator = len(directional)
        median = statistics.median(directional)
        positive = sum(value > tolerance for value in directional)
        negative = sum(value < -tolerance for value in directional)
        zero = 0
    elif zero_mode == "include_zeros":
        denominator = len(numeric)
        if denominator == 0:
            return "mixed"
        median = statistics.median(numeric)
        positive = sum(value > tolerance for value in numeric)
        negative = sum(value < -tolerance for value in numeric)
        zero = denominator - positive - negative
    else:
        raise ValueError(f"unsupported zero mode: {zero_mode}")
    if positive / denominator >= threshold and median > tolerance:
        return "directionally_positive"
    if negative / denominator >= threshold and median < -tolerance:
        return "directionally_negative"
    if zero / denominator >= threshold and abs(median) <= tolerance:
        return "stable_zero"
    return "mixed"


def _pair_values(
    pairs: Sequence[Mapping[str, Any]],
    *,
    metrics: Sequence[str] = ALL_METRICS,
) -> dict[str, dict[str, list[float]]]:
    result = {str(seed): {metric: [] for metric in metrics} for seed in (1, 3)}
    for row in pairs:
        delta = row.get("nominal_minus_opaque")
        if not row.get("pair_complete") or not isinstance(delta, Mapping):
            continue
        seed = str(int(row["world_seed"]))
        for metric in metrics:
            result[seed][metric].append(float(delta[metric]))
    return result


def _classification_table(
    values: Mapping[str, Mapping[str, Sequence[float]]],
    *,
    threshold: float,
    zero_mode: str,
) -> dict[str, Any]:
    classes = {
        seed: {
            metric: _classify(metric_values, threshold=threshold, zero_mode=zero_mode)
            for metric, metric_values in world.items()
        }
        for seed, world in values.items()
    }
    mixed_core = sum(
        classes[seed][metric] == "mixed" for seed in classes for metric in CORE_METRICS
    )
    return {
        "threshold": threshold,
        "zero_mode": zero_mode,
        "mixed_core_classification_count": mixed_core,
        "core_classification_count": len(classes) * len(CORE_METRICS),
        "world_metric_classifications": classes,
    }


def _classification_sensitivity(pairs: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    values = _pair_values(pairs)
    return [
        _classification_table(values, threshold=threshold, zero_mode=zero_mode)
        for threshold in (0.60, 0.75, 0.80)
        for zero_mode in ("include_zeros", "exclude_zeros")
    ]


def _missing_sign_sensitivity(pairs: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    values = _pair_values(pairs)
    per_metric: dict[str, dict[str, Any]] = {}
    for seed in ("1", "3"):
        per_metric[seed] = {}
        for metric in ALL_METRICS:
            observed = list(values[seed][metric])
            scale = max([abs(value) for value in observed] + [1.0])
            possible = {
                label: _classify(
                    [*observed, sign * scale],
                    threshold=0.75,
                    zero_mode="include_zeros",
                )
                for label, sign in (("negative", -1.0), ("zero", 0.0), ("positive", 1.0))
            }
            per_metric[seed][metric] = {
                "observed_complete_pair_count": len(observed),
                "classification_by_missing_sign": possible,
                "classification_invariant": len(set(possible.values())) == 1,
            }
    core_entries = [per_metric[seed][metric] for seed in ("1", "3") for metric in CORE_METRICS]
    minimum_mixed = sum(
        all(value == "mixed" for value in entry["classification_by_missing_sign"].values())
        for entry in core_entries
    )
    maximum_mixed = sum(
        any(value == "mixed" for value in entry["classification_by_missing_sign"].values())
        for entry in core_entries
    )
    return {
        "assumption": (
            "Each right-censored pair is evaluated under negative, zero, and positive missing "
            "differences. Magnitude is immaterial to the sign-consistency rule."
        ),
        "minimum_possible_mixed_core_classifications": minimum_mixed,
        "maximum_possible_mixed_core_classifications": maximum_mixed,
        "core_classification_count": len(core_entries),
        "world_metric_results": per_metric,
    }


def _outcomes(scores: Sequence[float]) -> list[dict[str, Any]]:
    return [{"batch_index": index, "score": float(score)} for index, score in enumerate(scores)]


def _retention_fraction_sensitivity(audit: Mapping[str, Any]) -> list[dict[str, Any]]:
    completed = list(audit["completed_cells"])
    results: list[dict[str, Any]] = []
    for fraction in (0.80, 0.90, 0.95):
        cells: dict[tuple[int, str, str], dict[str, Any]] = {}
        for cell in completed:
            scores = [float(value) for value in cell["scores"]["final_score_sequence"]]
            metrics = _discovery_retention_recovery_metrics(
                _outcomes(scores), retention_fraction=fraction
            )
            key = (
                int(cell["world_seed"]),
                str(cell["trajectory_replicate_id"]),
                str(cell["arm"]),
            )
            cells[key] = metrics
        pairs: list[dict[str, Any]] = []
        for seed in (1, 3):
            for replicate in ("r01", "r02", "r03", "r04", "r05"):
                opaque = cells.get((seed, replicate, "opaque"))
                nominal = cells.get((seed, replicate, "nominal"))
                if opaque is None or nominal is None:
                    continue
                pairs.append(
                    {
                        "world_seed": seed,
                        "trajectory_replicate_id": replicate,
                        "nominal_minus_opaque": {
                            metric: float(nominal[source_key]) - float(opaque[source_key])
                            for metric, source_key in RAW_TRAJECTORY_METRIC_KEYS.items()
                        },
                        "pair_complete": True,
                    }
                )
        values = _pair_values(pairs, metrics=CORE_METRICS)
        classification = _classification_table(values, threshold=0.75, zero_mode="include_zeros")
        results.append(
            {
                "retention_fraction": fraction,
                "complete_pair_count": len(pairs),
                "classification": classification,
            }
        )
    return results


def _first_launch_sensitivity(
    first_summary: Mapping[str, Any],
    formal_audit: Mapping[str, Any],
    partial_accepted_operation_count: int,
) -> dict[str, Any]:
    scores = [float(value) for value in first_summary["behavior"]["terminal_scores"]]
    first_metrics = _discovery_retention_recovery_metrics(_outcomes(scores))
    cell = first_summary["cell"]
    opaque = next(
        row
        for row in formal_audit["completed_cells"]
        if int(row["world_seed"]) == int(cell["world_seed"])
        and str(row["trajectory_replicate_id"]) == str(cell["trajectory_replicate_id"])
        and str(row["arm"]) == "opaque"
    )
    opaque_scores = [float(value) for value in opaque["scores"]["final_score_sequence"]]
    opaque_metrics = _discovery_retention_recovery_metrics(_outcomes(opaque_scores))
    cross_launch_delta = {
        "best_final_score": max(scores) - max(opaque_scores),
        "final_score_mean": statistics.fmean(scores) - statistics.fmean(opaque_scores),
        **{
            metric: float(first_metrics[source_key]) - float(opaque_metrics[source_key])
            for metric, source_key in RAW_TRAJECTORY_METRIC_KEYS.items()
        },
    }
    formal_pairs = list(formal_audit["paired_trajectories"])
    augmented_values = _pair_values(formal_pairs)
    for metric, value in cross_launch_delta.items():
        augmented_values[str(cell["world_seed"])][metric].append(float(value))
    return {
        "status": "excluded_launch_reported_as_protocol_deviation",
        "completed_cell": {
            "world_seed": int(cell["world_seed"]),
            "trajectory_replicate_id": str(cell["trajectory_replicate_id"]),
            "arm": str(first_summary["arm"]),
            "operation_count": int(first_summary["behavior"]["operation_count"]),
            "completed_vessels": int(first_summary["behavior"]["complete_experiment_count"]),
            "final_score_sequence": scores,
            "best_final_score": max(scores),
            "final_score_mean": statistics.fmean(scores),
        },
        "partial_next_cell_accepted_operation_count": partial_accepted_operation_count,
        "cross_launch_pairing_primary_analysis_allowed": False,
        "cross_launch_descriptive_delta": cross_launch_delta,
        "augmented_world_1_descriptive_classification": _classification_table(
            {"1": augmented_values["1"]},
            threshold=0.75,
            zero_mode="include_zeros",
        ),
        "interpretation": (
            "The interrupted launch is not pooled into the frozen matrix. A transparent, "
            "cross-launch descriptive pairing is reported only to show the direction of the "
            "available outcome; it does not replace the pre-specified analysis."
        ),
    }


def build(
    *,
    derived_path: Path,
    g0_v10_path: Path,
    g0_v12_path: Path,
    g2_audit_path: Path,
    first_launch_summary_path: Path,
    first_launch_partial_trajectory_path: Path,
    incident_path: Path,
) -> dict[str, Any]:
    derived = _load(derived_path)
    g0_v10 = _load(g0_v10_path)
    g0_v12 = _load(g0_v12_path)
    g2_audit = _load(g2_audit_path)
    first_summary = _load(first_launch_summary_path)
    partial_operations = sum(
        1
        for line in first_launch_partial_trajectory_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    )
    result: dict[str, Any] = {
        "schema_version": SCHEMA,
        "status": "frozen_complete",
        "primary_analysis_unchanged": True,
        "analysis_units": {
            "g0": "paired physical world; n=10 worlds per task and information arm",
            "g2_v0_4": "development world by arm; n=5 worlds and one session per arm",
            "g2_v0_5": (
                "selected physical world by fresh session-level pair; n=4 complete pairs per world"
            ),
            "simulator_execution_counts_are_not_statistical_sample_sizes": True,
        },
        "sources": {
            "derived_data": _source(derived_path),
            "g0_v1_0": _source(g0_v10_path),
            "g0_v1_2": _source(g0_v12_path),
            "g2_v0_5_audit": _source(g2_audit_path),
            "first_launch_completed_summary": _source(first_launch_summary_path),
            "first_launch_partial_trajectory": _source(first_launch_partial_trajectory_path),
            "incident_record": _source(incident_path),
        },
        "g0": _g0_sensitivity(g0_v10, g0_v12),
        "g2_v0_5": {
            "classification_sensitivity": _classification_sensitivity(
                derived["g2_v0_5"]["paired_trajectories"]
            ),
            "right_censoring_missing_sign_sensitivity": _missing_sign_sensitivity(
                derived["g2_v0_5"]["paired_trajectories"]
            ),
            "retention_fraction_sensitivity": _retention_fraction_sensitivity(g2_audit),
            "first_launch_sensitivity": _first_launch_sensitivity(
                first_summary,
                g2_audit,
                partial_operations,
            ),
        },
    }
    result["sensitivity_sha256"] = _canonical_sha256(result)
    return result


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--derived",
        type=Path,
        default=ROOT / "benchmark/releases/chemworld-serious-v1/arxiv-v1-derived-data.json",
    )
    parser.add_argument(
        "--g0-v1-0",
        type=Path,
        default=ROOT / "workstreams/flagship_tasks/reports/"
        "static-s0-v1.0-formal-campaign-summary.json",
    )
    parser.add_argument(
        "--g0-v1-2",
        type=Path,
        default=ROOT / "workstreams/flagship_tasks/reports/"
        "static-s0-v1.2-three-arm-information-campaign-summary.json",
    )
    parser.add_argument(
        "--g2-audit",
        type=Path,
        default=ROOT.parent / "ChemWorld/runs/development/"
        "g2-autonomous-material-seed1-seed3-r5-codex-sol-medium-v2/audit.json",
    )
    parser.add_argument(
        "--first-launch-summary",
        type=Path,
        default=ROOT.parent / "ChemWorld/runs/development/"
        "g2-autonomous-material-seed1-seed3-r5-codex-sol-medium-v1/"
        "cell-001/attempt-01/run_summary.json",
    )
    parser.add_argument(
        "--first-launch-partial-trajectory",
        type=Path,
        default=ROOT.parent / "ChemWorld/runs/development/"
        "g2-autonomous-material-seed1-seed3-r5-codex-sol-medium-v1/"
        "cell-002/attempt-01/trajectory.jsonl",
    )
    parser.add_argument(
        "--incident",
        type=Path,
        default=ROOT / "workstreams/arxiv_v1/G2_V05_EXECUTION_INCIDENT_2026_08_01_ZH.md",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "benchmark/releases/chemworld-serious-v1/arxiv-v1-p0-sensitivity.json",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    result = build(
        derived_path=args.derived.resolve(),
        g0_v10_path=args.g0_v1_0.resolve(),
        g0_v12_path=args.g0_v1_2.resolve(),
        g2_audit_path=args.g2_audit.resolve(),
        first_launch_summary_path=args.first_launch_summary.resolve(),
        first_launch_partial_trajectory_path=args.first_launch_partial_trajectory.resolve(),
        incident_path=args.incident.resolve(),
    )
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps({"output": str(output), "sha256": result["sensitivity_sha256"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
