"""Run the paired 5-world autonomous electrochemistry material-information matrix."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import tempfile
from collections import Counter
from collections.abc import Mapping
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast

import gymnasium as gym

import chemworld  # noqa: F401
from chemworld.agents.base import HistoryRecord
from chemworld.agents.interactive_codex_experiment import (
    InteractiveCodexExperimentAgent,
)
from chemworld.agents.structured_g2 import StructuredG2Agent
from chemworld.campaign_resources import (
    CampaignResourceCard,
    CampaignResourceIntegrityError,
    CampaignResourceLedger,
    generous_electrochemical_max_envelope_card,
)
from chemworld.data.logging import load_jsonl
from chemworld.eval.provenance import (
    canonical_json_sha256,
    file_sha256,
    git_source_commit,
    git_worktree_dirty,
    repository_tree_sha256,
    write_json_atomic,
)
from chemworld.eval.resource_accounting import MethodResourceLimitError
from chemworld.eval.runner import run_agent
from chemworld.eval.static_optimization_seeds import exploration_observation_seed
from chemworld.eval.verify import verify_records
from chemworld.providers.codex_subscription import HTTPS_PROVIDER_ID
from chemworld.providers.deepseek import DeepSeekClient
from chemworld.providers.wellau import ReasoningEffort as WellAUReasoningEffort
from chemworld.providers.wellau import WellAUClient
from chemworld.tasks import get_task

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "configs/benchmark/g2_autonomous_electrochemical_material_5x2_v0.4_dev.json"
DEFAULT_MATRIX_ROOT = (
    ROOT / "runs/development/g2-autonomous-electrochemical-material-5x2-codex-sol-medium-mcp-v2"
)
DEFAULT_QUALIFICATION_ROOT = (
    ROOT / "runs/development/"
    "g2-autonomous-electrochemical-seed0-opaque-k1-qualification-mcp-medium-v2"
)
QUALIFICATION_CONDITION_IDS = {
    "opaque": "opaque_codes",
    "nominal": "anonymous_nominal_properties",
}
QUALIFICATION_EXPERIMENT_COUNTS = (1, 2, 6)
RUNNER_VERSION = "chemworld-g2-autonomous-material-runner-0.4"
INPUT_TOKEN_LIMIT_PER_OPERATION = 500_000


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _load_protocol(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("matrix protocol must be a JSON object")
    if payload.get("schema_version") not in {
        "chemworld-g2-autonomous-material-matrix-0.1",
        "chemworld-g2-autonomous-material-matrix-0.2",
        "chemworld-g2-autonomous-material-matrix-0.3",
        "chemworld-g2-autonomous-material-matrix-0.4",
    }:
        raise ValueError("unsupported autonomous material matrix protocol")
    task = payload.get("task")
    conditions = payload.get("paired_conditions")
    if not isinstance(task, dict) or not isinstance(conditions, list):
        raise ValueError("protocol task and paired_conditions are required")
    condition_ids = [str(item.get("condition_id")) for item in conditions if isinstance(item, dict)]
    if sorted(condition_ids) != [
        "anonymous_nominal_properties",
        "opaque_codes",
    ]:
        raise ValueError("protocol requires exactly the opaque and nominal conditions")
    seeds = task.get("world_seeds")
    if seeds != [0, 1, 2, 3, 4]:
        raise ValueError("protocol world_seeds must be frozen to [0,1,2,3,4]")
    return payload


def _conditions(protocol: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(item["condition_id"]): deepcopy(dict(item)) for item in protocol["paired_conditions"]
    }


def _scheduled_cells(protocol: Mapping[str, Any]) -> list[dict[str, Any]]:
    conditions = _conditions(protocol)
    schedule = protocol["execution_order"]
    cells: list[dict[str, Any]] = []
    ordinal = 0
    for seed in protocol["task"]["world_seeds"]:
        order = schedule["even_seed_order"] if int(seed) % 2 == 0 else schedule["odd_seed_order"]
        for within_pair_order, condition_id in enumerate(order, start=1):
            ordinal += 1
            cells.append(
                {
                    "cell_id": f"cell-{ordinal:02d}",
                    "world_seed": int(seed),
                    "condition_id": str(condition_id),
                    "within_pair_order": within_pair_order,
                    "material_information": deepcopy(
                        conditions[str(condition_id)]["material_information"]
                    ),
                }
            )
    return cells


def _campaign_card(
    protocol: Mapping[str, Any],
    *,
    qualification: bool,
    qualification_experiments: int = 1,
) -> CampaignResourceCard:
    requested = protocol["campaign_resource_card"]
    attempts_per_experiment = int(requested["operation_attempt_limit"]) // int(
        requested["complete_experiments"]
    )
    if qualification:
        if qualification_experiments not in QUALIFICATION_EXPERIMENT_COUNTS:
            raise ValueError("qualification_experiments must be one of 1, 2, or 6")
        return generous_electrochemical_max_envelope_card(
            experiment_count=qualification_experiments,
            operation_attempt_limit=(attempts_per_experiment * qualification_experiments),
            nonfinal_instrument_use_limit=3 * qualification_experiments,
            stock_action_envelopes_per_experiment=float(
                protocol["campaign_resource_card"].get(
                    "stock_action_envelopes_per_experiment",
                    1.0,
                )
            ),
            card_id=(
                f"electrochemical-k{qualification_experiments}-"
                "shared-stock-envelope-qualification-v2"
            ),
        )
    card = generous_electrochemical_max_envelope_card(
        experiment_count=int(requested["complete_experiments"]),
        operation_attempt_limit=int(requested["operation_attempt_limit"]),
        nonfinal_instrument_use_limit=int(requested["nonfinal_instrument_use_limit"]),
        stock_action_envelopes_per_experiment=float(
            requested.get("stock_action_envelopes_per_experiment", 1.0)
        ),
        card_id=str(requested["card_id"]),
    )
    expected = {
        "vessel_start_limit": card.vessel_start_limit,
        "final_assay_limit": card.final_assay_limit,
        "stock_limits": dict(card.stock_limits),
    }
    observed = {
        "vessel_start_limit": int(requested["vessel_start_limit"]),
        "final_assay_limit": int(requested["final_assay_limit"]),
        "stock_limits": {
            str(key): float(value) for key, value in requested["stock_limits"].items()
        },
    }
    if expected != observed:
        raise ValueError("protocol resource card disagrees with its frozen factory")
    return card


def _method_limits(
    protocol: Mapping[str, Any],
    *,
    qualification: bool,
    qualification_experiments: int = 1,
) -> dict[str, Any]:
    requested = protocol["campaign_resource_card"]
    attempts_per_experiment = int(requested["operation_attempt_limit"]) // int(
        requested["complete_experiments"]
    )
    if qualification:
        if qualification_experiments not in QUALIFICATION_EXPERIMENT_COUNTS:
            raise ValueError("qualification_experiments must be one of 1, 2, or 6")
        return {
            "operation_limit": (attempts_per_experiment * qualification_experiments),
            "complete_experiment_limit": qualification_experiments,
            "checkpoint_complete_experiments": tuple(range(1, qualification_experiments + 1)),
            "wall_time_limit_s": 3_600.0 * qualification_experiments,
            "model_call_limit": qualification_experiments,
            # Codex reports cumulative multi-turn input, including cache hits.
            # That quantity grows faster than the number of physical batches,
            # so bind the hard envelope to primitive-operation capacity rather
            # than assuming one million reported tokens per experiment.
            "input_token_limit": (
                INPUT_TOKEN_LIMIT_PER_OPERATION
                * attempts_per_experiment
                * qualification_experiments
            ),
            "output_token_limit": 200_000 * qualification_experiments,
            "training_environment_step_limit": 0,
        }
    limits = deepcopy(dict(protocol["method_resource_limits_per_cell"]))
    limits["checkpoint_complete_experiments"] = tuple(
        int(item) for item in limits["checkpoint_complete_experiments"]
    )
    return limits


def _qualification_cell(
    protocol: Mapping[str, Any],
    *,
    condition: str,
    experiment_count: int,
    world_seed: int = 0,
) -> dict[str, Any]:
    if condition not in QUALIFICATION_CONDITION_IDS:
        raise ValueError("qualification condition must be either 'opaque' or 'nominal'")
    if experiment_count not in QUALIFICATION_EXPERIMENT_COUNTS:
        raise ValueError("qualification experiment count must be one of 1, 2, or 6")
    condition_id = QUALIFICATION_CONDITION_IDS[condition]
    selected = _conditions(protocol)[condition_id]
    if world_seed not in protocol["task"]["world_seeds"]:
        raise ValueError("qualification world seed must be in the frozen matrix")
    cell_id = f"qualification-seed{world_seed}-{condition}-k{experiment_count}"
    return {
        "cell_id": cell_id,
        "world_seed": world_seed,
        "condition_id": condition_id,
        "within_pair_order": 1,
        "material_information": deepcopy(dict(selected["material_information"])),
        "qualification_condition": condition,
        "qualification_experiments": experiment_count,
    }


def _qualification_output_root(
    *,
    condition: str,
    experiment_count: int,
    world_seed: int = 0,
) -> Path:
    if condition not in QUALIFICATION_CONDITION_IDS:
        raise ValueError("qualification condition must be either 'opaque' or 'nominal'")
    if experiment_count not in QUALIFICATION_EXPERIMENT_COUNTS:
        raise ValueError("qualification experiment count must be one of 1, 2, or 6")
    if condition == "opaque" and experiment_count == 1 and world_seed == 0:
        return DEFAULT_QUALIFICATION_ROOT
    return (
        ROOT
        / "runs/development"
        / (
            f"g2-autonomous-electrochemical-seed{world_seed}-"
            f"{condition}-k{experiment_count}-qualification-mcp-medium-v2"
        )
    )


def _source_manifest(config_path: Path) -> dict[str, Any]:
    source_roots = (
        "src/chemworld",
        "scripts/run_g2_autonomous_material_matrix.py",
        config_path.relative_to(ROOT).as_posix(),
    )
    return {
        "git_commit": git_source_commit(ROOT),
        "worktree_dirty": git_worktree_dirty(
            ROOT,
            excluded_prefixes=("runs/development/",),
        ),
        "material_source_roots": list(source_roots),
        "material_source_tree_sha256": repository_tree_sha256(
            ROOT,
            relative_roots=source_roots,
        ),
        "protocol_file": config_path.relative_to(ROOT).as_posix(),
        "protocol_file_sha256": file_sha256(config_path),
        "runner_version": RUNNER_VERSION,
    }


def _codex_cli_manifest() -> dict[str, Any]:
    executable = shutil.which("codex")
    if not executable:
        raise RuntimeError("codex executable is unavailable")
    version = subprocess.run(
        [executable, "--version"],
        capture_output=True,
        text=True,
        check=True,
        timeout=20,
    ).stdout.strip()
    login_result = subprocess.run(
        [executable, "login", "status"],
        capture_output=True,
        text=True,
        check=True,
        timeout=20,
    )
    login = "\n".join(
        part.strip() for part in (login_result.stdout, login_result.stderr) if part.strip()
    )
    if "logged in" not in login.lower():
        raise RuntimeError("Codex CLI is not logged in")
    return {
        "executable_name": Path(executable).name,
        "version": version,
        "authentication": "existing ChatGPT login verified",
    }


def _env_kwargs(
    *,
    protocol: Mapping[str, Any],
    cell: Mapping[str, Any],
    card: CampaignResourceCard,
    operation_limit: int,
) -> dict[str, Any]:
    task = protocol["task"]
    seed = int(cell["world_seed"])
    return {
        "world_split": str(task["world_split"]),
        "budget": operation_limit,
        "objective": str(task["objective"]),
        "seed": seed,
        "task_id": str(task["task_id"]),
        "budget_override": operation_limit,
        "episode_mode_override": str(task["episode_mode"]),
        "observation_seed_override": exploration_observation_seed(
            str(task["task_id"]),
            seed,
        ),
        "observation_noise_mode": str(task["observation_noise_mode"]),
        "observation_noise_namespace": str(task["observation_noise_namespace"]),
        "material_information": deepcopy(dict(cell["material_information"])),
        "electrochemical_material_family_id": str(task["electrochemical_material_family_id"]),
        "electrochemical_workflow_mode": str(task["electrochemical_workflow_mode"]),
        "scoring_contract_id": str(task["scoring_contract_id"]),
        "campaign_resource_card": card.to_dict(),
    }


def _inspect_cell_environment(
    *,
    protocol: Mapping[str, Any],
    cell: Mapping[str, Any],
    card: CampaignResourceCard,
    operation_limit: int,
) -> dict[str, Any]:
    task = protocol["task"]
    env = gym.make(
        get_task(str(task["task_id"])).env_id,
        **_env_kwargs(
            protocol=protocol,
            cell=cell,
            card=card,
            operation_limit=operation_limit,
        ),
    )
    try:
        env.reset(seed=int(cell["world_seed"]))
        base = cast(Any, env.unwrapped)
        public = base.task_info()
        private = base.evaluator_provenance()
        resources = base.public_campaign_resource_state(include_card=True)
        return {
            "public_contract": {
                "task_contract_hash": public.get("task_contract_hash"),
                "runtime_profile_hash": public.get("runtime_profile_hash"),
                "scoring_contract_hash": public.get("scoring_contract_hash"),
                "observation_contract_hash": public.get("observation_contract_hash"),
                "workflow_mode": public.get("electrochemical_workflow_mode"),
                "material_information": public.get("material_information"),
            },
            "evaluator_identity": private,
            "initial_campaign_resources": resources,
        }
    finally:
        env.close()


def _pair_config_sha256(
    *,
    protocol: Mapping[str, Any],
    source: Mapping[str, Any],
    world_seed: int,
    card: CampaignResourceCard,
    method_limits: Mapping[str, Any],
    trajectory_replicate_id: str | None = None,
    agent_seed: int | None = None,
) -> str:
    task = deepcopy(dict(protocol["task"]))
    task.pop("world_seeds", None)
    payload: dict[str, Any] = {
        "protocol_id": protocol["protocol_id"],
        "source_tree_sha256": source["material_source_tree_sha256"],
        "task": task,
        "world_seed": world_seed,
        "observation_seed": exploration_observation_seed(
            str(task["task_id"]),
            world_seed,
        ),
        "campaign_resource_card_sha256": card.card_sha256,
        "method_resource_limits": {
            key: list(value) if isinstance(value, tuple) else value
            for key, value in method_limits.items()
        },
        "agent": protocol["agent"],
    }
    if trajectory_replicate_id is not None:
        payload["trajectory_replicate_id"] = trajectory_replicate_id
    if agent_seed is not None:
        payload["agent_seed"] = agent_seed
    return canonical_json_sha256(payload)


def _cell_config(
    *,
    protocol: Mapping[str, Any],
    source: Mapping[str, Any],
    cli: Mapping[str, Any],
    cell: Mapping[str, Any],
    card: CampaignResourceCard,
    method_limits: Mapping[str, Any],
    qualification: bool,
) -> dict[str, Any]:
    world_seed = int(cell["world_seed"])
    pair_hash = _pair_config_sha256(
        protocol=protocol,
        source=source,
        world_seed=world_seed,
        card=card,
        method_limits=method_limits,
        trajectory_replicate_id=(
            str(cell["trajectory_replicate_id"])
            if cell.get("trajectory_replicate_id") is not None
            else None
        ),
        agent_seed=(int(cell["agent_seed"]) if cell.get("agent_seed") is not None else None),
    )
    payload: dict[str, Any] = {
        "schema_version": "chemworld-g2-autonomous-material-cell-0.1",
        "runner_version": RUNNER_VERSION,
        "protocol_id": protocol["protocol_id"],
        "qualification_only": qualification,
        "formal_result": False,
        "confirmatory_claim_allowed": False,
        "created_at": _now(),
        "cell": deepcopy(dict(cell)),
        "world_seed": world_seed,
        "seed": world_seed,
        "condition_id": str(cell["condition_id"]),
        "arm": str(cell["condition_id"]),
        "material_information": deepcopy(dict(cell["material_information"])),
        "task": deepcopy(dict(protocol["task"])),
        "observation_seed": exploration_observation_seed(
            str(protocol["task"]["task_id"]),
            world_seed,
        ),
        "campaign_resource_card": card.to_dict(),
        "campaign_resource_card_sha256": card.card_sha256,
        "method_resource_limits": {
            key: list(value) if isinstance(value, tuple) else value
            for key, value in method_limits.items()
        },
        "agent": deepcopy(dict(protocol["agent"])),
        "source": deepcopy(dict(source)),
        "codex_cli": deepcopy(dict(cli)),
        "pair_config_sha256": pair_hash,
        "pair_invariants_exclude": ["material_information", "execution_order"],
    }
    if cell.get("trajectory_replicate_id") is not None:
        payload["trajectory_replicate_id"] = str(cell["trajectory_replicate_id"])
    if cell.get("agent_seed") is not None:
        payload["agent_seed"] = int(cell["agent_seed"])
    payload["config_sha256"] = canonical_json_sha256(payload)
    return payload


def _resource_snapshot_from_history(
    history: list[HistoryRecord],
    *,
    card: CampaignResourceCard,
) -> dict[str, Any]:
    ledger = CampaignResourceLedger(card)
    expected_final_hash: str | None = None
    for record in history:
        preflight = record.info.get("campaign_resource_preflight")
        delta = record.info.get("campaign_resource_outcome_delta")
        if not isinstance(preflight, Mapping) or not isinstance(delta, Mapping):
            raise CampaignResourceIntegrityError(
                f"step {record.step} lacks campaign resource receipts"
            )
        event_id = str(preflight["event_id"])
        proposed = preflight.get("proposed_delta")
        starts_vessel = bool(
            isinstance(proposed, Mapping) and int(proposed.get("vessel_starts", 0)) == 1
        )
        replayed = ledger.preflight(
            event_id,
            record.action,
            starts_vessel=starts_vessel,
        )
        if replayed.to_dict() != dict(preflight):
            raise CampaignResourceIntegrityError(f"step {record.step} preflight replay mismatch")
        report = delta.get("report_only")
        if not isinstance(report, Mapping):
            raise CampaignResourceIntegrityError(f"step {record.step} resource report is missing")
        replayed_delta = ledger.record_outcome(
            event_id,
            record.action,
            {
                "operation_committed": (record.info.get("transaction_status") == "committed"),
                "campaign_resource_report_delta": dict(report),
            },
            starts_vessel=starts_vessel,
        )
        if replayed_delta.to_dict() != dict(delta):
            raise CampaignResourceIntegrityError(f"step {record.step} outcome replay mismatch")
        public_resources = record.info.get("campaign_resources")
        if isinstance(public_resources, Mapping):
            candidate = public_resources.get("ledger_sha256")
            if isinstance(candidate, str):
                expected_final_hash = candidate
    snapshot = ledger.snapshot()
    if expected_final_hash is not None and snapshot["ledger_sha256"] != expected_final_hash:
        raise CampaignResourceIntegrityError(
            "final public campaign resource hash does not match replay"
        )
    return snapshot


def _write_exact_replay_receipt(
    trajectory_path: Path,
    receipt_path: Path,
    *,
    campaign_resource_ledger_sha256: str,
) -> dict[str, Any]:
    """Replay the materialized trajectory and bind the result to its bytes."""

    records = load_jsonl(trajectory_path)
    verification = verify_records(records)
    receipt = {
        "schema_version": "chemworld-g2-exact-trajectory-replay-0.1",
        "replay_scope": "deterministic_environment_transitions",
        "trajectory_path": trajectory_path.name,
        "trajectory_sha256": file_sha256(trajectory_path),
        "trajectory_record_count": len(records),
        "campaign_resource_ledger_sha256": (campaign_resource_ledger_sha256),
        **verification.to_dict(),
    }
    write_json_atomic(receipt_path, receipt)
    if not verification.verified:
        raise RuntimeError(f"exact deterministic trajectory replay failed; see {receipt_path}")
    return receipt


def _experiment_rows(history: list[HistoryRecord]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    actions: list[HistoryRecord] = []
    experiment_index = 0
    for record in history:
        actions.append(record)
        if record.event_type not in {"experiment_end", "batch_discard"}:
            continue
        experiment_index += 1
        solvents = [
            item.action.get("solvent")
            for item in actions
            if item.action.get("operation") == "add_solvent"
            and item.info.get("transaction_status") == "committed"
        ]
        electrolytes = [
            item.action.get("electrolyte_profile")
            for item in actions
            if item.action.get("operation") == "set_potential"
            and item.info.get("transaction_status") == "committed"
        ]
        measurements = [
            item.action.get("instrument")
            for item in actions
            if item.action.get("operation") == "measure"
        ]
        rows.append(
            {
                "experiment_index": experiment_index,
                "start_step": actions[0].step,
                "end_step": actions[-1].step,
                "operation_count": len(actions),
                "invalid_operation_count": sum(
                    item.info.get("transaction_status") != "committed" for item in actions
                ),
                "solvent_choices": solvents,
                "electrolyte_choices": electrolytes,
                "setpoints": [
                    {
                        key: item.action.get(key)
                        for key in ("potential_V", "current_mA")
                        if key in item.action
                    }
                    for item in actions
                    if item.action.get("operation") == "set_potential"
                ],
                "electrolysis_stages": [
                    {key: item.action.get(key) for key in ("duration_s",) if key in item.action}
                    for item in actions
                    if item.action.get("operation") == "electrolyze"
                ],
                "measurements": measurements,
                "diagnostic_measurement_count": sum(
                    instrument != "final_assay" for instrument in measurements
                ),
                "outcome": ("discarded" if record.event_type == "batch_discard" else "completed"),
                "leaderboard_score": record.info.get("leaderboard_score"),
            }
        )
        actions = []
    return rows


def _history_summary(history: list[HistoryRecord]) -> dict[str, Any]:
    experiments = _experiment_rows(history)
    discarded_batches = [record for record in history if record.event_type == "batch_discard"]
    terminal_scores = [
        float(row["leaderboard_score"])
        for row in experiments
        if isinstance(row.get("leaderboard_score"), int | float)
        and not isinstance(row.get("leaderboard_score"), bool)
    ]
    incumbent = 0.0
    incumbent_curve: list[float] = []
    for record in history:
        score = record.info.get("leaderboard_score")
        if isinstance(score, int | float) and not isinstance(score, bool):
            incumbent = max(incumbent, float(score))
        incumbent_curve.append(incumbent)
    invalid = [
        {
            "step": record.step,
            "action": record.action,
            "transaction_status": record.info.get("transaction_status"),
            "error_message": record.info.get("error_message"),
        }
        for record in history
        if record.info.get("transaction_status") != "committed"
    ]
    return {
        "operation_count": len(history),
        "complete_experiment_count": len(experiments),
        "discarded_batch_count": len(discarded_batches),
        "closed_batch_count": len(experiments) + len(discarded_batches),
        "action_counts": dict(
            sorted(Counter(str(record.action.get("operation")) for record in history).items())
        ),
        "measurement_counts": dict(
            sorted(
                Counter(
                    str(record.action.get("instrument"))
                    for record in history
                    if record.action.get("operation") == "measure"
                ).items()
            )
        ),
        "invalid_operation_count": len(invalid),
        "invalid_operations": invalid,
        "resource_rejection_count": sum(
            record.info.get("campaign_resource_rejected") is True for record in history
        ),
        "experiments": experiments,
        "terminal_scores": terminal_scores,
        "best_final_score": max(terminal_scores) if terminal_scores else None,
        "mean_final_score": (
            sum(terminal_scores) / len(terminal_scores) if terminal_scores else None
        ),
        "incumbent_auc_per_operation": (
            sum(incumbent_curve) / len(incumbent_curve) if incumbent_curve else None
        ),
        "right_censored_open_experiment": bool(
            history and history[-1].event_type not in {"experiment_end", "batch_discard"}
        ),
    }


def _provider_decision_audit(
    receipts: list[dict[str, Any]],
    method_resources: Mapping[str, Any],
    *,
    target_operations: int,
    expected_provider: str = "WellAU",
) -> dict[str, Any]:
    """Qualify one logical strict decision, with bounded attempts, per operation."""

    attempt_limit = int(
        method_resources.get("model_provenance", {})
        .get("request_parameters", {})
        .get("provider_attempt_limit_per_operation", 1)
    )
    grouped: dict[int, list[dict[str, Any]]] = {}
    for receipt in receipts:
        logical_index = int(receipt.get("logical_decision_index", 0) or 0)
        grouped.setdefault(logical_index, []).append(receipt)
    decision_audits: list[dict[str, Any]] = []
    for operation_index in range(1, target_operations + 1):
        attempts = sorted(
            grouped.get(operation_index, []),
            key=lambda item: int(item.get("attempt_index", 0) or 0),
        )
        attempt_audits: list[dict[str, Any]] = []
        for attempt_position, receipt in enumerate(attempts, start=1):
            billable = receipt.get("billable") is True
            succeeded = receipt.get("status") == "succeeded"
            checks = {
                "provider_matches_runtime": receipt.get("provider") == expected_provider,
                "logical_decision_index_matches": (
                    receipt.get("logical_decision_index") == operation_index
                ),
                "attempt_index_matches": receipt.get("attempt_index") == attempt_position,
                "status_matches_position": (
                    succeeded if attempt_position == len(attempts) else not succeeded
                ),
                "token_accounting_matches_billability": (
                    receipt.get("provider_token_accounting_complete") is True
                    and int(receipt.get("input_token_count", 0) or 0) > 0
                    and int(receipt.get("output_token_count", 0) or 0) > 0
                    if billable
                    else int(receipt.get("input_token_count", 0) or 0) == 0
                    and int(receipt.get("output_token_count", 0) or 0) == 0
                ),
                "failure_type_matches_status": (
                    receipt.get("failure_type") is None
                    if succeeded
                    else bool(receipt.get("failure_type"))
                ),
            }
            attempt_audits.append(
                {
                    "attempt_index": attempt_position,
                    "request_id": receipt.get("request_id"),
                    "status": receipt.get("status"),
                    "billable": billable,
                    "checks": checks,
                    "passed": all(checks.values()),
                }
            )
        decision_checks = {
            "attempt_count_in_range": 1 <= len(attempts) <= attempt_limit,
            "final_attempt_succeeded": bool(attempts) and attempts[-1].get("status") == "succeeded",
            "all_attempts_passed": bool(attempt_audits)
            and all(item["passed"] for item in attempt_audits),
        }
        decision_audits.append(
            {
                "operation_index": operation_index,
                "attempt_count": len(attempts),
                "attempts": attempt_audits,
                "checks": decision_checks,
                "passed": all(decision_checks.values()),
            }
        )
    provenance = method_resources.get("model_provenance")
    provenance_mapping = provenance if isinstance(provenance, Mapping) else {}
    parameters = provenance_mapping.get("request_parameters")
    parameter_mapping = parameters if isinstance(parameters, Mapping) else {}
    method_checks = {
        "provider_usage_accounting_complete": (
            method_resources.get("provider_usage_accounting_complete") is True
        ),
        "provider_token_accounting_complete": (
            method_resources.get("provider_token_accounting_complete") is True
        ),
        "provider_call_accounting_complete": (
            method_resources.get("provider_call_accounting_complete") is True
        ),
        "model_call_count_matches_receipts": (
            method_resources.get("model_call_count") == len(receipts)
        ),
        "logical_decisions_match_operations": (
            parameter_mapping.get("logical_decisions") == target_operations
        ),
        "strict_json_schema_declared": (
            parameter_mapping.get("response_format") == "dynamic_strict_json_schema"
        ),
        "shell_tools_disabled": (parameter_mapping.get("shell_tools") is False),
        "logical_decision_transport_declared": (
            parameter_mapping.get("one_logical_provider_decision_per_primitive_operation") is True
        ),
        "provider_attempt_limit_declared": (
            parameter_mapping.get("provider_attempt_limit_per_operation") == attempt_limit
            and attempt_limit >= 1
        ),
    }
    logical_indices_match = sorted(grouped) == list(range(1, target_operations + 1))
    return {
        "schema_version": "chemworld-g2-provider-decision-audit-0.2",
        "target_operation_count": target_operations,
        "expected_provider": expected_provider,
        "provider_attempt_limit_per_operation": attempt_limit,
        "receipt_count": len(receipts),
        "logical_decision_count": len(grouped),
        "logical_indices_match_operations": logical_indices_match,
        "decisions": decision_audits,
        "all_decisions_passed": (
            logical_indices_match
            and len(decision_audits) == target_operations
            and all(item["passed"] for item in decision_audits)
        ),
        "method_resource_checks": method_checks,
        "all_method_resource_checks_passed": all(method_checks.values()),
        "passed": (
            logical_indices_match
            and len(decision_audits) == target_operations
            and all(item["passed"] for item in decision_audits)
            and all(method_checks.values())
        ),
    }


def _provider_session_audit(
    receipts: list[dict[str, Any]],
    method_resources: Mapping[str, Any],
    *,
    target_experiments: int,
) -> dict[str, Any]:
    """Compatibility audit for the deprecated long-session runner."""

    receipt_audits: list[dict[str, Any]] = []
    for index, receipt in enumerate(receipts, start=1):
        integrity_keys = (
            "experiment_tool_integrity_verified_after_session",
            "mcp_tool_integrity_verified_after_session",
            "lab_tool_integrity_verified_after_session",
        )
        present_integrity = [key for key in integrity_keys if key in receipt]
        checks = {
            "status_completed": receipt.get("status") == "completed",
            "return_code_zero": receipt.get("return_code") == 0,
            "terminal_reason_batch_closed": receipt.get("terminal_reason")
            in {"experiment_complete", "batch_discarded"},
            "final_payload_valid": receipt.get("final_payload_valid") is True,
            "final_payload_status_batch_closed": receipt.get("final_payload_status")
            in {"experiment_complete", "batch_discarded", "stopped"},
            "usage_complete": receipt.get("usage_complete") is True,
            "lab_tool_integrity_verified_after_session": (
                receipt.get("lab_tool_integrity_verified_after_session") is True
            ),
            "experiment_tool_integrity_verified_after_session": (
                bool(present_integrity)
                and all(receipt.get(key) is True for key in present_integrity)
            ),
        }
        receipt_audits.append(
            {
                "experiment_index": index,
                "session_id": receipt.get("session_id"),
                "checks": checks,
                "passed": all(checks.values()),
            }
        )
    method_checks = {
        "provider_usage_not_pending": method_resources.get("provider_usage_pending") is False,
        "provider_usage_accounting_complete": method_resources.get(
            "provider_usage_accounting_complete"
        )
        is True,
        "provider_token_accounting_complete": method_resources.get(
            "provider_token_accounting_complete"
        )
        is True,
        "provider_call_accounting_complete": method_resources.get(
            "provider_call_accounting_complete"
        )
        is True,
        "model_call_count_matches_target": method_resources.get("model_call_count")
        == target_experiments,
    }
    count_matches = len(receipts) == target_experiments
    return {
        "schema_version": "chemworld-g2-provider-session-audit-0.1",
        "target_experiment_count": target_experiments,
        "receipt_count": len(receipts),
        "receipt_count_matches_target": count_matches,
        "receipts": receipt_audits,
        "all_receipts_passed": (
            count_matches
            and len(receipt_audits) == target_experiments
            and all(item["passed"] for item in receipt_audits)
        ),
        "method_resource_checks": method_checks,
        "all_method_resource_checks_passed": all(method_checks.values()),
        "passed": (
            count_matches
            and len(receipt_audits) == target_experiments
            and all(item["passed"] for item in receipt_audits)
            and all(method_checks.values())
        ),
    }


def _archive_workspace(source: Path, destination: Path) -> dict[str, Any]:
    if destination.exists():
        raise FileExistsError(f"workspace archive already exists: {destination}")
    shutil.copytree(source, destination)
    files = sorted(path for path in destination.rglob("*") if path.is_file())
    entries = [
        {
            "path": path.relative_to(destination).as_posix(),
            "sha256": file_sha256(path),
            "byte_count": path.stat().st_size,
        }
        for path in files
    ]
    return {
        "relative_path": destination.name,
        "file_count": len(entries),
        "total_byte_count": sum(item["byte_count"] for item in entries),
        "tree_sha256": canonical_json_sha256(entries),
        "files": entries,
    }


def _redacted_failure(error: Exception) -> dict[str, Any]:
    return {
        "error_type": type(error).__name__,
        "error_text_retained": False,
    }


def _materialized_operation_count(
    trajectory_path: Path,
    history: list[HistoryRecord],
) -> int:
    """Keep failure summaries bound to the durable trajectory, if present."""

    if history:
        return len(history)
    if not trajectory_path.exists():
        return 0
    try:
        return len(load_jsonl(trajectory_path))
    except (OSError, ValueError, json.JSONDecodeError):
        return 0


def _provider_failure_metadata(
    receipts: list[dict[str, Any]],
) -> dict[str, Any]:
    """Summarize provider failures without retaining provider error bodies."""

    failures = [
        receipt
        for receipt in receipts
        if isinstance(receipt, Mapping)
        and (receipt.get("status") != "succeeded" or receipt.get("failure_type") is not None)
    ]
    if not failures:
        return {}
    return {
        "provider_failure_count": len(failures),
        "provider_failure_types": sorted(
            {str(item.get("failure_type") or "unknown") for item in failures}
        ),
    }


def _direct_provider_runtime(protocol: Mapping[str, Any]) -> dict[str, Any] | None:
    """Resolve the auditable direct-operation runtime frozen by a G2 protocol."""

    agent = protocol.get("agent")
    if not isinstance(agent, Mapping):
        return None
    provider = str(agent.get("provider") or "").strip().lower()
    if provider.startswith("deepseek direct"):
        return {
            "transport": "direct_deepseek_chat_completions",
            "provider_id": "deepseek",
            "provider_name": "DeepSeek",
            "provider_base_url": "https://api.deepseek.com/beta",
            "provider_env_key": "DEEPSEEK_API_KEY",
            "wire_api": "chat_completions",
            "model_catalog_endpoint": "https://api.deepseek.com/models",
            "structured_output_transport": "beta_strict_forced_tool_call",
        }
    if provider.startswith("wellau direct"):
        return {
            "transport": "direct_wellau_chat_completions",
            "provider_id": "wellau",
            "provider_name": "WellAU",
            "provider_base_url": "https://api.wellau.com/v1",
            "provider_env_key": "WELLAU_API_KEY",
            "wire_api": "chat_completions",
            "structured_output_transport": "json_object",
        }
    return None


def _run_cell(
    *,
    protocol: Mapping[str, Any],
    source: Mapping[str, Any],
    cli: Mapping[str, Any],
    cell: Mapping[str, Any],
    cell_root: Path,
    card: CampaignResourceCard,
    method_limits: Mapping[str, Any],
    qualification: bool,
    model_provider: str = HTTPS_PROVIDER_ID,
    model_provider_name: str = "OpenAI",
    model_provider_base_url: str | None = None,
    model_provider_env_key: str | None = None,
    model_provider_wire_api: str = "responses",
) -> dict[str, Any]:
    if cell_root.exists():
        raise FileExistsError(f"refusing to overwrite cell: {cell_root}")
    cell_root.mkdir(parents=True)
    config = _cell_config(
        protocol=protocol,
        source=source,
        cli=cli,
        cell=cell,
        card=card,
        method_limits=method_limits,
        qualification=qualification,
    )
    write_json_atomic(cell_root / "run_config.json", config)
    environment_contract = _inspect_cell_environment(
        protocol=protocol,
        cell=cell,
        card=card,
        operation_limit=int(method_limits["operation_limit"]),
    )
    write_json_atomic(
        cell_root / "environment_contract.json",
        environment_contract,
    )
    trajectory_path = cell_root / "trajectory.jsonl"
    summary_path = cell_root / "run_summary.json"
    resource_path = cell_root / "campaign_resource_ledger.json"
    replay_path = cell_root / "exact_replay.json"
    started_at = _now()
    workspace_archive: dict[str, Any] | None = None
    history: list[HistoryRecord] = []
    completed_progress = 0
    with tempfile.TemporaryDirectory(prefix="chemworld-g2-opaque-workspace-") as temporary:
        workspace = Path(temporary) / "workspace"
        agent = InteractiveCodexExperimentAgent(
            workspace=workspace,
            role_id="g2_autonomous_material_matrix_v01",
            model=str(protocol["agent"]["model"]),
            reasoning_effort=str(protocol["agent"]["reasoning_effort"]),
            model_provider=model_provider,
            model_provider_name=model_provider_name,
            model_provider_base_url=model_provider_base_url,
            model_provider_env_key=model_provider_env_key,
            model_provider_wire_api=model_provider_wire_api,
            request_timeout_s=float(protocol["agent"]["request_timeout_s"]),
            finalization_timeout_s=float(protocol["agent"]["finalization_timeout_s"]),
            pre_action_restart_limit=int(protocol["agent"]["pre_action_restart_limit"]),
        )

        def progress(
            record: HistoryRecord,
            trace: list[dict[str, Any]],
        ) -> None:
            nonlocal completed_progress
            del trace
            if record.event_type == "experiment_end":
                completed_progress += 1
            resources = record.info.get("campaign_resources")
            state = resources.get("state") if isinstance(resources, Mapping) else None
            remaining = state.get("remaining") if isinstance(state, Mapping) else None
            print(
                json.dumps(
                    {
                        "cell_id": cell["cell_id"],
                        "step": record.step,
                        "operation": record.action.get("operation"),
                        "instrument": record.action.get("instrument"),
                        "transaction_status": record.info.get("transaction_status"),
                        "event_type": record.event_type,
                        "complete_experiments": completed_progress,
                        "campaign_resources_remaining": remaining,
                    },
                    ensure_ascii=False,
                    sort_keys=True,
                ),
                flush=True,
            )

        try:
            task = protocol["task"]
            history = run_agent(
                env_id=get_task(str(task["task_id"])).env_id,
                agent=agent,
                world_split=str(task["world_split"]),
                budget=int(method_limits["operation_limit"]),
                objective=str(task["objective"]),
                seed=int(cell["world_seed"]),
                agent_seed=int(cell.get("agent_seed", cell["world_seed"])),
                observation_seed=exploration_observation_seed(
                    str(task["task_id"]),
                    int(cell["world_seed"]),
                ),
                task_id=str(task["task_id"]),
                output_path=trajectory_path,
                budget_override=int(method_limits["operation_limit"]),
                episode_mode_override=str(task["episode_mode"]),
                step_callback=progress,
                method_resource_limits=dict(method_limits),
                evaluation_policy="task_contract",
                material_information=dict(cell["material_information"]),
                electrochemical_material_family_id=str(task["electrochemical_material_family_id"]),
                electrochemical_workflow_mode=str(task["electrochemical_workflow_mode"]),
                scoring_contract_id=str(task["scoring_contract_id"]),
                observation_noise_mode=str(task["observation_noise_mode"]),
                observation_noise_namespace=str(task["observation_noise_namespace"]),
                campaign_resource_card=card.to_dict(),
            )
            resources = _resource_snapshot_from_history(history, card=card)
            write_json_atomic(resource_path, resources)
            exact_replay = _write_exact_replay_receipt(
                trajectory_path,
                replay_path,
                campaign_resource_ledger_sha256=str(resources["ledger_sha256"]),
            )
            behavior = _history_summary(history)
            target_batches = int(card.vessel_start_limit)
            ledger_state = resources["state"]
            physical_lifecycle_completed = (
                int(ledger_state.get("vessel_starts", 0)) == target_batches
                and int(ledger_state.get("closed_batches", 0)) == target_batches
                and not behavior["right_censored_open_experiment"]
            )
            method_resources = agent.method_resource_usage()
            receipts = agent.provider_receipts()
            provider_session_audit = _provider_session_audit(
                receipts,
                method_resources,
                target_experiments=target_batches,
            )
            completed = physical_lifecycle_completed and provider_session_audit["passed"]
            summary: dict[str, Any] = {
                "schema_version": "chemworld-g2-autonomous-material-cell-result-0.1",
                "run_status": (
                    "completed"
                    if completed
                    else (
                        "provider_session_audit_failed"
                        if physical_lifecycle_completed
                        else "operation_budget_exhausted_incomplete"
                    )
                ),
                "formal_result": False,
                "confirmatory_claim_allowed": False,
                "qualification_only": qualification,
                "started_at": started_at,
                "finished_at": _now(),
                "cell": deepcopy(dict(cell)),
                "world_seed": int(cell["world_seed"]),
                "seed": int(cell["world_seed"]),
                "condition_id": str(cell["condition_id"]),
                "arm": str(cell["condition_id"]),
                "material_information": deepcopy(dict(cell["material_information"])),
                "config_sha256": config["config_sha256"],
                "pair_config_sha256": config["pair_config_sha256"],
                "trajectory_sha256": file_sha256(trajectory_path),
                "campaign_resource_card_sha256": card.card_sha256,
                "campaign_resource_ledger_path": resource_path.name,
                "campaign_resource_ledger_sha256": resources["ledger_sha256"],
                "exact_replay_path": replay_path.name,
                "exact_replay_verified": exact_replay["verified"],
                "environment_contract": environment_contract,
                "evaluator_provenance": deepcopy(dict(environment_contract["evaluator_identity"])),
                "behavior": behavior,
                "method_resources": method_resources,
                "provider_receipts": receipts,
                "provider_session_audit": provider_session_audit,
                "agent_manifest": agent.manifest(),
                "strict_autonomy_contract": {
                    "one_agent_decision_per_primitive_operation": True,
                    "one_codex_exec_per_complete_experiment": True,
                    "experiment_tool_transport": "host_owned_stdio_mcp",
                    "model_generated_shell_for_lab_operations": False,
                    "codex_approval_policy": "never",
                    "automatic_action_repair": False,
                    "automatic_terminate": False,
                    "automatic_final_assay": False,
                    "forced_notebook": False,
                    "invalid_actions_retained": True,
                },
                "accounting_note": (
                    "Codex provider calls and reported tokens are exact after "
                    "each complete experiment; attributable subscription USD "
                    "cost remains unavailable."
                ),
            }
            write_json_atomic(summary_path, summary)
        except MethodResourceLimitError as error:
            receipts = agent.provider_receipts()
            write_json_atomic(
                summary_path,
                {
                    "schema_version": "chemworld-g2-autonomous-material-cell-result-0.1",
                    "run_status": "method_resource_limit_exhausted",
                    "started_at": started_at,
                    "finished_at": _now(),
                    "cell": deepcopy(dict(cell)),
                    "config_sha256": config["config_sha256"],
                    "pair_config_sha256": config["pair_config_sha256"],
                    "failure": {
                        **_redacted_failure(error),
                        **_provider_failure_metadata(receipts),
                    },
                    "trajectory_materialized": trajectory_path.exists(),
                    "trajectory_sha256": (
                        file_sha256(trajectory_path) if trajectory_path.exists() else None
                    ),
                    "accepted_operation_count": _materialized_operation_count(
                        trajectory_path,
                        history,
                    ),
                    "provider_receipts": receipts,
                    "method_resources": agent.method_resource_usage(),
                },
            )
        except Exception as error:
            receipts = agent.provider_receipts()
            write_json_atomic(
                summary_path,
                {
                    "schema_version": "chemworld-g2-autonomous-material-cell-result-0.1",
                    "run_status": (
                        "provider_infrastructure_failure"
                        if _provider_failure_metadata(receipts)
                        else "infrastructure_or_execution_failure"
                    ),
                    "started_at": started_at,
                    "finished_at": _now(),
                    "cell": deepcopy(dict(cell)),
                    "config_sha256": config["config_sha256"],
                    "pair_config_sha256": config["pair_config_sha256"],
                    "failure": {
                        **_redacted_failure(error),
                        **_provider_failure_metadata(receipts),
                    },
                    "trajectory_materialized": trajectory_path.exists(),
                    "trajectory_sha256": (
                        file_sha256(trajectory_path) if trajectory_path.exists() else None
                    ),
                    "accepted_operation_count": _materialized_operation_count(
                        trajectory_path,
                        history,
                    ),
                    "provider_receipts": receipts,
                    "method_resources": agent.method_resource_usage(),
                },
            )
            raise
        finally:
            agent.close()
            if workspace.exists():
                workspace_archive = _archive_workspace(
                    workspace,
                    cell_root / "codex_workspace",
                )
                write_json_atomic(
                    cell_root / "codex_workspace_manifest.json",
                    workspace_archive,
                )
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    summary["codex_workspace_archive"] = workspace_archive
    write_json_atomic(summary_path, summary)
    return summary


def _run_cell_light(
    *,
    protocol: Mapping[str, Any],
    source: Mapping[str, Any],
    provider_runtime: Mapping[str, Any],
    cell: Mapping[str, Any],
    cell_root: Path,
    card: CampaignResourceCard,
    method_limits: Mapping[str, Any],
    qualification: bool,
) -> dict[str, Any]:
    """Run one cell with one direct strict provider call per primitive operation."""

    if cell_root.exists():
        raise FileExistsError(f"refusing to overwrite cell: {cell_root}")
    cell_root.mkdir(parents=True)
    config = _cell_config(
        protocol=protocol,
        source=source,
        cli=provider_runtime,
        cell=cell,
        card=card,
        method_limits=method_limits,
        qualification=qualification,
    )
    config["provider_runtime"] = config.pop("codex_cli")
    config["execution_layer"] = {
        "decision_transport": "one_logical_provider_decision_per_primitive_operation",
        "provider_attempt_limit_per_operation": int(
            protocol["agent"].get("provider_max_attempts", 1)
        ),
        "shell_tools_enabled": False,
        "lab_tool_used": False,
        "strict_json_schema": True,
    }
    config["config_sha256"] = canonical_json_sha256(
        {key: value for key, value in config.items() if key != "config_sha256"}
    )
    write_json_atomic(cell_root / "run_config.json", config)
    environment_contract = _inspect_cell_environment(
        protocol=protocol,
        cell=cell,
        card=card,
        operation_limit=int(method_limits["operation_limit"]),
    )
    trajectory_path = cell_root / "trajectory.jsonl"
    summary_path = cell_root / "run_summary.json"
    resource_path = cell_root / "campaign_resource_ledger.json"
    replay_path = cell_root / "exact_replay.json"
    started_at = _now()
    history: list[HistoryRecord] = []
    agent: StructuredG2Agent | None = None
    completed_progress = 0

    def progress(record: HistoryRecord, trace: list[dict[str, Any]]) -> None:
        nonlocal completed_progress
        del trace
        if record.event_type in {"experiment_end", "batch_discard"}:
            completed_progress += 1
        resources = record.info.get("campaign_resources")
        state = resources.get("state") if isinstance(resources, Mapping) else None
        remaining = state.get("remaining") if isinstance(state, Mapping) else None
        print(
            json.dumps(
                {
                    "cell_id": cell["cell_id"],
                    "step": record.step,
                    "operation": record.action.get("operation"),
                    "instrument": record.action.get("instrument"),
                    "transaction_status": record.info.get("transaction_status"),
                    "event_type": record.event_type,
                    "closed_batches": completed_progress,
                    "campaign_resources_remaining": remaining,
                },
                ensure_ascii=False,
                sort_keys=True,
            ),
            flush=True,
        )

    try:
        provider_id = str(provider_runtime.get("provider_id") or "")
        if provider_id not in {"deepseek", "wellau"}:
            raise ValueError("light G2 execution requires provider_id=deepseek or wellau")
        default_env_key = "DEEPSEEK_API_KEY" if provider_id == "deepseek" else "WELLAU_API_KEY"
        env_key = str(provider_runtime.get("provider_env_key") or default_env_key)
        api_key = os.environ.get(env_key, "").strip()
        if not api_key:
            raise RuntimeError(f"required provider environment variable is not set: {env_key}")
        task = protocol["task"]
        agent_config = protocol["agent"]
        reasoning_effort = str(agent_config.get("reasoning_effort") or "high")
        if provider_id == "deepseek":
            if reasoning_effort not in {"high", "max"}:
                raise ValueError("DeepSeek reasoning_effort must be high or max")
            client = DeepSeekClient(
                api_key=api_key,
                base_url=str(
                    provider_runtime.get("provider_base_url") or "https://api.deepseek.com"
                ),
                model=str(agent_config["model"]),
                thinking=bool(agent_config.get("thinking", True)),
                reasoning_effort=cast(Any, reasoning_effort),
                strict_tool_calls=True,
                timeout_s=float(agent_config.get("provider_timeout_s", 180.0)),
                max_attempts=int(agent_config.get("provider_max_attempts", 1)),
            )
        else:
            if reasoning_effort not in {"medium", "high"}:
                raise ValueError("WellAU reasoning_effort must be medium or high")
            client = WellAUClient(
                api_key=api_key,
                base_url=str(
                    provider_runtime.get("provider_base_url") or "https://api.wellau.com/v1"
                ),
                model=str(agent_config["model"]),
                reasoning_effort=cast(WellAUReasoningEffort, reasoning_effort),
                timeout_s=float(agent_config.get("provider_timeout_s", 180.0)),
                max_attempts=int(agent_config.get("provider_max_attempts", 1)),
            )
        agent = StructuredG2Agent(
            client,
            role_id="g2_autonomous_material_direct_operation_v01",
            spectrum_disclosure="assigned",
            response_max_tokens=int(agent_config.get("response_max_tokens", 1800)),
            prompt_token_estimate_cap=int(agent_config.get("prompt_token_estimate_cap", 3200)),
            recent_decision_limit=int(agent_config.get("recent_decision_limit", 4)),
            experiment_memory_limit=int(agent_config.get("experiment_memory_limit", 4)),
            fail_fast_on_unbillable_provider_failure=True,
        )
        history = run_agent(
            env_id=get_task(str(task["task_id"])).env_id,
            agent=agent,
            world_split=str(task["world_split"]),
            budget=int(method_limits["operation_limit"]),
            objective=str(task["objective"]),
            seed=int(cell["world_seed"]),
            agent_seed=int(cell["world_seed"]),
            observation_seed=exploration_observation_seed(
                str(task["task_id"]), int(cell["world_seed"])
            ),
            task_id=str(task["task_id"]),
            output_path=trajectory_path,
            budget_override=int(method_limits["operation_limit"]),
            episode_mode_override=str(task["episode_mode"]),
            step_callback=progress,
            method_resource_limits=dict(method_limits),
            evaluation_policy="task_contract",
            material_information=dict(cell["material_information"]),
            electrochemical_material_family_id=str(task["electrochemical_material_family_id"]),
            electrochemical_workflow_mode=str(task["electrochemical_workflow_mode"]),
            scoring_contract_id=str(task["scoring_contract_id"]),
            observation_noise_mode=str(task["observation_noise_mode"]),
            observation_noise_namespace=str(task["observation_noise_namespace"]),
            campaign_resource_card=card.to_dict(),
        )
        resources = _resource_snapshot_from_history(history, card=card)
        write_json_atomic(resource_path, resources)
        exact_replay = _write_exact_replay_receipt(
            trajectory_path,
            replay_path,
            campaign_resource_ledger_sha256=str(resources["ledger_sha256"]),
        )
        behavior = _history_summary(history)
        target_batches = int(card.vessel_start_limit)
        physical_lifecycle_completed = (
            int(resources["state"].get("vessel_starts", 0)) == target_batches
            and int(resources["state"].get("closed_batches", 0)) == target_batches
            and not behavior["right_censored_open_experiment"]
        )
        method_resources = agent.method_resource_usage()
        receipts = agent.provider_receipts()
        provider_decision_audit = _provider_decision_audit(
            receipts,
            method_resources,
            target_operations=len(history),
            expected_provider=str(provider_runtime.get("provider_name") or "WellAU"),
        )
        completed = physical_lifecycle_completed and provider_decision_audit["passed"]
        summary: dict[str, Any] = {
            "schema_version": "chemworld-g2-autonomous-material-cell-result-0.2",
            "run_status": "completed" if completed else "provider_decision_audit_failed",
            "formal_result": False,
            "confirmatory_claim_allowed": False,
            "qualification_only": qualification,
            "started_at": started_at,
            "finished_at": _now(),
            "cell": deepcopy(dict(cell)),
            "world_seed": int(cell["world_seed"]),
            "seed": int(cell["world_seed"]),
            "condition_id": str(cell["condition_id"]),
            "arm": str(cell.get("arm", cell["condition_id"])),
            "material_information": deepcopy(dict(cell["material_information"])),
            "config_sha256": config["config_sha256"],
            "pair_config_sha256": config["pair_config_sha256"],
            "trajectory_sha256": file_sha256(trajectory_path),
            "campaign_resource_card_sha256": card.card_sha256,
            "campaign_resource_ledger_path": resource_path.name,
            "campaign_resource_ledger_sha256": resources["ledger_sha256"],
            "exact_replay_path": replay_path.name,
            "exact_replay_verified": exact_replay["verified"],
            "environment_contract": environment_contract,
            "evaluator_provenance": deepcopy(dict(environment_contract["evaluator_identity"])),
            "behavior": behavior,
            "method_resources": method_resources,
            "provider_receipts": receipts,
            "provider_decision_audit": provider_decision_audit,
            "agent_manifest": agent.manifest(),
            "strict_autonomy_contract": {
                "one_agent_decision_per_primitive_operation": True,
                "one_logical_provider_decision_per_primitive_operation": True,
                "provider_attempt_limit_per_operation": int(
                    agent_config.get("provider_max_attempts", 1)
                ),
                "strict_provider_json_schema": True,
                "shell_tools_enabled": False,
                "lab_tool_used": False,
                "automatic_action_repair": False,
                "automatic_terminate": False,
                "automatic_final_assay": False,
                "forced_notebook": False,
                "invalid_actions_retained": True,
            },
            "accounting_note": (
                "DeepSeek calls, reported token/cache usage, and the frozen pricing snapshot "
                "are retained exactly; billed USD is derived only when accounting is complete."
                if provider_id == "deepseek"
                else (
                    "WellAU calls and reported tokens are retained exactly; provider pricing "
                    "is unavailable, so billed USD is not inferred."
                )
            ),
        }
        write_json_atomic(summary_path, summary)
    except MethodResourceLimitError as error:
        receipts = agent.provider_receipts() if agent is not None else []
        write_json_atomic(
            summary_path,
            {
                "schema_version": "chemworld-g2-autonomous-material-cell-result-0.2",
                "run_status": "method_resource_limit_exhausted",
                "started_at": started_at,
                "finished_at": _now(),
                "cell": deepcopy(dict(cell)),
                "config_sha256": config["config_sha256"],
                "pair_config_sha256": config["pair_config_sha256"],
                "failure": {**_redacted_failure(error), **_provider_failure_metadata(receipts)},
                "trajectory_materialized": trajectory_path.exists(),
                "trajectory_sha256": (
                    file_sha256(trajectory_path) if trajectory_path.exists() else None
                ),
                "accepted_operation_count": _materialized_operation_count(trajectory_path, history),
                "provider_receipts": receipts,
                "method_resources": agent.method_resource_usage() if agent is not None else {},
            },
        )
    except Exception as error:
        receipts = agent.provider_receipts() if agent is not None else []
        write_json_atomic(
            summary_path,
            {
                "schema_version": "chemworld-g2-autonomous-material-cell-result-0.2",
                "run_status": (
                    "provider_infrastructure_failure"
                    if _provider_failure_metadata(receipts)
                    else "infrastructure_or_execution_failure"
                ),
                "started_at": started_at,
                "finished_at": _now(),
                "cell": deepcopy(dict(cell)),
                "config_sha256": config["config_sha256"],
                "pair_config_sha256": config["pair_config_sha256"],
                "failure": {**_redacted_failure(error), **_provider_failure_metadata(receipts)},
                "trajectory_materialized": trajectory_path.exists(),
                "trajectory_sha256": (
                    file_sha256(trajectory_path) if trajectory_path.exists() else None
                ),
                "accepted_operation_count": _materialized_operation_count(trajectory_path, history),
                "provider_receipts": receipts,
                "method_resources": agent.method_resource_usage() if agent is not None else {},
            },
        )
        raise
    return json.loads(summary_path.read_text(encoding="utf-8"))


def _pair_audit(
    left: Mapping[str, Any],
    right: Mapping[str, Any],
) -> dict[str, Any]:
    left_identity = left["environment_contract"]["evaluator_identity"]
    right_identity = right["environment_contract"]["evaluator_identity"]
    identity_keys = (
        "world_id",
        "mechanism_hash",
        "electrochemical_material_family_id",
        "electrochemical_material_family_sha256",
        "electrochemical_material_instance_sha256",
        "observation_noise_mode",
        "observation_noise_namespace",
    )
    invariants = {key: left_identity.get(key) == right_identity.get(key) for key in identity_keys}
    invariants["pair_config_sha256"] = left.get("pair_config_sha256") == right.get(
        "pair_config_sha256"
    )
    if (
        left["cell"].get("trajectory_replicate_id") is not None
        or right["cell"].get("trajectory_replicate_id") is not None
    ):
        invariants["trajectory_replicate_id"] = left["cell"].get(
            "trajectory_replicate_id"
        ) == right["cell"].get("trajectory_replicate_id")
    if left["cell"].get("agent_seed") is not None or right["cell"].get("agent_seed") is not None:
        invariants["agent_seed"] = left["cell"].get("agent_seed") == right["cell"].get("agent_seed")
    left_public = left["environment_contract"]["public_contract"]
    right_public = right["environment_contract"]["public_contract"]
    for key in (
        "task_contract_hash",
        "runtime_profile_hash",
        "scoring_contract_hash",
        "observation_contract_hash",
        "workflow_mode",
    ):
        invariants[key] = left_public.get(key) == right_public.get(key)
    return {
        "world_seed": left["cell"]["world_seed"],
        "trajectory_replicate_id": left["cell"].get("trajectory_replicate_id"),
        "agent_seed": left["cell"].get("agent_seed"),
        "conditions": [
            left["cell"]["condition_id"],
            right["cell"]["condition_id"],
        ],
        "invariants": invariants,
        "passed": all(invariants.values()),
    }


def _write_matrix_manifest(
    path: Path,
    *,
    protocol: Mapping[str, Any],
    source: Mapping[str, Any],
    cli: Mapping[str, Any],
    started_at: str,
    cell_results: list[dict[str, Any]],
    status: str,
) -> dict[str, Any]:
    by_seed: dict[int, list[dict[str, Any]]] = {}
    for item in cell_results:
        by_seed.setdefault(int(item["cell"]["world_seed"]), []).append(item)
    pair_audits = [
        _pair_audit(items[0], items[1]) for _, items in sorted(by_seed.items()) if len(items) == 2
    ]
    payload: dict[str, Any] = {
        "schema_version": "chemworld-g2-autonomous-material-matrix-run-0.1",
        "runner_version": RUNNER_VERSION,
        "protocol_id": protocol["protocol_id"],
        "run_status": status,
        "formal_result": False,
        "confirmatory_claim_allowed": False,
        "started_at": started_at,
        "updated_at": _now(),
        "source": deepcopy(dict(source)),
        "codex_cli": deepcopy(dict(cli)),
        "world_seeds": [int(seed) for seed in protocol["task"]["world_seeds"]],
        "expected_vessels_per_cell": int(
            protocol["campaign_resource_card"]["complete_experiments"]
        ),
        "planned_cell_count": 10,
        "completed_cell_count": sum(item.get("run_status") == "completed" for item in cell_results),
        "planned_physical_experiment_count": 60,
        "completed_physical_experiment_count": sum(
            int(item.get("behavior", {}).get("closed_batch_count", 0)) for item in cell_results
        ),
        "cells": [
            {
                "cell_id": item["cell"]["cell_id"],
                "world_seed": int(item["cell"]["world_seed"]),
                "seed": int(item["cell"]["world_seed"]),
                "condition_id": item["cell"]["condition_id"],
                "arm": item["cell"]["condition_id"],
                "within_pair_order": item["cell"]["within_pair_order"],
                "material_information": deepcopy(dict(item["cell"]["material_information"])),
                "run_dir": item["cell"]["cell_id"],
                "config_path": "run_config.json",
                "summary_path": "run_summary.json",
                "trajectory_path": "trajectory.jsonl",
                "campaign_resource_ledger_path": ("campaign_resource_ledger.json"),
                "exact_replay_path": "exact_replay.json",
                "run_status": item.get("run_status"),
                "config_sha256": item.get("config_sha256"),
                "pair_config_sha256": item.get("pair_config_sha256"),
                "trajectory_sha256": item.get("trajectory_sha256"),
                "campaign_resource_card_sha256": item.get("campaign_resource_card_sha256"),
                "campaign_resource_ledger_sha256": item.get("campaign_resource_ledger_sha256"),
                "provider_session_audit_passed": item.get(
                    "provider_session_audit",
                    {},
                ).get("passed"),
                "provider_receipt_count": item.get(
                    "provider_session_audit",
                    {},
                ).get("receipt_count"),
                "complete_experiment_count": item.get("behavior", {}).get(
                    "complete_experiment_count"
                ),
                "discarded_batch_count": item.get("behavior", {}).get("discarded_batch_count"),
                "closed_batch_count": item.get("behavior", {}).get("closed_batch_count"),
                "best_final_score": item.get("behavior", {}).get("best_final_score"),
            }
            for item in cell_results
        ],
        "pair_audits": pair_audits,
        "all_materialized_pair_audits_passed": all(item["passed"] for item in pair_audits),
        "protocol_file_sha256": source["protocol_file_sha256"],
    }
    payload["manifest_sha256"] = canonical_json_sha256(payload)
    write_json_atomic(path, payload)
    return payload


def _load_json_object(path: Path, *, label: str) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise RuntimeError(f"invalid {label}: {path}") from error
    if not isinstance(payload, dict):
        raise RuntimeError(f"{label} must be a JSON object: {path}")
    return payload


def _validated_resume_result(
    *,
    cell_root: Path,
    cell: Mapping[str, Any],
    protocol: Mapping[str, Any],
    source: Mapping[str, Any],
    cli: Mapping[str, Any],
    card: CampaignResourceCard,
    method_limits: Mapping[str, Any],
) -> dict[str, Any]:
    """Load one completed cell without mutating any of its artifacts."""

    required_paths = {
        "run config": cell_root / "run_config.json",
        "run summary": cell_root / "run_summary.json",
        "trajectory": cell_root / "trajectory.jsonl",
        "campaign resource ledger": (cell_root / "campaign_resource_ledger.json"),
        "exact replay receipt": cell_root / "exact_replay.json",
    }
    missing = [label for label, path in required_paths.items() if not path.is_file()]
    if missing:
        raise RuntimeError(
            f"resume refuses incomplete cell {cell['cell_id']}: " + ", ".join(missing)
        )
    config = _load_json_object(
        required_paths["run config"],
        label="resume run config",
    )
    summary = _load_json_object(
        required_paths["run summary"],
        label="resume run summary",
    )
    resources = _load_json_object(
        required_paths["campaign resource ledger"],
        label="resume campaign resource ledger",
    )
    replay = _load_json_object(
        required_paths["exact replay receipt"],
        label="resume exact replay receipt",
    )
    trajectory_path = required_paths["trajectory"]
    records = load_jsonl(trajectory_path)
    light_execution = "provider_runtime" in config
    expected_limits = {
        key: list(value) if isinstance(value, tuple) else value
        for key, value in method_limits.items()
    }
    expected_pair_hash = _pair_config_sha256(
        protocol=protocol,
        source=source,
        world_seed=int(cell["world_seed"]),
        card=card,
        method_limits=method_limits,
        trajectory_replicate_id=(
            str(cell["trajectory_replicate_id"])
            if cell.get("trajectory_replicate_id") is not None
            else None
        ),
        agent_seed=(int(cell["agent_seed"]) if cell.get("agent_seed") is not None else None),
    )
    config_without_hash = dict(config)
    declared_config_hash = config_without_hash.pop("config_sha256", None)
    observed_config_hash = canonical_json_sha256(config_without_hash)
    raw_receipts = summary.get("provider_receipts")
    raw_method_resources = summary.get("method_resources")
    resume_receipts = (
        [dict(item) for item in raw_receipts if isinstance(item, Mapping)]
        if isinstance(raw_receipts, list)
        else []
    )
    resume_method_resources = (
        dict(raw_method_resources) if isinstance(raw_method_resources, Mapping) else {}
    )
    recomputed_provider_audit = (
        _provider_decision_audit(
            resume_receipts,
            resume_method_resources,
            target_operations=len(records),
            expected_provider=str(cli.get("provider_name") or "WellAU"),
        )
        if light_execution
        else _provider_session_audit(
            resume_receipts,
            resume_method_resources,
            target_experiments=int(card.vessel_start_limit),
        )
    )
    checks = {
        "completed": summary.get("run_status") == "completed",
        "runner_version": config.get("runner_version") == RUNNER_VERSION,
        "protocol_id": config.get("protocol_id") == protocol["protocol_id"],
        "cell": config.get("cell") == dict(cell),
        "world_seed": config.get("world_seed") == int(cell["world_seed"]),
        "trajectory_replicate_id": config.get("trajectory_replicate_id")
        == cell.get("trajectory_replicate_id"),
        "agent_seed": config.get("agent_seed") == cell.get("agent_seed"),
        "material_information": config.get("material_information")
        == dict(cell["material_information"]),
        "source_tree": (
            config.get("source", {}).get("material_source_tree_sha256")
            == source["material_source_tree_sha256"]
        ),
        "protocol_file": (
            config.get("source", {}).get("protocol_file_sha256") == source["protocol_file_sha256"]
        ),
        "provider_runtime": (
            config.get("provider_runtime") == dict(cli)
            if light_execution
            else config.get("codex_cli") == dict(cli)
        ),
        "campaign_card": config.get("campaign_resource_card") == card.to_dict(),
        "campaign_card_sha256": (config.get("campaign_resource_card_sha256") == card.card_sha256),
        "method_limits": config.get("method_resource_limits") == expected_limits,
        "pair_config_sha256": (
            config.get("pair_config_sha256") == expected_pair_hash
            and summary.get("pair_config_sha256") == expected_pair_hash
        ),
        "config_sha256": (
            declared_config_hash == observed_config_hash
            and summary.get("config_sha256") == observed_config_hash
        ),
        "summary_cell": summary.get("cell") == dict(cell),
        "summary_closed_batches": (
            summary.get("behavior", {}).get("closed_batch_count") == int(card.vessel_start_limit)
        ),
        "summary_not_censored": (
            summary.get("behavior", {}).get("right_censored_open_experiment") is False
        ),
        "evaluator_provenance": isinstance(
            summary.get("evaluator_provenance"),
            Mapping,
        ),
        "provider_audit": (
            recomputed_provider_audit["passed"] is True
            and summary.get(
                "provider_decision_audit" if light_execution else "provider_session_audit"
            )
            == recomputed_provider_audit
        ),
    }
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise RuntimeError(f"resume validation failed for {cell['cell_id']}: " + ", ".join(failed))

    trajectory_hash = file_sha256(trajectory_path)
    if (
        summary.get("trajectory_sha256") != trajectory_hash
        or replay.get("trajectory_sha256") != trajectory_hash
        or replay.get("trajectory_record_count") != len(records)
        or replay.get("checked_steps") != len(records)
        or replay.get("verified") is not True
    ):
        raise RuntimeError(f"resume trajectory/replay binding failed for {cell['cell_id']}")
    ledger = CampaignResourceLedger.from_snapshot(resources)
    ledger_state = ledger.snapshot()["state"]
    expected_batches = int(card.vessel_start_limit)
    events = resources.get("events")
    if (
        resources.get("ledger_sha256") != summary.get("campaign_resource_ledger_sha256")
        or resources.get("ledger_sha256") != replay.get("campaign_resource_ledger_sha256")
        or ledger.card.card_sha256 != card.card_sha256
        or int(ledger_state["vessel_starts"]) != expected_batches
        or int(ledger_state["final_assays"]) + int(ledger_state.get("discarded_batches", 0))
        != expected_batches
        or not isinstance(events, list)
        or len(events) != len(records)
    ):
        raise RuntimeError(f"resume resource binding failed for {cell['cell_id']}")
    for index, (event, record) in enumerate(
        zip(events, records, strict=True),
        start=1,
    ):
        outcome = event.get("outcome") if isinstance(event, Mapping) else None
        recorded_status = record.get(
            "transaction_status",
            record.get("environment_outcome", {}).get("transaction_status"),
        )
        if (
            not isinstance(event, Mapping)
            or event.get("action") != record.get("action")
            or not isinstance(outcome, Mapping)
            or (outcome.get("committed") is True) != (recorded_status == "committed")
        ):
            raise RuntimeError(
                f"resume ledger/trajectory mismatch for {cell['cell_id']} at event {index}"
            )
    verification = verify_records(records)
    if not verification.verified:
        raise RuntimeError(f"resume exact replay failed for {cell['cell_id']}")
    return summary


def _load_resume_results(
    output_root: Path,
    *,
    protocol: Mapping[str, Any],
    source: Mapping[str, Any],
    cli: Mapping[str, Any],
    card: CampaignResourceCard,
    method_limits: Mapping[str, Any],
) -> tuple[list[dict[str, Any]], str]:
    """Validate a partial matrix and return only immutable completed cells."""

    manifest_path = output_root / "matrix_manifest.json"
    children = list(output_root.iterdir())
    if not manifest_path.is_file():
        if children:
            raise RuntimeError("resume requires matrix_manifest.json for a non-empty output root")
        return [], _now()
    manifest = _load_json_object(
        manifest_path,
        label="resume matrix manifest",
    )
    manifest_source = manifest.get("source")
    manifest_cli = manifest.get("codex_cli")
    checks = {
        "runner_version": manifest.get("runner_version") == RUNNER_VERSION,
        "protocol_id": manifest.get("protocol_id") == protocol["protocol_id"],
        "world_seeds": manifest.get("world_seeds") == list(protocol["task"]["world_seeds"]),
        "source": (
            isinstance(manifest_source, Mapping)
            and manifest_source.get("material_source_tree_sha256")
            == source["material_source_tree_sha256"]
            and manifest_source.get("protocol_file_sha256") == source["protocol_file_sha256"]
        ),
        "codex_cli": manifest_cli == dict(cli),
    }
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise RuntimeError("resume matrix identity mismatch: " + ", ".join(failed))
    scheduled = _scheduled_cells(protocol)
    expected_ids = {str(cell["cell_id"]) for cell in scheduled}
    unexpected = sorted(
        path.name
        for path in output_root.iterdir()
        if path.name.startswith("cell-") and path.name not in expected_ids
    )
    if unexpected:
        raise RuntimeError("resume found unexpected cell directories: " + ", ".join(unexpected))
    present_flags = [(output_root / str(cell["cell_id"])).exists() for cell in scheduled]
    prefix_length = 0
    while prefix_length < len(present_flags) and present_flags[prefix_length]:
        prefix_length += 1
    if any(present_flags[prefix_length:]):
        raise RuntimeError("resume cell directories are not an exact frozen-schedule prefix")
    manifest_cells = manifest.get("cells")
    if not isinstance(manifest_cells, list):
        raise RuntimeError("resume matrix manifest cells must be a list")
    manifest_prefix = scheduled[:prefix_length]
    if len(manifest_cells) != prefix_length:
        raise RuntimeError("resume manifest cell list does not bind the materialized prefix")
    for expected, observed in zip(
        manifest_prefix,
        manifest_cells,
        strict=True,
    ):
        if not isinstance(observed, Mapping):
            raise RuntimeError("resume manifest cell entry must be an object")
        manifest_identity = {
            "cell_id": observed.get("cell_id"),
            "world_seed": observed.get("world_seed"),
            "condition_id": observed.get("condition_id"),
            "run_dir": observed.get("run_dir"),
        }
        expected_identity = {
            "cell_id": expected["cell_id"],
            "world_seed": expected["world_seed"],
            "condition_id": expected["condition_id"],
            "run_dir": expected["cell_id"],
        }
        if manifest_identity != expected_identity:
            raise RuntimeError(
                "resume manifest cell identity does not match the frozen prefix: "
                f"{expected['cell_id']}"
            )
    results = [
        _validated_resume_result(
            cell_root=output_root / str(cell["cell_id"]),
            cell=cell,
            protocol=protocol,
            source=source,
            cli=cli,
            card=card,
            method_limits=method_limits,
        )
        for cell in manifest_prefix
    ]
    return results, str(manifest.get("started_at") or _now())


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--output-root", type=Path)
    parser.add_argument(
        "--qualification",
        action="store_true",
        help=("Run one seed-0 lifecycle qualification cell instead of the frozen ten-cell matrix."),
    )
    parser.add_argument(
        "--qualification-condition",
        choices=tuple(QUALIFICATION_CONDITION_IDS),
        default="opaque",
        help=("Material-information condition for --qualification (default: opaque)."),
    )
    parser.add_argument(
        "--qualification-experiments",
        type=int,
        choices=QUALIFICATION_EXPERIMENT_COUNTS,
        default=1,
        help=("Fresh-vessel experiments in the same qualification cell (default: 1)."),
    )
    parser.add_argument(
        "--qualification-world-seed",
        type=int,
        choices=(0, 1, 2, 3, 4),
        default=0,
        help="Physical world seed for --qualification (default: 0).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate the frozen protocol and paired environment identities without Codex.",
    )
    parser.add_argument(
        "--allow-external-provider",
        action="store_true",
        help="Required opt-in for ChatGPT-subscription Codex execution.",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help=(
            "Resume a validated partial matrix; completed cell directories are "
            "replayed and never overwritten."
        ),
    )
    return parser


def main() -> int:
    args = _parser().parse_args()
    config_path = args.config.resolve()
    protocol = _load_protocol(config_path)
    source = _source_manifest(config_path)
    if args.dry_run:
        card = _campaign_card(protocol, qualification=False)
        limits = _method_limits(protocol, qualification=False)
        inspections: dict[int, list[dict[str, Any]]] = {}
        for cell in _scheduled_cells(protocol):
            inspection = _inspect_cell_environment(
                protocol=protocol,
                cell=cell,
                card=card,
                operation_limit=int(limits["operation_limit"]),
            )
            inspections.setdefault(int(cell["world_seed"]), []).append(
                {
                    "cell": cell,
                    "environment_contract": inspection,
                    "pair_config_sha256": _pair_config_sha256(
                        protocol=protocol,
                        source=source,
                        world_seed=int(cell["world_seed"]),
                        card=card,
                        method_limits=limits,
                    ),
                }
            )
        audits = [_pair_audit(items[0], items[1]) for _, items in sorted(inspections.items())]
        print(
            json.dumps(
                {
                    "protocol_id": protocol["protocol_id"],
                    "planned_cells": 10,
                    "planned_physical_experiments": 60,
                    "campaign_resource_card_sha256": card.card_sha256,
                    "pair_audits": audits,
                    "passed": all(item["passed"] for item in audits),
                },
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
        )
        return 0
    if not args.allow_external_provider:
        raise RuntimeError("external execution requires --allow-external-provider")
    direct_provider_runtime = _direct_provider_runtime(protocol)
    cli = direct_provider_runtime or _codex_cli_manifest()

    qualification = bool(args.qualification)
    qualification_condition = str(args.qualification_condition)
    qualification_experiments = int(args.qualification_experiments)
    qualification_world_seed = int(args.qualification_world_seed)
    if not qualification and (
        qualification_condition != "opaque"
        or qualification_experiments != 1
        or qualification_world_seed != 0
    ):
        raise RuntimeError(
            "--qualification-condition and --qualification-experiments "
            "select non-default modes only with --qualification"
        )
    if qualification and args.resume:
        raise RuntimeError("--resume is supported only for the ten-cell matrix")
    output_root = (
        args.output_root.resolve()
        if args.output_root is not None
        else (
            _qualification_output_root(
                condition=qualification_condition,
                experiment_count=qualification_experiments,
                world_seed=qualification_world_seed,
            )
            if qualification
            else DEFAULT_MATRIX_ROOT
        )
    )
    if output_root.exists() and not args.resume:
        raise FileExistsError(f"refusing to overwrite existing output root: {output_root}")
    if not output_root.exists():
        output_root.mkdir(parents=True)
    card = _campaign_card(
        protocol,
        qualification=qualification,
        qualification_experiments=qualification_experiments,
    )
    limits = _method_limits(
        protocol,
        qualification=qualification,
        qualification_experiments=qualification_experiments,
    )
    results: list[dict[str, Any]] = []
    started_at = _now()
    if args.resume:
        results, started_at = _load_resume_results(
            output_root,
            protocol=protocol,
            source=source,
            cli=cli,
            card=card,
            method_limits=limits,
        )
    if qualification:
        cell = _qualification_cell(
            protocol,
            condition=qualification_condition,
            experiment_count=qualification_experiments,
            world_seed=qualification_world_seed,
        )
        cell_run_dir = str(cell["cell_id"])
        common_cell_arguments = {
            "protocol": protocol,
            "source": source,
            "cell": cell,
            "cell_root": output_root / cell_run_dir,
            "card": card,
            "method_limits": limits,
            "qualification": True,
        }
        result = (
            _run_cell_light(
                provider_runtime=direct_provider_runtime,
                **common_cell_arguments,
            )
            if direct_provider_runtime is not None
            else _run_cell(cli=cli, **common_cell_arguments)
        )
        write_json_atomic(
            output_root / "qualification_summary.json",
            {
                "schema_version": "chemworld-g2-autonomous-qualification-0.1",
                "run_status": result["run_status"],
                "started_at": started_at,
                "finished_at": _now(),
                "source": source,
                "qualification_condition": qualification_condition,
                "condition_id": cell["condition_id"],
                "material_information": cell["material_information"],
                "qualification_experiments": qualification_experiments,
                "qualification_world_seed": qualification_world_seed,
                "cell_id": cell["cell_id"],
                "cell_run_dir": cell_run_dir,
                "campaign_resource_card_sha256": card.card_sha256,
                "method_resource_limits": {
                    key: list(value) if isinstance(value, tuple) else value
                    for key, value in limits.items()
                },
                "cell_summary": result,
            },
        )
        return 0 if result["run_status"] == "completed" else 2

    manifest_path = output_root / "matrix_manifest.json"
    _write_matrix_manifest(
        manifest_path,
        protocol=protocol,
        source=source,
        cli=cli,
        started_at=started_at,
        cell_results=results,
        status="running",
    )
    completed_cell_ids = {str(result["cell"]["cell_id"]) for result in results}
    try:
        for cell in _scheduled_cells(protocol):
            if str(cell["cell_id"]) in completed_cell_ids:
                continue
            common_cell_arguments = {
                "protocol": protocol,
                "source": source,
                "cell": cell,
                "cell_root": output_root / str(cell["cell_id"]),
                "card": card,
                "method_limits": limits,
                "qualification": False,
            }
            result = (
                _run_cell_light(
                    provider_runtime=direct_provider_runtime,
                    **common_cell_arguments,
                )
                if direct_provider_runtime is not None
                else _run_cell(cli=cli, **common_cell_arguments)
            )
            results.append(result)
            _write_matrix_manifest(
                manifest_path,
                protocol=protocol,
                source=source,
                cli=cli,
                started_at=started_at,
                cell_results=results,
                status="running",
            )
    except Exception:
        _write_matrix_manifest(
            manifest_path,
            protocol=protocol,
            source=source,
            cli=cli,
            started_at=started_at,
            cell_results=results,
            status="failed_or_incomplete",
        )
        raise
    final = _write_matrix_manifest(
        manifest_path,
        protocol=protocol,
        source=source,
        cli=cli,
        started_at=started_at,
        cell_results=results,
        status=(
            "completed"
            if len(results) == 10 and all(item.get("run_status") == "completed" for item in results)
            else "incomplete"
        ),
    )
    return 0 if final["run_status"] == "completed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
