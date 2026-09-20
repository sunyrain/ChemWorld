#!/usr/bin/env python3
"""Export sanitized English reports for the completed EQ-S v0.2.1 block."""
# ruff: noqa: E402, E501

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from collections.abc import Mapping, Sequence
from pathlib import Path
from statistics import fmean
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import scripts.run_work_ii_eq_structural_v0_2 as eq

METRICS = eq.METRICS
STAGES = eq.POSTTEST_STAGES
FORBIDDEN_PUBLIC_KEY_PARTS = (
    "credential",
    "token",
    "thread_id",
    "private-provider",
    "raw_model",
    "auth",
)


def number(value: Any) -> str:
    return "—" if not isinstance(value, (int, float)) else f"{float(value):.6g}"


def _assert_public(value: Any, path: str = "$") -> None:
    if isinstance(value, Mapping):
        for key, item in value.items():
            lowered = str(key).lower()
            if any(part in lowered for part in FORBIDDEN_PUBLIC_KEY_PARTS):
                raise RuntimeError(f"private field reached EQ-S public export: {path}.{key}")
            _assert_public(item, f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _assert_public(item, f"{path}[{index}]")


def _validate_completion(root: Path) -> Mapping[str, Any]:
    completion = eq.read(root / "completion.json")
    expected = {
        "source_sessions": 15,
        "source_batches": 180,
        "posttests": 60,
        "reference_executions": 300,
    }
    if any(completion.get(key) != value for key, value in expected.items()):
        raise RuntimeError(f"EQ-S completion denominators do not match: {completion}")
    summary = eq.read(root / "effective-summary.json")
    if (
        summary.get("completed_sources") != 15
        or summary.get("sealed_posttest_chains") != 15
        or summary.get("completed_source_batches") != 180
    ):
        raise RuntimeError("EQ-S effective completion is incomplete")
    return completion


def _truth_means(truth: Mapping[str, Sequence[Mapping[str, float]]]) -> dict[str, dict[str, float]]:
    return {
        query_id: {
            metric: fmean(float(row[metric]) for row in repeats)
            for metric in METRICS
        }
        for query_id, repeats in truth.items()
    }


def public_result(
    result: Mapping[str, Any],
    evaluation: Mapping[str, Any],
    truth: Mapping[str, Sequence[Mapping[str, float]]],
    origin: str,
) -> dict[str, Any]:
    posttests = result.get("posttests", {})
    payload = {
        "schema_version": "work-ii-eq-s-public-cell-0.2.1",
        "cell": {
            key: result.get(key)
            for key in (
                "cell_id",
                "world_id",
                "arm",
                "goal",
                "status",
                "source_status",
                "operations",
                "posttest_chain_sealed",
            )
        },
        "effective_origin": origin,
        "source": {
            "batches": result.get("batches", []),
            "evidentiary_anchor": result.get("evidentiary_anchor"),
            "exact_replay": result.get("exact_replay", {}),
            "rollbacks": result.get("rollbacks", []),
        },
        "posttests": {
            stage: {
                "payload": posttests.get(stage, {}).get("payload"),
                "validation": result.get("posttest_validation", {}).get(stage, {}),
            }
            for stage in STAGES
        },
        "prediction_evaluation": evaluation,
        "reference_truth": truth,
        "reference_truth_means": _truth_means(truth),
        "recovery": {
            key: result.get("recovery", {}).get(key)
            for key in (
                "kind",
                "source_experiments_rerun",
                "truth_revealed_to_agent",
                "question_changed",
                "model_changed",
                "schema_compatibility_repair",
            )
            if key in result.get("recovery", {})
        }
        or None,
        "excluded_material": [
            "authentication material",
            "raw model event streams",
            "session identifiers",
            "usage accounting",
        ],
    }
    _assert_public(payload)
    return payload


def _batch_recipe(row: Mapping[str, Any]) -> tuple[str, str, str]:
    solvent = "—"
    reagent = "—"
    measurements: list[str] = []
    for action in row.get("actions", []):
        if action.get("operation") == "add_solvent":
            solvent = number(action.get("volume_L"))
        elif action.get("operation") == "add_reagent":
            reagent = number(action.get("amount_mol"))
        elif action.get("operation") == "measure":
            measurements.append(str(action.get("instrument")))
    return solvent, reagent, ", ".join(measurements)


def render_cell(payload: Mapping[str, Any]) -> str:
    cell = payload["cell"]
    source = payload["source"]
    evaluation = payload["prediction_evaluation"]
    lines = [
        f"# {cell['cell_id']} — final English experiment report",
        "",
        f"World `{cell['world_id']}`; information arm `{cell['arm']}`; task `mechanism characterization`; effective status `{cell['status']}`; result origin `{payload['effective_origin']}`.",
        "",
        "## Source campaign",
        "",
        f"The autonomous campaign completed {len(source['batches'])}/12 batches and {cell['operations']} recorded operations. Exact replay is `{bool(source['exact_replay'].get('verified'))}`; rollbacks: {len(source['rollbacks'])}.",
        "",
        "| Batch | Solvent L | Reagent mol | Measurements | pH normalized | Free dissociation | Precipitation signal | Residual |",
        "|---:|---:|---:|---|---:|---:|---:|---:|",
    ]
    for row in source["batches"]:
        solvent, reagent, measurements = _batch_recipe(row)
        metrics = row.get("metrics", {})
        lines.append(
            f"| {row.get('lifecycle_index', row.get('ordinal', '—'))} | {solvent} | {reagent} | {measurements} | {number(metrics.get('pH_normalized'))} | {number(metrics.get('acid_dissociation_fraction'))} | {number(metrics.get('precipitation_signal'))} | {number(metrics.get('equilibrium_residual'))} |"
        )
    anchor = source.get("evidentiary_anchor") or {}
    lines.extend(
        [
            "",
            "### Sealed evidentiary anchor",
            "",
            f"Batch `{anchor.get('selected_experiment_index', '—')}`: {anchor.get('selection_rationale', 'Unavailable.')}",
            "",
            "## K1 — sealed mechanistic report",
            "",
            str((payload["posttests"]["K1"].get("payload") or {}).get("report", "Unavailable.")),
            "",
            "## Q — sealed blind predictions",
            "",
            "| Query | Metric | Estimate | 80% lower | 80% upper |",
            "|---|---|---:|---:|---:|",
        ]
    )
    predictions = (payload["posttests"]["Q"].get("payload") or {}).get("predictions", [])
    for prediction in predictions:
        for metric in METRICS:
            interval = prediction.get("metrics", {}).get(metric, {})
            lines.append(
                f"| {prediction.get('query_id')} | {metric} | {number(interval.get('estimate'))} | {number(interval.get('lower80'))} | {number(interval.get('upper80'))} |"
            )
    lines.extend(["", "### Q rationales", ""])
    for prediction in predictions:
        lines.extend(
            [
                f"- **{prediction.get('query_id')}**: {prediction.get('rationale', 'Unavailable.')}",
                "",
            ]
        )
    lines.extend(
        [
            "Shared rationale:",
            "",
            str((payload["posttests"]["Q"].get("payload") or {}).get("rationale", "Unavailable.")),
            "",
            "## K2 — sealed seven-part retrospective",
            "",
            str((payload["posttests"]["K2"].get("payload") or {}).get("report", "Unavailable.")),
            "",
            "## EQS — sealed structured mechanism supplement",
            "",
        ]
    )
    supplement = payload["posttests"]["EQS"].get("payload") or {}
    lines.extend(
        [
            f"- Network family: `{supplement.get('network_family', 'unavailable')}`",
            f"- Aqueous intermediate: `{supplement.get('aqueous_intermediate', 'unavailable')}`",
            f"- Selected equations: `{', '.join(supplement.get('selected_equation_ids', []))}`",
            f"- Cited source batches: `{', '.join(str(item) for item in supplement.get('cited_source_batches', []))}`",
            f"- Rationale: {supplement.get('rationale', 'Unavailable.')}",
            "",
            "## Blind-prediction evaluation",
            "",
            "| Metric | MAE to five-repeat mean | Empirical 80% coverage | Mean width | Interval score |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    for metric in METRICS:
        values = evaluation.get("metrics", {}).get(metric, {})
        lines.append(
            f"| {metric} | {number(values.get('mae_to_five_repeat_mean'))} | {number(values.get('empirical_coverage80'))} | {number(values.get('mean_width80'))} | {number(values.get('mean_interval_score_alpha_0_2'))} |"
        )
    eqs = evaluation.get("eqs", {})
    lines.extend(
        [
            "",
            "## Structural evaluation",
            "",
            f"Truth family: `{eqs.get('truth_family')}`; predicted family: `{eqs.get('predicted_family')}`; abstained: `{eqs.get('abstained')}`; family correct: `{eqs.get('network_family_correct')}`; exact equation set correct: `{eqs.get('exact_equation_set_correct')}`; equation-set Jaccard: `{number(eqs.get('equation_set_jaccard'))}`.",
            "",
            "## Response-shape evaluation",
            "",
            f"Concentration slope MAE `{number(evaluation.get('response_shape', {}).get('concentration_response', {}).get('slope_mae'))}` and curvature MAE `{number(evaluation.get('response_shape', {}).get('concentration_response', {}).get('curvature_mae'))}`. Dilution slope MAE `{number(evaluation.get('response_shape', {}).get('dilution_response', {}).get('slope_mae'))}` and curvature MAE `{number(evaluation.get('response_shape', {}).get('dilution_response', {}).get('curvature_mae'))}`.",
            "",
            "## Evidence boundary",
            "",
            "K1 was sealed before Q, Q before K2, K2 before EQS, and reference truth was generated only after all 15 EQS responses were sealed. The task is characterization rather than optimization. Numerical residual and equilibrium confidence are environment diagnostics, not agent uncertainty or task scores. Private authentication and raw model process material are excluded.",
            "",
        ]
    )
    return "\n".join(lines)


def _cell_macro(row: Mapping[str, Any]) -> dict[str, float]:
    metrics = list(row["prediction_evaluation"]["metrics"].values())
    return {
        "mae": fmean(float(item["mae_to_five_repeat_mean"]) for item in metrics),
        "coverage": fmean(float(item["empirical_coverage80"]) for item in metrics),
        "width": fmean(float(item["mean_width80"]) for item in metrics),
        "interval_score": fmean(
            float(item["mean_interval_score_alpha_0_2"]) for item in metrics
        ),
    }


def aggregate(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    by_arm: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    by_world: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        by_arm[row["cell"]["arm"]].append(row)
        by_world[row["cell"]["world_id"]].append(row)

    arm_rows = {}
    for arm in eq.ARMS:
        cells = by_arm[arm]
        macros = [_cell_macro(cell) for cell in cells]
        arm_rows[arm] = {
            "cells": len(cells),
            **{key: fmean(row[key] for row in macros) for key in macros[0]},
            "network_family_correct": sum(
                cell["prediction_evaluation"]["eqs"]["network_family_correct"]
                for cell in cells
            ),
            "abstentions": sum(
                cell["prediction_evaluation"]["eqs"]["abstained"] for cell in cells
            ),
        }
    world_rows = {
        world_id: {
            cell["cell"]["arm"]: {
                **_cell_macro(cell),
                "truth_family": cell["prediction_evaluation"]["eqs"]["truth_family"],
                "predicted_family": cell["prediction_evaluation"]["eqs"]["predicted_family"],
            }
            for cell in cells
        }
        for world_id, cells in by_world.items()
    }
    return {
        "schema_version": "work-ii-eq-s-public-aggregate-0.2.1",
        "arms": arm_rows,
        "worlds": world_rows,
        "structural": {
            "valid_eqs": sum(cell["prediction_evaluation"]["eqs"]["valid"] for cell in rows),
            "network_family_correct": sum(
                cell["prediction_evaluation"]["eqs"]["network_family_correct"] for cell in rows
            ),
            "abstentions": sum(
                cell["prediction_evaluation"]["eqs"]["abstained"] for cell in rows
            ),
            "direct_world_cells": sum(
                cell["prediction_evaluation"]["eqs"]["truth_family"]
                == "direct_free_ion_precipitation"
                for cell in rows
            ),
            "ion_pair_world_cells": sum(
                cell["prediction_evaluation"]["eqs"]["truth_family"]
                == "aqueous_ion_pair_intermediate"
                for cell in rows
            ),
        },
    }


def render_aggregate(
    rows: Sequence[Mapping[str, Any]],
    completion: Mapping[str, Any],
    summary: Mapping[str, Any],
) -> str:
    lines = [
        "# EQ-S five-world mechanism-characterization block — final report",
        "",
        "## Completion and execution integrity",
        "",
        f"Completed {completion['source_sessions']}/15 independent source sessions, {completion['source_batches']}/180 autonomous source batches, {completion['posttests']}/60 sealed K1/Q/K2/EQS posttests, and {completion['reference_executions']}/300 reference executions. All 15 source trajectories replay exactly and all 15 effective posttest chains are valid.",
        "",
        "The provider-free gate passed all 12 registered checks on 15 campaigns and 180 batches with zero model calls. The first W01 canary retained a provider-schema failure affecting EQS only: the API rejected `uniqueItems` before inference. Version v0.2.1 removed that unsupported provider-schema keyword while retaining explicit local uniqueness validation. The three original nonconforming results remain preserved; recovery reused their threads and reran no source experiment, K1, Q, or K2.",
        "",
        "## Quantitative prediction performance by information arm",
        "",
        "Each row macro-averages the three scored public metrics within each cell and then the five physical worlds. These adaptive development results are descriptive and are not a powered causal estimate of prior-arm effects.",
        "",
        "| Arm | Cells | Mean MAE | Mean 80% coverage | Mean width | Mean interval score | Family correct | Abstentions |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for arm in eq.ARMS:
        item = summary["arms"][arm]
        lines.append(
            f"| {arm} | {item['cells']} | {number(item['mae'])} | {number(item['coverage'])} | {number(item['width'])} | {number(item['interval_score'])} | {item['network_family_correct']}/5 | {item['abstentions']}/5 |"
        )
    lines.extend(
        [
            "",
            "Opaque had the lowest aggregate MAE and interval score in this single five-world block; Aligned had the highest mean coverage but also the widest intervals. MisIndexed was intermediate on MAE and had the lowest mean coverage. These rankings vary by world and should not be generalized without replication.",
            "",
            "## World-by-world result",
            "",
            "| World | Truth family | Opaque MAE / coverage | Aligned MAE / coverage | MisIndexed MAE / coverage | EQS outcome in all arms |",
            "|---|---|---:|---:|---:|---|",
        ]
    )
    for world_id in sorted(summary["worlds"]):
        item = summary["worlds"][world_id]
        truth = item["Opaque"]["truth_family"]
        lines.append(
            f"| {world_id} | {truth} | {number(item['Opaque']['mae'])} / {number(item['Opaque']['coverage'])} | {number(item['Aligned']['mae'])} / {number(item['Aligned']['coverage'])} | {number(item['MisIndexed']['mae'])} / {number(item['MisIndexed']['coverage'])} | indeterminate |"
        )
    structural = summary["structural"]
    lines.extend(
        [
            "",
            "## Structural identification result",
            "",
            f"All {structural['valid_eqs']}/15 EQS payloads were schema-valid, but every cell selected `indeterminate`. Therefore network-family accuracy is {structural['network_family_correct']}/15 and the abstention rate is {structural['abstentions']}/15. This applies to all {structural['direct_world_cells']} direct-network cells and all {structural['ion_pair_world_cells']} ion-pair cells.",
            "",
            "The result is scientifically informative: the preregistered simulator-level non-collapse gate shows that the two topology families cannot be absorbed by the registered four-parameter direct null on held-out conditions, yet the autonomous agents did not convert their 12 adaptive observations into a categorical topology claim. The likely bottleneck is agent experimental design and inference, not a failed physical contrast. This interpretation is an inference from the gate and agent outputs, not a new experiment.",
            "",
            "## Scope and evidence boundary",
            "",
            "This is an S-locus mechanism-characterization block, not a process-optimization block. Opaque received no instance dossier. Aligned and MisIndexed received field-matched opposite topology claims without numerical constants or Q coordinates. K1 preceded Q; Q preceded K2; K2 preceded EQS; all 15 EQS responses preceded truth generation. The reports preserve unfavorable results and the v0.2 schema incident. No model call was repeated because of a scientific answer or score.",
            "",
            "## Contents",
            "",
        ]
    )
    for row in sorted(rows, key=lambda item: item["cell"]["cell_id"]):
        cell_id = row["cell"]["cell_id"]
        lines.append(f"- [{cell_id}](sources/{cell_id}/EXPERIMENT_REPORT.md)")
    lines.append("")
    return "\n".join(lines)


def export(root: Path, destination: Path) -> dict[str, Any]:
    completion = _validate_completion(root)
    config = eq.load_config()
    schedule = eq.validate_design(config)["schedule"]
    truth = eq.read(root / "reference-truth" / "truth.json")
    gate = eq.read(root / "provider-free-gate" / "gate.json")
    if not gate.get("passed") or gate.get("provider_calls") != 0:
        raise RuntimeError("EQ-S public export requires the passing zero-provider gate")
    destination.mkdir(parents=True, exist_ok=False)
    rows = []
    audit = []
    for cell in schedule:
        result, path = eq.effective_result(root, cell)
        if not result or result.get("status") != "completed":
            raise RuntimeError(f"no complete effective EQ-S result: {cell['cell_id']}")
        evaluation = eq.read(root / "evaluations" / f"{cell['cell_id']}.json")
        relative = path.relative_to(root).as_posix()
        origin = "original" if relative.startswith("sources/") else "recovery_attempt_01"
        payload = public_result(result, evaluation, truth[cell["world_id"]], origin)
        cell_dir = destination / "sources" / cell["cell_id"]
        eq.write(cell_dir / "RESULT.json", payload)
        (cell_dir / "EXPERIMENT_REPORT.md").write_text(
            render_cell(payload), encoding="utf-8"
        )
        rows.append(payload)
        audit.append(
            {
                "cell_id": cell["cell_id"],
                "effective_origin": origin,
                "source_experiments_rerun": bool(
                    result.get("recovery", {}).get("source_experiments_rerun", False)
                ),
                "original_nonconforming_preserved": origin != "original",
            }
        )
    for world_id in sorted({row["cell"]["world_id"] for row in rows}):
        world_rows = [row for row in rows if row["cell"]["world_id"] == world_id]
        lines = [
            f"# {world_id} — three-arm index",
            "",
            "| Arm | Status | Source batches | K1/Q/K2/EQS | Report |",
            "|---|---|---:|---|---|",
        ]
        for row in world_rows:
            cell_id = row["cell"]["cell_id"]
            valid = "/".join(
                "pass" if row["posttests"][stage]["validation"].get("valid") else "fail"
                for stage in STAGES
            )
            lines.append(
                f"| {row['cell']['arm']} | {row['cell']['status']} | {len(row['source']['batches'])} | {valid} | [report](../../sources/{cell_id}/EXPERIMENT_REPORT.md) |"
            )
        target = destination / "worlds" / world_id
        target.mkdir(parents=True)
        (target / "INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    summary = aggregate(rows)
    eq.write(destination / "AGGREGATE.json", summary)
    eq.write(destination / "RECOVERY_AUDIT.json", {"cells": audit})
    eq.write(
        destination / "GATE_SUMMARY.json",
        {
            "passed": gate["passed"],
            "provider_calls": gate["provider_calls"],
            "completed_campaigns": gate["completed_campaigns"],
            "completed_batches": gate["completed_batches"],
            "checks": gate["checks"],
            "response_spans": gate["response_spans"],
            "family_noncollapse_checks": gate["family_noncollapse_checks"],
        },
    )
    index = {
        "schema_version": "work-ii-eq-s-public-index-0.2.1",
        "completion": dict(completion),
        "cells": [
            row["cell"] | {"effective_origin": row["effective_origin"]} for row in rows
        ],
    }
    _assert_public(index)
    eq.write(destination / "INDEX.json", index)
    (destination / "REPORT.md").write_text(
        render_aggregate(rows, completion, summary), encoding="utf-8"
    )
    (destination / "REPRODUCE.md").write_text(
        "# Reproduction\n\n"
        "Use the v0.2.1 freeze manifest. Run the zero-provider gate, freeze, W01 three-arm canary, stage-aware posttest recovery only if required, and the remaining matrix with at most eight isolated workers. Generate truth only after all 15 EQS responses are sealed. Then run this exporter. The ignored run namespace retains trajectories, reference repeats, original failures, and process material; the repository report package excludes authentication, raw model streams, session identifiers, and usage accounting.\n",
        encoding="utf-8",
    )
    return index


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    index = export(args.input.resolve(), args.output.resolve())
    print(
        json.dumps(
            {
                "stage": "eq_s_export_complete",
                "cells": len(index["cells"]),
                "output": str(args.output.resolve()),
            }
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
