#!/usr/bin/env python3
"""Compare frozen RX structural candidates on non-benchmark calibration Worlds."""

from __future__ import annotations

import argparse
import json
import math
from collections.abc import Mapping, Sequence
from pathlib import Path
from statistics import fmean
from typing import Any

from chemworld.eval.provenance import canonical_json_sha256, file_sha256, write_json_atomic
from chemworld.eval.work_ii_catalyst_deactivation_q0 import (
    DECLARED_SIGMA,
    DIRECT_METRICS,
    PRODUCT_METRICS,
    registered_cells,
    stable_catalyst_intervention,
)
from chemworld.eval.work_ii_catalyst_deactivation_q0 import (
    analyze as analyze_stable,
)
from chemworld.world.mechanism_family import (
    MechanismFamilyIntervention,
    TopologyFamilyChange,
)
from chemworld.world.scenario import DefaultScenarioGenerator, get_scenario

try:
    from scripts.run_experiment_1_rx_qualification import (
        _execute_structural,
        _structural_mechanism_audit,
    )
except ModuleNotFoundError:
    from run_experiment_1_rx_qualification import (
        _execute_structural,
        _structural_mechanism_audit,
    )

ROOT = Path(__file__).resolve().parents[1]
NOTE = (
    ROOT / "workstreams/flagship_tasks/experiment_1/systems/RX/"
    "STRUCTURAL_REDESIGN_AUTHORING_NOTE_V1_1_0.md"
)
NOTE_SHA256 = "7aeb1139eeca9c3ada2d6678d7042348480ad74ed606c56bb120a84e947a0f64"
CALIBRATION_SEEDS = (201, 202, 203)
LAW_IDS = ("deactivating_baseline", "stable_catalyst", "reversible_target_pathway")


def reversible_intervention() -> dict[str, Any]:
    return {
        "kind": "mechanism_family",
        "mode": "topology_family",
        "severity": 0.8,
        "topology_change": {
            "reaction_role": "primary_target_pathway",
            "transform_id": "reversible_target_pathway_stress_v1",
            "reverse_rate_constant_s_inv_at_full_severity": 0.000625,
        },
    }


def _reversible_mechanism_audit(world_seed: int) -> dict[str, Any]:
    intervention = MechanismFamilyIntervention(
        "topology_family",
        0.8,
        topology_change=TopologyFamilyChange(
            reaction_role="primary_target_pathway",
            transform_id="reversible_target_pathway_stress_v1",
            reverse_rate_constant_s_inv_at_full_severity=0.000625,
        ),
    )
    generator = DefaultScenarioGenerator()
    scenario = get_scenario("reaction-safety")
    baseline = generator.generate(scenario, world_seed)
    reversible = generator.generate(scenario, world_seed, (intervention.to_dict(),))
    repeated = generator.generate(scenario, world_seed, (intervention.to_dict(),))
    baseline_ids = {
        reaction.reaction_id for reaction in baseline.compiled_mechanism.network.reactions
    }
    reversible_ids = {
        reaction.reaction_id for reaction in reversible.compiled_mechanism.network.reactions
    }
    added = sorted(reversible_ids - baseline_ids)
    reverse = next(
        (
            reaction
            for reaction in reversible.compiled_mechanism.network.reactions
            if reaction.reaction_id == "family_reverse_channel"
        ),
        None,
    )
    return {
        "baseline_mechanism_hash": baseline.compiled_mechanism.mechanism_hash,
        "reversible_mechanism_hash": reversible.compiled_mechanism.mechanism_hash,
        "mechanism_hash_changed": (
            baseline.compiled_mechanism.mechanism_hash
            != reversible.compiled_mechanism.mechanism_hash
        ),
        "reversible_hash_deterministic": (
            reversible.compiled_mechanism.mechanism_hash
            == repeated.compiled_mechanism.mechanism_hash
        ),
        "added_reaction_count": len(added),
        "added_reaction_id": added[0] if len(added) == 1 else None,
        "opposite_stoichiometric_channel": bool(
            reverse is not None
            and reverse.reactants == {"P": 1.0}
            and reverse.products == {"A": 1.0}
        ),
    }


def _pairs(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    pairs = []
    for cell in registered_cells():
        selected = [row for row in rows if row.get("cell_id") == cell["cell_id"]]
        laws = {str(row["law_id"]): row for row in selected}
        if set(laws) != {"deactivating_baseline", "reversible_target_pathway"}:
            raise ValueError(f"cell {cell['cell_id']} lacks the reversible pair")
        pairs.append(
            {
                **cell,
                "baseline": laws["deactivating_baseline"],
                "reversible": laws["reversible_target_pathway"],
            }
        )
    return pairs


def _analyze_reversible(
    rows: Sequence[Mapping[str, Any]], mechanism: Mapping[str, Any]
) -> dict[str, Any]:
    pairs = _pairs(rows)
    completed = [
        pair
        for pair in pairs
        if pair["baseline"].get("status") == "completed"
        and pair["reversible"].get("status") == "completed"
    ]
    safe = [
        pair
        for pair in completed
        if pair["baseline"].get("safe") is True and pair["reversible"].get("safe") is True
    ]
    checks = {
        "fixed_execution_denominator": len(rows) == 54,
        "all_exact_replay": all(row.get("exact_replay") is True for row in rows),
        "zero_platform_failures": not any(row.get("status") == "platform_failure" for row in rows),
        "at_least_24_completed_pairs": len(completed) >= 24,
        "at_least_18_safe_pairs": len(safe) >= 18,
        "paired_action_plans": all(
            pair["baseline"].get("action_plan_sha256")
            == pair["reversible"].get("action_plan_sha256")
            for pair in pairs
        ),
        "paired_observation_noise": all(
            pair["baseline"].get("direct_noise_key_sha256")
            == pair["reversible"].get("direct_noise_key_sha256")
            for pair in pairs
        ),
        "mechanism_adds_one_reverse_reaction": (
            mechanism.get("added_reaction_count") == 1
            and mechanism.get("added_reaction_id") == "family_reverse_channel"
        ),
        "mechanism_hash_changes": mechanism.get("mechanism_hash_changed") is True,
        "mechanism_binding_deterministic": (mechanism.get("reversible_hash_deterministic") is True),
        "execution_mechanism_binding_matches": (
            mechanism.get("execution_mechanism_binding_matches") is True
        ),
        "opposite_stoichiometric_channel": (
            mechanism.get("opposite_stoichiometric_channel") is True
        ),
    }
    metric_reports: dict[str, dict[str, Any]] = {}
    for metric in DIRECT_METRICS:
        gate = max(0.05, 3.0 * float(DECLARED_SIGMA[metric]))
        cells = [
            {
                "cell_id": pair["cell_id"],
                "temperature_index": pair["temperature_index"],
                "duration_index": pair["duration_index"],
                "dose_index": pair["dose_index"],
                "both_safe": pair in safe,
                "signed_gap": float(pair["baseline"]["direct_metrics"][metric])
                - float(pair["reversible"]["direct_metrics"][metric]),
            }
            for pair in completed
        ]
        maximum = max((abs(row["signed_gap"]) for row in cells), default=0.0)
        metric_reports[metric] = {
            "effect_gate": gate,
            "max_absolute_paired_gap": maximum,
            "effect_passed": maximum >= gate,
            "cell_gaps": cells,
        }
    passing_metric_count = sum(report["effect_passed"] for report in metric_reports.values())
    supporting = {
        (
            int(cell["temperature_index"]),
            int(cell["duration_index"]),
            int(cell["dose_index"]),
            str(cell["cell_id"]),
        )
        for report in metric_reports.values()
        for cell in report["cell_gaps"]
        if cell["both_safe"] and abs(float(cell["signed_gap"])) >= float(report["effect_gate"])
    }
    separated = any(
        abs(left[0] - right[0]) + abs(left[1] - right[1]) + abs(left[2] - right[2]) >= 2
        for index, left in enumerate(sorted(supporting))
        for right in sorted(supporting)[index + 1 :]
    )
    accumulation = {}
    for metric in PRODUCT_METRICS:
        cells = metric_reports[metric]["cell_gaps"]
        shortest = [row["signed_gap"] for row in cells if row["duration_index"] == 0]
        longest = [row["signed_gap"] for row in cells if row["duration_index"] == 2]
        increase = fmean(longest) - fmean(shortest) if shortest and longest else -math.inf
        threshold = max(0.03, 2.0 * float(DECLARED_SIGMA[metric]))
        accumulation[metric] = {
            "increase": increase,
            "threshold": threshold,
            "passed": increase >= threshold,
        }
    best_baseline = max(
        safe,
        key=lambda pair: float(pair["baseline"]["direct_metrics"]["yield"]),
        default=None,
    )
    best_reversible = max(
        safe,
        key=lambda pair: float(pair["reversible"]["direct_metrics"]["yield"]),
        default=None,
    )
    stopping_changed = bool(
        best_baseline is not None
        and best_reversible is not None
        and int(best_baseline["duration_index"]) != int(best_reversible["duration_index"])
    )
    checks.update(
        {
            "at_least_two_direct_metrics_resolve_topology": passing_metric_count >= 2,
            "two_separated_safe_supporting_cells": separated,
            "support_spans_two_catalyst_doses": len({row[2] for row in supporting}) >= 2,
            "duration_accumulation_signature": any(
                report["passed"] for report in accumulation.values()
            ),
            "stopping_decision_changed": stopping_changed,
        }
    )
    return {
        "passed": all(checks.values()),
        "checks": checks,
        "failures": sorted(key for key, value in checks.items() if not value),
        "passing_metric_count": passing_metric_count,
        "minimum_candidate_effect": min(
            report["max_absolute_paired_gap"] for report in metric_reports.values()
        ),
        "metric_reports": metric_reports,
        "supporting_cells": [row[3] for row in sorted(supporting)],
        "accumulation_reports": accumulation,
        "best_baseline_cell": None if best_baseline is None else best_baseline["cell_id"],
        "best_reversible_cell": (None if best_reversible is None else best_reversible["cell_id"]),
        "mechanism_audit": dict(mechanism),
    }


def _candidate_projection(candidate_id: str, analysis: Mapping[str, Any]) -> dict[str, Any]:
    metric_reports = analysis.get("metric_reports") or {}
    effects = [
        float(report["max_absolute_paired_gap"])
        for report in metric_reports.values()
        if isinstance(report, Mapping)
    ]
    return {
        "candidate_id": candidate_id,
        "passed": analysis.get("passed") is True,
        "failures": list(analysis.get("failures", [])),
        "passing_metric_count": int(analysis.get("passing_metric_count", 0)),
        "minimum_maximum_public_effect": min(effects) if effects else 0.0,
        "checks": dict(analysis.get("checks", {})),
    }


def run(output: Path) -> dict[str, Any]:
    if output.exists():
        raise FileExistsError(f"refusing to overwrite {output}")
    if file_sha256(NOTE) != NOTE_SHA256:
        raise ValueError("RX-S authoring note digest changed")
    output.mkdir(parents=True)
    cells = registered_cells()
    total = len(CALIBRATION_SEEDS) * len(cells) * len(LAW_IDS)
    completed = 0
    exact_replays = 0
    world_results = []
    for index, world_seed in enumerate(CALIBRATION_SEEDS, start=1):
        world_id = f"RX-S-CAL{index:02d}"
        world_root = output / world_id
        world_root.mkdir()
        rows = []
        interventions = {
            "deactivating_baseline": [],
            "stable_catalyst": [stable_catalyst_intervention()],
            "reversible_target_pathway": [reversible_intervention()],
        }
        for cell in cells:
            for law_id in LAW_IDS:
                row = _execute_structural(
                    world_seed=world_seed,
                    cell=cell,
                    law_id=law_id,
                    output_root=world_root,
                    world_interventions=interventions[law_id],
                )
                rows.append(row)
                completed += 1
                exact_replays += int(row.get("exact_replay") is True)
                if completed % 9 == 0:
                    print(
                        json.dumps(
                            {
                                "event": "rx_structural_authoring_progress",
                                "completed": completed,
                                "total": total,
                                "world_id": world_id,
                            },
                            sort_keys=True,
                        ),
                        flush=True,
                    )
        write_json_atomic(world_root / "rows.json", rows)
        baseline_rows = [row for row in rows if row["law_id"] == "deactivating_baseline"]
        stable_rows = [row for row in rows if row["law_id"] == "stable_catalyst"]
        reversible_rows = [row for row in rows if row["law_id"] == "reversible_target_pathway"]
        stable_mechanism = _structural_mechanism_audit(world_seed)
        stable_mechanism["execution_mechanism_binding_matches"] = {
            row["mechanism_hash"] for row in stable_rows
        } == {stable_mechanism["stable_mechanism_hash"]}
        reversible_mechanism = _reversible_mechanism_audit(world_seed)
        reversible_mechanism["execution_mechanism_binding_matches"] = {
            row["mechanism_hash"] for row in reversible_rows
        } == {reversible_mechanism["reversible_mechanism_hash"]}
        stable = analyze_stable([*baseline_rows, *stable_rows], stable_mechanism)
        reversible = _analyze_reversible([*baseline_rows, *reversible_rows], reversible_mechanism)
        result = {
            "world_id": world_id,
            "world_seed": world_seed,
            "candidates": [
                _candidate_projection("stable_catalyst", stable),
                _candidate_projection("reversible_target_pathway", reversible),
            ],
        }
        write_json_atomic(world_root / "analysis.json", result)
        world_results.append(result)

    candidates = []
    for candidate_order, candidate_id in enumerate(
        ("stable_catalyst", "reversible_target_pathway")
    ):
        rows = [
            next(
                candidate
                for candidate in world["candidates"]
                if candidate["candidate_id"] == candidate_id
            )
            for world in world_results
        ]
        candidates.append(
            {
                "candidate_id": candidate_id,
                "candidate_order": candidate_order,
                "qualified_worlds": sum(row["passed"] for row in rows),
                "minimum_passing_metric_count": min(row["passing_metric_count"] for row in rows),
                "minimum_maximum_public_effect": min(
                    row["minimum_maximum_public_effect"] for row in rows
                ),
                "worlds": rows,
            }
        )
    ranked = sorted(
        candidates,
        key=lambda row: (
            -int(row["qualified_worlds"]),
            -int(row["minimum_passing_metric_count"]),
            -float(row["minimum_maximum_public_effect"]),
            int(row["candidate_order"]),
        ),
    )
    selected = ranked[0] if ranked[0]["qualified_worlds"] == len(CALIBRATION_SEEDS) else None
    summary: dict[str, Any] = {
        "schema_version": "chemworld-experiment-1-rx-structural-authoring-1.1.0",
        "formal_result": False,
        "provider_call_count": 0,
        "benchmark_denominator": False,
        "calibration_world_seeds": list(CALIBRATION_SEEDS),
        "planned_executions": total,
        "completed_executions": completed,
        "exact_replays": exact_replays,
        "selection_rule": (
            "qualified_worlds_then_resolving_metrics_then_public_effect_then_fixed_order"
        ),
        "candidates": ranked,
        "selected_candidate": None if selected is None else selected["candidate_id"],
        "note_sha256": NOTE_SHA256,
    }
    summary["summary_sha256"] = canonical_json_sha256(summary)
    write_json_atomic(output / "summary.json", summary)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    summary = run(args.output.resolve())
    print(json.dumps(summary, sort_keys=True), flush=True)
    return 0 if summary["selected_candidate"] is not None else 1


if __name__ == "__main__":
    raise SystemExit(main())
