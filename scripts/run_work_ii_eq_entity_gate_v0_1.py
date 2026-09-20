#!/usr/bin/env python3
"""Run the small provider-free EQ-E multi-entity substrate gate."""
# ruff: noqa: E402, E501

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import sys
from collections.abc import Mapping
from pathlib import Path
from statistics import fmean
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from chemworld.physchem.equilibrium_entity_panel import (
    EquilibriumEntityProfile,
    solve_equilibrium_entity,
)

CONFIG = ROOT / "configs/benchmark/work_ii_eq_entity_substrate_v0.1.json"
METRICS = (
    "pH_normalized",
    "acid_dissociation_fraction",
    "precipitation_signal",
)


def read(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def digest(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def load_config() -> dict[str, Any]:
    config = read(CONFIG)
    if config.get("provider_calls_authorized") != 0:
        raise RuntimeError("EQ-E small gate must remain provider-free")
    return config


def profiles(config: Mapping[str, Any]) -> dict[str, EquilibriumEntityProfile]:
    return {
        row["entity_id"]: EquilibriumEntityProfile(
            entity_id=str(row["entity_id"]),
            pka_shift=float(row["pka_shift"]),
            log10_ksp=float(row["log10_ksp"]),
            cation_fraction=float(row["cation_fraction"]),
            activity_coefficient_ratio=float(row["activity_coefficient_ratio"]),
        )
        for row in config["private_entity_profiles"]
    }


def public_prior(config: Mapping[str, Any], arm: str) -> dict[str, Any] | None:
    dossier = config["public_entity_dossier"]
    if arm == "Opaque":
        return None
    key = {"Aligned": "aligned", "MisIndexed": "misindexed"}.get(arm)
    if key is None:
        raise ValueError(f"unknown EQ-E arm: {arm}")
    return {
        "schema_version": dossier["schema_version"],
        **copy.deepcopy(dossier["common_fields"]),
        "entities": copy.deepcopy(dossier[key]),
    }


def conditions(config: Mapping[str, Any]) -> list[dict[str, Any]]:
    gate = config["provider_free_gate"]
    primary_volume = float(gate["primary_volume_L"])
    rows = []
    for entity in config["private_entity_profiles"]:
        entity_id = str(entity["entity_id"])
        for index, concentration in enumerate(gate["analytical_concentrations_M"], 1):
            concentration = float(concentration)
            rows.append(
                {
                    "condition_id": f"{entity_id}-C{index:02d}",
                    "entity_id": entity_id,
                    "selector": int(entity["public_selector"]),
                    "concentration_M": concentration,
                    "volume_L": primary_volume,
                    "acid_total_mol": concentration * primary_volume,
                    "scale_control": False,
                }
            )
        concentration = float(gate["scale_control_concentration_M"])
        volume = float(gate["scale_control_volume_L"])
        rows.append(
            {
                "condition_id": f"{entity_id}-scale",
                "entity_id": entity_id,
                "selector": int(entity["public_selector"]),
                "concentration_M": concentration,
                "volume_L": volume,
                "acid_total_mol": concentration * volume,
                "scale_control": True,
            }
        )
    return rows


def _seed(*parts: object) -> int:
    return int.from_bytes(
        hashlib.sha256("|".join(str(part) for part in parts).encode()).digest()[:8],
        "big",
    )


def execute(
    config: Mapping[str, Any],
    condition: Mapping[str, Any],
    repeat: int,
) -> dict[str, Any]:
    profile = profiles(config)[str(condition["entity_id"])]
    result = solve_equilibrium_entity(
        profile=profile,
        acid_total_mol=float(condition["acid_total_mol"]),
        volume_L=float(condition["volume_L"]),
        base_pka=float(config["base_pka_nuisance"]),
    )
    truth = {
        "pH_normalized": result.pH / 14.0,
        "acid_dissociation_fraction": result.acid_dissociation_fraction,
        "precipitation_signal": result.precipitation_signal,
    }
    rng = np.random.default_rng(_seed("eq-e-v0.1", condition["condition_id"], repeat))
    noise = float(config["provider_free_gate"]["observation_noise_sd"])
    observed = {
        metric: float(np.clip(value + rng.normal(0.0, noise), 0.0, 1.0))
        for metric, value in truth.items()
    }
    return {
        "condition_id": condition["condition_id"],
        "entity_id": condition["entity_id"],
        "selector": condition["selector"],
        "concentration_M": condition["concentration_M"],
        "volume_L": condition["volume_L"],
        "scale_control": condition["scale_control"],
        "repeat": repeat,
        "public_metrics": observed,
        "solver_residual": result.equilibrium_residual,
        "mechanism_family": result.mechanism_family,
        "aqueous_pair_mol_L": result.aqueous_pair_mol_L,
    }


def validate_design(config: Mapping[str, Any]) -> None:
    profile_rows = config["private_entity_profiles"]
    if len(profile_rows) != 3 or {row["public_selector"] for row in profile_rows} != {0, 1, 2}:
        raise ValueError("EQ-E substrate requires exactly three selectable entities")
    topology = config["common_private_topology"]
    if topology["mechanism_family"] != "direct_free_ion_precipitation":
        raise ValueError("EQ-E v0.1 must hold topology fixed")
    if topology["aqueous_intermediate_present"] is not False:
        raise ValueError("EQ-E v0.1 cannot introduce an S-locus intermediate")
    if len(conditions(config)) != int(config["provider_free_gate"]["planned_conditions_per_repeat"]):
        raise ValueError("EQ-E condition denominator changed")
    opaque = public_prior(config, "Opaque")
    aligned = public_prior(config, "Aligned")
    wrong = public_prior(config, "MisIndexed")
    if opaque is not None or aligned is None or wrong is None:
        raise ValueError("EQ-E prior arms are malformed")
    if aligned.keys() != wrong.keys() or aligned == wrong:
        raise ValueError("EQ-E A/M dossiers are not matched and distinct")


def run_gate(output: Path) -> dict[str, Any]:
    config = load_config()
    validate_design(config)
    if (output / "gate.json").exists():
        return read(output / "gate.json")
    gate = config["provider_free_gate"]
    rows = conditions(config)
    repeats = int(gate["noise_repeats"])
    executions = [execute(config, row, repeat) for repeat in range(1, repeats + 1) for row in rows]
    replays = [execute(config, row, repeat) for repeat in range(1, repeats + 1) for row in rows]
    exact_replay = digest(executions) == digest(replays)

    means: dict[str, dict[str, float]] = {}
    for condition in rows:
        selected = [
            row for row in executions if row["condition_id"] == condition["condition_id"]
        ]
        means[condition["condition_id"]] = {
            metric: fmean(row["public_metrics"][metric] for row in selected)
            for metric in METRICS
        }

    primary = [row for row in rows if not row["scale_control"]]
    concentrations = sorted({float(row["concentration_M"]) for row in primary})
    identity_spans = {}
    for concentration in concentrations:
        selected = [row for row in primary if float(row["concentration_M"]) == concentration]
        identity_spans[str(concentration)] = {
            metric: max(means[row["condition_id"]][metric] for row in selected)
            - min(means[row["condition_id"]][metric] for row in selected)
            for metric in METRICS
        }
    span_threshold = float(gate["minimum_identity_response_span"])
    min_span_metrics = int(gate["minimum_metrics_above_span_per_concentration"])
    p_noncollapse = all(
        sum(value > span_threshold for value in spans.values()) >= min_span_metrics
        for spans in identity_spans.values()
    )

    scale_gaps = {}
    for entity in profiles(config):
        reference_id = next(
            row["condition_id"]
            for row in primary
            if row["entity_id"] == entity
            and math.isclose(
                float(row["concentration_M"]),
                float(gate["scale_control_concentration_M"]),
            )
        )
        scale_id = next(
            row["condition_id"]
            for row in rows
            if row["entity_id"] == entity and row["scale_control"]
        )
        scale_gaps[entity] = max(
            abs(means[reference_id][metric] - means[scale_id][metric]) for metric in METRICS
        )

    aligned = public_prior(config, "Aligned")
    wrong = public_prior(config, "MisIndexed")
    assert aligned is not None and wrong is not None
    forbidden = [
        str(field).lower()
        for field in config["public_entity_dossier"]["forbidden_public_fields"]
    ]
    public_text = json.dumps([aligned, wrong], sort_keys=True).lower()
    permutation = config["public_entity_dossier"]["misindex_permutation"]
    checks = {
        "provider_calls_zero": True,
        "three_selectable_entities": len(profiles(config)) == 3,
        "forty_five_executions": len(executions) == int(gate["planned_executions"]),
        "exact_replay": exact_replay,
        "identity_response_signal": all(
            sum(value > span_threshold for value in spans.values()) >= min_span_metrics
            for spans in identity_spans.values()
        ),
        "identity_independent_P_null_refuted": p_noncollapse,
        "common_topology_not_S": all(
            row["mechanism_family"] == "direct_free_ion_precipitation"
            and row["aqueous_pair_mol_L"] == 0.0
            for row in executions
        ),
        "solver_residual": max(row["solver_residual"] for row in executions)
        <= float(gate["maximum_solver_residual"]),
        "scale_controls": max(scale_gaps.values())
        <= float(gate["maximum_scale_control_mean_gap"]),
        "strict_opaque": public_prior(config, "Opaque") is None,
        "matched_distinct_A_M": aligned.keys() == wrong.keys() and aligned != wrong,
        "no_fixed_point_misindex": all(int(key) != int(value) for key, value in permutation.items()),
        "no_numeric_or_query_prior_leakage": not any(field in public_text for field in forbidden),
        "numeric_stability": all(
            math.isfinite(value) and 0.0 <= value <= 1.0
            for row in executions
            for value in row["public_metrics"].values()
        ),
    }
    report = {
        "schema_version": "work-ii-eq-e-provider-free-gate-0.1",
        "passed": all(checks.values()),
        "provider_calls": 0,
        "completed_executions": len(executions),
        "exact_replay_executions": len(replays) if exact_replay else 0,
        "checks": checks,
        "identity_response_spans": identity_spans,
        "scale_control_max_mean_gaps": scale_gaps,
        "public_mean_grid": means,
        "thresholds": copy.deepcopy(gate),
        "config_sha256": hashlib.sha256(CONFIG.read_bytes()).hexdigest(),
    }
    write(output / "gate.json", report)
    write(output / "executions.json", {"executions": executions})
    lines = [
        "# EQ-E multi-entity provider-free gate v0.1",
        "",
        f"Status: **{'PASS' if report['passed'] else 'FAIL'}**. Provider calls: 0.",
        "",
        f"Completed {len(executions)}/45 numerical executions and {len(replays)}/45 exact replays.",
        "",
        "| Check | Pass |",
        "|---|---|",
        *[f"| {name} | {'yes' if passed else 'no'} |" for name, passed in checks.items()],
        "",
        "A pass licenses five-world O/A/M design work only. EQ-E provider execution remains unauthorized.",
        "",
    ]
    (output / "REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = run_gate(args.output.resolve())
    print(
        json.dumps(
            {
                "stage": "eq_e_provider_free_gate_complete",
                "passed": report["passed"],
                "executions": report["completed_executions"],
                "provider_calls": 0,
            }
        ),
        flush=True,
    )
    if not report["passed"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
