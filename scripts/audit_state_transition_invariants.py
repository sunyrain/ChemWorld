"""Audit operation semantics and transactional state invariants for all public actions."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import subprocess
from copy import deepcopy
from pathlib import Path
from typing import Any
from unittest.mock import patch

import gymnasium as gym
import numpy as np

import chemworld  # noqa: F401
from chemworld.foundation import Observation, audit_ledger_single_source_of_truth
from chemworld.runtime.kernel_registry import affected_ledgers
from chemworld.world.operations import OPERATION_TYPES, operation_contracts

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROTOCOL = ROOT / "configs/foundation/state_transition_invariants_vnext.json"
DEFAULT_OUTPUT = ROOT / "workstreams/world_foundation/reports/state-transition-invariants.json"
PROTOCOL_SCHEMA_VERSION = "chemworld-foundation-state-transition-protocol-0.1"
REPORT_SCHEMA_VERSION = "chemworld-foundation-state-transition-report-0.1"


def load_protocol(path: Path = DEFAULT_PROTOCOL) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema_version") != PROTOCOL_SCHEMA_VERSION:
        raise ValueError("unsupported state-transition protocol schema")
    operations = payload.get("operations")
    if not isinstance(operations, dict) or set(operations) != set(OPERATION_TYPES):
        raise ValueError("protocol must declare every registered operation exactly once")
    semantics = {case.get("semantic") for case in operations.values()}
    if not semantics <= set(payload["allowed_semantics"]):
        raise ValueError("protocol contains an unsupported operation semantic")
    fixtures = payload.get("setup_fixtures", {})
    missing_fixtures = sorted({case.get("setup") for case in operations.values()} - set(fixtures))
    if missing_fixtures:
        raise ValueError(f"missing setup fixtures: {missing_fixtures}")
    return payload


def build_report(
    protocol: dict[str, Any] | None = None,
    *,
    repository_root: Path = ROOT,
) -> dict[str, Any]:
    protocol = load_protocol() if protocol is None else protocol
    operation_results: dict[str, dict[str, Any]] = {}
    zero_effect_acceptances: list[dict[str, str]] = []
    negative_value_acceptances: list[dict[str, str]] = []
    control_failures: list[str] = []

    for operation in OPERATION_TYPES:
        case = protocol["operations"][operation]
        primary = _run_positive_case(protocol, case, seed=0, include_repeat=True)
        replay = _run_positive_case(protocol, case, seed=0, include_repeat=False)
        invalid = _run_invalid_case(protocol, case, operation)
        boundaries = _probe_numeric_boundaries(protocol, case, operation)
        zero_effect_acceptances.extend(boundaries["accepted_zero"])
        negative_value_acceptances.extend(boundaries["accepted_negative"])

        case_checks = {
            "committed": primary["transaction_status"] == "committed",
            "declared_effect_observed": primary["declared_effect_observed"],
            "constitution_passed": primary["constitution_passed"],
            "typed_state_authoritative": primary["typed_state_authoritative"],
            "internal_conservation_passed": primary["internal_conservation_passed"],
            "repeat_evidence_recorded": primary["repeat"]["status"]
            in {
                "committed",
                "rolled_back",
                "validation_failed",
            },
            "deterministic_replay": (
                primary["state_digest"] == replay["state_digest"]
                and primary["observation_digest"] == replay["observation_digest"]
            ),
            "invalid_action_atomic": invalid["atomic"],
            "invalid_action_penalty_declared": invalid["penalty_declared"],
            "invalid_observation_not_committed": invalid["observation_history_unchanged"],
            "negative_values_rejected": not boundaries["accepted_negative"],
        }
        for name, passed in case_checks.items():
            if not passed:
                control_failures.append(f"{operation}:{name}")
        operation_results[operation] = {
            "declaration": {
                "semantic": case["semantic"],
                "conservation": case["conservation"],
                "task_id": case["task_id"],
                "setup_fixture": case["setup"],
                "required_effect_any": case["required_effect_any"],
                "contract": operation_contracts()[operation].to_dict(),
                "affected_ledgers": list(affected_ledgers(operation)),
            },
            "checks": case_checks,
            "positive_probe": primary,
            "invalid_probe": invalid,
            "numeric_boundary_probe": boundaries,
        }

    final_assay = _probe_final_assay_boundary()
    rollback_final_assay = _probe_rolled_back_final_assay_boundary()
    malformed_actions = _probe_malformed_action_boundary()
    observation_integrity = _probe_observation_integrity_boundary()
    post_terminal = _probe_post_terminal_barrier(protocol)
    if not final_assay["repeated_final_assay_rejected"]:
        control_failures.append("measure:repeated_final_assay_rejected")
    if not rollback_final_assay["passed"]:
        control_failures.append("measure:rolled_back_final_assay_fail_closed")
    if not malformed_actions["passed"]:
        control_failures.append("input:malformed_actions_fail_closed")
    if not observation_integrity["passed"]:
        control_failures.append("output:observation_integrity_fail_closed")
    if not post_terminal["all_process_operations_rejected"]:
        control_failures.append("terminate:post_terminal_barrier")

    defect_inventory: list[dict[str, Any]] = []
    if zero_effect_acceptances:
        defect_inventory.append(
            {
                "defect_id": "state-zero-effect-actions-accepted",
                "severity": "P0",
                "summary": (
                    "Zero-effect process payloads are accepted for one or more "
                    "operations, allowing budget-consuming no-op transactions."
                ),
                "evidence": zero_effect_acceptances,
                "recommended_slice": "foundation-state-fix--zero-effect-actions",
            }
        )
    if negative_value_acceptances:
        defect_inventory.append(
            {
                "defect_id": "state-negative-payload-accepted",
                "severity": "P0",
                "summary": "Negative process payloads crossed public validation.",
                "evidence": negative_value_acceptances,
                "recommended_slice": "foundation-state-fix--negative-payloads",
            }
        )
    if control_failures:
        defect_inventory.append(
            {
                "defect_id": "state-transition-control-failure",
                "severity": "P0",
                "summary": "One or more transaction controls failed.",
                "evidence": sorted(control_failures),
                "recommended_slice": "foundation-state-fix--transaction-controls",
            }
        )

    source_commit, source_tree_dirty = _git_state(repository_root)
    checks = {
        "operation_count_exact": len(operation_results)
        == protocol["expected_operation_count"]
        == len(OPERATION_TYPES),
        "operation_coverage_exact": set(operation_results) == set(OPERATION_TYPES),
        "semantic_declarations_complete": all(
            result["declaration"]["semantic"] in protocol["allowed_semantics"]
            for result in operation_results.values()
        ),
        "positive_probe_complete": all(
            result["positive_probe"]["transaction_status"] for result in operation_results.values()
        ),
        "invalid_atomicity_probe_complete": all(
            result["invalid_probe"]["atomic"] for result in operation_results.values()
        ),
        "replay_probe_complete": all(
            "deterministic_replay" in result["checks"] for result in operation_results.values()
        ),
        "numeric_boundary_probe_complete": all(
            operation in operation_results for operation in protocol["zero_effect_fields"]
        ),
        "final_assay_repeat_guarded": final_assay["repeated_final_assay_rejected"],
        "rolled_back_final_assay_fail_closed": rollback_final_assay["passed"],
        "malformed_actions_fail_closed": malformed_actions["passed"],
        "observation_integrity_fail_closed": observation_integrity["passed"],
        "post_terminal_process_barrier": post_terminal["all_process_operations_rejected"],
    }
    report: dict[str, Any] = {
        "schema_version": REPORT_SCHEMA_VERSION,
        "protocol_id": protocol["protocol_id"],
        "protocol_sha256": _json_hash(protocol),
        "source_commit": source_commit,
        "source_tree_dirty": source_tree_dirty,
        "status": (
            "audit_complete_defects_found"
            if defect_inventory
            else "audit_complete_no_defects_found"
        ),
        "controls_complete": all(checks.values()),
        "benchmark_claim_allowed": False,
        "operation_count": len(operation_results),
        "checks": checks,
        "operation_results": operation_results,
        "final_assay_boundary": final_assay,
        "rolled_back_final_assay_boundary": rollback_final_assay,
        "malformed_action_boundary": malformed_actions,
        "observation_integrity_boundary": observation_integrity,
        "post_terminal_boundary": post_terminal,
        "defect_inventory": defect_inventory,
        "control_failures": sorted(control_failures),
        "zero_effect_acceptances": zero_effect_acceptances,
        "negative_value_acceptances": negative_value_acceptances,
        "failure_policy": protocol["failure_policy"],
        "legacy_constraints": protocol["legacy_constraints"],
        "limitations": [
            "This artifact audits runtime controls; it is not benchmark evidence.",
            "External-input/output operations use declared open-system conservation semantics.",
            (
                "An invalid action intentionally consumes one environment attempt "
                "and only the declared process penalty."
            ),
        ],
        "report_hash": None,
    }
    report["report_hash"] = _report_hash(report)
    return report


def validate_report(
    report: dict[str, Any],
    protocol: dict[str, Any] | None = None,
) -> list[str]:
    protocol = load_protocol() if protocol is None else protocol
    errors: list[str] = []
    if report.get("schema_version") != REPORT_SCHEMA_VERSION:
        errors.append("unsupported report schema")
    if report.get("protocol_sha256") != _json_hash(protocol):
        errors.append("protocol hash mismatch")
    if report.get("operation_count") != protocol["expected_operation_count"]:
        errors.append("operation count mismatch")
    if set(report.get("operation_results", {})) != set(OPERATION_TYPES):
        errors.append("operation coverage mismatch")
    checks = report.get("checks")
    if not isinstance(checks, dict) or not checks or not all(checks.values()):
        errors.append("one or more audit-completeness controls failed")
    if report.get("report_hash") != _report_hash({**report, "report_hash": None}):
        errors.append("report hash mismatch")
    return errors


def write_report(report: dict[str, Any], path: Path = DEFAULT_OUTPUT) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _run_positive_case(
    protocol: dict[str, Any],
    case: dict[str, Any],
    *,
    seed: int,
    include_repeat: bool,
) -> dict[str, Any]:
    env = gym.make(
        "ChemWorld",
        task_id=case["task_id"],
        seed=seed,
        budget_override=100,
    )
    try:
        env.reset(seed=seed)
        base: Any = env.unwrapped
        setup_evidence = []
        for action in protocol["setup_fixtures"][case["setup"]]:
            _observation, _reward, terminated, truncated, info = env.step(deepcopy(action))
            setup_evidence.append(
                {
                    "operation": action["operation"],
                    "transaction_status": info["transaction_status"],
                }
            )
            if info["transaction_status"] != "committed" or terminated or truncated:
                raise AssertionError(
                    f"setup {case['setup']} failed at {action['operation']}: {info}"
                )
        before = base._state
        before_payload = before.to_dict(include_hidden=True)
        observation, _reward, _terminated, _truncated, info = env.step(deepcopy(case["action"]))
        after = base._state
        after_payload = after.to_dict(include_hidden=True)
        effects = _effect_flags(before_payload, after_payload, info)
        state_findings = [
            finding.to_dict() for finding in audit_ledger_single_source_of_truth(after)
        ]
        state_report = base.constitution.check_state(after)
        internal_conservation = True
        conservation_detail: dict[str, Any] | None = None
        if case["conservation"] == "internal_transform":
            conservation = base.constitution.check_material_conservation(before, after)
            internal_conservation = conservation.passed
            conservation_detail = conservation.to_dict()

        repeat: dict[str, Any] = {"status": "not_run"}
        if include_repeat:
            repeat_before = base._state
            repeat_snapshot = _failure_atomic_snapshot(repeat_before)
            _repeat_observation, _repeat_reward, _term, _trunc, repeat_info = env.step(
                deepcopy(case["action"])
            )
            repeat_after = base._state
            repeat = {
                "status": repeat_info["transaction_status"],
                "rollback_reason": repeat_info["rollback_reason"],
                "changed_roots": _changed_roots(
                    repeat_before.to_dict(include_hidden=True),
                    repeat_after.to_dict(include_hidden=True),
                ),
                "atomic_if_rejected": (
                    True
                    if repeat_info["transaction_status"] == "committed"
                    else repeat_snapshot == _failure_atomic_snapshot(repeat_after)
                ),
            }

        return {
            "transaction_status": info["transaction_status"],
            "rollback_reason": info["rollback_reason"],
            "setup": setup_evidence,
            "changed_roots": _changed_roots(before_payload, after_payload),
            "effect_flags": effects,
            "declared_effect_observed": any(
                effects.get(effect, False) for effect in case["required_effect_any"]
            ),
            "constitution_passed": state_report.passed,
            "constitution_checks": {
                "count": len(state_report.checks),
                "failures": [check.to_dict() for check in state_report.checks if not check.passed],
            },
            "typed_state_authoritative": all(finding["passed"] for finding in state_findings),
            "typed_state_findings": {
                "count": len(state_findings),
                "failures": [finding for finding in state_findings if not finding["passed"]],
            },
            "internal_conservation_passed": internal_conservation,
            "internal_conservation": conservation_detail,
            "state_digest": _json_hash(after_payload),
            "observation_digest": _observation_hash(observation),
            "repeat": repeat,
        }
    finally:
        env.close()


def _run_invalid_case(
    protocol: dict[str, Any],
    case: dict[str, Any],
    operation: str,
) -> dict[str, Any]:
    env = gym.make(
        "ChemWorld",
        task_id=case["task_id"],
        seed=0,
        budget_override=100,
    )
    try:
        env.reset(seed=0)
        base: Any = env.unwrapped
        before = base._state
        before_snapshot = _failure_atomic_snapshot(before)
        before_history = _observation_history(before)
        before_step = base._step_count
        _obs, reward, terminated, truncated, info = env.step({"operation": operation})
        after = base._state
        cost_delta = after.ledger.cost - before.ledger.cost
        risk_delta = after.ledger.risk - before.ledger.risk
        allowed_costs = protocol["failure_policy"]["allowed_cost_penalties"]
        expected_risk = protocol["failure_policy"]["expected_risk_penalty"]
        return {
            "transaction_status": info["transaction_status"],
            "rollback_reason": info["rollback_reason"],
            "invalid_reasons": info.get(
                "invalid_reasons",
                [key for key, passed in info.get("preconditions", {}).items() if passed is False],
            ),
            "atomic": before_snapshot == _failure_atomic_snapshot(after),
            "penalty_declared": (
                any(math.isclose(cost_delta, value, abs_tol=1.0e-12) for value in allowed_costs)
                and math.isclose(risk_delta, expected_risk, abs_tol=1.0e-12)
            ),
            "cost_delta": cost_delta,
            "risk_delta": risk_delta,
            "attempt_consumed": base._step_count == before_step + 1,
            "observation_history_unchanged": before_history == _observation_history(after),
            "reward": reward,
            "terminated": terminated,
            "truncated": truncated,
        }
    finally:
        env.close()


def _probe_numeric_boundaries(
    protocol: dict[str, Any],
    case: dict[str, Any],
    operation: str,
) -> dict[str, Any]:
    fields = protocol["zero_effect_fields"].get(operation, [])
    if not fields:
        return {"probed_fields": [], "accepted_zero": [], "accepted_negative": []}
    env = gym.make(
        "ChemWorld",
        task_id=case["task_id"],
        seed=0,
        budget_override=100,
    )
    try:
        env.reset(seed=0)
        base: Any = env.unwrapped
        for setup_action in protocol["setup_fixtures"][case["setup"]]:
            _obs, _reward, _terminated, _truncated, info = env.step(deepcopy(setup_action))
            if info["transaction_status"] != "committed":
                raise AssertionError(f"numeric boundary setup failed: {info}")
        accepted_zero: list[dict[str, str]] = []
        accepted_negative: list[dict[str, str]] = []
        for field in fields:
            zero_action = deepcopy(case["action"])
            zero_action[field] = 0.0
            if base.operation_validator.validate(
                zero_action, base._state
            ).is_valid:
                accepted_zero.append({"operation": operation, "field": field})
            negative_action = deepcopy(case["action"])
            negative_action[field] = -1.0
            if base.operation_validator.validate(
                negative_action, base._state
            ).is_valid:
                accepted_negative.append({"operation": operation, "field": field})
        return {
            "probed_fields": fields,
            "accepted_zero": accepted_zero,
            "accepted_negative": accepted_negative,
        }
    finally:
        env.close()


def _probe_final_assay_boundary() -> dict[str, Any]:
    env = gym.make("ChemWorld", task_id="reaction-to-assay", seed=0, budget_override=100)
    try:
        env.reset(seed=0)
        base: Any = env.unwrapped
        for action in (
            {"operation": "add_solvent", "volume_L": 0.026, "solvent": 1},
            {"operation": "add_reagent", "amount_mol": 0.01},
            {"operation": "terminate"},
            {"operation": "measure", "instrument": "final_assay"},
        ):
            _obs, _reward, _terminated, _truncated, info = env.step(action)
            if info["transaction_status"] != "committed":
                raise AssertionError(f"final-assay setup failed: {info}")
        validation = base.operation_validator.validate(
            {"operation": "measure", "instrument": "final_assay"},
            base._state,
        )
        runtime_guard = not validation.is_valid and (
            "measure_final_not_repeated" in validation.invalid_reasons
        )
        step_guard = False
        try:
            env.step({"operation": "measure", "instrument": "final_assay"})
        except RuntimeError:
            step_guard = True
        return {
            "runtime_guard": runtime_guard,
            "episode_guard": step_guard,
            "repeated_final_assay_rejected": runtime_guard and step_guard,
        }
    finally:
        env.close()


def _probe_rolled_back_final_assay_boundary() -> dict[str, Any]:
    env = gym.make("ChemWorld", task_id="reaction-to-assay", seed=17, budget_override=100)
    try:
        env.reset(seed=17)
        base: Any = env.unwrapped
        for action in (
            {"operation": "add_solvent", "volume_L": 0.025, "solvent": 2},
            {"operation": "add_reagent", "amount_mol": 0.008},
            {"operation": "measure", "instrument": "hplc"},
            {"operation": "terminate"},
        ):
            _obs, _reward, _terminated, _truncated, setup_info = env.step(action)
            if setup_info["transaction_status"] != "committed":
                raise AssertionError(f"rollback-assay setup failed: {setup_info}")

        before_history = _observation_history(base._state)
        before_provider_execution = deepcopy(
            base.observation_kernel.last_provider_execution
        )
        transaction_manager = base.runtime.transaction_manager

        def reject_candidate(
            *,
            state: Any,
            operation_type: str,
            events: tuple[Any, ...],
            patches: tuple[Any, ...],
        ) -> Any:
            del patches
            return transaction_manager.rollback(
                state=state,
                operation_type=operation_type,
                rollback_reason="constitution_failed",
                failed_checks=("injected_measurement_failure",),
                events=events,
            )

        with patch.object(
            transaction_manager,
            "commit",
            side_effect=reject_candidate,
        ):
            _observation, reward, terminated, truncated, info = env.step(
                {"operation": "measure", "instrument": "final_assay"}
            )

        checks = {
            "transaction_rolled_back": info["transaction_status"] == "rolled_back"
            and info["rollback_reason"] == "constitution_failed",
            "no_fresh_observation": info["environment_reward"]["fresh_measurement"]
            is False,
            "no_reward": math.isclose(float(reward), 0.0, abs_tol=1.0e-15),
            "no_leaderboard_score": info["leaderboard_score"] is None,
            "no_measurement_consumption": math.isclose(
                float(info["measurement_cost"]), 0.0, abs_tol=1.0e-15
            )
            and math.isclose(float(info["sample_consumed"]), 0.0, abs_tol=1.0e-15),
            "episode_remains_open": not terminated
            and not truncated
            and info["experiment_ended"] is False,
            "observation_history_preserved": before_history
            == _observation_history(base._state),
            "provider_not_executed": before_provider_execution
            == base.observation_kernel.last_provider_execution,
            "rollback_reported_as_reward_source": info["reward_source"]
            == "constitution_rollback",
        }
        return {
            "checks": checks,
            "passed": all(checks.values()),
            "transaction_status": info["transaction_status"],
            "rollback_reason": info["rollback_reason"],
            "reward": float(reward),
            "measurement_cost": float(info["measurement_cost"]),
            "sample_consumed": float(info["sample_consumed"]),
        }
    finally:
        env.close()


def _probe_malformed_action_boundary() -> dict[str, Any]:
    cases: tuple[tuple[str, Any], ...] = (
        ("infinite_operation", {"operation": float("inf")}),
        ("empty_operation", {"operation": np.asarray([], dtype=float)}),
        ("fractional_operation", {"operation": 1.5}),
        (
            "infinite_material_choice",
            {"operation": "add_solvent", "volume_L": 0.02, "solvent": float("inf")},
        ),
        (
            "infinite_phase_choice",
            {"operation": "separate_phase", "target_phase": float("inf")},
        ),
        ("none_action", None),
        ("list_action", []),
        ("scalar_action", 7),
    )
    results: dict[str, dict[str, Any]] = {}
    for case_id, action in cases:
        env = gym.make(
            "ChemWorld",
            task_id="partition-discovery",
            seed=0,
            budget_override=100,
        )
        try:
            env.reset(seed=0)
            base: Any = env.unwrapped
            before = base._state
            before_snapshot = _failure_atomic_snapshot(before)
            before_history = _observation_history(before)
            before_step = base._step_count
            try:
                _observation, reward, terminated, truncated, info = env.step(action)
            except Exception as exc:  # pragma: no cover - reported as an audit defect
                results[case_id] = {
                    "passed": False,
                    "error_type": type(exc).__name__,
                    "error_message": str(exc),
                }
                continue
            after = base._state
            checks = {
                "validation_failed": info["transaction_status"] == "validation_failed"
                and info["rollback_reason"] == "validation_failed",
                "material_state_atomic": before_snapshot == _failure_atomic_snapshot(after),
                "observation_history_preserved": before_history == _observation_history(after),
                "attempt_consumed": base._step_count == before_step + 1,
                "penalty_recorded": after.ledger.cost > before.ledger.cost
                and after.ledger.risk > before.ledger.risk,
                "no_reward_or_termination": math.isclose(
                    float(reward), 0.0, abs_tol=1.0e-15
                )
                and not terminated
                and not truncated,
            }
            results[case_id] = {
                "passed": all(checks.values()),
                "checks": checks,
                "transaction_status": info["transaction_status"],
            }
        finally:
            env.close()
    return {
        "case_count": len(results),
        "passed": len(results) == len(cases)
        and all(result["passed"] for result in results.values()),
        "cases": results,
    }


def _probe_observation_integrity_boundary() -> dict[str, Any]:
    cases = (
        (
            "nonfinite_value",
            Observation(
                values={"score": float("inf")},
                units={"score": "dimensionless"},
                observed_mask={"score": True},
            ),
        ),
        (
            "private_payload",
            Observation(
                values={"score": 0.5},
                units={"score": "dimensionless"},
                observed_mask={"score": True},
                raw_signal={"species_amounts": {"A": 1.0}},
            ),
        ),
        (
            "nonfinite_uncertainty",
            Observation(
                values={"score": 0.5},
                units={"score": "dimensionless"},
                observed_mask={"score": True},
                uncertainty={"score_std": float("nan")},
            ),
        ),
    )
    results: dict[str, dict[str, Any]] = {}
    infinity_rejected_by_space = False
    for case_id, faulty_observation in cases:
        env = gym.make(
            "ChemWorld",
            task_id="reaction-to-assay",
            seed=0,
            budget_override=100,
        )
        try:
            env.reset(seed=0)
            base: Any = env.unwrapped
            before = base._state
            before_snapshot = _failure_atomic_snapshot(before)
            before_history = _observation_history(before)
            before_rng = deepcopy(base._rng.bit_generator.state)
            score_space = env.observation_space.spaces["score"]
            infinity_rejected_by_space = not score_space.contains(
                np.asarray([np.inf], dtype=np.float32)
            )

            def inject_fault(
                state: Any,
                action: Any,
                rng: np.random.Generator,
                faulty: Observation = faulty_observation,
            ) -> Observation:
                del state, action
                rng.normal()
                return faulty

            with patch.object(
                base.observation_kernel,
                "observe",
                side_effect=inject_fault,
            ):
                observation, reward, terminated, truncated, info = env.step(
                    {"operation": "add_solvent", "volume_L": 0.02, "solvent": 1}
                )
            after = base._state
            failed_checks = {
                str(check.get("name"))
                for check in info["constitution_checks"]
                if check.get("passed") is False
            }
            checks = {
                "validation_failed": info["transaction_status"] == "validation_failed"
                and info["preconditions"].get("observation_domain_valid") is False,
                "material_state_atomic": before_snapshot
                == _failure_atomic_snapshot(after),
                "observation_history_preserved": before_history
                == _observation_history(after),
                "observation_rng_preserved": before_rng
                == base._rng.bit_generator.state,
                "candidate_failure_reported": bool(failed_checks)
                and info["constraint_flags"]["constitution_failed"] is True,
                "faulty_payload_not_exposed": info["raw_signal"] == {}
                and env.observation_space.contains(observation),
                "penalty_recorded": after.ledger.cost > before.ledger.cost
                and after.ledger.risk > before.ledger.risk,
                "no_reward_or_termination": math.isclose(
                    float(reward), 0.0, abs_tol=1.0e-15
                )
                and not terminated
                and not truncated,
            }
            results[case_id] = {
                "passed": all(checks.values()),
                "checks": checks,
                "failed_constitution_checks": sorted(failed_checks),
                "transaction_status": info["transaction_status"],
            }
        finally:
            env.close()
    return {
        "case_count": len(results),
        "infinity_rejected_by_observation_space": infinity_rejected_by_space,
        "passed": infinity_rejected_by_space
        and len(results) == len(cases)
        and all(result["passed"] for result in results.values()),
        "cases": results,
    }


def _probe_post_terminal_barrier(protocol: dict[str, Any]) -> dict[str, Any]:
    case = protocol["operations"]["terminate"]
    env = gym.make("ChemWorld", task_id=case["task_id"], seed=0, budget_override=100)
    try:
        env.reset(seed=0)
        base: Any = env.unwrapped
        for action in protocol["setup_fixtures"]["charged_basic"]:
            env.step(deepcopy(action))
        env.step(deepcopy(case["action"]))
        results: dict[str, bool] = {}
        for operation in OPERATION_TYPES:
            if operation in {"terminate", "measure"}:
                continue
            validation = base.operation_validator.operation_affordance(
                operation, base._state
            )
            results[operation] = (
                not validation.is_valid and "not_terminated" in validation.invalid_reasons
            )
        return {
            "operations": results,
            "all_process_operations_rejected": all(results.values()),
            "measurement_remains_available_for_terminal_assay": (
                "measure"
                in base.operation_validator.valid_operations(base._state)
            ),
        }
    finally:
        env.close()


def _effect_flags(
    before: dict[str, Any],
    after: dict[str, Any],
    info: dict[str, Any],
) -> dict[str, bool]:
    before_ledger = before["ledger"]
    after_ledger = after["ledger"]
    return {
        "material": before["species_amounts"] != after["species_amounts"],
        "volume": not math.isclose(before["volume_L"], after["volume_L"], abs_tol=1e-15),
        "time": not math.isclose(before_ledger["time_s"], after_ledger["time_s"], abs_tol=1e-12),
        "temperature": not math.isclose(
            before["temperature_K"], after["temperature_K"], abs_tol=1e-12
        ),
        "phase": before["phases"] != after["phases"],
        "configuration": before["equipment"] != after["equipment"],
        "termination": not before["terminated"] and after["terminated"],
        "measurement": bool(info.get("measurement_cost", 0.0))
        or bool(info.get("sample_consumed", 0.0)),
        "cost": not math.isclose(before_ledger["cost"], after_ledger["cost"], abs_tol=1e-12),
        "sample": not math.isclose(
            before_ledger["sample_consumed_L"],
            after_ledger["sample_consumed_L"],
            abs_tol=1e-15,
        ),
        "quenched": not before["quenched"] and after["quenched"],
    }


def _failure_atomic_snapshot(state: Any) -> dict[str, Any]:
    payload = state.to_dict(include_hidden=True)
    payload["ledger"] = {
        key: value for key, value in payload["ledger"].items() if key not in {"cost", "risk"}
    }
    if payload["process"] is not None:
        payload["process"] = {
            key: value for key, value in payload["process"].items() if key not in {"cost", "risk"}
        }
    return payload


def _observation_history(state: Any) -> dict[str, Any]:
    if state.process is None:
        return {"last_observation": {}, "last_observed_mask": {}}
    return {
        "last_observation": state.process.last_observation,
        "last_observed_mask": state.process.last_observed_mask,
    }


def _changed_roots(before: dict[str, Any], after: dict[str, Any]) -> list[str]:
    return sorted(key for key in before.keys() | after.keys() if before.get(key) != after.get(key))


def _observation_hash(observation: dict[str, np.ndarray]) -> str:
    payload = {
        key: [None if not np.isfinite(float(value)) else float(value) for value in array]
        for key, array in sorted(observation.items())
    }
    return _json_hash(payload)


def _json_hash(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def _report_hash(report: dict[str, Any]) -> str:
    payload = dict(report)
    payload["report_hash"] = None
    return _json_hash(payload)


def _git_state(repository_root: Path) -> tuple[str, bool]:
    snapshot_commit = os.environ.get("CHEMWORLD_EVIDENCE_SOURCE_COMMIT")
    snapshot_dirty = os.environ.get("CHEMWORLD_EVIDENCE_SOURCE_TREE_DIRTY")
    if snapshot_commit and snapshot_dirty in {"true", "false"}:
        return snapshot_commit, snapshot_dirty == "true"
    commit = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repository_root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    dirty = bool(
        subprocess.run(
            ["git", "status", "--porcelain", "--untracked-files=no"],
            cwd=repository_root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    )
    return commit, dirty


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    protocol = load_protocol(args.protocol)
    report = build_report(protocol)
    errors = validate_report(report, protocol)
    if args.check:
        print(json.dumps({"errors": errors, "report": report}, indent=2, sort_keys=True))
        return 1 if errors else 0
    write_report(report, args.output)
    print(
        json.dumps(
            {
                "output": str(args.output),
                "status": report["status"],
                "operation_count": report["operation_count"],
                "defect_count": len(report["defect_inventory"]),
                "errors": errors,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
