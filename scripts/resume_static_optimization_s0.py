"""Resume an auditable S0 run from a completed exploration prefix."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from run_static_optimization_s0 import (
    _build_client,
    _execute_predictive_validation,
    _execute_validation_target,
    _exploration_horizon,
    _load_json,
    _plan_from_payload,
    _predictive_contract,
    _require_external_execution_confirmation,
)

from chemworld.eval.electrochemical_predictive import (
    PREDICTIVE_PHYSICAL_EXPERIMENT_COUNT,
)
from chemworld.eval.provenance import (
    canonical_json_sha256 as canonical_sha256,
)
from chemworld.eval.provenance import (
    write_json_atomic,
)
from chemworld.eval.static_optimization_execution import (
    StaticOptimizationExperimentSession,
    build_static_optimization_agent,
    static_optimization_workflow_mode,
)
from chemworld.eval.static_optimization_protocol import (
    validate_static_optimization_protocol,
)
from chemworld.eval.static_optimization_seeds import exploration_observation_seed


def _merge_resource_usage(
    prior: Mapping[str, Any], continuation: Mapping[str, Any]
) -> dict[str, Any]:
    combined = copy.deepcopy(dict(prior))
    additive_fields = (
        "model_call_count",
        "input_token_count",
        "output_token_count",
        "monetary_cost_usd",
        "training_environment_step_count",
        "cpu_time_s",
        "gpu_time_s",
        "provider_attempt_count",
        "provider_failure_count",
    )
    for field in additive_fields:
        combined[field] = prior.get(field, 0) + continuation.get(field, 0)
    combined["accounting_complete"] = bool(prior.get("accounting_complete")) and bool(
        continuation.get("accounting_complete")
    )
    combined["usage_source"] = "source_prefix_plus_stateless_continuation"
    usage_keys = {
        *prior.get("provider_usage", {}),
        *continuation.get("provider_usage", {}),
    }
    combined["provider_usage"] = {
        key: int(prior.get("provider_usage", {}).get(key, 0))
        + int(continuation.get("provider_usage", {}).get(key, 0))
        for key in usage_keys
    }
    prior_records = copy.deepcopy(list(prior.get("provider_attempt_records", [])))
    continuation_records = copy.deepcopy(
        list(continuation.get("provider_attempt_records", []))
    )
    logical_offset = int(prior.get("model_call_count", 0))
    for record in continuation_records:
        record["logical_decision_index"] = (
            int(record.get("logical_decision_index", 0)) + logical_offset
        )
    combined["provider_attempt_records"] = prior_records + continuation_records
    return combined


def _resume_cell(
    *,
    source_receipt: Mapping[str, Any],
    protocol: Mapping[str, Any],
    methods: Mapping[str, Any],
    provider: str,
    allow_external_provider: bool,
    source_run_root: Path,
    stop_after_exploration: bool = False,
    known_unreceipted_provider_calls: int = 0,
    redo_final_synthesis: bool = False,
) -> dict[str, Any]:
    receipt = copy.deepcopy(dict(source_receipt))
    horizon = _exploration_horizon(protocol)
    completed_prefix = int(receipt["completed_experiment_count"])
    if not 0 < completed_prefix <= horizon:
        raise ValueError("source receipt must contain a non-empty S0 exploration prefix")
    if known_unreceipted_provider_calls < 0:
        raise ValueError("known unreceipted provider calls must be non-negative")
    source_final_synthesis = copy.deepcopy(receipt.get("final_synthesis"))
    if receipt.get("final_synthesis") is not None and not redo_final_synthesis:
        raise ValueError("source receipt already contains final synthesis")
    if redo_final_synthesis:
        receipt.update(
            {
                "completed_synthesis_call_count": 0,
                "final_synthesis": None,
                "completed_predictive_validation_experiment_count": 0,
                "completed_validation_experiment_count": 0,
                "total_physical_experiment_count": completed_prefix,
                "predictive_validation": None,
                "validation": None,
                "primary_score": None,
            }
        )
    world_seed = int(receipt["cell"]["world_seed"])
    accepted_source_hashes = protocol.get("continuation_contract", {}).get(
        "accepted_source_protocol_sha256_by_world_seed", {}
    )
    accepted_source_hash = (
        str(accepted_source_hashes.get(str(world_seed), ""))
        if isinstance(accepted_source_hashes, Mapping)
        else ""
    )
    if receipt["protocol_sha256"] not in {
        canonical_sha256(protocol),
        accepted_source_hash,
    }:
        raise ValueError("source prefix protocol hash does not match continuation protocol")
    method_id = str(receipt["method_id"])
    if method_id not in methods["methods"]:
        raise ValueError("source prefix method ID is absent from continuation methods")
    task_id = str(receipt["cell"]["task_id"])
    if world_seed != int(protocol["world_policy"]["world_seed"]):
        raise ValueError("source prefix world seed does not match continuation protocol")
    method = methods["methods"][method_id]
    client = _build_client(method, provider, allow_external_provider)
    agent = build_static_optimization_agent(
        protocol,
        task_id,
        llm_methods=methods,
        method_id=method_id,
        client=client,
    )
    history = copy.deepcopy(list(receipt["public_history"]))
    experiments = copy.deepcopy(list(receipt["experiments"]))
    if len(history) != completed_prefix or len(experiments) != completed_prefix:
        raise ValueError("source prefix history and experiment counts disagree")
    observation_seed = exploration_observation_seed(task_id, world_seed)
    for experiment_index in range(completed_prefix, horizon):
        with StaticOptimizationExperimentSession(
            task_id=task_id,
            seed=world_seed,
            experiment_horizon=1,
            experiment_index_offset=experiment_index,
            observation_seed=observation_seed,
            observation_noise_namespace=(
                f"{protocol['observation_noise_namespace']}-{task_id}-"
                f"experiment-{experiment_index:03d}"
            ),
            electrochemical_workflow_mode=static_optimization_workflow_mode(
                protocol
            ),
        ) as session:
            plan = agent.plan_next(history)
            result = session.execute(plan)
        history.append(result.public_record())
        experiments.append(
            {
                "result": result.to_dict(),
                "decision_audit": agent.decision_audit(),
            }
        )
    continuation_usage = agent.method_resource_usage()
    source_failure = copy.deepcopy(receipt.get("failure"))
    prefix_continuation = {
        "source_run_root": str(source_run_root),
        "source_receipt_sha256": canonical_sha256(source_receipt),
        "source_method_config_sha256": source_receipt["method_config_sha256"],
        "source_protocol_sha256": source_receipt["protocol_sha256"],
        "source_failure": source_failure,
        "source_final_synthesis_present": source_final_synthesis is not None,
        "source_completed_predictive_validation_experiment_count": int(
            source_receipt.get(
                "completed_predictive_validation_experiment_count", 0
            )
        ),
        "source_completed_validation_experiment_count": int(
            source_receipt.get("completed_validation_experiment_count", 0)
        ),
        "source_total_physical_experiment_count": int(
            source_receipt.get(
                "total_physical_experiment_count",
                source_receipt["completed_experiment_count"],
            )
        ),
        "redo_final_synthesis": bool(redo_final_synthesis),
        "completed_prefix_experiment_count": completed_prefix,
        "stateless_continuation": True,
        "exploration_prefix_reused_without_modification": True,
        "continuation_model_call_count": continuation_usage["model_call_count"],
        "known_unreceipted_provider_call_count": known_unreceipted_provider_calls,
    }
    if stop_after_exploration:
        receipt.update(
            {
                "method_config_freeze_id": methods["freeze_id"],
                "method_config_sha256": canonical_sha256(methods),
                "protocol_id": protocol["protocol_id"],
                "protocol_sha256": canonical_sha256(protocol),
                "cell_status": "exploration_complete_pending_synthesis",
                "failure": None,
                "agent_manifest": agent.manifest(),
                "resources": _merge_resource_usage(
                    receipt["resources"], continuation_usage
                ),
                "experiment_count": len(experiments),
                "completed_experiment_count": len(experiments),
                "scores": [
                    float(item["terminal_summary"]["leaderboard_score"])
                    for item in history
                ],
                "experiments": experiments,
                "public_history": history,
                "total_physical_experiment_count": len(experiments),
                "continuation": prefix_continuation,
            }
        )
        return receipt
    try:
        recommendation = agent.synthesize_final(history)
    except Exception as error:
        continuation_usage = agent.method_resource_usage()
        failure: dict[str, Any] = {
            "reason_code": "final_synthesis_validation_failure",
            "error_type": type(error).__name__,
            "message": " ".join(str(error).split())[:500],
            "scientific_retry_allowed": False,
        }
        diagnostics = getattr(error, "validation_diagnostics", None)
        if isinstance(diagnostics, Mapping):
            failure["validation_diagnostics"] = copy.deepcopy(dict(diagnostics))
        receipt.update(
            {
                "method_config_freeze_id": methods["freeze_id"],
                "method_config_sha256": canonical_sha256(methods),
                "protocol_id": protocol["protocol_id"],
                "protocol_sha256": canonical_sha256(protocol),
                "cell_status": "method_failure",
                "failure": failure,
                "agent_manifest": agent.manifest(),
                "resources": _merge_resource_usage(
                    receipt["resources"], continuation_usage
                ),
                "experiment_count": len(experiments),
                "completed_experiment_count": len(experiments),
                "scores": [
                    float(item["terminal_summary"]["leaderboard_score"])
                    for item in history
                ],
                "experiments": experiments,
                "public_history": history,
                "total_physical_experiment_count": len(experiments),
                "continuation": {
                    **prefix_continuation,
                    "continuation_model_call_count": continuation_usage[
                        "model_call_count"
                    ],
                },
            }
        )
        return receipt
    final_synthesis = {
        "recommendation": recommendation.to_dict(),
        "synthesis_audit": agent.synthesis_audit(),
        "executes_experiment": False,
        "validation_feedback_returned_to_agent": False,
    }
    predictive_contract = _predictive_contract(protocol)
    predictive_validation: dict[str, Any] | None = None
    if predictive_contract is not None:
        calls_before = int(agent.method_resource_usage()["model_call_count"])
        predictive_validation = _execute_predictive_validation(
            protocol=protocol,
            task_id=task_id,
            world_seed=world_seed,
            history=history,
            predictions_payload=list(recommendation.counterfactual_predictions),
            experiment_index_offset=horizon,
            model_call_count_before_execution=(
                int(receipt["resources"]["model_call_count"]) + calls_before
            ),
        )
        calls_after = int(agent.method_resource_usage()["model_call_count"])
        if calls_after != calls_before:
            raise RuntimeError("predictive continuation changed the model call count")
        predictive_validation["model_call_count_after_execution"] = (
            int(receipt["resources"]["model_call_count"]) + calls_after
        )
    scores = [float(item["terminal_summary"]["leaderboard_score"]) for item in history]
    incumbent_index = max(range(len(scores)), key=scores.__getitem__)
    incumbent_plan = _plan_from_payload(history[incumbent_index]["plan"])
    validation_config = protocol["validation_budget"]
    incumbent_replicates = int(validation_config["incumbent_replicates"])
    recommendation_replicates = int(validation_config["recommendation_replicates"])
    validation_offset = horizon + (
        PREDICTIVE_PHYSICAL_EXPERIMENT_COUNT
        if predictive_contract is not None
        else 0
    )
    incumbent_validation = _execute_validation_target(
        protocol=protocol,
        task_id=task_id,
        world_seed=world_seed,
        target="incumbent",
        plan=incumbent_plan,
        replicate_count=incumbent_replicates,
        experiment_index_offset=validation_offset,
    )
    recommendation_validation = _execute_validation_target(
        protocol=protocol,
        task_id=task_id,
        world_seed=world_seed,
        target="recommendation",
        plan=recommendation.execution_plan(),
        replicate_count=recommendation_replicates,
        experiment_index_offset=validation_offset + incumbent_replicates,
    )
    recommendation_mean = float(recommendation_validation["score_summary"]["mean"])
    incumbent_mean = float(incumbent_validation["score_summary"]["mean"])
    validation = {
        "blind": True,
        "feedback_returned_to_agent": False,
        "incumbent_source_experiment_index": incumbent_index,
        "incumbent_observed_score": scores[incumbent_index],
        "incumbent": incumbent_validation,
        "recommendation": recommendation_validation,
        "primary_validated_recommendation_score_mean": recommendation_mean,
        "validated_incumbent_score_mean": incumbent_mean,
        "recommendation_gain_over_incumbent_mean": recommendation_mean
        - incumbent_mean,
    }
    continuation_usage = agent.method_resource_usage()
    completed_predictive = (
        int(predictive_validation["completed_physical_experiment_count"])
        if predictive_validation is not None
        else 0
    )
    receipt.update(
        {
            "method_config_freeze_id": methods["freeze_id"],
            "method_config_sha256": canonical_sha256(methods),
            "protocol_id": protocol["protocol_id"],
            "protocol_sha256": canonical_sha256(protocol),
            "formal_result": bool(protocol.get("formal_result", False)) and bool(
                methods.get("formal_result", False)
            ),
            "benchmark_claim_allowed": bool(
                protocol.get("benchmark_claim_allowed", False)
            )
            and bool(methods.get("benchmark_claim_allowed", False)),
            "cell_status": "completed",
            "failure": None,
            "agent_manifest": agent.manifest(),
            "resources": _merge_resource_usage(
                receipt["resources"], continuation_usage
            ),
            "experiment_count": len(experiments),
            "completed_experiment_count": len(experiments),
            "scores": scores,
            "experiments": experiments,
            "public_history": history,
            "completed_synthesis_call_count": 1,
            "final_synthesis": final_synthesis,
            "completed_predictive_validation_experiment_count": completed_predictive,
            "completed_validation_experiment_count": (
                incumbent_replicates + recommendation_replicates
            ),
            "total_physical_experiment_count": len(experiments)
            + completed_predictive
            + incumbent_replicates
            + recommendation_replicates,
            "predictive_validation": predictive_validation,
            "validation": validation,
            "primary_score": recommendation_mean,
            "continuation": {
                **prefix_continuation,
                "continuation_model_call_count": continuation_usage[
                    "model_call_count"
                ],
            },
        }
    )
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol", type=Path, required=True)
    parser.add_argument("--llm-methods", type=Path, required=True)
    parser.add_argument("--source-run-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--provider", choices=("mock", "deepseek", "wellau"), required=True)
    parser.add_argument("--allow-external-provider", action="store_true")
    parser.add_argument("--confirm-protocol-sha256")
    parser.add_argument("--confirm-method-sha256")
    parser.add_argument("--world-seed", type=int)
    parser.add_argument("--redo-final-synthesis", action="store_true")
    parser.add_argument("--stop-after-exploration", action="store_true")
    parser.add_argument(
        "--known-unreceipted-provider-calls",
        type=int,
        default=0,
    )
    args = parser.parse_args()
    protocol = _load_json(args.protocol)
    if args.world_seed is not None:
        protocol = copy.deepcopy(protocol)
        protocol["world_policy"] = copy.deepcopy(protocol["world_policy"])
        protocol["world_policy"]["world_seed"] = int(args.world_seed)
    validate_static_optimization_protocol(protocol)
    methods = _load_json(args.llm_methods)
    _require_external_execution_confirmation(
        protocol=protocol,
        methods=methods,
        provider=str(args.provider),
        allow_external_provider=bool(args.allow_external_provider),
        confirmed_protocol_sha256=args.confirm_protocol_sha256,
        confirmed_method_sha256=args.confirm_method_sha256,
    )
    source_report_path = args.source_run_root / "report.json"
    source_report = json.loads(source_report_path.read_text(encoding="utf-8"))
    source_receipt_paths = sorted((args.source_run_root / "receipts").glob("*.json"))
    source_receipts = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in source_receipt_paths
    ]
    cells = [
        _resume_cell(
            source_receipt=receipt,
            protocol=protocol,
            methods=methods,
            provider=str(args.provider),
            allow_external_provider=bool(args.allow_external_provider),
            source_run_root=args.source_run_root,
            stop_after_exploration=bool(args.stop_after_exploration),
            known_unreceipted_provider_calls=int(
                args.known_unreceipted_provider_calls
            ),
            redo_final_synthesis=bool(args.redo_final_synthesis),
        )
        for receipt in source_receipts
    ]
    for cell in cells:
        filename = f"{cell['method_id']}--{cell['cell']['task_id']}.json"
        write_json_atomic(args.output / "receipts" / filename, cell)
    report = copy.deepcopy(source_report)
    formal_result = bool(protocol.get("formal_result", False)) and bool(
        methods.get("formal_result", False)
    )
    superseded_source_physical_experiments = sum(
        int(
            item.get("continuation", {}).get(
                "source_completed_predictive_validation_experiment_count", 0
            )
        )
        + int(
            item.get("continuation", {}).get(
                "source_completed_validation_experiment_count", 0
            )
        )
        for item in cells
        if item.get("continuation", {}).get("redo_final_synthesis") is True
    )
    report.update(
        {
            "method_config_freeze_id": methods["freeze_id"],
            "method_config_sha256": canonical_sha256(methods),
            "protocol_id": protocol["protocol_id"],
            "protocol_sha256": canonical_sha256(protocol),
            "formal_result": formal_result,
            "benchmark_claim_allowed": bool(
                protocol.get("benchmark_claim_allowed", False)
            )
            and bool(methods.get("benchmark_claim_allowed", False)),
            "completed_cell_count": sum(
                item["cell_status"] == "completed" for item in cells
            ),
            "method_failure_cell_count": sum(
                item["cell_status"] == "method_failure" for item in cells
            ),
            "completed_experiment_count": sum(
                item["completed_experiment_count"] for item in cells
            ),
            "completed_synthesis_call_count": sum(
                item["completed_synthesis_call_count"] for item in cells
            ),
            "completed_predictive_validation_experiment_count": sum(
                item["completed_predictive_validation_experiment_count"]
                for item in cells
            ),
            "completed_validation_experiment_count": sum(
                item["completed_validation_experiment_count"] for item in cells
            ),
            "total_physical_experiment_count": sum(
                item["total_physical_experiment_count"] for item in cells
            ),
            "superseded_source_physical_experiment_count": (
                superseded_source_physical_experiments
            ),
            "effective_lineage_total_physical_experiment_count": sum(
                item["total_physical_experiment_count"] for item in cells
            )
            + superseded_source_physical_experiments,
            "provider_call_count": sum(
                item["resources"]["model_call_count"] for item in cells
            ),
            "known_unreceipted_provider_call_count": int(
                args.known_unreceipted_provider_calls
            ),
            "effective_minimum_provider_call_count": sum(
                item["resources"]["model_call_count"] for item in cells
            )
            + int(args.known_unreceipted_provider_calls),
            "provider_token_accounting_complete": (
                int(args.known_unreceipted_provider_calls) == 0
            ),
            "provider_attempt_count": sum(
                item["resources"]["provider_attempt_count"] for item in cells
            ),
            "provider_reported_total_tokens": sum(
                item["resources"]["provider_usage"]["total_tokens"]
                for item in cells
            ),
            "accounting_complete": all(
                item["resources"]["accounting_complete"] for item in cells
            ),
            "known_billed_cost_usd": sum(
                item["resources"]["monetary_cost_usd"]
                for item in cells
                if item["resources"]["accounting_complete"]
            ),
            "receipt_sha256": {
                f"{item['method_id']}:{item['cell']['task_id']}": canonical_sha256(
                    item
                )
                for item in cells
            },
            "cells": cells,
            "continuation": {
                "source_run_root": str(args.source_run_root),
                "source_report_sha256": hashlib.sha256(
                    source_report_path.read_bytes()
                ).hexdigest(),
                "stateless_prefix_continuation": True,
                "redo_final_synthesis": bool(args.redo_final_synthesis),
                "formal_result": formal_result,
            },
            "interpretation": (
                "Owner-authorized S0 continuation. The completed exploration prefix is "
                "reused exactly; final synthesis, predictive validation, and blind "
                "validation are executed under the declared continuation contract."
            ),
        }
    )
    write_json_atomic(args.output / "report.json", report)
    print(
        json.dumps(
            {
                "output": str(args.output),
                "completed_cells": report["completed_cell_count"],
                "completed_experiments": report["completed_experiment_count"],
                "provider_calls": report["provider_call_count"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
