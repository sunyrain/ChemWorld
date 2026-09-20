#!/usr/bin/env python3
"""Validate the five-world EQ-E v0.2 design without provider calls."""
# ruff: noqa: E402, E501

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import sys
from collections.abc import Mapping, Sequence
from itertools import pairwise
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

CONFIG = ROOT / "configs/benchmark/work_ii_eq_entity_v0.2.design.json"
ARMS = ("Opaque", "Aligned", "MisIndexed")
METRICS = (
    "pH_normalized",
    "acid_dissociation_fraction",
    "precipitation_signal",
)


def read(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def digest(payload: Any) -> str:
    body = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(body.encode()).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _seed(*parts: object) -> int:
    body = "|".join(str(part) for part in parts).encode()
    return int.from_bytes(hashlib.sha256(body).digest()[:8], "big")


def load_config() -> dict[str, Any]:
    config = read(CONFIG)
    if config.get("provider_execution_authorized") is not False:
        raise RuntimeError("EQ-E v0.2 design gate requires provider execution to remain sealed")
    if config.get("provider_calls_authorized") != 0:
        raise RuntimeError("EQ-E v0.2 design gate must remain provider-free")
    for key in ("base_substrate", "canonical_posttest_protocol"):
        binding = config[key]
        path = ROOT / binding["path"]
        if not path.is_file() or file_sha256(path) != binding["sha256"]:
            raise RuntimeError(f"EQ-E v0.2 binding changed: {key}")
    return config


def queries(config: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = copy.deepcopy(list(config["queries"]))
    expected = [f"Q{index:02d}" for index in range(1, 13)]
    if [row.get("query_id") for row in rows] != expected:
        raise ValueError("EQ-E v0.2 Q must be ordered Q01--Q12")
    return rows


def profiles(world: Mapping[str, Any]) -> dict[int, EquilibriumEntityProfile]:
    return {
        int(row["selector"]): EquilibriumEntityProfile(
            entity_id=f"{world['world_id']}-medium-{row['selector']}",
            pka_shift=float(row["pka_shift"]),
            log10_ksp=float(row["log10_ksp"]),
            cation_fraction=float(row["cation_fraction"]),
            activity_coefficient_ratio=float(row["activity_coefficient_ratio"]),
        )
        for row in world["profiles"]
    }


def public_prior(
    config: Mapping[str, Any],
    world: Mapping[str, Any],
    arm: str,
) -> dict[str, Any] | None:
    if arm == "Opaque":
        return None
    aligned = {
        int(row["selector"]): copy.deepcopy(dict(row))
        for row in world["aligned_descriptors"]
    }
    if arm == "Aligned":
        rows = [aligned[selector] for selector in range(3)]
    elif arm == "MisIndexed":
        permutation = config["prior_contract"]["misindex_permutation"]
        rows = []
        for selector in range(3):
            source = aligned[int(permutation[str(selector)])]
            row = {"selector": selector}
            row.update({key: value for key, value in source.items() if key != "selector"})
            rows.append(row)
    else:
        raise ValueError(f"unknown EQ-E arm: {arm}")
    return {
        "schema_version": config["prior_contract"]["schema_version"],
        "locus": "E",
        "scope": "qualitative local selector-to-property mapping only",
        "entities": rows,
    }


def validate_design(config: Mapping[str, Any]) -> dict[str, Any]:
    expected_counts = {
        "worlds": 5,
        "arms": 3,
        "independent_source_sessions": 15,
        "source_batches_per_session": 12,
        "source_batches": 180,
        "posttests_per_session": 3,
        "posttests": 45,
        "queries_per_session": 12,
        "reference_repeats_per_query": 5,
        "reference_executions": 300,
    }
    if config.get("counts") != expected_counts:
        raise ValueError("EQ-E v0.2 denominators changed")
    if tuple(config.get("arms", ())) != ARMS:
        raise ValueError("EQ-E v0.2 arms changed")
    if tuple(config.get("prediction_metrics", ())) != METRICS:
        raise ValueError("EQ-E v0.2 prediction metrics changed")
    if tuple(config.get("participant_posttest_stages", ())) != ("K1", "Q", "K2"):
        raise ValueError("EQ-E v0.2 posttest chain is not canonical")
    if config["research_goal"] != "characterization":
        raise ValueError("EQ-E v0.2 cannot be an optimization task")
    worlds = list(config["worlds"])
    if len(worlds) != 5 or len({world["world_id"] for world in worlds}) != 5:
        raise ValueError("EQ-E v0.2 requires five unique worlds")
    descriptor_fields = set(config["prior_contract"]["descriptor_fields"])
    if descriptor_fields != {
        "selector",
        "acid_ionization_tendency",
        "solid_formation_tendency",
    }:
        raise ValueError("EQ-E v0.2 descriptor schema changed")
    for world in worlds:
        if set(profiles(world)) != {0, 1, 2}:
            raise ValueError(f"EQ-E v0.2 world lacks three entities: {world['world_id']}")
        descriptor_rows = world["aligned_descriptors"]
        if {row["selector"] for row in descriptor_rows} != {0, 1, 2}:
            raise ValueError(f"EQ-E descriptor selectors changed: {world['world_id']}")
        if any(set(row) != descriptor_fields for row in descriptor_rows):
            raise ValueError(f"EQ-E descriptor fields changed: {world['world_id']}")
        aligned = public_prior(config, world, "Aligned")
        wrong = public_prior(config, world, "MisIndexed")
        if aligned is None or wrong is None or aligned.keys() != wrong.keys() or aligned == wrong:
            raise ValueError(f"EQ-E A/M prior mismatch: {world['world_id']}")
        if [set(row) for row in aligned["entities"]] != [
            set(row) for row in wrong["entities"]
        ]:
            raise ValueError(f"EQ-E A/M row schema mismatch: {world['world_id']}")

    query_rows = queries(config)
    for query in query_rows:
        selector = int(query["selector"])
        volume = float(query["volume_L"])
        amount = float(query["acid_total_mol"])
        if selector not in {0, 1, 2} or not math.isclose(
            amount / volume,
            float(query["concentration_M"]),
            rel_tol=0.0,
            abs_tol=1e-12,
        ):
            raise ValueError(f"EQ-E malformed Q coordinate: {query['query_id']}")
        actions = query["actions"]
        if actions != [
            {"operation": "add_solvent", "solvent": selector, "volume_L": volume},
            {"operation": "add_reagent", "amount_mol": amount},
            {"operation": "terminate"},
            {"operation": "measure", "instrument": "final_assay"},
        ]:
            raise ValueError(f"EQ-E Q action mismatch: {query['query_id']}")
    observed_coverage = {tag for query in query_rows for tag in query["coverage"]}
    required_coverage = {
        "low_concentration",
        "interior_concentration",
        "high_concentration",
        "entity_contrast",
        "same_concentration_scale_control",
        "selector_0",
        "selector_1",
        "selector_2",
    }
    if not required_coverage <= observed_coverage:
        raise ValueError("EQ-E v0.2 Q coverage is incomplete")
    schedule = [
        {
            "cell_id": f"{world['world_id']}--{arm}",
            "world_id": world["world_id"],
            "arm": arm,
            "goal": "characterization",
        }
        for world in worlds
        for arm in ARMS
    ]
    return {
        "schedule": schedule,
        "query_sha256": digest(query_rows),
        "prior_sha256": {
            row["cell_id"]: digest(
                public_prior(
                    config,
                    next(world for world in worlds if world["world_id"] == row["world_id"]),
                    row["arm"],
                )
            )
            for row in schedule
        },
    }


def execute(
    config: Mapping[str, Any],
    world: Mapping[str, Any],
    arm: str,
    query: Mapping[str, Any],
) -> dict[str, Any]:
    selector = int(query["selector"])
    result = solve_equilibrium_entity(
        profile=profiles(world)[selector],
        acid_total_mol=float(query["acid_total_mol"]),
        volume_L=float(query["volume_L"]),
        base_pka=float(world["base_pka_nuisance"]),
    )
    truth = {
        "pH_normalized": result.pH / 14.0,
        "acid_dissociation_fraction": result.acid_dissociation_fraction,
        "precipitation_signal": result.precipitation_signal,
    }
    rng = np.random.default_rng(_seed("eq-e-v0.2-design-gate", world["world_id"], query["query_id"]))
    noise = float(config["provider_free_design_gate"]["observation_noise_sd"])
    observed = {
        metric: float(np.clip(value + rng.normal(0.0, noise), 0.0, 1.0))
        for metric, value in truth.items()
    }
    return {
        "cell_id": f"{world['world_id']}--{arm}",
        "world_id": world["world_id"],
        "arm": arm,
        "query_id": query["query_id"],
        "selector": selector,
        "concentration_M": query["concentration_M"],
        "volume_L": query["volume_L"],
        "public_metrics": observed,
        "private_noiseless_metrics": truth,
        "solver_residual": result.equilibrium_residual,
        "mechanism_family": result.mechanism_family,
        "aqueous_pair_mol_L": result.aqueous_pair_mol_L,
    }


def _rank_labels(scores: Mapping[int, float]) -> dict[int, str]:
    ordered = sorted(scores, key=lambda selector: scores[selector], reverse=True)
    if any(
        math.isclose(scores[left], scores[right], rel_tol=0.0, abs_tol=1e-10)
        for left, right in pairwise(ordered)
    ):
        raise ValueError("EQ-E descriptor score has an unresolved tie")
    return dict(zip(ordered, ("higher", "intermediate", "lower"), strict=True))


def _descriptor_check(
    world: Mapping[str, Any],
    rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    primary = [row for row in rows if float(row["volume_L"]) == 0.024]
    acid_scores = {
        selector: fmean(
            float(row["private_noiseless_metrics"]["acid_dissociation_fraction"])
            for row in primary
            if int(row["selector"]) == selector
        )
        for selector in range(3)
    }
    solid_scores = {
        selector: fmean(
            float(row["private_noiseless_metrics"]["precipitation_signal"])
            for row in primary
            if int(row["selector"]) == selector
        )
        for selector in range(3)
    }
    acid_labels = _rank_labels(acid_scores)
    solid_labels = _rank_labels(solid_scores)
    expected = {int(row["selector"]): row for row in world["aligned_descriptors"]}
    checks = {
        selector: (
            expected[selector]["acid_ionization_tendency"] == acid_labels[selector]
            and expected[selector]["solid_formation_tendency"] == solid_labels[selector]
        )
        for selector in range(3)
    }
    return {
        "passed": all(checks.values()),
        "selector_checks": checks,
        "acid_scores": acid_scores,
        "solid_scores": solid_scores,
        "derived_acid_labels": acid_labels,
        "derived_solid_labels": solid_labels,
    }


def run_gate(output: Path) -> dict[str, Any]:
    report_path = output / "gate.json"
    if report_path.exists():
        return read(report_path)
    config = load_config()
    validated = validate_design(config)
    query_rows = queries(config)
    worlds = list(config["worlds"])
    executions = [
        execute(config, world, arm, query)
        for world in worlds
        for arm in ARMS
        for query in query_rows
    ]
    replays = [
        execute(config, world, arm, query)
        for world in worlds
        for arm in ARMS
        for query in query_rows
    ]
    gate = config["provider_free_design_gate"]
    exact_replay = digest(executions) == digest(replays)

    by_world: dict[str, list[dict[str, Any]]] = {
        world["world_id"]: [
            row
            for row in executions
            if row["world_id"] == world["world_id"] and row["arm"] == "Opaque"
        ]
        for world in worlds
    }
    identity_spans: dict[str, dict[str, dict[str, float]]] = {}
    scale_gaps: dict[str, dict[str, float]] = {}
    within_entity: dict[str, dict[str, dict[str, float]]] = {}
    descriptor_checks = {}
    for world in worlds:
        world_id = str(world["world_id"])
        rows = by_world[world_id]
        primary = [row for row in rows if float(row["volume_L"]) == 0.024]
        concentrations = sorted({float(row["concentration_M"]) for row in primary})
        identity_spans[world_id] = {
            str(concentration): {
                metric: max(
                    float(row["public_metrics"][metric])
                    for row in primary
                    if float(row["concentration_M"]) == concentration
                )
                - min(
                    float(row["public_metrics"][metric])
                    for row in primary
                    if float(row["concentration_M"]) == concentration
                )
                for metric in METRICS
            }
            for concentration in concentrations
        }
        scale_gaps[world_id] = {}
        within_entity[world_id] = {}
        for selector in range(3):
            interior = next(
                row
                for row in rows
                if int(row["selector"]) == selector
                and math.isclose(float(row["concentration_M"]), 0.08)
                and math.isclose(float(row["volume_L"]), 0.024)
            )
            scaled = next(
                row
                for row in rows
                if int(row["selector"]) == selector
                and math.isclose(float(row["concentration_M"]), 0.08)
                and math.isclose(float(row["volume_L"]), 0.048)
            )
            scale_gaps[world_id][str(selector)] = max(
                abs(
                    float(interior["public_metrics"][metric])
                    - float(scaled["public_metrics"][metric])
                )
                for metric in METRICS
            )
            selected = [row for row in primary if int(row["selector"]) == selector]
            spans = {
                metric: max(float(row["public_metrics"][metric]) for row in selected)
                - min(float(row["public_metrics"][metric]) for row in selected)
                for metric in METRICS
            }
            within_entity[world_id][str(selector)] = spans
        descriptor_checks[world_id] = _descriptor_check(world, rows)

    span_threshold = float(gate["minimum_identity_response_span"])
    minimum_span_metrics = int(gate["minimum_metrics_above_span_per_concentration"])
    response_signal = all(
        sum(value > span_threshold for value in spans.values()) >= minimum_span_metrics
        for world in identity_spans.values()
        for spans in world.values()
    )
    within_entity_signal = all(
        spans["pH_normalized"] > float(gate["minimum_within_entity_pH_span"])
        and max(
            spans["acid_dissociation_fraction"],
            spans["precipitation_signal"],
        )
        > float(gate["minimum_within_entity_non_pH_span"])
        for world in within_entity.values()
        for spans in world.values()
    )

    arm_physics_identity = all(
        len(
            {
                digest(row["public_metrics"])
                for row in executions
                if row["world_id"] == world["world_id"]
                and row["query_id"] == query["query_id"]
            }
        )
        == 1
        for world in worlds
        for query in query_rows
    )
    permutation = config["prior_contract"]["misindex_permutation"]
    public_payloads = [
        public_prior(config, world, arm)
        for world in worlds
        for arm in ("Aligned", "MisIndexed")
    ]
    public_text = json.dumps(public_payloads, sort_keys=True).lower()
    forbidden = [
        str(field).lower() for field in config["prior_contract"]["forbidden_public_fields"]
    ]
    descriptor_levels = set(
        config["prior_contract"]["descriptor_levels"]["acid_ionization_tendency"]
    )
    selector_role_coverage = all(
        {
            next(
                row[descriptor]
                for row in world["aligned_descriptors"]
                if int(row["selector"]) == selector
            )
            for world in worlds
        }
        == descriptor_levels
        for descriptor in (
            "acid_ionization_tendency",
            "solid_formation_tendency",
        )
        for selector in range(3)
    )
    descriptor_patterns = {
        tuple(
            (
                row["acid_ionization_tendency"],
                row["solid_formation_tendency"],
            )
            for row in sorted(world["aligned_descriptors"], key=lambda item: item["selector"])
        )
        for world in worlds
    }
    checks = {
        "provider_calls_zero": True,
        "canonical_characterization_contract": (
            config["research_goal"] == "characterization"
            and tuple(config["participant_posttest_stages"]) == ("K1", "Q", "K2")
        ),
        "five_world_fifteen_campaign_design": (
            len(validated["schedule"]) == int(gate["planned_campaigns"]) == 15
        ),
        "one_hundred_eighty_batches": len(executions) == int(gate["planned_batches"]) == 180,
        "exact_replay": exact_replay
        and len(replays) == int(gate["planned_exact_replays"]) == 180,
        "arm_physics_identity": arm_physics_identity,
        "identity_response_signal": response_signal,
        "identity_independent_P_null_refuted": response_signal,
        "within_entity_concentration_transfer_signal": within_entity_signal,
        "scale_controls": max(
            gap for world in scale_gaps.values() for gap in world.values()
        )
        <= float(gate["maximum_scale_control_mean_gap"]),
        "common_topology_not_S": all(
            row["mechanism_family"] == "direct_free_ion_precipitation"
            and row["aqueous_pair_mol_L"] == 0.0
            for row in executions
        ),
        "solver_residual": max(float(row["solver_residual"]) for row in executions)
        <= float(gate["maximum_solver_residual"]),
        "descriptors_match_registered_behavior": all(
            row["passed"] for row in descriptor_checks.values()
        ),
        "selector_roles_counterbalanced": selector_role_coverage,
        "world_mapping_patterns_diverse": len(descriptor_patterns) >= 4,
        "strict_opaque_instance_mapping": all(
            public_prior(config, world, "Opaque") is None for world in worlds
        ),
        "matched_distinct_A_M": all(
            public_prior(config, world, "Aligned") != public_prior(config, world, "MisIndexed")
            for world in worlds
        ),
        "no_fixed_point_misindex": all(
            int(source) != int(target) for source, target in permutation.items()
        ),
        "no_numeric_or_query_prior_leakage": not any(field in public_text for field in forbidden),
        "fixed_twelve_query_contract": len(query_rows) == 12,
        "numeric_stability": all(
            math.isfinite(float(value)) and 0.0 <= float(value) <= 1.0
            for row in executions
            for value in row["public_metrics"].values()
        ),
    }
    report = {
        "schema_version": "work-ii-eq-e-provider-free-design-gate-0.2",
        "passed": all(checks.values()),
        "provider_calls": 0,
        "completed_campaigns": 15,
        "completed_batches": len(executions),
        "exact_replay_batches": len(replays) if exact_replay else 0,
        "checks": checks,
        "identity_response_spans": identity_spans,
        "within_entity_response_spans": within_entity,
        "scale_control_max_gaps": scale_gaps,
        "descriptor_checks": descriptor_checks,
        "thresholds": copy.deepcopy(gate),
        "query_sha256": validated["query_sha256"],
        "prior_sha256": validated["prior_sha256"],
        "config_sha256": file_sha256(CONFIG),
    }
    output.mkdir(parents=True, exist_ok=False)
    write(output / "gate.json", report)
    write(output / "executions.json", {"executions": executions})
    lines = [
        "# EQ-E v0.2 five-world provider-free design gate",
        "",
        f"Status: **{'PASS' if report['passed'] else 'FAIL'}**. Provider calls: 0.",
        "",
        f"Completed {report['completed_campaigns']}/15 campaigns, {report['completed_batches']}/180 batches, and {report['exact_replay_batches']}/180 tolerance-zero exact replays.",
        "",
        "| Check | Pass |",
        "|---|---|",
        *[f"| {name} | {'yes' if passed else 'no'} |" for name, passed in checks.items()],
        "",
        "| World | Minimum qualifying identity metrics | Maximum scale gap | Descriptor audit |",
        "|---|---:|---:|---|",
    ]
    for world in worlds:
        world_id = str(world["world_id"])
        minimum_metrics = min(
            sum(value > span_threshold for value in spans.values())
            for spans in identity_spans[world_id].values()
        )
        maximum_gap = max(scale_gaps[world_id].values())
        lines.append(
            f"| {world_id} | {minimum_metrics}/3 | {maximum_gap:.6f} | {'pass' if descriptor_checks[world_id]['passed'] else 'fail'} |"
        )
    lines.extend(
        [
            "",
            "This gate qualifies the frozen design only. It does not authorize an Agent canary or bulk provider execution.",
            "",
        ]
    )
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
                "stage": "eq_e_v02_provider_free_design_gate_complete",
                "passed": report["passed"],
                "campaigns": report["completed_campaigns"],
                "batches": report["completed_batches"],
                "provider_calls": 0,
            }
        ),
        flush=True,
    )
    if not report["passed"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
