"""Audit the RL substrate without upgrading diagnostic checkpoints to evidence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np

from chemworld.rl.environment import RLWorldAllocation, build_rl_environment, load_rl_protocol

ROOT = Path(__file__).resolve().parents[1]
RL_PROTOCOL = ROOT / "configs/benchmark/rl_baselines_vnext.json"
FREEZE_PROTOCOL = ROOT / "configs/benchmark/confirmatory_freeze_vnext.json"
OUTPUT = ROOT / "workstreams/benchmark_v1/reports/rl-baseline-controls.json"
DEVELOPMENT_REPORT = ROOT / "workstreams/benchmark_v1/reports/rl-interaction-development.json"
HUNDRED_K_REPORT = ROOT / "workstreams/benchmark_v1/reports/rl-100k-development.json"


def build_report() -> dict[str, Any]:
    rl_protocol = load_rl_protocol(RL_PROTOCOL)
    freeze = load_rl_protocol(FREEZE_PROTOCOL)
    train = freeze["world_family_allocation"]["train"]
    dev = freeze["world_family_allocation"]["dev"]
    bench = freeze["world_family_allocation"]["bench"]
    seed_sets = {
        name: set(
            range(int(card["base_seeds"]["start"]), int(card["base_seeds"]["stop_inclusive"]) + 1)
        )
        for name, card in (("train", train), ("dev", dev), ("bench", bench))
    }
    task_probes: dict[str, Any] = {}
    observed_action_keys: list[str] | None = None
    for task_id in rl_protocol["core_tasks"]:
        allocation = RLWorldAllocation.from_protocol(freeze, task_id=task_id, name="train")
        env = build_rl_environment(
            task_id=task_id, allocation=allocation, sampler_seed=7, operation_budget=4
        )
        try:
            observation, info = env.reset()
            action = env.action_space.sample()
            next_observation, reward, terminated, truncated, next_info = env.step(action)
            current: Any = env
            while current is not None and not hasattr(current, "action_contract"):
                current = getattr(current, "env", None)
            action_contract = current.action_contract() if current is not None else {}
            observed_action_keys = list(action_contract.get("action_keys", []))
            task_probes[task_id] = {
                "allocation": allocation.public_manifest(),
                "box_action": env.action_space.shape == (49,),
                "finite_observation": bool(np.all(np.isfinite(observation))),
                "finite_step": bool(
                    np.all(np.isfinite(next_observation)) and np.isfinite(float(reward))
                ),
                "world_cell_exposed_to_audit": "rl_world_cell" in info,
                "hidden_axis_identity_absent": info.get("rl_world_cell", {}).get(
                    "axis_identity_visible"
                )
                is False
                and "axis_id" not in info.get("rl_world_cell", {})
                and "world_seed" not in info.get("rl_world_cell", {}),
                "terminated_or_truncated_is_boolean": isinstance(terminated, bool)
                and isinstance(truncated, bool),
                "constraint_flags_retained": "constraint_flags" in next_info,
            }
        finally:
            env.close()
    checks = {
        "schema": rl_protocol.get("schema_version") == "chemworld-rl-baseline-protocol-0.3",
        "candidate_is_non_claiming": rl_protocol.get("benchmark_claim_allowed") is False,
        "ppo_and_sac_declared": set(rl_protocol["algorithms"]) == {"ppo", "sac"},
        "shared_action_contract": set(rl_protocol["action_contract"]["shared_by_algorithms"])
        == {"ppo", "sac"},
        "fixed_action_semantics": rl_protocol["action_contract"]["fixed_global_operation_semantics"]
        is True,
        "public_affordance_masked_decoding": rl_protocol["action_contract"][
            "public_affordance_masked_decoding"
        ]
        is True,
        "action_key_order_frozen": observed_action_keys == rl_protocol["action_contract"]["keys"],
        "json_stable_action_execution": rl_protocol["action_contract"].get(
            "execution_numeric_policy"
        )
        == (
            "normalize numpy values to their JSON trajectory representation before "
            "environment execution"
        ),
        "train_dev_bench_seed_disjoint": not (
            seed_sets["train"] & seed_sets["dev"]
            or seed_sets["train"] & seed_sets["bench"]
            or seed_sets["dev"] & seed_sets["bench"]
        ),
        "bench_finetuning_forbidden": rl_protocol["training"]["bench_finetuning_allowed"] is False,
        "exact_training_step_budget": rl_protocol["training"].get(
            "actual_environment_steps_must_equal_budget"
        )
        is True
        and 1_000_000 % int(rl_protocol["algorithms"]["ppo"]["hyperparameters"]["n_steps"])
        == 0,
        "periodic_checkpointing_required": int(
            rl_protocol["training"].get("periodic_checkpoint_interval_steps", 0)
        )
        > 0
        and rl_protocol["training"].get("sac_replay_buffer_checkpoint_required") is True,
        "all_core_task_probes_pass": all(
            all(value for key, value in card.items() if key != "allocation")
            for card in task_probes.values()
        ),
    }
    controls_ready = all(checks.values())
    development_evidence: dict[str, Any] | None = None
    if DEVELOPMENT_REPORT.is_file():
        development = load_rl_protocol(DEVELOPMENT_REPORT)
        development_checks = {
            "schema": development.get("schema_version")
            == "chemworld-rl-interaction-development-report-0.1",
            "nonclaiming": development.get("benchmark_claim_allowed") is False,
            "source_commit_bound": isinstance(
                development.get("evaluated_source_commit"), str
            )
            and len(development["evaluated_source_commit"]) == 40,
            "ppo_and_sac_present": set(development.get("algorithm_cards", {}))
            == {"ppo", "sac"},
            "formal_training_still_open": development.get("formal_training_complete")
            is False,
            "formal_bench_still_open": development.get(
                "formal_bench_evaluation_complete"
            )
            is False,
        }
        development_evidence = {
            "report_path": str(DEVELOPMENT_REPORT.relative_to(ROOT)),
            "checks": development_checks,
            "eligible_algorithms": development.get("eligible_algorithms", []),
            "all_algorithms_eligible": development.get("all_algorithms_eligible", False),
            "passed": all(development_checks.values()),
        }
    hundred_k_evidence: dict[str, Any] | None = None
    if HUNDRED_K_REPORT.is_file():
        hundred_k = load_rl_protocol(HUNDRED_K_REPORT)
        manifest = hundred_k.get("training_manifest", {})
        hundred_k_checks = {
            "schema": hundred_k.get("schema_version")
            == "chemworld-rl-100k-development-report-0.1",
            "nonclaiming": hundred_k.get("benchmark_claim_allowed") is False,
            "source_commit_bound": isinstance(hundred_k.get("evaluated_source_commit"), str)
            and len(hundred_k["evaluated_source_commit"]) == 40,
            "exact_100k_steps": manifest.get("training_environment_step_count") == 100_000
            and manifest.get("requested_training_environment_step_count") == 100_000
            and manifest.get("step_budget_exact") is True,
            "all_development_gates_pass": all(
                hundred_k.get("evidence_gate", {}).values()
            ),
            "eligible_for_multiseed_development": hundred_k.get(
                "eligible_for_multiseed_development"
            )
            is True,
            "formal_training_still_open": hundred_k.get("formal_training_complete")
            is False,
            "formal_bench_still_open": hundred_k.get(
                "formal_bench_evaluation_complete"
            )
            is False,
        }
        hundred_k_evidence = {
            "report_path": str(HUNDRED_K_REPORT.relative_to(ROOT)),
            "checks": hundred_k_checks,
            "learning_curve_checkpoint_count": len(
                hundred_k.get("learning_curve_dev", [])
            ),
            "passed": all(hundred_k_checks.values()),
        }
    return {
        "schema_version": "chemworld-rl-baseline-audit-0.1",
        "protocol_id": rl_protocol["protocol_id"],
        "status": (
            "controls_ready_100k_development_passed_formal_training_missing"
            if controls_ready and hundred_k_evidence is not None
            else "controls_ready_development_completed_formal_training_missing"
            if controls_ready and development_evidence is not None
            else "controls_ready_training_missing"
            if controls_ready
            else "controls_failed"
        ),
        "controls_ready": controls_ready,
        "formal_training_complete": False,
        "formal_bench_evaluation_complete": False,
        "benchmark_claim_allowed": False,
        "publication_ready": False,
        "checks": checks,
        "development_evidence": development_evidence,
        "hundred_k_development_evidence": hundred_k_evidence,
        "task_probes": task_probes,
        "remaining_release_gates": rl_protocol["formal_readiness_requirements"],
    }


def main() -> None:
    report = build_report()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    if not report["controls_ready"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
