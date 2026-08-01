"""Run the frozen G2 known/unknown/mismatched Codex matrix.

The existing two-arm runner remains unchanged for the historical opaque/nominal
matrix.  This runner binds the same Codex cell implementation to the three-arm
protocol: opaque codes, correct nominal properties, and agent-blind solvent
misindexing.  ``--dry-run`` validates all 15 scheduled cells without probing
the external provider.
"""

from __future__ import annotations

import argparse
import json
import statistics
from collections.abc import Mapping, Sequence
from copy import deepcopy
from pathlib import Path
from typing import Any

try:
    from scripts import run_g2_autonomous_material_matrix as matrix
except ModuleNotFoundError:  # direct ``python scripts/...`` execution
    import run_g2_autonomous_material_matrix as matrix

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = (
    ROOT
    / "configs/benchmark/"
    "g2_autonomous_electrochemical_material_3x3_v0.1_dev.json"
)
DEFAULT_OUTPUT_ROOT = (
    ROOT
    / "runs/development/"
    "g2-autonomous-electrochemical-material-3x3-codex-lean-v1"
)
ARMS = ("unknown", "known", "mismatched")
CONDITION_IDS = (
    "opaque_codes",
    "anonymous_nominal_properties",
    "anonymous_misindexed_properties",
)
RUNNER_VERSION = "chemworld-g2-autonomous-material-triarm-runner-0.2"


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate all tri-arm environments and pair invariants without Codex.",
    )
    parser.add_argument(
        "--allow-external-provider",
        action="store_true",
        help="Required opt-in for real Codex execution.",
    )
    parser.add_argument(
        "--world-seeds",
        help="Optional comma-separated subset of frozen seeds for staged execution.",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume a validated completed-cell prefix without overwriting artifacts.",
    )
    parser.add_argument(
        "--provider-id",
        default="wellau",
        help="Codex CLI model provider id (default: wellau).",
    )
    parser.add_argument(
        "--provider-name",
        default="WellAU",
        help="Codex CLI provider display name.",
    )
    parser.add_argument(
        "--provider-base-url",
        default="https://api.wellau.com/v1",
        help="OpenAI-compatible provider base URL.",
    )
    parser.add_argument(
        "--provider-env-key",
        default="WELLAU_API_KEY",
        help="Environment variable name consumed by the provider.",
    )
    return parser


def _load_protocol(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("tri-arm protocol must be a JSON object")
    if payload.get("schema_version") != (
        "chemworld-g2-autonomous-material-triarm-matrix-0.1"
    ):
        raise ValueError("unsupported tri-arm autonomous material protocol")
    task = payload.get("task")
    if not isinstance(task, dict):
        raise ValueError("tri-arm protocol task is required")
    if task.get("world_seeds") != [0, 1, 2, 3, 4]:
        raise ValueError("tri-arm protocol world_seeds must be frozen to [0,1,2,3,4]")
    conditions = payload.get("conditions")
    if not isinstance(conditions, list):
        raise ValueError("tri-arm protocol conditions must be a list")
    observed_ids = [
        str(item.get("condition_id"))
        for item in conditions
        if isinstance(item, Mapping)
    ]
    if tuple(sorted(observed_ids)) != tuple(sorted(CONDITION_IDS)):
        raise ValueError(
            "tri-arm protocol must contain exactly opaque, nominal, and misindexed conditions"
        )
    observed_arms = [
        str(item.get("arm_id"))
        for item in conditions
        if isinstance(item, Mapping)
    ]
    if tuple(sorted(observed_arms)) != tuple(sorted(ARMS)):
        raise ValueError(f"tri-arm protocol arms must be {list(ARMS)}")
    schedule = payload.get("execution_order", {}).get("order_by_seed_mod_3")
    if not isinstance(schedule, Mapping):
        raise ValueError("tri-arm protocol requires order_by_seed_mod_3")
    for key in ("0", "1", "2"):
        if sorted(schedule.get(key, [])) != sorted(ARMS):
            raise ValueError(f"execution_order[{key}] must contain all three arms")
    return payload


def _conditions(protocol: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(item["arm_id"]): deepcopy(dict(item))
        for item in protocol["conditions"]
    }


def _scheduled_cells(
    protocol: Mapping[str, Any],
    world_seeds: Sequence[int] | None = None,
) -> list[dict[str, Any]]:
    conditions = _conditions(protocol)
    schedule = protocol["execution_order"]["order_by_seed_mod_3"]
    cells: list[dict[str, Any]] = []
    ordinal = 0
    seeds = (
        [int(seed) for seed in protocol["task"]["world_seeds"]]
        if world_seeds is None
        else [int(seed) for seed in world_seeds]
    )
    frozen_seeds = {int(seed) for seed in protocol["task"]["world_seeds"]}
    if any(seed not in frozen_seeds for seed in seeds):
        raise ValueError("world_seeds must be a subset of the frozen protocol seeds")
    if len(set(seeds)) != len(seeds):
        raise ValueError("world_seeds must not contain duplicates")
    for seed in seeds:
        order = schedule[str(int(seed) % 3)]
        for within_world_order, arm in enumerate(order, start=1):
            ordinal += 1
            condition = conditions[str(arm)]
            cells.append(
                {
                    "cell_id": f"cell-{ordinal:02d}",
                    "world_seed": int(seed),
                    "condition_id": str(condition["condition_id"]),
                    "arm": str(arm),
                    "within_world_order": within_world_order,
                    "material_information": deepcopy(
                        dict(condition["material_information"])
                    ),
                }
            )
    return cells


def _environment_contract(item: Mapping[str, Any]) -> Mapping[str, Any]:
    contract = item.get("environment_contract")
    if not isinstance(contract, Mapping):
        raise ValueError("tri-arm cell is missing environment_contract")
    return contract


def _triarm_audits(
    cells: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    grouped: dict[int, list[Mapping[str, Any]]] = {}
    for item in cells:
        cell = item.get("cell") if isinstance(item.get("cell"), Mapping) else item
        grouped.setdefault(int(cell["world_seed"]), []).append(item)
    audits: list[dict[str, Any]] = []
    identity_keys = (
        "world_id",
        "mechanism_hash",
        "electrochemical_material_family_id",
        "electrochemical_material_family_sha256",
        "electrochemical_material_instance_sha256",
        "observation_noise_mode",
        "observation_noise_namespace",
    )
    public_keys = (
        "task_contract_hash",
        "runtime_profile_hash",
        "scoring_contract_hash",
        "observation_contract_hash",
        "workflow_mode",
    )
    for seed, rows in sorted(grouped.items()):
        if len(rows) != 3:
            audits.append(
                {
                    "world_seed": seed,
                    "conditions": [
                        str(
                            (
                                row.get("cell")
                                if isinstance(row.get("cell"), Mapping)
                                else row
                            ).get("condition_id")
                        )
                        for row in rows
                    ],
                    "material_information": [],
                    "invariants": {},
                    "incomplete": True,
                    "passed": False,
                }
            )
            continue
        first_contract = _environment_contract(rows[0])
        first_identity = first_contract.get("evaluator_identity", {})
        first_public = first_contract.get("public_contract", {})
        invariants: dict[str, bool] = {}
        for key in identity_keys:
            invariants[f"evaluator_identity.{key}"] = all(
                _environment_contract(row).get("evaluator_identity", {}).get(key)
                == first_identity.get(key)
                for row in rows
            )
        for key in public_keys:
            invariants[f"public_contract.{key}"] = all(
                _environment_contract(row).get("public_contract", {}).get(key)
                == first_public.get(key)
                for row in rows
            )
        condition_ids = [
            str(
                (row.get("cell") if isinstance(row.get("cell"), Mapping) else row)[
                    "condition_id"
                ]
            )
            for row in rows
        ]
        material_information = [
            deepcopy(
                dict(
                    (row.get("cell") if isinstance(row.get("cell"), Mapping) else row)[
                        "material_information"
                    ]
                )
            )
            for row in rows
        ]
        audits.append(
            {
                "world_seed": seed,
                "conditions": condition_ids,
                "material_information": material_information,
                "invariants": invariants,
                "passed": all(invariants.values())
                and sorted(condition_ids) == sorted(CONDITION_IDS),
            }
        )
    return audits


def _summary(values: Sequence[float]) -> dict[str, Any]:
    numeric = [float(value) for value in values]
    return {
        "count": len(numeric),
        "mean": statistics.fmean(numeric) if numeric else None,
        "minimum": min(numeric) if numeric else None,
        "maximum": max(numeric) if numeric else None,
        "values": numeric,
    }


def _cell_metrics(
    result: Mapping[str, Any],
    *,
    operation_limit: int,
    target_batches: int,
) -> dict[str, Any]:
    behavior = result.get("behavior", {})
    scores = [
        float(value)
        for value in behavior.get("terminal_scores", [])
        if isinstance(value, int | float) and not isinstance(value, bool)
    ]
    experiments = behavior.get("experiments", [])
    solvents: list[int] = []
    if isinstance(experiments, list):
        for experiment in experiments:
            if not isinstance(experiment, Mapping):
                continue
            choices = experiment.get("solvent_choices", [])
            if isinstance(choices, list):
                solvents.extend(
                    int(choice)
                    for choice in choices
                    if isinstance(choice, int) and not isinstance(choice, bool)
                )
    split = max(len(scores) // 2, 1)
    late_minus_early = None
    if len(scores) >= 2:
        late_minus_early = statistics.fmean(scores[split:]) - statistics.fmean(
            scores[:split]
        )
    operation_count = int(behavior.get("operation_count", 0))
    return {
        "world_seed": int(result.get("world_seed", result.get("cell", {}).get("world_seed", 0))),
        "arm": str(result.get("arm", result.get("condition_id", ""))),
        "condition_id": str(result.get("condition_id", "")),
        "best_final_score": (
            float(behavior["best_final_score"])
            if isinstance(behavior.get("best_final_score"), int | float)
            and not isinstance(behavior.get("best_final_score"), bool)
            else None
        ),
        "mean_final_score": (
            float(behavior["mean_final_score"])
            if isinstance(behavior.get("mean_final_score"), int | float)
            and not isinstance(behavior.get("mean_final_score"), bool)
            else None
        ),
        "incumbent_auc_per_operation": (
            float(behavior["incumbent_auc_per_operation"])
            if isinstance(behavior.get("incumbent_auc_per_operation"), int | float)
            and not isinstance(behavior.get("incumbent_auc_per_operation"), bool)
            else None
        ),
        "first_solvent": solvents[0] if solvents else None,
        "last_solvent": solvents[-1] if solvents else None,
        "late_minus_early_score": late_minus_early,
        "operation_count": operation_count,
        "operation_utilization": (
            operation_count / operation_limit if operation_limit else None
        ),
        "invalid_operation_count": int(behavior.get("invalid_operation_count", 0)),
        "resource_rejection_count": int(behavior.get("resource_rejection_count", 0)),
        "lifecycle_completed": result.get("run_status") == "completed"
        and int(behavior.get("closed_batch_count", 0))
        == target_batches,
        "exact_replay_verified": result.get("exact_replay_verified") is True,
    }


def _paired_difference(
    left: Mapping[int, Mapping[str, Any]],
    right: Mapping[int, Mapping[str, Any]],
    field: str,
) -> dict[str, Any]:
    seeds = sorted(set(left) & set(right))
    values = [
        float(left[seed][field]) - float(right[seed][field])
        for seed in seeds
        if left[seed].get(field) is not None and right[seed].get(field) is not None
    ]
    return {
        **_summary(values),
        "paired_world_seeds": seeds,
        "win_tie_loss": {
            "wins": sum(value > 1.0e-12 for value in values),
            "ties": sum(abs(value) <= 1.0e-12 for value in values),
            "losses": sum(value < -1.0e-12 for value in values),
        },
    }


def _triarm_analysis(
    results: Sequence[Mapping[str, Any]],
    *,
    operation_limit: int,
    target_batches: int,
) -> dict[str, Any] | None:
    metrics = [
        _cell_metrics(
            result,
            operation_limit=operation_limit,
            target_batches=target_batches,
        )
        for result in results
        if result.get("behavior")
    ]
    if not metrics:
        return None
    # The runner uses condition ids as `arm` in the durable cell summaries;
    # normalize them to the human arm names before aggregating.
    condition_to_arm = {
        "opaque_codes": "unknown",
        "anonymous_nominal_properties": "known",
        "anonymous_misindexed_properties": "mismatched",
    }
    normalized: dict[str, dict[int, dict[str, Any]]] = {arm: {} for arm in ARMS}
    for row in metrics:
        arm = row["arm"] if row["arm"] in ARMS else condition_to_arm.get(row["condition_id"])
        if arm in normalized:
            normalized[arm][int(row["world_seed"])] = row
    arm_summary: dict[str, Any] = {}
    for arm in ARMS:
        rows = list(normalized[arm].values())
        arm_summary[arm] = {
            "cell_count": len(rows),
            "best_final_score": _summary(
                [row["best_final_score"] for row in rows if row["best_final_score"] is not None]
            ),
            "mean_final_score": _summary(
                [row["mean_final_score"] for row in rows if row["mean_final_score"] is not None]
            ),
            "incumbent_auc_per_operation": _summary(
                [
                    row["incumbent_auc_per_operation"]
                    for row in rows
                    if row["incumbent_auc_per_operation"] is not None
                ]
            ),
            "first_solvent_values": [row["first_solvent"] for row in rows],
            "last_solvent_values": [row["last_solvent"] for row in rows],
            "late_minus_early_score": _summary(
                [
                    row["late_minus_early_score"]
                    for row in rows
                    if row["late_minus_early_score"] is not None
                ]
            ),
            "lifecycle_completion_rate": statistics.fmean(
                [float(row["lifecycle_completed"]) for row in rows]
            )
            if rows
            else None,
        }
    mismatch_rows = list(normalized["mismatched"].values())
    known_rows = list(normalized["known"].values())
    manipulation_rate = statistics.fmean(
        [
            float(row["first_solvent"] == 3)
            for row in mismatch_rows
            if row["first_solvent"] is not None
        ]
    ) if mismatch_rows else None
    known_rate = statistics.fmean(
        [float(row["first_solvent"] == 1) for row in known_rows if row["first_solvent"] is not None]
    ) if known_rows else None
    recovery_rate = statistics.fmean(
        [
            float(row["last_solvent"] != 3)
            for row in mismatch_rows
            if row["last_solvent"] is not None
        ]
    ) if mismatch_rows else None
    return {
        "cell_count": len(metrics),
        "arm_summary": arm_summary,
        "paired_best_final_score": {
            "known_minus_unknown": _paired_difference(
                normalized["known"], normalized["unknown"], "best_final_score"
            ),
            "mismatched_minus_known": _paired_difference(
                normalized["mismatched"], normalized["known"], "best_final_score"
            ),
            "mismatched_minus_unknown": _paired_difference(
                normalized["mismatched"], normalized["unknown"], "best_final_score"
            ),
        },
        "wrong_prior": {
            "mismatched_first_transposed_solvent_rate": manipulation_rate,
            "known_first_nominal_solvent_rate": known_rate,
            "mismatched_late_leaves_transposed_solvent_rate": recovery_rate,
            "manipulation_visible": manipulation_rate is not None
            and known_rate is not None
            and manipulation_rate >= 0.8
            and known_rate >= 0.8,
            "recovery_visible": recovery_rate is not None
            and recovery_rate >= 0.6
            and bool(arm_summary["mismatched"]["late_minus_early_score"]["mean"] is not None)
            and float(arm_summary["mismatched"]["late_minus_early_score"]["mean"]) > 0.0,
        },
        "all_lifecycles_completed": all(
            row["lifecycle_completed"] for row in metrics
        ),
        "all_exact_replays_verified": all(
            row["exact_replay_verified"] for row in metrics
        ),
    }


def _load_resume_results(
    output_root: Path,
    *,
    protocol: Mapping[str, Any],
    source: Mapping[str, Any],
    cli: Mapping[str, Any],
    card: Any,
    method_limits: Mapping[str, Any],
    scheduled_cells: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    """Load and validate an immutable completed-cell prefix for tri-arm resume."""

    manifest_path = output_root / "triarm_manifest.json"
    if not manifest_path.is_file():
        if any(output_root.iterdir()):
            raise RuntimeError(
                "tri-arm resume requires triarm_manifest.json for a non-empty output root"
            )
        return []
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, Mapping):
        raise RuntimeError("tri-arm resume manifest must be an object")
    expected_seeds = sorted({int(cell["world_seed"]) for cell in scheduled_cells})
    checks = {
        "runner_version": manifest.get("runner_version") == RUNNER_VERSION,
        "protocol_id": manifest.get("protocol_id") == protocol["protocol_id"],
        "world_seeds": manifest.get("world_seeds") == expected_seeds,
        "source_tree": manifest.get("source", {}).get("material_source_tree_sha256")
        == source.get("material_source_tree_sha256"),
        "protocol_file": manifest.get("source", {}).get("protocol_file_sha256")
        == source.get("protocol_file_sha256"),
        "provider_runtime": (
            manifest.get("provider_runtime", manifest.get("codex_cli"))
            == dict(cli)
        ),
    }
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise RuntimeError(
            "tri-arm resume identity mismatch: " + ", ".join(failed)
        )
    raw_cells = manifest.get("cells")
    if not isinstance(raw_cells, list):
        raise RuntimeError("tri-arm resume manifest cells must be a list")
    if len(raw_cells) > len(scheduled_cells):
        raise RuntimeError("tri-arm resume manifest has too many cells")
    prefix = len(raw_cells)
    expected_prefix = scheduled_cells[:prefix]
    for expected, observed in zip(expected_prefix, raw_cells, strict=True):
        if not isinstance(observed, Mapping):
            raise RuntimeError("tri-arm resume cell entry must be an object")
        if {
            "cell_id": observed.get("cell_id"),
            "world_seed": observed.get("world_seed"),
            "condition_id": observed.get("condition_id"),
            "run_dir": observed.get("run_dir"),
        } != {
            "cell_id": expected["cell_id"],
            "world_seed": expected["world_seed"],
            "condition_id": expected["condition_id"],
            "run_dir": expected["cell_id"],
        }:
            raise RuntimeError(
                f"tri-arm resume cell identity mismatch: {expected['cell_id']}"
            )
    present = [
        (output_root / str(cell["cell_id"])).exists()
        for cell in scheduled_cells
    ]
    if any(present[prefix:]):
        raise RuntimeError("tri-arm resume found a non-prefix cell directory")
    results: list[dict[str, Any]] = []
    for cell in expected_prefix:
        results.append(
            matrix._validated_resume_result(
                cell_root=output_root / str(cell["cell_id"]),
                cell=cell,
                protocol=protocol,
                source=source,
                cli=cli,
                card=card,
                method_limits=method_limits,
            )
        )
    audits = _triarm_audits(results)
    complete_audits = [item for item in audits if not item.get("incomplete")]
    incomplete_audits = [item for item in audits if item.get("incomplete")]
    if any(not item["passed"] for item in complete_audits):
        raise RuntimeError("tri-arm resume prefix failed world identity audit")
    if len(incomplete_audits) > 1:
        raise RuntimeError("tri-arm resume prefix spans multiple incomplete worlds")
    return results


def _manifest(
    *,
    protocol: Mapping[str, Any],
    source: Mapping[str, Any],
    cli: Mapping[str, Any],
    cells: Sequence[Mapping[str, Any]],
    planned_cells: Sequence[Mapping[str, Any]] | None = None,
    audits: Sequence[Mapping[str, Any]],
    status: str,
    dry_run: bool,
) -> dict[str, Any]:
    card = matrix._campaign_card(protocol, qualification=False)
    frozen_plan = list(planned_cells) if planned_cells is not None else list(cells)
    cell_rows = []
    for item in cells:
        cell = item["cell"]
        cell_rows.append(
            {
                "cell_id": cell["cell_id"],
                "world_seed": int(cell["world_seed"]),
                "arm": cell["arm"],
                "condition_id": cell["condition_id"],
                "within_world_order": int(cell["within_world_order"]),
                "material_information": deepcopy(
                    dict(cell["material_information"])
                ),
                "run_status": item.get("run_status", "inspected"),
                "run_dir": cell["cell_id"],
                "config_sha256": item.get("config_sha256"),
                "trajectory_sha256": item.get("trajectory_sha256"),
                "campaign_resource_ledger_sha256": item.get(
                    "campaign_resource_ledger_sha256"
                ),
                "exact_replay_verified": item.get("exact_replay_verified"),
                "closed_batch_count": item.get("behavior", {}).get(
                    "closed_batch_count"
                ),
            }
        )
    payload: dict[str, Any] = {
        "schema_version": "chemworld-g2-autonomous-material-triarm-run-0.1",
        "runner_version": RUNNER_VERSION,
        "protocol_id": protocol["protocol_id"],
        "run_status": status,
        "dry_run": dry_run,
        "formal_result": False,
        "confirmatory_claim_allowed": False,
        "source": deepcopy(dict(source)),
        "provider_runtime": deepcopy(dict(cli)),
        "world_seeds": sorted(
            {int(item["world_seed"]) for item in frozen_plan}
        ),
        "planned_cell_count": len(frozen_plan),
        "planned_physical_experiment_count": (
            len(frozen_plan) * int(card.vessel_start_limit)
        ),
        "completed_cell_count": sum(
            item.get("run_status") == "completed" for item in cells
        ),
        "completed_physical_experiment_count": sum(
            int(item.get("behavior", {}).get("closed_batch_count", 0))
            for item in cells
        ),
        "campaign_resource_card_sha256": card.card_sha256,
        "cells": cell_rows,
        "triarm_audits": deepcopy(list(audits)),
        "all_triarm_audits_passed": all(
            bool(item["passed"]) for item in audits
        ),
        "analysis": _triarm_analysis(
            cells,
            operation_limit=int(card.operation_attempt_limit),
            target_batches=int(card.vessel_start_limit),
        ),
    }
    payload["manifest_sha256"] = matrix.canonical_json_sha256(payload)
    return payload


def main() -> int:
    args = _parser().parse_args()
    config_path = args.config.resolve()
    protocol = _load_protocol(config_path)
    source = matrix._source_manifest(config_path)
    selected_seeds = (
        None
        if args.world_seeds is None
        else [
            int(value.strip())
            for value in args.world_seeds.split(",")
            if value.strip()
        ]
    )
    if selected_seeds is not None and not selected_seeds:
        raise ValueError("--world-seeds must contain at least one seed")
    cells = _scheduled_cells(protocol, selected_seeds)
    card = matrix._campaign_card(protocol, qualification=False)
    method_limits = matrix._method_limits(protocol, qualification=False)

    if args.dry_run:
        inspected: list[dict[str, Any]] = []
        for cell in cells:
            contract = matrix._inspect_cell_environment(
                protocol=protocol,
                cell=cell,
                card=card,
                operation_limit=int(method_limits["operation_limit"]),
            )
            inspected.append(
                {
                    "cell": cell,
                    "environment_contract": contract,
                    "run_status": "inspected",
                }
            )
        audits = _triarm_audits(inspected)
        manifest = _manifest(
            protocol=protocol,
            source=source,
            cli={},
            cells=inspected,
            planned_cells=cells,
            audits=audits,
            status="dry_run_passed" if all(a["passed"] for a in audits) else "dry_run_failed",
            dry_run=True,
        )
        print(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))
        return 0 if manifest["all_triarm_audits_passed"] else 2

    if not args.allow_external_provider:
        raise RuntimeError("external execution requires --allow-external-provider")
    if args.dry_run and args.resume:
        raise RuntimeError("--resume cannot be combined with --dry-run")
    if not args.provider_id or not args.provider_name or not args.provider_base_url:
        raise RuntimeError("provider id, name, and base URL must be non-empty")
    if args.provider_env_key and not __import__("os").environ.get(args.provider_env_key):
        raise RuntimeError(
            f"required provider environment variable is not set: {args.provider_env_key}"
        )
    cli = {
        "transport": "direct_wellau_chat_completions",
        "provider_id": str(args.provider_id),
        "provider_name": str(args.provider_name),
        "provider_base_url": str(args.provider_base_url),
        "provider_env_key": str(args.provider_env_key),
        "wire_api": "chat_completions",
        "structured_output": "strict_json_schema",
    }
    output_root = args.output_root.resolve()
    if args.resume:
        if not output_root.exists():
            raise FileNotFoundError(
                f"tri-arm resume output root does not exist: {output_root}"
            )
        results = _load_resume_results(
            output_root,
            protocol=protocol,
            source=source,
            cli=cli,
            card=card,
            method_limits=method_limits,
            scheduled_cells=cells,
        )
    else:
        if output_root.exists():
            raise FileExistsError(
                f"refusing to overwrite existing output root: {output_root}"
            )
        output_root.mkdir(parents=True)
        results = []
    try:
        for cell in cells[len(results) :]:
            print(json.dumps(cell, ensure_ascii=False, sort_keys=True), flush=True)
            result = matrix._run_cell_light(
                protocol=protocol,
                source=source,
                provider_runtime=cli,
                cell=cell,
                cell_root=output_root / str(cell["cell_id"]),
                card=card,
                method_limits=method_limits,
                qualification=False,
            )
            results.append(result)
    finally:
        audits = _triarm_audits(results) if results else []
        status = (
            "completed"
            if len(results) == len(cells)
            and all(item.get("run_status") == "completed" for item in results)
            else "incomplete"
        )
        payload = _manifest(
            protocol=protocol,
            source=source,
            cli=cli,
            cells=results,
            planned_cells=cells,
            audits=audits,
            status=status,
            dry_run=False,
        )
        matrix.write_json_atomic(output_root / "triarm_manifest.json", payload)
    return 0 if status == "completed" and payload["all_triarm_audits_passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
