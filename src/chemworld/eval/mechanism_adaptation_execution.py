"""Executable orchestration for the v0.2 mechanism-adaptation benchmark.

The module has two deliberately separate jobs:

* produce Gate A from environment observations without making provider calls; and
* expand and execute the frozen paired campaign matrix with durable per-row artifacts.

Gate A uses only numeric values available in the public observation/reward stream.  It
does not train or update an evaluated Agent, and it does not expose hidden candidate
IDs to an Agent.  The Gaussian oracle is an evaluator-side diagnostic used to decide
whether the environment contains enough information at the frozen budget.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from collections.abc import Callable, Mapping, Sequence
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Any, cast

import numpy as np

from chemworld.agents.mechanism_adaptation_live_llm import (
    CandidateLabelMode,
    MechanismAdaptationLiveLLMAgent,
    MechanismCandidateSpec,
)
from chemworld.agents.task_recipes import (
    task_recipe_dimension,
    task_recipe_event_count,
    task_recipe_from_unit_vector,
)
from chemworld.envs.chemworld_env import ChemWorldEnv
from chemworld.eval.flagship_diagnostics import (
    ContinuingPublicViewAgent,
    FeedbackCondition,
    run_two_phase_campaign,
)
from chemworld.eval.mechanism_adaptation import (
    GaussianMechanismOracle,
    build_paired_campaign_matrix,
    identifiability_certificate,
    validate_mechanism_adaptation_protocol,
)
from chemworld.eval.mechanism_design_audit import audit_mechanism_design
from chemworld.eval.provenance import (
    canonical_json_sha256 as canonical_sha256,
)
from chemworld.eval.provenance import (
    file_sha256,
    repository_tree_sha256,
)
from chemworld.physchem.mechanism_library import configuration_root
from chemworld.providers.deepseek import DeepSeekClient
from chemworld.tasks import get_task
from chemworld.world.operations import operation_contracts

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROTOCOL_PATH = configuration_root() / "benchmark/mechanism_adaptation_v0.2.1.json"
DEFAULT_GATE_A_PLAN_PATH = (
    configuration_root() / "benchmark/mechanism_adaptation_gate_a_v0.2.4.json"
)
DEFAULT_LLM_METHODS_PATH = configuration_root() / "methods/llm_v0.4/llm_methods.json"
EXECUTION_SCHEMA_VERSION = "chemworld-mechanism-adaptation-execution-0.2"
GATE_A_REPORT_VERSION = "chemworld-mechanism-adaptation-gate-a-report-0.2.4"
ONLINE_POLICY_CERTIFICATE_VERSION = (
    "chemworld-mechanism-adaptation-online-policy-certificate-0.1"
)

_CRITICAL_INSTRUMENTS = {
    "reaction-to-crystallization": "hplc",
    "electrochemical-conversion": "uvvis",
}


def load_json_object(path: str | Path) -> dict[str, Any]:
    """Load a JSON object and reject ambiguous non-object roots."""

    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected a JSON object: {path}")
    return payload


def gate_a_execution_contract_binding(
    protocol: Mapping[str, Any],
    plan: Mapping[str, Any],
) -> dict[str, Any]:
    """Bind a Gate A result to all runtime semantics that determine its evidence."""

    config_paths = {
        "backend_contract": configuration_root() / "foundation/backend_v0.5.json",
        "evaluation_contract": configuration_root() / "benchmark/evaluation_vnext.json",
        "public_boundary_contract": (
            configuration_root() / "foundation/public_boundary_security_vnext.json"
        ),
    }
    binding: dict[str, Any] = {
        "schema_version": "chemworld-gate-a-execution-binding-0.1",
        "runtime_source_tree_sha256": repository_tree_sha256(
            PACKAGE_ROOT,
            relative_roots=(".",),
        ),
        "task_contract_hashes": {
            str(task_id): get_task(str(task_id)).contract_hash
            for task_id in protocol["design"]["tasks"]
        },
        "operation_contract_sha256": canonical_sha256(
            {
                key: value.to_dict()
                for key, value in sorted(operation_contracts().items())
            }
        ),
        "bound_config_sha256": {
            key: file_sha256(path) for key, path in sorted(config_paths.items())
        },
        "protocol_sha256": canonical_sha256(protocol),
        "gate_a_plan_sha256": canonical_sha256(plan),
    }
    binding["binding_sha256"] = canonical_sha256(binding)
    return binding


def gate_a_certificate_decision(
    protocol: Mapping[str, Any],
    plan: Mapping[str, Any],
    *,
    controlled_gate_pass: bool,
    online_policy_certificate: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Compose Gate A from two independently bound required certificates.

    The controlled matched oracle establishes that the public experiment contract
    contains diagnostic information.  It is not a substitute for demonstrating that
    an online policy can select and use diagnostic experiments under the same budget.
    Missing, stale, or malformed online-policy evidence therefore fails closed.
    """

    requirement = plan.get("online_policy_feasible_certificate")
    if not isinstance(requirement, Mapping) or requirement.get(
        "required_before_formal_mechanism_claim"
    ) is not True:
        raise ValueError("Gate A plan must require an online-policy-feasible certificate")

    expected_protocol_sha = canonical_sha256(protocol)
    expected_plan_sha = canonical_sha256(plan)
    primary_budget = int(plan["held_out_certificate"]["primary_gate_budget"])
    if online_policy_certificate is None:
        online_summary = {
            "schema_version": ONLINE_POLICY_CERTIFICATE_VERSION,
            "status": "pending_execution",
            "gate_pass": False,
            "required": True,
            "certificate_present": False,
            "primary_gate_budget": primary_budget,
        }
    else:
        certificate = dict(online_policy_certificate)
        errors: list[str] = []
        expected_values = {
            "schema_version": ONLINE_POLICY_CERTIFICATE_VERSION,
            "certificate_scope": "online_policy_feasible_diagnosis",
            "protocol_sha256": expected_protocol_sha,
            "gate_a_plan_sha256": expected_plan_sha,
            "primary_gate_budget": primary_budget,
            "hidden_change_time": True,
            "uses_actual_available_pre_change_history": True,
            "uses_actual_action_measurement_and_budget_contract": True,
        }
        for field, expected in expected_values.items():
            if certificate.get(field) != expected:
                errors.append(f"{field} must equal {expected!r}")
        gate_pass = certificate.get("gate_pass")
        if not isinstance(gate_pass, bool):
            errors.append("gate_pass must be boolean")
        expected_status = "passed" if gate_pass is True else "failed"
        if certificate.get("status") != expected_status:
            errors.append(f"status must equal {expected_status!r}")
        if errors:
            raise ValueError("invalid online-policy-feasible certificate: " + "; ".join(errors))
        online_summary = {
            **certificate,
            "required": True,
            "certificate_present": True,
            "certificate_sha256": canonical_sha256(certificate),
        }

    online_gate_pass = online_summary["gate_pass"] is True
    combined_pass = bool(controlled_gate_pass and online_gate_pass)
    if combined_pass:
        status = "gate_a_passed"
    elif not controlled_gate_pass:
        status = "gate_a_failed_controlled_matched_certificate"
    elif online_summary["certificate_present"] is not True:
        status = "gate_a_blocked_online_policy_certificate_pending"
    else:
        status = "gate_a_failed_online_policy_certificate"
    return {
        "schema_version": "chemworld-mechanism-adaptation-gate-a-decision-0.1",
        "status": status,
        "required_certificates": [
            "controlled_matched_identifiability",
            "online_policy_feasible_diagnosis",
        ],
        "controlled_matched_gate_pass": bool(controlled_gate_pass),
        "online_policy_feasible_gate_pass": online_gate_pass,
        "online_policy_feasible_certificate": online_summary,
        "gate_a_pass": combined_pass,
    }


def build_action_library(
    task_id: str,
    *,
    action_count: int,
    seed: int,
) -> dict[str, np.ndarray]:
    """Return a deterministic bounded set of public complete-recipe designs."""

    if action_count < 3:
        raise ValueError("Gate A requires at least three public actions per task")
    task_info = get_task(task_id).to_dict()
    dimension = task_recipe_dimension(task_info)
    anchors = [
        np.full(dimension, 0.15, dtype=float),
        np.full(dimension, 0.50, dtype=float),
        np.full(dimension, 0.85, dtype=float),
    ]
    task_seed = _stable_seed(seed, task_id)
    rng = np.random.default_rng(task_seed)
    vectors = anchors + [rng.random(dimension) for _ in range(action_count - len(anchors))]
    return {
        f"design-{index:02d}": np.asarray(vector, dtype=float)
        for index, vector in enumerate(vectors)
    }


def encode_public_experiment_trace(
    trace: Sequence[tuple[Mapping[str, Any], float]],
) -> list[float]:
    """Encode only agent-visible numeric observation/reward packets.

    Each scalar contributes a finite-value mask and a value.  This keeps the feature
    dimension fixed when an instrument does not release a metric and avoids using a
    sentinel that could be confused with a physical value.
    """

    features: list[float] = []
    for observation, reward in trace:
        for key in sorted(observation):
            raw = np.asarray(observation[key], dtype=float).reshape(-1)
            finite = np.isfinite(raw)
            features.extend(finite.astype(float).tolist())
            features.extend(np.where(finite, raw, 0.0).astype(float).tolist())
        reward_value = float(reward)
        features.extend(
            [
                float(np.isfinite(reward_value)),
                reward_value if np.isfinite(reward_value) else 0.0,
            ]
        )
    if not features:
        raise ValueError("a public experiment trace cannot be empty")
    return features


class PublicCampaignObservationSession:
    """Execute complete public recipes in one nuisance-consistent campaign world."""

    def __init__(
        self,
        *,
        task_id: str,
        seed: int,
        interventions: Sequence[Mapping[str, Any]],
        action_library: Mapping[str, np.ndarray],
        experiment_horizon: int,
        observation_seed: int | None = None,
    ) -> None:
        if experiment_horizon <= 0:
            raise ValueError("experiment_horizon must be positive")
        self.task_id = task_id
        self.task_info = get_task(task_id).to_dict()
        self.action_library = action_library
        per_experiment = task_recipe_event_count(self.task_info)
        self.environment = ChemWorldEnv(
            task_id=task_id,
            seed=int(seed),
            episode_mode_override="campaign",
            budget_override=(per_experiment + 1) * int(experiment_horizon),
            observation_seed_override=observation_seed,
            world_interventions=tuple(dict(item) for item in interventions),
        )
        self.environment.reset(seed=int(seed))

    def observe(self, action_id: str) -> list[float]:
        try:
            vector = self.action_library[action_id]
        except KeyError as error:
            raise ValueError(f"unknown public action ID: {action_id}") from error
        recipe = task_recipe_from_unit_vector(self.task_info, vector)
        trace: list[tuple[Mapping[str, Any], float]] = []
        experiment_ended = False
        for action in recipe["steps"]:
            observation, reward, _terminated, _truncated, info = self.environment.step(action)
            trace.append((observation, float(reward)))
            experiment_ended = bool(info.get("experiment_ended"))
        if not experiment_ended or info.get("transaction_status") != "committed":
            raise RuntimeError("compiled Gate A recipe did not produce a committed experiment")
        return encode_public_experiment_trace(trace)

    def close(self) -> None:
        self.environment.close()

    def __enter__(self) -> PublicCampaignObservationSession:
        return self

    def __exit__(self, *_args: Any) -> None:
        self.close()


def _sample_experiment_job(job: Mapping[str, Any]) -> list[float]:
    action_id = str(job["action_id"])
    action_library = {action_id: np.asarray(job["action_vector"], dtype=float)}
    with PublicCampaignObservationSession(
        task_id=str(job["task_id"]),
        seed=int(job["seed"]),
        interventions=job["interventions"],
        action_library=action_library,
        experiment_horizon=1,
        observation_seed=(
            None if job.get("observation_seed") is None else int(job["observation_seed"])
        ),
    ) as session:
        return session.observe(action_id)


def _sample_paired_contrast_job(job: Mapping[str, Any]) -> list[float]:
    """Return post-minus-pre public traces for one matched recipe batch."""

    action_ids = [str(item) for item in job["action_ids"]]
    action_library = {
        str(key): np.asarray(value, dtype=float) for key, value in job["action_library"].items()
    }
    with PublicCampaignObservationSession(
        task_id=str(job["task_id"]),
        seed=int(job["world_seed"]),
        interventions=(),
        action_library=action_library,
        experiment_horizon=len(action_ids),
        observation_seed=int(job["pre_observation_seed"]),
    ) as pre_session:
        pre = [np.asarray(pre_session.observe(action_id), dtype=float) for action_id in action_ids]
    with PublicCampaignObservationSession(
        task_id=str(job["task_id"]),
        seed=int(job["world_seed"]),
        interventions=job["interventions"],
        action_library=action_library,
        experiment_horizon=len(action_ids),
        observation_seed=int(job["post_observation_seed"]),
    ) as post_session:
        post = [
            np.asarray(post_session.observe(action_id), dtype=float) for action_id in action_ids
        ]
    return np.concatenate(
        [post_values - pre_values for pre_values, post_values in zip(pre, post, strict=True)]
    ).tolist()


def _unreachable_sample(_candidate_id: str, _action_id: str, _seed: int) -> list[float]:
    raise RuntimeError("loaded Gate A predictives do not sample during evaluation")


def _execute_gate_a_trial_job(job: Mapping[str, Any]) -> dict[str, Any]:
    task_id = str(job["task_id"])
    truth_id = str(job["truth_id"])
    trial_seed = int(job["trial_seed"])
    budgets = [int(item) for item in job["budgets"]]
    maximum_budget = max(budgets)
    action_ids = [str(item) for item in job["action_ids"]]
    action_library = {
        str(key): np.asarray(value, dtype=float) for key, value in job["action_library"].items()
    }

    def loaded_oracle() -> GaussianMechanismOracle:
        oracle = GaussianMechanismOracle(
            candidate_ids=[str(item) for item in job["candidate_ids"]],
            action_ids=action_ids,
            sample_public_observation=_unreachable_sample,
            samples_per_candidate=4,
            variance_floor=float(job["variance_floor"]),
            seed=int(job["oracle_seed"]),
        )
        oracle.load_predictives(job["predictives"])
        return oracle

    active_oracle = loaded_oracle()
    active_rows: dict[int, dict[str, Any]] = {}
    selected_actions: list[str] = []
    with PublicCampaignObservationSession(
        task_id=task_id,
        seed=trial_seed,
        interventions=job["interventions"],
        action_library=action_library,
        experiment_horizon=maximum_budget,
    ) as active_session:
        for experiment_index in range(1, maximum_budget + 1):
            information = active_oracle.expected_information_by_action(
                draws=int(job["information_draws"])
            )
            eligible = list(action_ids)
            if job.get("repeat_policy") == "without_replacement_within_budget":
                unused = [item for item in action_ids if item not in selected_actions]
                if unused:
                    eligible = unused
            action_id = max(eligible, key=information.__getitem__)
            selected_actions.append(action_id)
            active_oracle.update(
                action_id=action_id,
                observation=active_session.observe(action_id),
            )
            if experiment_index in budgets:
                active_rows[experiment_index] = {
                    "truth_id": truth_id,
                    "world_seed": trial_seed,
                    "prediction": max(
                        active_oracle.posterior,
                        key=active_oracle.posterior.__getitem__,
                    ),
                    "actions": list(selected_actions),
                    "posterior": dict(active_oracle.posterior),
                }

    decoder_oracle = loaded_oracle()
    decoder_rows: dict[int, dict[str, Any]] = {}
    fixed_actions = action_ids[:maximum_budget]
    with PublicCampaignObservationSession(
        task_id=task_id,
        seed=trial_seed,
        interventions=job["interventions"],
        action_library=action_library,
        experiment_horizon=maximum_budget,
    ) as decoder_session:
        for experiment_index, action_id in enumerate(fixed_actions, start=1):
            decoder_oracle.update(
                action_id=action_id,
                observation=decoder_session.observe(action_id),
            )
            if experiment_index in budgets:
                decoder_rows[experiment_index] = {
                    "truth_id": truth_id,
                    "world_seed": trial_seed,
                    "prediction": max(
                        decoder_oracle.posterior,
                        key=decoder_oracle.posterior.__getitem__,
                    ),
                    "actions": fixed_actions[:experiment_index],
                    "posterior": dict(decoder_oracle.posterior),
                }
    return {"active": active_rows, "decoder": decoder_rows}


def _execute_jobs(
    function: Any,
    jobs: Sequence[Mapping[str, Any]],
    *,
    workers: int,
) -> list[Any]:
    if workers <= 0:
        raise ValueError("Gate A execution workers must be positive")
    if workers == 1:
        return [function(job) for job in jobs]
    with ProcessPoolExecutor(max_workers=workers) as executor:
        return list(executor.map(function, jobs))


def _paired_action_id(action_ids: Sequence[str]) -> str:
    return "+".join(str(item) for item in action_ids)


def _fit_paired_batch_oracle(
    *,
    candidate_ids: Sequence[str],
    action_ids: Sequence[str],
    per_action_samples: Mapping[tuple[str, str], Sequence[Sequence[float]]],
    batch_size: int,
    variance_floor: float,
    seed: int,
) -> tuple[GaussianMechanismOracle, dict[str, tuple[str, ...]]]:
    """Fit batch predictives from nuisance-aligned per-action contrast samples."""

    batches = {
        _paired_action_id(batch): tuple(batch)
        for batch in itertools.combinations(action_ids, batch_size)
    }
    if not batches:
        raise ValueError("paired Gate A batch size exceeds the public action library")
    batch_samples: dict[tuple[str, str], list[list[float]]] = {}
    for candidate_id in candidate_ids:
        counts = {
            len(per_action_samples[(str(candidate_id), action_id)]) for action_id in action_ids
        }
        if len(counts) != 1:
            raise ValueError("paired Gate A samples must align by nuisance seed")
        sample_count = counts.pop()
        for batch_id, batch in batches.items():
            batch_samples[(str(candidate_id), batch_id)] = [
                np.concatenate(
                    [
                        np.asarray(per_action_samples[(str(candidate_id), action_id)][index])
                        for action_id in batch
                    ]
                ).tolist()
                for index in range(sample_count)
            ]
    oracle = GaussianMechanismOracle(
        candidate_ids=candidate_ids,
        action_ids=list(batches),
        sample_public_observation=_unreachable_sample,
        samples_per_candidate=4,
        variance_floor=variance_floor,
        seed=seed,
    )
    oracle.fit_predictives_from_samples(batch_samples)
    return oracle, batches


def _execute_paired_gate_a_trial_job(job: Mapping[str, Any]) -> dict[str, Any]:
    candidate_ids = [str(item) for item in job["candidate_ids"]]
    batch_ids = [str(item) for item in job["batch_ids"]]
    oracle = GaussianMechanismOracle(
        candidate_ids=candidate_ids,
        action_ids=batch_ids,
        sample_public_observation=_unreachable_sample,
        samples_per_candidate=4,
        variance_floor=float(job["variance_floor"]),
        seed=int(job["oracle_seed"]),
    )
    oracle.load_predictives(job["predictives"])
    rows: dict[str, dict[str, Any]] = {}
    contrasts: dict[str, list[float]] = {}
    for role in ("active", "decoder"):
        batch_id = str(job[f"{role}_batch_id"])
        if batch_id not in contrasts:
            action_ids = [str(item) for item in job["batches"][batch_id]]
            contrasts[batch_id] = _sample_paired_contrast_job(
                {
                    "task_id": job["task_id"],
                    "world_seed": job["world_seed"],
                    "interventions": job["interventions"],
                    "action_ids": action_ids,
                    "action_library": {
                        action_id: job["action_library"][action_id] for action_id in action_ids
                    },
                    "pre_observation_seed": _stable_seed(
                        int(job["world_seed"]), f"gate-a-v0.2.2:{batch_id}:pre"
                    ),
                    "post_observation_seed": _stable_seed(
                        int(job["world_seed"]), f"gate-a-v0.2.2:{batch_id}:post"
                    ),
                }
            )
        oracle.reset_posterior()
        oracle.update(action_id=batch_id, observation=contrasts[batch_id])
        rows[role] = {
            "truth_id": str(job["truth_id"]),
            "world_seed": int(job["world_seed"]),
            "pre_observation_seed": _stable_seed(
                int(job["world_seed"]), f"gate-a-v0.2.2:{batch_id}:pre"
            ),
            "post_observation_seed": _stable_seed(
                int(job["world_seed"]), f"gate-a-v0.2.2:{batch_id}:post"
            ),
            "prediction": max(oracle.posterior, key=oracle.posterior.__getitem__),
            "actions": list(job["batches"][batch_id]),
            "batch_id": batch_id,
            "posterior": dict(oracle.posterior),
        }
    return rows


def validate_precomputed_design_audit(
    protocol: Mapping[str, Any],
    plan: Mapping[str, Any],
    report: Mapping[str, Any],
) -> dict[str, Any]:
    """Validate a frozen design audit before reusing it in an expensive Gate run."""

    expected = {
        "pass": True,
        "protocol_id": protocol.get("protocol_id"),
        "gate_a_plan_id": plan.get("plan_id"),
        "protocol_sha256": canonical_sha256(protocol),
        "gate_a_plan_sha256": canonical_sha256(plan),
    }
    mismatches = [
        key for key, value in expected.items() if report.get(key) != value
    ]
    if mismatches:
        raise ValueError(
            "precomputed mechanism design audit is stale or failed: "
            + ", ".join(mismatches)
        )
    return dict(report)


def _emit_gate_a_progress(
    callback: Callable[[Mapping[str, Any]], None] | None,
    *,
    event: str,
    **details: Any,
) -> None:
    if callback is not None:
        callback({"stage": "gate-a", "event": event, **details})


def _run_paired_gate_a(
    protocol: Mapping[str, Any],
    plan: Mapping[str, Any],
    *,
    online_policy_certificate: Mapping[str, Any] | None = None,
    design_validity_audit: Mapping[str, Any] | None = None,
    progress_callback: Callable[[Mapping[str, Any]], None] | None = None,
) -> dict[str, Any]:
    """Run the pre/post paired controlled certificate and compose full Gate A."""

    errors = validate_mechanism_adaptation_protocol(protocol)
    if errors:
        raise ValueError("invalid mechanism-adaptation protocol: " + "; ".join(errors))
    action_plan = plan["action_library"]
    fit_plan = plan["candidate_predictive_fit"]
    certificate_plan = plan["held_out_certificate"]
    phase_plan = plan["paired_phase_design"]
    gate = protocol["gates"]["gate_a"]
    matched_primary_budget = int(phase_plan["pre_change_reference_experiments"])
    protocol_pre_change = int(protocol["design"]["pre_change_experiments"])
    if matched_primary_budget != protocol_pre_change:
        raise ValueError("paired Gate A must use the protocol pre-change experiment budget")
    budgets = [int(item) for item in certificate_plan["budgets"]]
    if budgets != [int(item) for item in gate["budget_checkpoints"]]:
        raise ValueError("paired Gate A budgets must match the frozen protocol checkpoints")
    primary_budget = int(certificate_plan["primary_gate_budget"])
    if primary_budget != matched_primary_budget:
        raise ValueError("paired Gate A primary budget must equal the matched batch size")
    if int(action_plan["action_count_per_task"]) < max(budgets):
        raise ValueError(
            "paired Gate A action library cannot underfill its largest decoder budget"
        )
    if (
        len(budgets) > 1
        and phase_plan.get("diagnostic_curve_matches_reference_count_to_budget") is not True
    ):
        raise ValueError(
            "multi-budget paired Gate A must declare matched reference counts for its curve"
        )
    if phase_plan.get("same_hidden_world_seed_across_phases") is not True:
        raise ValueError("paired Gate A requires the same hidden-world seed across phases")
    if phase_plan.get("independent_observation_seed_across_phases") is not True:
        raise ValueError("paired Gate A requires independent phase observation seeds")
    if phase_plan.get("public_contrast_encoding") != "post_minus_pre_same_recipe":
        raise ValueError("unsupported paired Gate A public contrast encoding")

    action_libraries = {
        str(task_id): build_action_library(
            str(task_id),
            action_count=int(action_plan["action_count_per_task"]),
            seed=int(action_plan["design_seed"]),
        )
        for task_id in protocol["design"]["tasks"]
    }
    if design_validity_audit is None:
        _emit_gate_a_progress(progress_callback, event="design_audit_started")
        design_audit = audit_mechanism_design(
            protocol,
            plan,
            action_libraries=action_libraries,
        )
        _emit_gate_a_progress(progress_callback, event="design_audit_completed")
    else:
        design_audit = validate_precomputed_design_audit(
            protocol,
            plan,
            design_validity_audit,
        )
        _emit_gate_a_progress(progress_callback, event="design_audit_reused")
    if not design_audit["pass"]:
        failed = "; ".join(
            f"{item.get('task_id')}:{item['check']}" for item in design_audit["failures"]
        )
        raise ValueError(f"mechanism design audit failed: {failed}")

    task_reports: dict[str, Any] = {}
    active_truths: dict[int, list[str]] = {budget: [] for budget in budgets}
    active_predictions: dict[int, list[str]] = {budget: [] for budget in budgets}
    decoder_truths: dict[int, list[str]] = {budget: [] for budget in budgets}
    decoder_predictions: dict[int, list[str]] = {budget: [] for budget in budgets}
    candidate_union: list[str] = []
    sample_count = int(fit_plan["samples_per_candidate_action"])

    for task_index, task_id in enumerate(protocol["design"]["tasks"]):
        task_id = str(task_id)
        contract = protocol["task_mechanism_contracts"][task_id]
        candidate_ids = [str(item) for item in contract["candidate_ids"]]
        for candidate_id in candidate_ids:
            if candidate_id not in candidate_union:
                candidate_union.append(candidate_id)
        action_library = action_libraries[task_id]
        action_ids = list(action_library)
        fit_world_seeds = [
            int(fit_plan["nuisance_seed_namespace_start"]) + task_index * 1_000_000 + index
            for index in range(sample_count)
        ]
        fit_keys: list[tuple[str, str]] = []
        fit_jobs: list[dict[str, Any]] = []
        for candidate_id in candidate_ids:
            for action_id in action_ids:
                for world_seed in fit_world_seeds:
                    fit_keys.append((candidate_id, action_id))
                    fit_jobs.append(
                        {
                            "task_id": task_id,
                            "world_seed": world_seed,
                            "interventions": contract["interventions"][candidate_id],
                            "action_ids": [action_id],
                            "action_library": {action_id: action_library[action_id].tolist()},
                            "pre_observation_seed": _stable_seed(
                                world_seed, f"gate-a-v0.2.2:{action_id}:fit-pre"
                            ),
                            "post_observation_seed": _stable_seed(
                                world_seed, f"gate-a-v0.2.2:{action_id}:fit-post"
                            ),
                        }
                    )
        _emit_gate_a_progress(
            progress_callback,
            event="predictive_fit_started",
            task_id=task_id,
            job_count=len(fit_jobs),
        )
        fit_results = _execute_jobs(
            _sample_paired_contrast_job,
            fit_jobs,
            workers=int(fit_plan.get("execution_workers", 1)),
        )
        _emit_gate_a_progress(
            progress_callback,
            event="predictive_fit_completed",
            task_id=task_id,
            job_count=len(fit_jobs),
        )
        per_action_samples: dict[tuple[str, str], list[Sequence[float]]] = {
            (candidate_id, action_id): []
            for candidate_id in candidate_ids
            for action_id in action_ids
        }
        for key, values in zip(fit_keys, fit_results, strict=True):
            per_action_samples[key].append(values)

        serialized_actions = {key: vector.tolist() for key, vector in action_library.items()}
        task_trials: dict[str, list[dict[str, Any]]] = {
            f"{role}_budget_{budget}": []
            for budget in budgets
            for role in ("active", "decoder")
        }
        budget_designs: dict[str, Any] = {}
        for budget in budgets:
            oracle_seed = _stable_seed(
                int(fit_plan["oracle_seed"]), f"{task_id}:budget-{budget}"
            )
            oracle, batches = _fit_paired_batch_oracle(
                candidate_ids=candidate_ids,
                action_ids=action_ids,
                per_action_samples=per_action_samples,
                batch_size=budget,
                variance_floor=float(fit_plan["variance_floor"]),
                seed=oracle_seed,
            )
            information = oracle.expected_information_by_action(
                draws=int(certificate_plan["information_draws_per_batch"])
            )
            active_batch_id = max(information, key=information.__getitem__)
            decoder_batch_id = _paired_action_id(action_ids[:budget])
            trial_jobs = []
            trial_keys: list[tuple[str, int]] = []
            for candidate_id in candidate_ids:
                for repeat_index in range(
                    int(certificate_plan["world_seeds_per_family"])
                ):
                    world_seed = (
                        int(certificate_plan["seed_namespace_start"])
                        + task_index * 1_000_000
                        + repeat_index
                    )
                    trial_keys.append((candidate_id, repeat_index))
                    trial_jobs.append(
                        {
                            "task_id": task_id,
                            "truth_id": candidate_id,
                            "world_seed": world_seed,
                            "interventions": contract["interventions"][candidate_id],
                            "candidate_ids": candidate_ids,
                            "batch_ids": list(batches),
                            "batches": {
                                key: list(value) for key, value in batches.items()
                            },
                            "active_batch_id": active_batch_id,
                            "decoder_batch_id": decoder_batch_id,
                            "action_library": serialized_actions,
                            "predictives": oracle.export_predictives(),
                            "variance_floor": float(fit_plan["variance_floor"]),
                            "oracle_seed": oracle_seed,
                        }
                    )
            _emit_gate_a_progress(
                progress_callback,
                event="certificate_trials_started",
                task_id=task_id,
                budget=budget,
                job_count=len(trial_jobs),
            )
            completed_trials = _execute_jobs(
                _execute_paired_gate_a_trial_job,
                trial_jobs,
                workers=int(certificate_plan.get("execution_workers", 1)),
            )
            _emit_gate_a_progress(
                progress_callback,
                event="certificate_trials_completed",
                task_id=task_id,
                budget=budget,
                job_count=len(trial_jobs),
            )
            for (truth_id, _repeat_index), completed in zip(
                trial_keys, completed_trials, strict=True
            ):
                qualified_truth = _qualified_candidate(task_id, truth_id)
                active = completed["active"]
                decoder = completed["decoder"]
                active_truths[budget].append(qualified_truth)
                active_predictions[budget].append(
                    _qualified_candidate(task_id, str(active["prediction"]))
                )
                decoder_truths[budget].append(qualified_truth)
                decoder_predictions[budget].append(
                    _qualified_candidate(task_id, str(decoder["prediction"]))
                )
                task_trials[f"active_budget_{budget}"].append(active)
                task_trials[f"decoder_budget_{budget}"].append(decoder)
            budget_designs[str(budget)] = {
                "matched_pre_change_reference_experiments": budget,
                "post_change_diagnostic_experiments": budget,
                "online_history_aligned": budget == primary_budget,
                "active_batch_id": active_batch_id,
                "active_batch_information_nats": float(information[active_batch_id]),
                "decoder_batch_id": decoder_batch_id,
                "batch_information_nats": {
                    key: float(value) for key, value in information.items()
                },
            }
        task_reports[task_id] = {
            "candidate_ids": candidate_ids,
            "action_library": serialized_actions,
            "budget_designs": budget_designs,
            "trials": task_trials,
        }

    qualified_candidates = [
        _qualified_candidate(str(task_id), str(candidate_id))
        for task_id in protocol["design"]["tasks"]
        for candidate_id in protocol["task_mechanism_contracts"][task_id]["candidate_ids"]
    ]
    active_certificates = {
        budget: identifiability_certificate(
            truths=active_truths[budget],
            predictions=active_predictions[budget],
            candidate_ids=qualified_candidates,
            overall_lower_bound_threshold=float(gate["overall_top1_wilson_lower_bound"]),
            family_recall_lower_bound_threshold=float(
                gate["per_family_recall_wilson_lower_bound"]
            ),
        )
        for budget in budgets
    }
    decoder_certificates = {
        budget: identifiability_certificate(
            truths=decoder_truths[budget],
            predictions=decoder_predictions[budget],
            candidate_ids=qualified_candidates,
            overall_lower_bound_threshold=float(gate["overall_top1_wilson_lower_bound"]),
            family_recall_lower_bound_threshold=float(
                gate["per_family_recall_wilson_lower_bound"]
            ),
        )
        for budget in budgets
    }
    controlled_gate_pass = bool(active_certificates[primary_budget]["gate_pass"])
    decision = gate_a_certificate_decision(
        protocol,
        plan,
        controlled_gate_pass=controlled_gate_pass,
        online_policy_certificate=online_policy_certificate,
    )
    return {
        "schema_version": GATE_A_REPORT_VERSION,
        "status": decision["status"],
        "formal_benchmark_result": False,
        "protocol_id": protocol["protocol_id"],
        "protocol_sha256": canonical_sha256(protocol),
        "gate_a_plan_id": plan["plan_id"],
        "gate_a_plan_sha256": canonical_sha256(plan),
        "execution_contract_binding": gate_a_execution_contract_binding(protocol, plan),
        "environment_role": protocol["environment_role"],
        "agent_weight_updates_performed": False,
        "design_validity_audit": design_audit,
        "public_feature_contract": dict(plan["public_feature_contract"]),
        "paired_phase_design": dict(phase_plan),
        "nuisance_integration": {
            "performed": True,
            "mode": "paired_common_hidden_world_with_independent_phase_observation_noise",
            "predictive_samples_per_candidate_action": sample_count,
            "held_out_world_seeds_per_family": int(certificate_plan["world_seeds_per_family"]),
            "same_world_seeds_reused_across_candidate_twins": True,
            "fit_and_certificate_seed_namespaces_disjoint": True,
        },
        "primary_gate_budget": primary_budget,
        "active_oracle": {
            "type": "batch_information_gain_over_matched_pre_post_recipe_contrasts",
            "gate_pass": controlled_gate_pass,
            "primary_budget": primary_budget,
            "by_budget": {
                str(budget): active_certificates[budget] for budget in budgets
            },
        },
        "fixed_trajectory_decoder": {
            "controls_gate": False,
            "by_budget": {
                str(budget): decoder_certificates[budget] for budget in budgets
            },
        },
        "certificate_decision": decision,
        "online_policy_feasible_certificate": decision[
            "online_policy_feasible_certificate"
        ],
        "gate_a_pass": decision["gate_a_pass"],
        "task_reports": task_reports,
        "interpretation": (
            "The primary checkpoint establishes controlled identifiability from an "
            "online-history-aligned matched pre/post public recipe budget. Larger "
            "checkpoints are diagnostic curves with equally sized matched reference sets; "
            "they do not establish online-policy-feasible mechanism discovery. Full Gate A "
            "requires a separately bound online-policy-feasible certificate."
        ),
        "candidate_family_names": candidate_union,
        "publication_ready": False,
    }


def run_gate_a(
    protocol: Mapping[str, Any],
    plan: Mapping[str, Any],
    *,
    online_policy_certificate: Mapping[str, Any] | None = None,
    design_validity_audit: Mapping[str, Any] | None = None,
    progress_callback: Callable[[Mapping[str, Any]], None] | None = None,
) -> dict[str, Any]:
    """Run the frozen active-oracle and fixed-decoder identifiability checks."""

    if plan.get("schema_version") in {
        "chemworld-mechanism-adaptation-gate-a-plan-0.2.2",
        "chemworld-mechanism-adaptation-gate-a-plan-0.2.3",
        "chemworld-mechanism-adaptation-gate-a-plan-0.2.4",
    }:
        return _run_paired_gate_a(
            protocol,
            plan,
            online_policy_certificate=online_policy_certificate,
            design_validity_audit=design_validity_audit,
            progress_callback=progress_callback,
        )
    errors = validate_mechanism_adaptation_protocol(protocol)
    if errors:
        raise ValueError("invalid mechanism-adaptation protocol: " + "; ".join(errors))
    if plan.get("schema_version") != "chemworld-mechanism-adaptation-gate-a-plan-0.2.1":
        raise ValueError("unsupported Gate A plan schema")

    action_plan = plan["action_library"]
    fit_plan = plan["candidate_predictive_fit"]
    certificate_plan = plan["held_out_certificate"]
    gate = protocol["gates"]["gate_a"]
    budgets = [int(item) for item in certificate_plan["budgets"]]
    primary_budget = int(certificate_plan["primary_gate_budget"])
    if budgets != [int(item) for item in gate["budget_checkpoints"]]:
        raise ValueError("Gate A plan budgets do not match the frozen protocol")
    if primary_budget not in budgets:
        raise ValueError("primary Gate A budget must be one of the frozen budgets")
    if int(action_plan["action_count_per_task"]) < max(budgets):
        raise ValueError("Gate A action library must cover the largest decoder budget")

    action_libraries = {
        str(task_id): build_action_library(
            str(task_id),
            action_count=int(action_plan["action_count_per_task"]),
            seed=int(action_plan["design_seed"]),
        )
        for task_id in protocol["design"]["tasks"]
    }
    design_audit = audit_mechanism_design(
        protocol,
        plan,
        action_libraries=action_libraries,
    )
    if not design_audit["pass"]:
        failed = "; ".join(
            f"{item.get('task_id')}:{item['check']}" for item in design_audit["failures"]
        )
        raise ValueError(f"mechanism design audit failed: {failed}")

    active_by_budget: dict[int, dict[str, Any]] = {}
    decoder_by_budget: dict[int, dict[str, Any]] = {}
    task_reports: dict[str, Any] = {}
    active_truths: dict[int, list[str]] = {budget: [] for budget in budgets}
    active_predictions: dict[int, list[str]] = {budget: [] for budget in budgets}
    decoder_truths: dict[int, list[str]] = {budget: [] for budget in budgets}
    decoder_predictions: dict[int, list[str]] = {budget: [] for budget in budgets}
    candidate_union: list[str] = []

    for task_index, task_id in enumerate(protocol["design"]["tasks"]):
        contract = protocol["task_mechanism_contracts"][task_id]
        candidate_ids = [str(item) for item in contract["candidate_ids"]]
        for candidate_id in candidate_ids:
            if candidate_id not in candidate_union:
                candidate_union.append(candidate_id)
        action_library = action_libraries[task_id]
        action_ids = list(action_library)

        oracle = GaussianMechanismOracle(
            candidate_ids=candidate_ids,
            action_ids=action_ids,
            sample_public_observation=_unreachable_sample,
            samples_per_candidate=int(fit_plan["samples_per_candidate_action"]),
            variance_floor=float(fit_plan["variance_floor"]),
            seed=_stable_seed(int(fit_plan["oracle_seed"]), task_id),
        )
        fit_rng = np.random.default_rng(oracle.seed)
        fit_jobs: list[dict[str, Any]] = []
        fit_keys: list[tuple[str, str]] = []
        for action_id in action_ids:
            for candidate_id in candidate_ids:
                seeds = fit_rng.integers(
                    0,
                    np.iinfo(np.int32).max,
                    size=int(fit_plan["samples_per_candidate_action"]),
                )
                for nuisance_seed in seeds:
                    fit_keys.append((candidate_id, action_id))
                    fit_jobs.append(
                        {
                            "task_id": task_id,
                            "seed": int(fit_plan["nuisance_seed_namespace_start"])
                            + int(nuisance_seed) % 500_000_000,
                            "interventions": contract["interventions"][candidate_id],
                            "action_id": action_id,
                            "action_vector": action_library[action_id].tolist(),
                        }
                    )
        fit_results = _execute_jobs(
            _sample_experiment_job,
            fit_jobs,
            workers=int(fit_plan.get("execution_workers", 1)),
        )
        sample_groups: dict[tuple[str, str], list[Sequence[float]]] = {
            (candidate_id, action_id): []
            for action_id in action_ids
            for candidate_id in candidate_ids
        }
        for key, values in zip(fit_keys, fit_results, strict=True):
            sample_groups[key].append(values)
        oracle.fit_predictives_from_samples(sample_groups)
        task_trials: dict[str, list[dict[str, Any]]] = {
            f"active_budget_{budget}": [] for budget in budgets
        }
        task_trials.update({f"decoder_budget_{budget}": [] for budget in budgets})

        trial_keys = [
            (candidate_index, truth_id, repeat_index)
            for candidate_index, truth_id in enumerate(candidate_ids)
            for repeat_index in range(int(certificate_plan["world_seeds_per_family"]))
        ]
        exported_predictives = oracle.export_predictives()
        serialized_actions = {key: vector.tolist() for key, vector in action_library.items()}
        trial_jobs = [
            {
                "task_id": task_id,
                "truth_id": truth_id,
                "trial_seed": int(certificate_plan["seed_namespace_start"])
                + task_index * 1_000_000
                + candidate_index * 10_000
                + repeat_index,
                "interventions": contract["interventions"][truth_id],
                "budgets": budgets,
                "action_ids": action_ids,
                "action_library": serialized_actions,
                "candidate_ids": candidate_ids,
                "predictives": exported_predictives,
                "variance_floor": float(fit_plan["variance_floor"]),
                "oracle_seed": oracle.seed,
                "information_draws": int(certificate_plan["information_draws_per_action"]),
                "repeat_policy": str(action_plan["repeat_policy"]),
            }
            for candidate_index, truth_id, repeat_index in trial_keys
        ]
        completed_trials = _execute_jobs(
            _execute_gate_a_trial_job,
            trial_jobs,
            workers=int(certificate_plan.get("execution_workers", 1)),
        )

        for job, completed in zip(trial_keys, completed_trials, strict=True):
            _candidate_index, truth_id, _repeat_index = job
            qualified_truth = _qualified_candidate(task_id, truth_id)
            for budget in budgets:
                active = completed["active"][budget]
                decoder = completed["decoder"][budget]
                active_truths[budget].append(qualified_truth)
                active_predictions[budget].append(
                    _qualified_candidate(task_id, active["prediction"])
                )
                decoder_truths[budget].append(qualified_truth)
                decoder_predictions[budget].append(
                    _qualified_candidate(task_id, decoder["prediction"])
                )
                task_trials[f"active_budget_{budget}"].append(active)
                task_trials[f"decoder_budget_{budget}"].append(decoder)
        task_reports[task_id] = {
            "candidate_ids": candidate_ids,
            "action_library": {
                key: [float(item) for item in vector] for key, vector in action_library.items()
            },
            "trials": task_trials,
        }

    qualified_candidates = [
        _qualified_candidate(task_id, candidate_id)
        for task_id in protocol["design"]["tasks"]
        for candidate_id in protocol["task_mechanism_contracts"][task_id]["candidate_ids"]
    ]
    for budget in budgets:
        active_by_budget[budget] = identifiability_certificate(
            truths=active_truths[budget],
            predictions=active_predictions[budget],
            candidate_ids=qualified_candidates,
            overall_lower_bound_threshold=float(gate["overall_top1_wilson_lower_bound"]),
            family_recall_lower_bound_threshold=float(gate["per_family_recall_wilson_lower_bound"]),
        )
        decoder_by_budget[budget] = identifiability_certificate(
            truths=decoder_truths[budget],
            predictions=decoder_predictions[budget],
            candidate_ids=qualified_candidates,
            overall_lower_bound_threshold=float(gate["overall_top1_wilson_lower_bound"]),
            family_recall_lower_bound_threshold=float(gate["per_family_recall_wilson_lower_bound"]),
        )

    primary_active = active_by_budget[primary_budget]
    decision = gate_a_certificate_decision(
        protocol,
        plan,
        controlled_gate_pass=bool(primary_active["gate_pass"]),
        online_policy_certificate=online_policy_certificate,
    )
    return {
        "schema_version": GATE_A_REPORT_VERSION,
        "status": decision["status"],
        "formal_benchmark_result": False,
        "protocol_id": protocol["protocol_id"],
        "protocol_sha256": canonical_sha256(protocol),
        "gate_a_plan_id": plan["plan_id"],
        "gate_a_plan_sha256": canonical_sha256(plan),
        "execution_contract_binding": gate_a_execution_contract_binding(protocol, plan),
        "environment_role": protocol["environment_role"],
        "agent_weight_updates_performed": False,
        "design_validity_audit": design_audit,
        "public_feature_contract": dict(plan["public_feature_contract"]),
        "nuisance_integration": {
            "performed": True,
            "predictive_samples_per_candidate_action": int(
                fit_plan["samples_per_candidate_action"]
            ),
            "held_out_world_seeds_per_family": int(certificate_plan["world_seeds_per_family"]),
            "fit_and_certificate_seed_namespaces_disjoint": True,
        },
        "primary_gate_budget": primary_budget,
        "active_oracle": {
            "gate_pass": bool(primary_active["gate_pass"]),
            "primary_budget": primary_budget,
            "by_budget": {str(key): value for key, value in active_by_budget.items()},
        },
        "fixed_trajectory_decoder": {
            "controls_gate": False,
            "by_budget": {str(key): value for key, value in decoder_by_budget.items()},
        },
        "certificate_decision": decision,
        "online_policy_feasible_certificate": decision[
            "online_policy_feasible_certificate"
        ],
        "gate_a_pass": decision["gate_a_pass"],
        "task_reports": task_reports,
        "interpretation": (
            "The controlled oracle establishes budgeted identifiability only. Full Gate A "
            "also requires a separately bound online-policy-feasible certificate; neither "
            "certificate alone establishes evaluated-Agent mechanism discovery."
        ),
        "candidate_family_names": candidate_union,
        "publication_ready": False,
    }


def run_campaign_row(
    protocol: Mapping[str, Any],
    row: Mapping[str, Any],
    *,
    output_root: str | Path,
    llm_methods: Mapping[str, Any],
    method_id: str = "live_llm_b",
    spectrum_disclosure: str = "assigned",
    feedback_condition: FeedbackCondition = "true_feedback",
    progress_callback: (Callable[[str, Any, list[dict[str, Any]]], None] | None) = None,
) -> dict[str, Any]:
    """Execute one frozen changed/no-change row with a real DeepSeek-backed Agent."""

    agent = build_mechanism_agent(
        protocol,
        row,
        llm_methods=llm_methods,
        method_id=method_id,
        spectrum_disclosure=spectrum_disclosure,
    )
    task_id = str(row["task_id"])
    adapter = ContinuingPublicViewAgent(
        agent,
        method_id=method_id,
        feedback_condition=feedback_condition,
        critical_instrument=_CRITICAL_INSTRUMENTS[task_id],
    )
    change_time = int(row["phase_reset_after_experiment"])
    horizon = int(row["total_experiment_horizon"])
    condition_suffix = "" if feedback_condition == "true_feedback" else f"--{feedback_condition}"
    campaign_id = f"{row['pair_id']}--{row['arm']}{condition_suffix}"
    result = run_two_phase_campaign(
        task_id=task_id,
        adapter=adapter,
        seed=int(row["world_seed"]),
        pre_change_experiments=change_time,
        post_change_experiments=horizon - change_time,
        shifted_interventions=row["world_interventions"],
        output_root=Path(output_root) / "trajectories",
        campaign_id=campaign_id,
        observation_pair_id=str(row["pair_id"]),
        progress_callback=progress_callback,
    )
    result.update(
        {
            "schema_version": EXECUTION_SCHEMA_VERSION,
            "protocol_id": protocol["protocol_id"],
            "protocol_sha256": canonical_sha256(protocol),
            "matrix_row": dict(row),
            "truth_id": row["truth_id"],
            "hidden_law_changes": bool(row["hidden_law_changes"]),
            "feedback_condition": feedback_condition,
            "formal_result": False,
            "agent_weight_updates_performed": False,
        }
    )
    return result


def build_mechanism_agent(
    protocol: Mapping[str, Any],
    row: Mapping[str, Any],
    *,
    llm_methods: Mapping[str, Any],
    method_id: str = "live_llm_b",
    spectrum_disclosure: str = "assigned",
    client: Any | None = None,
) -> MechanismAdaptationLiveLLMAgent:
    """Build the exact leakage-resistant Agent used by campaign and local audits."""

    method = llm_methods["methods"][method_id]
    request = method["request_configuration"]
    planner = client or DeepSeekClient(
        model=str(method["model_id"]),
        thinking=bool(request["thinking"]),
        reasoning_effort=cast(Any, str(request.get("reasoning_effort") or "max")),
        timeout_s=float(request["timeout_s"]),
        max_attempts=int(request["max_attempts"]),
        retry_backoff_s=float(request["retry_backoff_s"]),
    )
    definitions = protocol["diagnosis_contract"]["candidate_definitions"]
    specs = tuple(
        MechanismCandidateSpec(
            candidate_id=str(candidate_id),
            public_definition=str(definitions[candidate_id]),
        )
        for candidate_id in row["candidate_ids"]
    )
    candidate_label_mode = _parse_candidate_label_mode(row["candidate_label_mode"])
    return MechanismAdaptationLiveLLMAgent(
        planner,
        role_id=f"mechanism_adaptation_{method_id}",
        spectrum_disclosure=spectrum_disclosure,
        response_max_tokens=int(request["max_tokens"]),
        fail_fast_on_unbillable_provider_failure=True,
        candidate_specs=specs,
        candidate_label_mode=candidate_label_mode,
        candidate_order_seed=int(row["candidate_order_seed"]),
        randomize_candidate_order=True,
    )


def _parse_candidate_label_mode(value: Any) -> CandidateLabelMode:
    mode = str(value)
    if mode not in {"semantic", "anonymous"}:
        raise ValueError("candidate_label_mode must be semantic or anonymous")
    return cast(CandidateLabelMode, mode)


def selected_campaign_rows(
    protocol: Mapping[str, Any],
    *,
    tasks: Sequence[str] | None = None,
    pair_ids: Sequence[str] | None = None,
    limit: int | None = None,
) -> list[dict[str, Any]]:
    """Select complete pairs from the frozen matrix for resumable pilots or runs."""

    rows = build_paired_campaign_matrix(protocol)
    task_filter = set(tasks or ())
    pair_filter = set(pair_ids or ())
    if task_filter:
        rows = [row for row in rows if row["task_id"] in task_filter]
    if pair_filter:
        rows = [row for row in rows if row["pair_id"] in pair_filter]
    if limit is not None:
        if limit <= 0:
            raise ValueError("campaign pair limit must be positive")
        ordered_pairs = list(dict.fromkeys(row["pair_id"] for row in rows))[:limit]
        retained = set(ordered_pairs)
        rows = [row for row in rows if row["pair_id"] in retained]
    return rows


def _qualified_candidate(task_id: str, candidate_id: str) -> str:
    return f"{task_id}::{candidate_id}"


def _stable_seed(seed: int, label: str) -> int:
    digest = hashlib.sha256(f"{seed}|{label}".encode()).digest()
    return int.from_bytes(digest[:4], "big") % np.iinfo(np.int32).max
