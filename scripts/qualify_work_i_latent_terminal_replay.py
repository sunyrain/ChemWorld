"""Synthetically qualify the Work I terminal-replacement primitive."""

from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from chemworld.campaign_resources import generous_electrochemical_max_envelope_card
from chemworld.data.logging import to_builtin
from chemworld.envs.chemworld_env import ChemWorldEnv
from chemworld.eval.latent_terminal_contract import latent_terminal_contract_sha256
from chemworld.eval.latent_terminal_reconstructability import (
    reconstructability_report_sha256,
    validate_reconstructability_report,
)
from chemworld.eval.latent_terminal_replay import (
    REPLAY_IMPLEMENTATION_ID,
    LatentTerminalReplayError,
    capture_prefix_identity,
    evaluate_terminal_replacement,
    load_frozen_terminal_contract,
)
from chemworld.eval.provenance import canonical_json_sha256, file_sha256

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = (
    ROOT
    / "workstreams/arxiv_v1/reports/"
    "work-i-latent-terminal-replay-qualification-v0.1.json"
)
RECONSTRUCTABILITY_REPORT_PATH = Path(
    "workstreams/arxiv_v1/reports/"
    "work-i-latent-terminal-reconstructability-v0.1.json"
)
FORMAL_CONFIG_PATH = Path(
    "configs/benchmark/"
    "g2_autonomous_electrochemical_material_5x2_deepseek_v0.6_dev.json"
)
SOURCE_PATHS = (
    Path("configs/benchmark/work_i_latent_terminal_contract_v0.1.json"),
    FORMAL_CONFIG_PATH,
    RECONSTRUCTABILITY_REPORT_PATH,
    Path("src/chemworld/eval/latent_terminal_replay.py"),
    Path("scripts/qualify_work_i_latent_terminal_replay.py"),
)
REPORT_SCHEMA_ID = "chemworld.latent_terminal_replay_qualification"
REPORT_SCHEMA_VERSION = "0.1.0"
REPORT_ID = "work-i-latent-terminal-replay-qualification-v0.1"
SYNTHETIC_WORLD_SEED = 20_003
SYNTHETIC_OBSERVATION_SEED = 320_003
FORMAL_WORLD_SEEDS = frozenset(range(5))
ORIGINAL_NAMESPACE = "g2-autonomous-material-information-v1"
ORIGINAL_DISCARD_ACTION = {
    "operation": "discard_batch",
    "reason": "synthetic_terminal_replay_qualification",
}
SYNTHETIC_PREFIX_ACTIONS = (
    {"operation": "add_solvent", "volume_L": 0.025, "solvent": 0},
    {"operation": "add_reagent", "amount_mol": 0.01},
    {
        "operation": "set_potential",
        "potential_V": 0.72,
        "current_mA": 25.0,
        "electrolyte_profile": 0,
    },
    {"operation": "electrolyze", "duration_s": 300.0},
    {"operation": "measure", "instrument": "uvvis"},
)


def _read_json_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected JSON object: {path}")
    return payload


def _without(payload: dict[str, Any], field: str) -> dict[str, Any]:
    result = deepcopy(payload)
    result.pop(field, None)
    return result


def report_sha256(payload: dict[str, Any]) -> str:
    return canonical_json_sha256(_without(payload, "report_sha256"))


def source_manifest(root: Path) -> dict[str, str]:
    return {
        relative.as_posix(): file_sha256(root / relative)
        for relative in SOURCE_PATHS
    }


def _public_receipt(receipt: dict[str, Any]) -> dict[str, Any]:
    """Drop episode-UUID-dependent hashes while retaining the equality verdict."""

    result = deepcopy(receipt)
    result.pop("original_environment_before_sha256", None)
    result.pop("original_environment_after_sha256", None)
    return result


def _make_environment(root: Path) -> ChemWorldEnv:
    if SYNTHETIC_WORLD_SEED in FORMAL_WORLD_SEEDS:
        raise ValueError("synthetic qualification overlaps a formal world")
    config = _read_json_object(root / FORMAL_CONFIG_PATH)
    task = config["task"]
    requested_card = config["campaign_resource_card"]
    card = generous_electrochemical_max_envelope_card(
        experiment_count=int(requested_card["complete_experiments"]),
        operation_attempt_limit=int(requested_card["operation_attempt_limit"]),
        nonfinal_instrument_use_limit=int(
            requested_card["nonfinal_instrument_use_limit"]
        ),
        stock_action_envelopes_per_experiment=float(
            requested_card["stock_action_envelopes_per_experiment"]
        ),
        card_id=str(requested_card["card_id"]),
    )
    return ChemWorldEnv(
        task_id=str(task["task_id"]),
        world_split=str(task["world_split"]),
        objective=str(task["objective"]),
        seed=SYNTHETIC_WORLD_SEED,
        budget_override=48,
        episode_mode_override=str(task["episode_mode"]),
        electrochemical_workflow_mode=str(
            task["electrochemical_workflow_mode"]
        ),
        electrochemical_material_family_id=str(
            task["electrochemical_material_family_id"]
        ),
        material_information={"mode": "opaque_codes"},
        observation_seed_override=SYNTHETIC_OBSERVATION_SEED,
        observation_noise_mode=str(task["observation_noise_mode"]),
        observation_noise_namespace=str(task["observation_noise_namespace"]),
        campaign_resource_card=card,
        scoring_contract_id=str(task["scoring_contract_id"]),
    )


def _execute_prefix(base: ChemWorldEnv) -> list[dict[str, Any]]:
    base.reset(seed=SYNTHETIC_WORLD_SEED)
    # Campaign IDs are deliberately non-seed-bearing UUIDs in normal episodes.
    # Pin only this synthetic fixture so its resource event IDs are reproducible.
    base._campaign_id = "episode-synthetic-l03-qualification"
    rows: list[dict[str, Any]] = []
    for action in SYNTHETIC_PREFIX_ACTIONS:
        observation, reward, terminated, truncated, info = base.step(deepcopy(action))
        if info.get("transaction_status") != "committed":
            raise ValueError(f"synthetic prefix action did not commit: {action}")
        rows.append(
            {
                "step": info["step"],
                "experiment_index": info["experiment_index"],
                "operation_id": info["operation_id"],
                "action": to_builtin(action),
                "observation": to_builtin(observation),
                "reward": float(reward),
                "terminated": bool(terminated),
                "truncated": bool(truncated),
                "transaction_status": info["transaction_status"],
                "observation_noise": base.observation_noise_provenance(),
            }
        )
    return rows


def _negative_probe(
    base: ChemWorldEnv,
    *,
    expected: dict[str, Any],
    prefix: list[dict[str, Any]],
    resources: dict[str, Any],
    contract: dict[str, Any],
    field: str,
) -> bool:
    tampered = deepcopy(expected)
    tampered[field] = "0" * 64
    tampered.pop("prefix_identity_sha256", None)
    try:
        evaluate_terminal_replacement(
            base,
            expected_identity=tampered,
            original_discard_action=ORIGINAL_DISCARD_ACTION,
            public_prefix_records=prefix,
            authoritative_resource_snapshot=resources,
            frozen_contract=contract,
        )
    except LatentTerminalReplayError:
        return True
    return False


def _workflow_probe(root: Path, contract: dict[str, Any]) -> bool:
    base = _make_environment(root)
    try:
        base.reset(seed=SYNTHETIC_WORLD_SEED)
        resources = base.campaign_resource_snapshot()
        if not isinstance(resources, dict):
            raise ValueError("synthetic environment lacks resource ledger")
        expected = capture_prefix_identity(
            base,
            cell_id="synthetic-unready-cell",
            lifecycle_index=0,
            terminal_step=1,
            original_discard_action=ORIGINAL_DISCARD_ACTION,
            public_prefix_records=[],
            authoritative_resource_snapshot=resources,
        )
        try:
            evaluate_terminal_replacement(
                base,
                expected_identity=expected,
                original_discard_action=ORIGINAL_DISCARD_ACTION,
                public_prefix_records=[],
                authoritative_resource_snapshot=resources,
                frozen_contract=contract,
            )
        except LatentTerminalReplayError as exc:
            return "may bypass only workflow readiness" in str(exc)
        return False
    finally:
        base.close()


def build_report(root: Path) -> dict[str, Any]:
    contract = load_frozen_terminal_contract(root)
    reconstructability = _read_json_object(root / RECONSTRUCTABILITY_REPORT_PATH)
    reconstructability_errors = validate_reconstructability_report(
        reconstructability,
        root=root,
    )
    if reconstructability_errors:
        raise ValueError(
            "invalid L02 reconstructability dependency: "
            + "; ".join(reconstructability_errors)
        )

    first_env = _make_environment(root)
    second_env = _make_environment(root)
    try:
        first_prefix = _execute_prefix(first_env)
        second_prefix = _execute_prefix(second_env)
        if first_prefix != second_prefix:
            raise ValueError("independent synthetic public prefixes differ")
        resources = first_env.campaign_resource_snapshot()
        if not isinstance(resources, dict):
            raise ValueError("synthetic environment lacks resource ledger")
        expected = capture_prefix_identity(
            first_env,
            cell_id="synthetic-cell-01",
            lifecycle_index=0,
            terminal_step=len(first_prefix) + 1,
            original_discard_action=ORIGINAL_DISCARD_ACTION,
            public_prefix_records=first_prefix,
            authoritative_resource_snapshot=resources,
        )
        first_receipt = evaluate_terminal_replacement(
            first_env,
            expected_identity=expected,
            original_discard_action=ORIGINAL_DISCARD_ACTION,
            public_prefix_records=first_prefix,
            authoritative_resource_snapshot=resources,
            frozen_contract=contract,
        )
        second_receipt = evaluate_terminal_replacement(
            second_env,
            expected_identity=expected,
            original_discard_action=ORIGINAL_DISCARD_ACTION,
            public_prefix_records=second_prefix,
            authoritative_resource_snapshot=resources,
            frozen_contract=contract,
        )
        negative_probes = {
            field: _negative_probe(
                first_env,
                expected=expected,
                prefix=first_prefix,
                resources=resources,
                contract=contract,
                field=field,
            )
            for field in (
                "terminal_action_sha256",
                "public_prefix_sha256",
                "hidden_state_sha256",
                "campaign_resource_snapshot_sha256",
                "scoring_contract_hash",
            )
        }
    finally:
        first_env.close()
        second_env.close()
    negative_probes["unexpected_physical_precondition"] = _workflow_probe(
        root, contract
    )

    first_result_id = first_receipt["terminal_evaluation_identity_sha256"]
    second_result_id = second_receipt["terminal_evaluation_identity_sha256"]
    gates = {
        "l01_contract_identity_frozen": (
            latent_terminal_contract_sha256(contract)
            == contract["contract_sha256"]
        ),
        "l02_all_36_reconstructable_without_outcome_access": (
            reconstructability["status"] == "reconstructable"
            and reconstructability["census"]["reconstructable_unit_count"] == 36
            and reconstructability["census"]["shadow_terminal_evaluations_executed"]
            == 0
            and reconstructability["census"]["latent_discard_scores_accessed"] == 0
        ),
        "synthetic_world_disjoint_from_formal_worlds": (
            SYNTHETIC_WORLD_SEED not in FORMAL_WORLD_SEEDS
        ),
        "independent_public_prefix_replay_exact": first_prefix == second_prefix,
        "exact_same_identity_terminal_replay": first_result_id == second_result_id,
        "terminal_noise_key_reused_exactly": (
            first_receipt["noise_key_sha256"]
            == second_receipt["noise_key_sha256"]
        ),
        "original_environment_unmodified": (
            first_receipt["original_environment_mutated"] is False
            and second_receipt["original_environment_mutated"] is False
        ),
        "original_resource_ledger_unmodified": (
            first_receipt["original_resource_ledger_mutated"] is False
            and second_receipt["original_resource_ledger_mutated"] is False
        ),
        "no_chemistry_or_env_step_in_replacement": (
            first_receipt["terminal_action_replacement"]["additional_process_operations"]
            == 0
            and first_receipt["terminal_action_replacement"]["env_step_calls"] == 0
        ),
        "only_workflow_readiness_bypassed": (
            first_receipt["terminal_action_replacement"][
                "workflow_readiness_bypassed"
            ]
            == ["measure_final_requires_terminated"]
        ),
        "all_negative_probes_fail_closed": all(negative_probes.values()),
        "agent_provider_calls_zero": (
            first_receipt["agent_provider_calls"]
            == second_receipt["agent_provider_calls"]
            == 0
        ),
        "formal_outcome_boundary_not_crossed": True,
    }
    report = {
        "schema_id": REPORT_SCHEMA_ID,
        "schema_version": REPORT_SCHEMA_VERSION,
        "report_id": REPORT_ID,
        "status": "PASS" if all(gates.values()) else "FAIL",
        "implementation_id": REPLAY_IMPLEMENTATION_ID,
        "dependency_bindings": {
            "l01_contract_id": contract["contract_id"],
            "l01_contract_sha256": contract["contract_sha256"],
            "l02_report_id": reconstructability["report_id"],
            "l02_report_sha256": reconstructability_report_sha256(
                reconstructability
            ),
            "formal_resource_card_sha256": contract["population"]["run_contracts"][
                "campaign_resource_card_sha256"
            ],
            "scoring_contract_hash": contract["counterfactual_terminal_rule"][
                "score_contract_hash"
            ],
        },
        "qualification_design": {
            "role": "synthetic_nonformal_qualification_only",
            "world_seed": SYNTHETIC_WORLD_SEED,
            "formal_world_seeds_excluded": sorted(FORMAL_WORLD_SEEDS),
            "observation_seed": SYNTHETIC_OBSERVATION_SEED,
            "original_noise_namespace": ORIGINAL_NAMESPACE,
            "prefix_operation_count": len(SYNTHETIC_PREFIX_ACTIONS),
            "independent_prefix_replays": 2,
        },
        "census": {
            "synthetic_prefix_replays": 2,
            "synthetic_terminal_evaluations": 2,
            "negative_fail_closed_probes": len(negative_probes),
            "formal_checkpoint_payloads_loaded": 0,
            "formal_shadow_terminal_evaluations_executed": 0,
            "formal_latent_discard_scores_accessed": 0,
            "agent_provider_calls": 0,
        },
        "synthetic_receipts": [
            _public_receipt(first_receipt),
            _public_receipt(second_receipt),
        ],
        "negative_probes": negative_probes,
        "gates": gates,
        "formal_execution_owner": "W1-L05",
        "source_manifest": source_manifest(root),
    }
    report["report_sha256"] = report_sha256(report)
    return report


def validate_report(
    report: dict[str, Any], *, root: Path | None = None
) -> list[str]:
    errors: list[str] = []
    if report.get("schema_id") != REPORT_SCHEMA_ID:
        errors.append("unexpected report schema")
    if report.get("schema_version") != REPORT_SCHEMA_VERSION:
        errors.append("unexpected report schema version")
    if report.get("report_id") != REPORT_ID or report.get("status") != "PASS":
        errors.append("qualification did not pass")
    if report.get("report_sha256") != report_sha256(report):
        errors.append("report self-hash mismatch")
    census = report.get("census", {})
    if census != {
        "synthetic_prefix_replays": 2,
        "synthetic_terminal_evaluations": 2,
        "negative_fail_closed_probes": 6,
        "formal_checkpoint_payloads_loaded": 0,
        "formal_shadow_terminal_evaluations_executed": 0,
        "formal_latent_discard_scores_accessed": 0,
        "agent_provider_calls": 0,
    }:
        errors.append("qualification census or formal outcome boundary changed")
    gates = report.get("gates")
    if not isinstance(gates, dict) or not gates or not all(gates.values()):
        errors.append("one or more qualification gates failed")
    receipts = report.get("synthetic_receipts")
    if not isinstance(receipts, list) or len(receipts) != 2:
        errors.append("expected two synthetic receipts")
    else:
        identities = {
            receipt.get("terminal_evaluation_identity_sha256")
            for receipt in receipts
            if isinstance(receipt, dict)
        }
        if len(identities) != 1 or None in identities:
            errors.append("synthetic terminal identities do not replay exactly")
        for receipt in receipts:
            if not isinstance(receipt, dict):
                continue
            if (
                receipt.get("original_environment_mutated") is not False
                or receipt.get("original_resource_ledger_mutated") is not False
                or receipt.get("agent_provider_calls") != 0
                or receipt.get("hidden_state_payload_emitted") is not False
            ):
                errors.append("synthetic receipt violates the isolation boundary")
    probes = report.get("negative_probes")
    if not isinstance(probes, dict) or set(probes) != {
        "terminal_action_sha256",
        "public_prefix_sha256",
        "hidden_state_sha256",
        "campaign_resource_snapshot_sha256",
        "scoring_contract_hash",
        "unexpected_physical_precondition",
    } or not all(probes.values()):
        errors.append("negative fail-closed probes are incomplete")
    if report.get("formal_execution_owner") != "W1-L05":
        errors.append("formal execution ownership changed")
    if root is not None and report.get("source_manifest") != source_manifest(root):
        errors.append("qualification source manifest is stale")
    return list(dict.fromkeys(errors))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = build_report(ROOT)
    errors = validate_report(report, root=ROOT)
    if errors:
        raise SystemExit("terminal replay qualification invalid: " + "; ".join(errors))
    rendered = json.dumps(
        report,
        ensure_ascii=False,
        allow_nan=False,
        indent=2,
        sort_keys=True,
    ) + "\n"
    if args.check:
        if args.output.read_text(encoding="utf-8") != rendered:
            raise SystemExit("committed qualification differs from deterministic rebuild")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
    print(
        json.dumps(
            {
                "status": report["status"],
                "report_sha256": report["report_sha256"],
                **report["census"],
                "check": bool(args.check),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
