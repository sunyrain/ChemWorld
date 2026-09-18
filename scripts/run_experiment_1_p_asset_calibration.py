#!/usr/bin/env python3
"""Run the frozen, provider-free Experiment 1 P asset calibration campaign."""

from __future__ import annotations

import argparse
import json
import subprocess
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from chemworld.data.logging import load_jsonl
from chemworld.eval.experiment_1_p_assets import structural_intervention
from chemworld.eval.provenance import canonical_json_sha256, file_sha256, write_json_atomic
from chemworld.eval.runner import run_agent
from chemworld.eval.verify import verify_records
from chemworld.eval.work_ii_truth import _FrozenTruthReplayAgent
from chemworld.tasks import get_task
from chemworld.world.scenario import DefaultScenarioGenerator, get_scenario

ROOT = Path(__file__).resolve().parents[1]
TASK_ID = "reaction-to-purification"
WORLD_IDS = tuple(f"P-W0{index}" for index in range(1, 6))
EXTRACTANTS = (0, 1, 2, 3)
REAGENT_LEVELS_MOL = (0.008, 0.012)
CELLS_PER_WORLD = len(EXTRACTANTS) * len(REAGENT_LEVELS_MOL)
PLANNED_CELLS = len(WORLD_IDS) * CELLS_PER_WORLD
PLANNED_EXECUTIONS = 2 * PLANNED_CELLS
PUBLIC_METRICS = (
    "purity",
    "recovery",
    "phase_ratio",
    "product_in_organic",
    "product_in_aqueous",
    "impurity_signal",
    "process_mass_balance_error",
)
FORK_METRICS = (
    "purity",
    "recovery",
    "product_in_organic",
    "product_in_aqueous",
    "impurity_signal",
)
FORBIDDEN_VISIBLE_TOKENS = (
    "mechanism_family",
    "world_intervention",
    "private_seed",
    "hidden_state",
    "evaluator_truth",
    "partition_composition_coupling_multiplier",
    "partition_composition_response_stress_v1",
    "constitutive_law_family",
)
MASS_BALANCE_ABSOLUTE_GATE = 1.0e-8
MINIMUM_PUBLIC_LAW_GAP = 0.02
MINIMUM_COMPOSITION_INTERACTION = 0.01
OBSERVATION_NOISE_NAMESPACE = "experiment-1-p-calibration-v1.0.0"
OBSERVATION_SEED_FORMULA = (
    "10000 + world_ordinal*1000 + reagent_index*100 + extractant"
)
REQUIRED_SOURCE_PATHS = {
    "scripts/run_experiment_1_p_asset_calibration.py",
    "src/chemworld/eval/experiment_1_p_assets.py",
    "src/chemworld/eval/provenance.py",
    "src/chemworld/runtime/phase_separation_services.py",
    "src/chemworld/world/phase_kernel.py",
    "src/chemworld/world/world_family.py",
    "src/chemworld/world/mechanism_family.py",
    "src/chemworld/world/scenario.py",
    "src/chemworld/world/instruments.py",
    "src/chemworld/envs/observation_noise.py",
    "src/chemworld/envs/chemworld_env.py",
    "src/chemworld/eval/runner.py",
    "src/chemworld/eval/verify.py",
    "src/chemworld/eval/work_ii_truth.py",
    "src/chemworld/data/logging.py",
    "src/chemworld/tasks.py",
}


def _observation_seed(world_id: str, reagent_index: int, extractant: int) -> int:
    try:
        world_ordinal = WORLD_IDS.index(world_id) + 1
    except ValueError as error:
        raise ValueError(f"P calibration seed requested for unknown World: {world_id}") from error
    if reagent_index not in range(len(REAGENT_LEVELS_MOL)):
        raise ValueError("P calibration seed requested for unknown reagent level")
    if extractant not in EXTRACTANTS:
        raise ValueError("P calibration seed requested for unknown extractant")
    return 10_000 + world_ordinal * 1_000 + reagent_index * 100 + extractant


def _self_hash(value: Mapping[str, Any], field: str) -> str:
    return canonical_json_sha256({key: item for key, item in value.items() if key != field})


def _bound_json(binding: Mapping[str, Any], label: str) -> dict[str, Any]:
    target = ROOT / str(binding.get("path", ""))
    if not target.is_file() or file_sha256(target) != binding.get("sha256"):
        raise ValueError(f"P calibration {label} binding changed")
    value = json.loads(target.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"P calibration {label} is not a JSON object")
    return value


def load_calibration_contract(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("schema_version") != "chemworld-experiment-1-p-calibration-contract-1.0.0":
        raise ValueError("P calibration contract schema changed")
    if value.get("status") != "frozen_before_calibration":
        raise ValueError("P calibration contract is not frozen")
    if value.get("formal_qualification_authorized") is not False:
        raise ValueError("P calibration contract must not authorize formal qualification")
    if value.get("participant_execution_authorized") is not False:
        raise ValueError("P calibration contract must not authorize participant execution")
    if value.get("contract_sha256") != _self_hash(value, "contract_sha256"):
        raise ValueError("P calibration contract self-hash changed")

    note = value.get("calibration_note", {})
    note_path = ROOT / str(note.get("path", ""))
    if not note_path.is_file() or file_sha256(note_path) != note.get("sha256"):
        raise ValueError("P calibration note binding changed")
    manifest = _bound_json(value.get("asset_manifest", {}), "asset manifest")
    if manifest.get("manifest_sha256") != _self_hash(manifest, "manifest_sha256"):
        raise ValueError("P asset manifest self-hash changed")
    asset_contract = _bound_json(value.get("asset_contract", {}), "asset contract")
    if asset_contract.get("formal_qualification_authorized") is not False:
        raise ValueError("P asset contract unexpectedly authorizes formal qualification")

    source = value.get("source_binding", {})
    source_commit = str(source.get("source_commit", ""))
    subprocess.run(
        ["git", "merge-base", "--is-ancestor", source_commit, "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    source_rows = source.get("files", [])
    if {str(row.get("path")) for row in source_rows} != REQUIRED_SOURCE_PATHS:
        raise ValueError("P calibration execution source closure changed")
    for row in source_rows:
        target = ROOT / str(row["path"])
        if not target.is_file() or file_sha256(target) != row.get("sha256"):
            raise ValueError(f"P calibration source binding changed: {row.get('path')}")

    design = value.get("design", {})
    if tuple(design.get("world_ids", ())) != WORLD_IDS:
        raise ValueError("P calibration World coverage changed")
    if tuple(int(item) for item in design.get("extractants", ())) != EXTRACTANTS:
        raise ValueError("P calibration extractant domain changed")
    if tuple(float(item) for item in design.get("reagent_levels_mol", ())) != REAGENT_LEVELS_MOL:
        raise ValueError("P calibration reagent domain changed")
    if int(design.get("planned_cells", -1)) != PLANNED_CELLS:
        raise ValueError("P calibration cell denominator changed")
    if int(design.get("planned_executions", -1)) != PLANNED_EXECUTIONS:
        raise ValueError("P calibration execution denominator changed")
    if design.get("paired_noise_policy") != "same_cell_same_seed_parent_child":
        raise ValueError("P calibration paired-noise policy changed")
    if design.get("observation_seed_formula") != OBSERVATION_SEED_FORMULA:
        raise ValueError("P calibration observation-seed formula changed")
    if value.get("observation_noise_namespace") != OBSERVATION_NOISE_NAMESPACE:
        raise ValueError("P calibration observation-noise namespace changed")
    cells = value.get("cells", [])
    if not isinstance(cells, list) or len(cells) != PLANNED_CELLS:
        raise ValueError("P calibration cells have the wrong denominator")
    expected_ids = set()
    expected_coordinates: set[tuple[str, int]] = set()
    for world_id in WORLD_IDS:
        for reagent_index, reagent_mol in enumerate(REAGENT_LEVELS_MOL):
            for extractant in EXTRACTANTS:
                cell_id = f"{world_id}-r{reagent_index}-x{extractant}"
                expected_seed = _observation_seed(world_id, reagent_index, extractant)
                expected_ids.add(cell_id)
                expected_coordinates.add((cell_id, expected_seed))
                matches = [row for row in cells if row.get("cell_id") == cell_id]
                if len(matches) != 1:
                    raise ValueError(f"P calibration cell coverage changed: {cell_id}")
                row = matches[0]
                if row.get("world_id") != world_id:
                    raise ValueError(f"P calibration cell World mismatch: {cell_id}")
                if int(row.get("extractant", -1)) != extractant:
                    raise ValueError(f"P calibration cell extractant mismatch: {cell_id}")
                if float(row.get("reagent_mol", -1.0)) != reagent_mol:
                    raise ValueError(f"P calibration cell reagent mismatch: {cell_id}")
                seed = row.get("observation_seed")
                if isinstance(seed, bool) or not isinstance(seed, int) or seed < 0:
                    raise ValueError(f"P calibration observation seed invalid: {cell_id}")
                if seed != expected_seed:
                    raise ValueError(f"P calibration observation seed changed: {cell_id}")
    if {str(row.get("cell_id")) for row in cells} != expected_ids:
        raise ValueError("P calibration contains an unregistered cell")
    observed_coordinates = {
        (str(row.get("cell_id")), int(row.get("observation_seed", -1))) for row in cells
    }
    if observed_coordinates != expected_coordinates:
        raise ValueError("P calibration cell-to-observation-seed mapping changed")
    if len({coordinate[1] for coordinate in observed_coordinates}) != PLANNED_CELLS:
        raise ValueError("P calibration observation seeds are not unique")
    gates = value.get("gates", {})
    expected_gates = {
        "public_metrics": list(PUBLIC_METRICS),
        "fork_metrics": list(FORK_METRICS),
        "mass_balance_absolute_gate": MASS_BALANCE_ABSOLUTE_GATE,
        "minimum_public_law_gap": MINIMUM_PUBLIC_LAW_GAP,
        "minimum_composition_interaction": MINIMUM_COMPOSITION_INTERACTION,
        "all_worlds_required": True,
    }
    if gates != expected_gates:
        raise ValueError("P calibration gates changed")
    if tuple(value.get("forbidden_visible_tokens", ())) != FORBIDDEN_VISIBLE_TOKENS:
        raise ValueError("P calibration leakage denylist changed")
    return value


def frozen_action_plan(cell: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {"operation": "add_solvent", "volume_L": 0.028, "solvent": 2},
        {"operation": "add_reagent", "amount_mol": float(cell["reagent_mol"])},
        {"operation": "add_catalyst", "catalyst_amount_mol": 0.00025, "catalyst": 1},
        {
            "operation": "heat",
            "target_temperature_K": 385.0,
            "duration_s": 1500.0,
            "stirring_speed_rpm": 720.0,
        },
        {"operation": "quench"},
        {"operation": "add_phase", "phase": "aqueous", "volume_L": 0.012},
        {
            "operation": "add_extractant",
            "extractant": int(cell["extractant"]),
            "volume_L": 0.018,
        },
        {"operation": "mix", "duration_s": 240.0, "stirring_speed_rpm": 850.0},
        {"operation": "settle", "duration_s": 420.0},
        {"operation": "measure", "instrument": "hplc"},
        {"operation": "separate_phase", "target_phase": "organic"},
        {"operation": "terminate"},
        {"operation": "measure", "instrument": "final_assay"},
    ]


def _public_projection(records: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    keys = (
        "observation",
        "observed_mask",
        "processed_estimate",
        "raw_signal",
        "agent_visible_observation",
        "agent_view",
    )
    return [{key: row.get(key) for key in keys} for row in records]


def _leakage_findings(records: Sequence[Mapping[str, Any]]) -> list[dict[str, str]]:
    findings = []

    def inspect(value: object, path: str) -> None:
        if isinstance(value, Mapping):
            for key, child in value.items():
                key_text = str(key)
                for token in FORBIDDEN_VISIBLE_TOKENS:
                    if token.casefold() in key_text.casefold():
                        findings.append({"path": f"{path}.{key_text}", "token": token})
                inspect(child, f"{path}.{key_text}")
        elif isinstance(value, Sequence) and not isinstance(value, str | bytes):
            for index, child in enumerate(value):
                inspect(child, f"{path}[{index}]")
        elif isinstance(value, str):
            for token in FORBIDDEN_VISIBLE_TOKENS:
                if token.casefold() in value.casefold():
                    findings.append({"path": path, "token": token})

    inspect(_public_projection(records), "participant_visible")
    return sorted(findings, key=lambda row: (row["token"], row["path"]))


def _final_metrics(records: Sequence[Mapping[str, Any]]) -> dict[str, float]:
    finals = [
        row
        for row in records
        if row.get("transaction_status") == "committed"
        and row.get("operation_type") == "measure"
        and row.get("instrument") == "final_assay"
    ]
    if len(finals) != 1 or not isinstance(finals[0].get("processed_estimate"), Mapping):
        raise ValueError("P calibration execution lacks one committed final assay")
    estimate = finals[0]["processed_estimate"]
    metrics = {}
    for metric in PUBLIC_METRICS:
        number = estimate.get(metric)
        if isinstance(number, bool) or not isinstance(number, int | float):
            raise ValueError(f"P calibration final assay lacks finite {metric}")
        metrics[metric] = float(number)
    return metrics


def _truth_binding(
    records: Sequence[Mapping[str, Any]], world_seed: int, interventions: list[dict[str, Any]]
) -> dict[str, Any]:
    instance = DefaultScenarioGenerator().generate(
        get_scenario(TASK_ID), world_seed, tuple(interventions)
    )
    expected_world_hash = instance.initial_state.metadata.get("world_family_intervention_hash")
    expected_mechanism_hash = instance.initial_state.metadata.get(
        "mechanism_family_intervention_hash"
    )
    observed_world_hashes = {
        row.get("world_family_intervention_hash")
        for row in records
        if row.get("world_family_intervention_hash") is not None
    }
    observed_mechanism_hashes = {
        row.get("mechanism_family_intervention_hash")
        for row in records
        if row.get("mechanism_family_intervention_hash") is not None
    }
    observed_world_ids = {
        str(row["world_id"]) for row in records if isinstance(row.get("world_id"), str)
    }
    expected_world_hashes = (
        {expected_world_hash} if isinstance(expected_world_hash, str) else set()
    )
    expected_mechanism_hashes = (
        {expected_mechanism_hash} if isinstance(expected_mechanism_hash, str) else set()
    )
    passed = _truth_sets_match(
        expected_world_id=instance.parameters.world_id,
        expected_world_hashes=expected_world_hashes,
        expected_mechanism_hashes=expected_mechanism_hashes,
        observed_world_ids=observed_world_ids,
        observed_world_hashes=observed_world_hashes,
        observed_mechanism_hashes=observed_mechanism_hashes,
    )
    return {
        "passed": passed,
        "private_world_id": instance.parameters.world_id,
        "observed_private_world_ids": sorted(observed_world_ids),
        "expected_world_family_intervention_hash": expected_world_hash,
        "observed_world_family_intervention_hashes": sorted(observed_world_hashes),
        "expected_mechanism_family_intervention_hash": expected_mechanism_hash,
        "observed_mechanism_family_intervention_hashes": sorted(
            observed_mechanism_hashes
        ),
    }


def _truth_sets_match(
    *,
    expected_world_id: str,
    expected_world_hashes: set[str],
    expected_mechanism_hashes: set[str],
    observed_world_ids: set[str],
    observed_world_hashes: set[str],
    observed_mechanism_hashes: set[str],
) -> bool:
    return (
        observed_world_ids == {expected_world_id}
        and observed_world_hashes == expected_world_hashes
        and observed_mechanism_hashes == expected_mechanism_hashes
    )


def _portable_output_path(path: Path, output_root: Path) -> str:
    try:
        relative = path.resolve().relative_to(output_root.resolve())
    except ValueError as error:
        raise ValueError("P calibration artifact path escapes the output root") from error
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError("P calibration artifact path is not output-relative")
    return relative.as_posix()


def _execute(
    *,
    asset_contract: Mapping[str, Any],
    world: Mapping[str, Any],
    cell: Mapping[str, Any],
    law_id: str,
    namespace: str,
    output: Path,
) -> dict[str, Any]:
    actions = frozen_action_plan(cell)
    interventions = [dict(item) for item in world["world_interventions"]]
    if law_id == "composition_coupled":
        interventions.append(structural_intervention(asset_contract))
    execution_root = output / str(cell["cell_id"]) / law_id
    execution_root.mkdir(parents=True)
    trajectory = execution_root / "trajectory.jsonl"
    records: list[dict[str, Any]] = []
    failure = None
    replay = None
    metrics = None
    leakage = []
    truth = None
    try:
        run_agent(
            env_id=get_task(TASK_ID).env_id,
            agent=_FrozenTruthReplayAgent(actions),
            world_split=str(get_task(TASK_ID).world_split),
            budget=len(actions),
            objective="balanced",
            seed=int(world["world_seed"]),
            agent_seed=0,
            observation_seed=int(cell["observation_seed"]),
            task_id=TASK_ID,
            output_path=trajectory,
            budget_override=len(actions),
            episode_mode_override="single_experiment",
            observation_noise_mode="keyed",
            observation_noise_namespace=namespace,
            world_interventions=interventions,
        )
        records = load_jsonl(trajectory)
        replay = verify_records(
            records, tolerance=0.0, world_interventions=interventions
        ).to_dict()
        metrics = _final_metrics(records)
        leakage = _leakage_findings(records)
        truth = _truth_binding(records, int(world["world_seed"]), interventions)
    except Exception as error:
        failure = {"type": type(error).__name__, "message": str(error)[:1000]}
        if trajectory.is_file() and not records:
            records = load_jsonl(trajectory)
        if records:
            leakage = _leakage_findings(records)
    completed = bool(
        failure is None
        and records
        and all(row.get("transaction_status") == "committed" for row in records)
    )
    mass_balance = None if metrics is None else abs(metrics["process_mass_balance_error"])
    receipt: dict[str, Any] = {
        "cell_id": cell["cell_id"],
        "world_id": cell["world_id"],
        "law_id": law_id,
        "status": "completed" if completed else "failed",
        "failure": failure,
        "public_metrics": metrics,
        "action_plan_sha256": canonical_json_sha256(actions),
        "observation_seed": int(cell["observation_seed"]),
        "observation_noise_namespace": namespace,
        "observation_coordinate_sha256": canonical_json_sha256(
            {"namespace": namespace, "seed": int(cell["observation_seed"])}
        ),
        "exact_replay": replay is not None and replay.get("verified") is True,
        "truth_binding": truth,
        "participant_visible_leakage_findings": leakage,
        "mass_balance_absolute_error": mass_balance,
        "mass_balance_passed": (
            mass_balance is not None and mass_balance <= MASS_BALANCE_ABSOLUTE_GATE
        ),
        "trajectory": (
            {
                "path": _portable_output_path(trajectory, output),
                "path_scope": "calibration_output_root",
                "sha256": file_sha256(trajectory),
            }
            if trajectory.is_file()
            else None
        ),
    }
    receipt["receipt_sha256"] = canonical_json_sha256(receipt)
    write_json_atomic(execution_root / "receipt.json", receipt)
    return receipt


def _analyze(receipts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    pairs: dict[str, dict[str, Mapping[str, Any]]] = {}
    for row in receipts:
        pairs.setdefault(str(row["cell_id"]), {})[str(row["law_id"])] = row
    fork_rows = []
    for cell_id, laws in sorted(pairs.items()):
        parent = laws.get("constant_K", {})
        child = laws.get("composition_coupled", {})
        gaps = {
            metric: (
                abs(
                    float(child["public_metrics"][metric])
                    - float(parent["public_metrics"][metric])
                )
                if parent.get("public_metrics") is not None
                and child.get("public_metrics") is not None
                else None
            )
            for metric in FORK_METRICS
        }
        fork_rows.append(
            {
                "cell_id": cell_id,
                "world_id": parent.get("world_id") or child.get("world_id"),
                "paired_action_plan": parent.get("action_plan_sha256")
                == child.get("action_plan_sha256"),
                "paired_observation_coordinate": parent.get(
                    "observation_coordinate_sha256"
                )
                == child.get("observation_coordinate_sha256"),
                "absolute_public_metric_gaps": gaps,
                "maximum_public_metric_gap": max(
                    (value for value in gaps.values() if value is not None), default=0.0
                ),
            }
        )
    world_reports = []
    for world_id in WORLD_IDS:
        rows = [row for row in fork_rows if row["world_id"] == world_id]
        purity_by_extractant: dict[int, dict[int, float]] = {}
        for row in rows:
            _, reagent_token, extractant_token = str(row["cell_id"]).rsplit("-", 2)
            reagent_index = int(reagent_token[1:])
            extractant = int(extractant_token[1:])
            purity_by_extractant.setdefault(extractant, {})[reagent_index] = float(
                row["absolute_public_metric_gaps"]["purity"] or 0.0
            )
        maximum_interaction = max(
            (
                abs(values[1] - values[0])
                for values in purity_by_extractant.values()
                if set(values) == {0, 1}
            ),
            default=0.0,
        )
        maximum_gap = max((row["maximum_public_metric_gap"] for row in rows), default=0.0)
        world_reports.append(
            {
                "world_id": world_id,
                "pair_count": len(rows),
                "maximum_public_metric_gap": maximum_gap,
                "maximum_composition_interaction": maximum_interaction,
                "passed": (
                    len(rows) == CELLS_PER_WORLD
                    and maximum_gap >= MINIMUM_PUBLIC_LAW_GAP
                    and maximum_interaction >= MINIMUM_COMPOSITION_INTERACTION
                ),
            }
        )
    checks = {
        "fixed_execution_denominator": len(receipts) == PLANNED_EXECUTIONS,
        "all_completed": all(row.get("status") == "completed" for row in receipts),
        "all_exact_replay": all(row.get("exact_replay") is True for row in receipts),
        "all_truth_bound": all(
            isinstance(row.get("truth_binding"), Mapping)
            and row["truth_binding"].get("passed") is True
            for row in receipts
        ),
        "participant_visible_leakage_free": all(
            not row.get("participant_visible_leakage_findings") for row in receipts
        ),
        "all_mass_balances_pass": all(
            row.get("mass_balance_passed") is True for row in receipts
        ),
        "all_action_plans_paired": all(row["paired_action_plan"] for row in fork_rows),
        "all_noise_coordinates_paired": all(
            row["paired_observation_coordinate"] for row in fork_rows
        ),
        "all_five_world_fork_statistics_pass": all(row["passed"] for row in world_reports),
    }
    return {
        "passed": all(checks.values()),
        "checks": checks,
        "failures": sorted(key for key, passed in checks.items() if not passed),
        "fork_rows": fork_rows,
        "world_reports": world_reports,
    }


def run(contract_path: Path, output: Path) -> dict[str, Any]:
    if output.exists():
        raise FileExistsError(f"refusing to overwrite {output}")
    contract = load_calibration_contract(contract_path)
    asset_contract_path = ROOT / str(contract["asset_contract"]["path"])
    asset_contract = json.loads(asset_contract_path.read_text(encoding="utf-8"))
    worlds_by_id = {str(row["world_id"]): row for row in asset_contract["worlds"]}
    output.mkdir(parents=True)
    receipts = []
    for cell in contract["cells"]:
        world = worlds_by_id[str(cell["world_id"])]
        for law_id in ("constant_K", "composition_coupled"):
            receipts.append(
                _execute(
                    asset_contract=asset_contract,
                    world=world,
                    cell=cell,
                    law_id=law_id,
                    namespace=str(contract["observation_noise_namespace"]),
                    output=output,
                )
            )
            print(
                json.dumps(
                    {
                        "event": "p_calibration_progress",
                        "completed": len(receipts),
                        "total": PLANNED_EXECUTIONS,
                    },
                    sort_keys=True,
                ),
                flush=True,
            )
    analysis = _analyze(receipts)
    summary: dict[str, Any] = {
        "schema_version": "chemworld-experiment-1-p-calibration-summary-1.0.0",
        "formal_qualification_result": False,
        "provider_call_count": 0,
        "planned_executions": PLANNED_EXECUTIONS,
        "completed_executions": len(receipts),
        "calibration_status": "pass" if analysis["passed"] else "fail",
        "analysis": analysis,
        "contract_sha256": file_sha256(contract_path),
        "receipts": receipts,
    }
    summary["summary_sha256"] = canonical_json_sha256(summary)
    write_json_atomic(output / "summary.json", summary)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    summary = run(args.contract.resolve(), args.output.resolve())
    print(json.dumps(summary, sort_keys=True), flush=True)
    return 0 if summary["calibration_status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
