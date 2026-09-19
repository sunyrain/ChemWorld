#!/usr/bin/env python3
"""Export complete sanitized public reports for the frozen EQ block."""
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

import scripts.recover_work_ii_eq_bounded_equilibrium as recovery
import scripts.run_work_ii_eq_bounded_equilibrium as eq

STAGES = ("K1", "Q", "K2")
FORBIDDEN_PUBLIC_KEYS = ("thread", "credential", "token", "provider")


def _assert_public(value: Any, path: str = "$") -> None:
    if isinstance(value, Mapping):
        for key, item in value.items():
            lowered = str(key).lower()
            if any(word in lowered for word in FORBIDDEN_PUBLIC_KEYS):
                raise RuntimeError(f"private field reached public export: {path}.{key}")
            _assert_public(item, f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _assert_public(item, f"{path}[{index}]")


def public_result(
    result: Mapping[str, Any],
    evaluation: Mapping[str, Any],
    truth: Mapping[str, Any],
    origin: str,
) -> dict[str, Any]:
    posttests = result.get("posttests", {})
    payload = {
        "schema_version": "work-ii-eq-public-cell-1.0",
        "cell": {
            key: result.get(key)
            for key in ("cell_id", "world_id", "arm", "goal", "status", "source_status", "operations", "posttest_chain_sealed")
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
        "recovery": {
            key: result.get("recovery", {}).get(key)
            for key in ("kind", "source_experiments_rerun", "truth_revealed_to_agent", "question_changed", "model_changed")
            if key in result.get("recovery", {})
        } or None,
        "excluded_private_material": [
            "authentication material",
            "raw model event streams",
            "session identifiers",
            "usage accounting",
        ],
    }
    _assert_public(payload)
    return payload


def number(value: Any) -> str:
    return "—" if not isinstance(value, (int, float)) else f"{float(value):.6g}"


def render_cell(payload: Mapping[str, Any]) -> str:
    cell = payload["cell"]
    source = payload["source"]
    lines = [
        f"# {cell['cell_id']} — final public report",
        "",
        f"World `{cell['world_id']}`; prior arm `{cell['arm']}`; status `{cell['status']}`. The effective result came from `{payload['effective_origin']}`.",
        "",
        "## Source campaign",
        "",
        f"The campaign contains {len(source['batches'])}/12 completed batches and {cell['operations']} recorded operations. Exact replay: `{bool(source['exact_replay'].get('verified'))}`.",
        "",
        "| Batch | pH normalized | Acid dissociation | Precipitation signal | Residual |",
        "|---:|---:|---:|---:|---:|",
    ]
    for row in source["batches"]:
        metrics = row.get("metrics", {})
        lines.append(
            f"| {row.get('lifecycle_index', '—')} | {number(metrics.get('pH_normalized'))} | {number(metrics.get('acid_dissociation_fraction'))} | {number(metrics.get('precipitation_signal'))} | {number(metrics.get('equilibrium_residual'))} |"
        )
    lines.extend(["", "## Sealed scientific account", ""])
    for stage, title in (("K1", "K1 report"), ("Q", "Blind Q predictions"), ("K2", "K2 retrospective")):
        turn = payload["posttests"][stage]
        lines.extend([f"### {title}", ""])
        if stage == "Q":
            predictions = (turn.get("payload") or {}).get("predictions", [])
            lines.extend([
                "| Query | Metric | Estimate | 80% lower | 80% upper |",
                "|---|---|---:|---:|---:|",
            ])
            for prediction in predictions:
                for metric, interval in prediction.get("metrics", {}).items():
                    lines.append(
                        f"| {prediction.get('query_id')} | {metric} | {number(interval.get('estimate'))} | {number(interval.get('lower80'))} | {number(interval.get('upper80'))} |"
                    )
            rationale = (turn.get("payload") or {}).get("rationale")
            if rationale:
                lines.extend(["", str(rationale), ""])
        else:
            lines.extend([str((turn.get("payload") or {}).get("report", "Unavailable.")), ""])
    lines.extend([
        "## Blind-prediction evaluation",
        "",
        "| Metric | MAE | Empirical 80% coverage | Mean width | Interval score |",
        "|---|---:|---:|---:|---:|",
    ])
    for metric, values in payload["prediction_evaluation"].get("metrics", {}).items():
        lines.append(
            f"| {metric} | {number(values.get('mae_to_five_repeat_mean'))} | {number(values.get('empirical_coverage80'))} | {number(values.get('mean_width80'))} | {number(values.get('mean_interval_score_alpha_0_2'))} |"
        )
    lines.extend([
        "",
        "## Scope and privacy",
        "",
        "Reference truth was released only after every K2 response was sealed. The environment-derived equilibrium-confidence field is neither an agent uncertainty estimate nor a score. Authentication material, raw model events, session identifiers, and usage accounting are excluded.",
        "",
    ])
    return "\n".join(lines)


def validate_completion(root: Path) -> Mapping[str, Any]:
    completion = eq.read(root / "completion.json")
    expected = {"source_sessions": 15, "source_batches": 180, "posttests": 45, "reference_executions": 300}
    if any(completion.get(key) != value for key, value in expected.items()):
        raise RuntimeError(f"EQ completion denominators do not match: {completion}")
    if completion.get("equilibrium_confidence_used_as_agent_uncertainty_or_score") is not False:
        raise RuntimeError("EQ completion has an invalid confidence-scoring declaration")
    return completion


def render_aggregate(rows: Sequence[Mapping[str, Any]], completion: Mapping[str, Any]) -> str:
    grouped: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[row["cell"]["arm"]].append(row)
    lines = [
        "# EQ bounded-equilibrium block — aggregate final report",
        "",
        "## Completion",
        "",
        f"Completed {completion['source_sessions']}/15 independent source sessions, {completion['source_batches']}/180 batches, {completion['posttests']}/45 sealed K1/Q/K2 posttests, and {completion['reference_executions']}/300 provider-free reference executions.",
        "",
        "## Prediction performance by prior arm",
        "",
        "Each value macro-averages all five worlds, then the three scored public response metrics. Adaptive source trajectories mean these are descriptive development results, not a formal causal estimate.",
        "",
        "| Arm | Cells | Mean MAE | Mean 80% coverage | Mean interval width | Mean interval score |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for arm in eq.ARMS:
        cells = grouped[arm]
        metric_rows = [
            metric
            for cell in cells
            for metric in cell["prediction_evaluation"].get("metrics", {}).values()
        ]
        lines.append(
            f"| {arm} | {len(cells)} | {number(fmean(float(row['mae_to_five_repeat_mean']) for row in metric_rows))} | {number(fmean(float(row['empirical_coverage80']) for row in metric_rows))} | {number(fmean(float(row['mean_width80']) for row in metric_rows))} | {number(fmean(float(row['mean_interval_score_alpha_0_2']) for row in metric_rows))} |"
        )
    lines.extend([
        "",
        "## Evidence boundary",
        "",
        "Strict Opaque received no instance prior. Aligned and MisIndexed used structurally matched public priors. K1 preceded fixed blind Q; K2 preceded truth generation. The scored Q channels are pH_normalized, acid_dissociation_fraction, and precipitation_signal. equilibrium_residual is a numerical diagnostic, while equilibrium_confidence is excluded from uncertainty and scoring.",
        "",
    ])
    return "\n".join(lines)


def export(root: Path, destination: Path) -> dict[str, Any]:
    completion = validate_completion(root)
    config = eq.load_config()
    schedule = eq.validate_design(config)["schedule"]
    truth = eq.read(root / "reference-truth" / "truth.json")
    destination.mkdir(parents=True, exist_ok=False)
    rows = []
    audit = []
    for cell in schedule:
        result, path = recovery.effective_result(root, config, cell)
        if not result or result.get("status") != "completed":
            raise RuntimeError(f"no complete effective result for {cell['cell_id']}")
        evaluation = eq.read(root / "evaluations" / f"{cell['cell_id']}.json")
        relative = path.relative_to(root).as_posix()
        origin = "original" if relative.startswith("sources/") else relative.split("/")[2]
        payload = public_result(result, evaluation, truth[cell["world_id"]], origin)
        cell_dir = destination / "sources" / cell["cell_id"]
        eq.write(cell_dir / "RESULT.json", payload)
        (cell_dir / "EXPERIMENT_REPORT.md").write_text(render_cell(payload), encoding="utf-8")
        rows.append(payload)
        audit.append({"cell_id": cell["cell_id"], "effective_origin": origin, "recovered": origin != "original"})
    for world_id in sorted({row["cell"]["world_id"] for row in rows}):
        world_rows = [row for row in rows if row["cell"]["world_id"] == world_id]
        lines = [f"# {world_id}", "", "| Arm | Status | Source batches | Report |", "|---|---|---:|---|"]
        for row in world_rows:
            cell_id = row["cell"]["cell_id"]
            lines.append(f"| {row['cell']['arm']} | {row['cell']['status']} | {len(row['source']['batches'])} | [report](../../sources/{cell_id}/EXPERIMENT_REPORT.md) |")
        (destination / "worlds" / world_id).mkdir(parents=True)
        (destination / "worlds" / world_id / "INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    eq.write(destination / "RECOVERY_AUDIT.json", {"cells": audit})
    index = {
        "schema_version": "work-ii-eq-public-index-1.0",
        "completion": dict(completion),
        "cells": [row["cell"] | {"effective_origin": row["effective_origin"]} for row in rows],
    }
    _assert_public(index)
    eq.write(destination / "INDEX.json", index)
    (destination / "REPORT.md").write_text(render_aggregate(rows, completion), encoding="utf-8")
    (destination / "REPRODUCE.md").write_text(
        "# Reproduction\n\nThe frozen config, protocol, runner, recovery runner, exporter, and provider-free gate are SHA-256-bound by the repository freeze manifest. Execute the provider-free gate first, then the W01 three-arm canary, then the full matrix. Generate truth only after all 15 K2 turns are sealed; finally run this exporter. Private authentication material, raw model event streams, session identifiers, and usage accounting must remain outside this package.\n",
        encoding="utf-8",
    )
    return index


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    index = export(args.input.resolve(), args.output.resolve())
    print(json.dumps({"stage": "export_complete", "cells": len(index["cells"]), "output": str(args.output.resolve())}), flush=True)


if __name__ == "__main__":
    main()
