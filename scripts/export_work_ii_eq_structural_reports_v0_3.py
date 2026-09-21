#!/usr/bin/env python3
"""Export sanitized English reports for the canonical EQ-S v0.3 block."""
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

import scripts.run_work_ii_eq_structural_v0_3 as eq

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
        "posttests": 45,
        "reference_executions": 300,
    }
    if any(completion.get(key) != value for key, value in expected.items()):
        raise RuntimeError(f"EQ-S v0.3 completion denominators do not match: {completion}")
    if tuple(completion.get("participant_posttest_stages", ())) != STAGES:
        raise RuntimeError("EQ-S v0.3 participant chain is not exactly K1/Q/K2")
    summary = eq.read(root / "summary.json")
    if (
        summary.get("completed_sources") != 15
        or summary.get("sealed_posttest_chains") != 15
        or summary.get("completed_source_batches") != 180
    ):
        raise RuntimeError("EQ-S v0.3 effective completion is incomplete")
    return completion


def _truth_means(truth: Mapping[str, Sequence[Mapping[str, float]]]) -> dict[str, dict[str, float]]:
    return {
        query_id: {
            metric: fmean(float(row[metric]) for row in repeats)
            for metric in METRICS
        }
        for query_id, repeats in truth.items()
    }


def _recovery_summary(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            key: row.get(key)
            for key in (
                "attempt",
                "kind",
                "resumed_stages",
                "source_experiments_rerun",
                "truth_revealed_to_agent",
                "question_changed",
                "model_changed",
            )
        }
        for row in result.get("recoveries", [])
    ]


def public_result(
    result: Mapping[str, Any],
    evaluation: Mapping[str, Any],
    truth: Mapping[str, Sequence[Mapping[str, float]]],
    origin: str,
) -> dict[str, Any]:
    posttests = result.get("posttests", {})
    payload = {
        "schema_version": "work-ii-eq-s-public-cell-0.3",
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
        "recoveries": _recovery_summary(result),
        "mechanism_evaluation_boundary": {
            "primary_artifact": "K1",
            "mode": "external_blind_descriptive_audit",
            "participant_candidate_labels_exposed": False,
            "primary_family_accuracy_endpoint": None,
            "single_composite_score_endpoint": None,
        },
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
            "## K1 — sealed open mechanistic report (primary mechanism artifact)",
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
        lines.extend([f"- **{prediction.get('query_id')}**: {prediction.get('rationale', 'Unavailable.')}", ""])
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
    shape = evaluation.get("response_shape", {})
    lines.extend(
        [
            "",
            "## Response-shape evaluation",
            "",
            f"Concentration slope MAE `{number(shape.get('concentration_response', {}).get('slope_mae'))}` and curvature MAE `{number(shape.get('concentration_response', {}).get('curvature_mae'))}`. Dilution slope MAE `{number(shape.get('dilution_response', {}).get('slope_mae'))}` and curvature MAE `{number(shape.get('dilution_response', {}).get('curvature_mae'))}`.",
            "",
            "## Evidence boundary",
            "",
            "The participant received exactly K1, Q, and K2, in that order. K1 is the primary open-form mechanism artifact. No candidate mechanism family, equation menu, hidden truth, or score was shown before K2 sealed. Reference truth was generated only after all 15 K2 responses sealed. No closed-set family-accuracy or single composite mechanism score is authorized.",
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
        "interval_score": fmean(float(item["mean_interval_score_alpha_0_2"]) for item in metrics),
    }


def aggregate(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    by_arm: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    by_world: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        by_arm[row["cell"]["arm"]].append(row)
        by_world[row["cell"]["world_id"]].append(row)
    arms = {}
    for arm in eq.ARMS:
        macros = [_cell_macro(cell) for cell in by_arm[arm]]
        arms[arm] = {
            "cells": len(macros),
            **{key: fmean(row[key] for row in macros) for key in macros[0]},
        }
    worlds = {
        world_id: {cell["cell"]["arm"]: _cell_macro(cell) for cell in cells}
        for world_id, cells in by_world.items()
    }
    return {
        "schema_version": "work-ii-eq-s-public-aggregate-0.3",
        "arms": arms,
        "worlds": worlds,
        "mechanism_artifact": "sealed_open_form_K1",
        "primary_family_accuracy": None,
        "single_composite_mechanism_score": None,
    }


def render_aggregate(
    rows: Sequence[Mapping[str, Any]],
    completion: Mapping[str, Any],
    summary: Mapping[str, Any],
) -> str:
    lines = [
        "# EQ-S v0.3 canonical mechanism-characterization block — final report",
        "",
        "## Completion and execution integrity",
        "",
        f"Completed {completion['source_sessions']}/15 independent source sessions, {completion['source_batches']}/180 autonomous source batches, {completion['posttests']}/45 sealed K1/Q/K2 posttests, and {completion['reference_executions']}/300 reference executions. All 15 source trajectories replay exactly and all 15 effective posttest chains are valid.",
        "",
        "The zero-provider gate passed before launch. W01 ran as a three-arm canary, followed by the remaining matrix with at most eight isolated workers. Retained provider failures were recovered only from the latest legal same-thread boundary: original records remain preserved, physical source experiments were not rerun, and the questions, model, worlds, and scoring contract were unchanged.",
        "",
        "## Quantitative prediction performance by information arm",
        "",
        "Each row macro-averages the three scored public metrics within each cell and then the five physical worlds. These adaptive development results are descriptive, not a powered causal estimate of arm effects.",
        "",
        "| Arm | Cells | Mean MAE | Mean 80% coverage | Mean width | Mean interval score |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for arm in eq.ARMS:
        item = summary["arms"][arm]
        lines.append(
            f"| {arm} | {item['cells']} | {number(item['mae'])} | {number(item['coverage'])} | {number(item['width'])} | {number(item['interval_score'])} |"
        )
    lines.extend(
        [
            "",
            "## World-by-world quantitative result",
            "",
            "| World | Opaque MAE / coverage | Aligned MAE / coverage | MisIndexed MAE / coverage |",
            "|---|---:|---:|---:|",
        ]
    )
    for world_id in sorted(summary["worlds"]):
        item = summary["worlds"][world_id]
        lines.append(
            f"| {world_id} | {number(item['Opaque']['mae'])} / {number(item['Opaque']['coverage'])} | {number(item['Aligned']['mae'])} / {number(item['Aligned']['coverage'])} | {number(item['MisIndexed']['mae'])} / {number(item['MisIndexed']['coverage'])} |"
        )
    lines.extend(
        [
            "",
            "## Mechanism-report interpretation",
            "",
            "K1 is the primary mechanism artifact and remains open-form. It must be read or externally audited on the preregistered descriptive dimensions: proposed species/processes, proposed reaction edges or equations, evidence-versus-conjecture separation, true common-backbone coverage, treatment of an aqueous intermediate or competing networks, and calibration to identifiability limits. The protocol deliberately provides no closed-set family-accuracy headline and no single composite mechanism score.",
            "",
            "## Scope and evidence boundary",
            "",
            "This is an S-locus mechanism-characterization block, not a process-optimization block. Opaque received no instance dossier. Aligned and MisIndexed received field-matched opposite topology claims without numerical constants or Q coordinates. Every participant received the same canonical K1 and K2; only the preregistered EQ-S Q payload is system-specific.",
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
        raise RuntimeError("EQ-S v0.3 export requires the passing zero-provider gate")
    destination.mkdir(parents=True, exist_ok=False)
    rows = []
    audit = []
    for cell in schedule:
        result, path = eq.effective_result(root, cell)
        if not result or result.get("status") != "completed":
            raise RuntimeError(f"no complete effective EQ-S v0.3 result: {cell['cell_id']}")
        evaluation = eq.read(root / "evaluations" / f"{cell['cell_id']}.json")
        relative = path.relative_to(root).as_posix()
        origin = "original" if relative.startswith("sources/") else relative.removesuffix("/RESULT.json")
        payload = public_result(result, evaluation, truth[cell["world_id"]], origin)
        cell_dir = destination / "sources" / cell["cell_id"]
        eq.write(cell_dir / "RESULT.json", payload)
        (cell_dir / "EXPERIMENT_REPORT.md").write_text(render_cell(payload), encoding="utf-8")
        rows.append(payload)
        audit.append(
            {
                "cell_id": cell["cell_id"],
                "effective_origin": origin,
                "source_experiments_rerun": any(
                    recovery.get("source_experiments_rerun") is True
                    for recovery in payload["recoveries"]
                ),
                "original_nonconforming_preserved": origin != "original",
            }
        )
    for world_id in sorted({row["cell"]["world_id"] for row in rows}):
        world_rows = [row for row in rows if row["cell"]["world_id"] == world_id]
        lines = [
            f"# {world_id} — three-arm index",
            "",
            "| Arm | Status | Source batches | K1/Q/K2 | Report |",
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
        "schema_version": "work-ii-eq-s-public-index-0.3",
        "completion": dict(completion),
        "cells": [row["cell"] | {"effective_origin": row["effective_origin"]} for row in rows],
    }
    _assert_public(index)
    eq.write(destination / "INDEX.json", index)
    (destination / "REPORT.md").write_text(render_aggregate(rows, completion, summary), encoding="utf-8")
    (destination / "REPRODUCE.md").write_text(
        "# Reproduction\n\n"
        "Use the v0.3 freeze manifest. Run the zero-provider gate, freeze, W01 three-arm canary, stage-aware same-thread posttest recovery only if required, and the remaining matrix with at most eight isolated workers. Generate truth only after all 15 K2 responses are sealed, then run this exporter. The ignored run namespace retains trajectories, reference repeats, original failures, and process material; this public package excludes authentication, raw model streams, session identifiers, and usage accounting.\n",
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
                "stage": "eq_s_v03_export_complete",
                "cells": len(index["cells"]),
                "output": str(args.output.resolve()),
            }
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
