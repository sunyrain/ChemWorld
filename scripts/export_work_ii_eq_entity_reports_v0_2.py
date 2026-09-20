#!/usr/bin/env python3
"""Export sanitized English reports for the canonical EQ-E v0.2 block."""
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

import scripts.run_work_ii_eq_entity_v0_2 as eq

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
                raise RuntimeError(f"private field reached EQ-E public export: {path}.{key}")
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
        raise RuntimeError(f"EQ-E v0.2 completion denominators do not match: {completion}")
    if tuple(completion.get("participant_posttest_stages", ())) != STAGES:
        raise RuntimeError("EQ-E v0.2 participant chain is not exactly K1/Q/K2")
    summary = eq.read(root / "summary.json")
    if (
        summary.get("completed_sources") != 15
        or summary.get("sealed_posttest_chains") != 15
        or summary.get("completed_source_batches") != 180
        or summary.get("failures")
    ):
        raise RuntimeError("EQ-E v0.2 effective completion is incomplete")
    return completion


def _truth_means(
    truth: Mapping[str, Sequence[Mapping[str, float]]],
) -> dict[str, dict[str, float]]:
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
        "schema_version": "work-ii-eq-e-public-cell-0.2",
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
        "entity_mechanism_boundary": {
            "primary_artifact": "K1",
            "task": "open_form_entity_conditioned_mechanism_characterization",
            "fixed_common_topology": True,
            "participant_candidate_property_vectors_exposed": False,
            "operation_recommendation_applicable": False,
            "primary_family_accuracy_endpoint": None,
            "single_composite_mechanism_score_endpoint": None,
        },
        "excluded_material": [
            "authentication material",
            "raw model event streams",
            "session identifiers",
            "usage accounting",
            "private entity parameters",
        ],
    }
    _assert_public(payload)
    return payload


def _batch_recipe(row: Mapping[str, Any]) -> tuple[str, str, str, str]:
    selector = "—"
    volume = "—"
    reagent = "—"
    measurements: list[str] = []
    for action in row.get("actions", []):
        if action.get("operation") == "add_solvent":
            selector = str(action.get("solvent", "—"))
            volume = number(action.get("volume_L"))
        elif action.get("operation") == "add_reagent":
            reagent = number(action.get("amount_mol"))
        elif action.get("operation") == "measure":
            measurements.append(str(action.get("instrument")))
    return selector, volume, reagent, ", ".join(measurements)


def render_cell(payload: Mapping[str, Any]) -> str:
    cell = payload["cell"]
    source = payload["source"]
    evaluation = payload["prediction_evaluation"]
    lines = [
        f"# {cell['cell_id']} — final English experiment report",
        "",
        f"World `{cell['world_id']}`; information arm `{cell['arm']}`; task `entity-conditioned mechanism characterization`; effective status `{cell['status']}`; result origin `{payload['effective_origin']}`.",
        "",
        "## Source campaign",
        "",
        f"The autonomous campaign completed {len(source['batches'])}/12 batches and {cell['operations']} recorded operations. Exact replay is `{bool(source['exact_replay'].get('verified'))}`; rollbacks: {len(source['rollbacks'])}.",
        "",
        "| Batch | Medium selector | Volume L | Reagent mol | Measurements | pH normalized | Free dissociation | Precipitation signal | Residual |",
        "|---:|---:|---:|---:|---|---:|---:|---:|---:|",
    ]
    for row in source["batches"]:
        selector, volume, reagent, measurements = _batch_recipe(row)
        metrics = row.get("metrics", {})
        lines.append(
            f"| {row.get('lifecycle_index', row.get('ordinal', '—'))} | {selector} | {volume} | {reagent} | {measurements} | {number(metrics.get('pH_normalized'))} | {number(metrics.get('acid_dissociation_fraction'))} | {number(metrics.get('precipitation_signal'))} | {number(metrics.get('equilibrium_residual'))} |"
        )
    anchor = source.get("evidentiary_anchor") or {}
    lines.extend(
        [
            "",
            "### Sealed evidentiary anchor",
            "",
            f"Batch `{anchor.get('selected_experiment_index', '—')}`: {anchor.get('selection_rationale', 'Unavailable.')}",
            "",
            "## K1 — sealed open mechanistic report",
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
    entity = evaluation.get("entity_mapping", {})
    lines.extend(
        [
            "",
            "## Entity-map and scale-transfer evaluation",
            "",
            "| Concentration M | Pairwise entity-contrast MAE |",
            "|---:|---:|",
        ]
    )
    for row in entity.get("entity_contrast", []):
        lines.append(f"| {number(row.get('concentration_M'))} | {number(row.get('pairwise_contrast_mae'))} |")
    lines.extend(["", "| Selector | Same-concentration scale-gap MAE |", "|---:|---:|"])
    for row in entity.get("same_concentration_scale_transfer", []):
        lines.append(f"| {row.get('selector')} | {number(row.get('scale_gap_mae'))} |")
    lines.extend(
        [
            "",
            "## Evidence boundary",
            "",
            "The participant received exactly K1, Q, and K2, in that order. K1 is the primary open-form entity-mechanism artifact. No candidate property vector, numerical entity constant, hidden truth, or score was shown before K2 sealed. Reference truth was generated only after all 15 K2 responses sealed. The common direct weak-acid/free-ion-precipitation topology was fixed across worlds and arms; the task was entity mapping, not operation optimization.",
            "",
        ]
    )
    return "\n".join(lines)


def _cell_macro(row: Mapping[str, Any]) -> dict[str, float]:
    metrics = list(row["prediction_evaluation"]["metrics"].values())
    entity = row["prediction_evaluation"]["entity_mapping"]
    return {
        "mae": fmean(float(item["mae_to_five_repeat_mean"]) for item in metrics),
        "coverage": fmean(float(item["empirical_coverage80"]) for item in metrics),
        "width": fmean(float(item["mean_width80"]) for item in metrics),
        "interval_score": fmean(float(item["mean_interval_score_alpha_0_2"]) for item in metrics),
        "entity_contrast_mae": fmean(float(item["pairwise_contrast_mae"]) for item in entity["entity_contrast"]),
        "scale_gap_mae": fmean(float(item["scale_gap_mae"]) for item in entity["same_concentration_scale_transfer"]),
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
    return {
        "schema_version": "work-ii-eq-e-public-aggregate-0.2",
        "arms": arms,
        "worlds": {
            world_id: {cell["cell"]["arm"]: _cell_macro(cell) for cell in cells}
            for world_id, cells in by_world.items()
        },
        "mechanism_artifact": "sealed_open_form_K1",
        "operation_recommendation_applicable": False,
        "primary_family_accuracy": None,
        "single_composite_mechanism_score": None,
    }


def render_aggregate(
    rows: Sequence[Mapping[str, Any]],
    completion: Mapping[str, Any],
    summary: Mapping[str, Any],
) -> str:
    lines = [
        "# EQ-E v0.2 canonical entity-mechanism block — final report",
        "",
        "## Completion and execution integrity",
        "",
        f"Completed {completion['source_sessions']}/15 independent source sessions, {completion['source_batches']}/180 autonomous source batches, {completion['posttests']}/45 sealed K1/Q/K2 posttests, and {completion['reference_executions']}/300 reference executions. All 15 effective posttest chains are valid.",
        "",
        "The zero-provider gate passed before launch. W01 ran as a three-arm canary, followed by the remaining matrix with at most eight isolated workers. A missing persistent SSH proxy tunnel caused only zero-action preflight connection failures; those records remain preserved outside this public package. No accepted source trajectory was replayed, and the final scientific matrix used the unchanged frozen worlds, questions, model, and scoring contract.",
        "",
        "## Quantitative prediction performance by information arm",
        "",
        "Each row macro-averages the three public metrics within a cell and then the five physical worlds. These adaptive development results are descriptive, not a powered causal estimate of arm effects.",
        "",
        "| Arm | Cells | Mean MAE | Mean 80% coverage | Mean width | Mean interval score | Entity-contrast MAE | Scale-gap MAE |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for arm in eq.ARMS:
        item = summary["arms"][arm]
        lines.append(
            f"| {arm} | {item['cells']} | {number(item['mae'])} | {number(item['coverage'])} | {number(item['width'])} | {number(item['interval_score'])} | {number(item['entity_contrast_mae'])} | {number(item['scale_gap_mae'])} |"
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
            "## Interpretation boundary",
            "",
            "K1 is the primary open-form mechanism artifact. EQ-E fixes the common direct weak-acid/free-ion-precipitation topology and asks the Agent to characterize how each anonymous medium identity changes a joint property bundle. Opaque receives no selector mapping; Aligned receives the correct qualitative mapping; MisIndexed receives the frozen no-fixed-point permutation. The block does not ask for process optimization or a closed-set hidden property-vector answer.",
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


def _preflight_audit(root: Path) -> dict[str, Any]:
    groups = []
    for group in sorted((root / "failed-attempts").glob("*")):
        if not group.is_dir():
            continue
        rows = []
        for trajectory in sorted((group / "sources").glob("*/trajectory.jsonl")):
            rows.append(
                {
                    "cell_id": trajectory.parent.name,
                    "accepted_action_records": sum(1 for _ in trajectory.open(encoding="utf-8")),
                }
            )
        groups.append({"label": group.name, "cells": rows})
    payload = {
        "schema_version": "work-ii-eq-e-preflight-audit-0.2",
        "groups": groups,
        "all_attempts_zero_action": all(
            row["accepted_action_records"] == 0
            for group in groups
            for row in group["cells"]
        ),
        "included_in_scientific_matrix": False,
        "root_cause": "persistent SSH proxy tunnel absent during background provider startup",
    }
    _assert_public(payload)
    return payload


def export(root: Path, destination: Path) -> dict[str, Any]:
    completion = _validate_completion(root)
    config = eq.load_config()
    schedule = eq.validate_design(config)["schedule"]
    truth = eq.read(root / "reference-truth" / "truth.json")
    gate = eq.read(root / "provider-free-gate" / "gate.json")
    if not gate.get("passed") or gate.get("provider_calls") != 0:
        raise RuntimeError("EQ-E v0.2 export requires the passing zero-provider gate")
    destination.mkdir(parents=True, exist_ok=False)
    rows = []
    for cell in schedule:
        result, path = eq.effective_result(root, cell)
        if not result or result.get("status") != "completed":
            raise RuntimeError(f"no complete effective EQ-E v0.2 result: {cell['cell_id']}")
        evaluation = eq.read(root / "evaluations" / f"{cell['cell_id']}.json")
        relative = path.relative_to(root).as_posix()
        origin = "original" if relative.startswith("sources/") else relative.removesuffix("/RESULT.json")
        payload = public_result(result, evaluation, truth[cell["world_id"]], origin)
        cell_dir = destination / "sources" / cell["cell_id"]
        eq.write(cell_dir / "RESULT.json", payload)
        (cell_dir / "EXPERIMENT_REPORT.md").write_text(render_cell(payload), encoding="utf-8")
        rows.append(payload)
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
    eq.write(destination / "PREFLIGHT_AUDIT.json", _preflight_audit(root))
    eq.write(
        destination / "GATE_SUMMARY.json",
        {
            "passed": gate["passed"],
            "provider_calls": gate["provider_calls"],
            "completed_campaigns": gate["completed_campaigns"],
            "completed_batches": gate["completed_batches"],
            "exact_replay_campaigns": gate["exact_replay_campaigns"],
            "checks": gate["checks"],
        },
    )
    index = {
        "schema_version": "work-ii-eq-e-public-index-0.2",
        "completion": dict(completion),
        "cells": [row["cell"] | {"effective_origin": row["effective_origin"]} for row in rows],
    }
    _assert_public(index)
    eq.write(destination / "INDEX.json", index)
    (destination / "REPORT.md").write_text(render_aggregate(rows, completion, summary), encoding="utf-8")
    (destination / "REPRODUCE.md").write_text(
        "# Reproduction\n\n"
        "Use the EQ-E v0.2 freeze manifest. Maintain the configured persistent SSH proxy tunnel for background provider access. Run the zero-provider gate, freeze, W01 three-arm canary, and the remaining matrix with at most eight isolated workers. Generate truth only after all 15 K2 responses are sealed, then run this exporter. The ignored run namespace retains trajectories, preflight failures, reference repeats, process material, and provider-private files; this public package excludes authentication, raw model streams, session identifiers, private entity parameters, and usage accounting.\n",
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
                "stage": "eq_e_v02_export_complete",
                "cells": len(index["cells"]),
                "output": str(args.output.resolve()),
            }
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
