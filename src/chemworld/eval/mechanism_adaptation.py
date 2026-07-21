"""Core analysis primitives for the mechanism-adaptation benchmark.

The module deliberately separates declared model reports from calibrated environment
posteriors.  Helpers that operate on declared distributions never call their outputs
Bayesian beliefs or information gain.  The small Gaussian oracle is an executable
reference implementation for candidate generators that can provide public-observation
samples without revealing the true candidate or nuisance realization.
"""

from __future__ import annotations

import hashlib
import json
import math
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from statistics import NormalDist
from typing import Any, Literal

import numpy as np

MECHANISM_ADAPTATION_ANALYSIS_VERSION = "chemworld-mechanism-adaptation-analysis-0.2"

REQUIRED_GATE_IDS = ("gate_0", "gate_a", "gate_b", "gate_c", "gate_d", "gate_e")

AutonomyStatus = Literal[
    "fully_autonomous_campaign",
    "autonomous_current_experiment_with_assisted_history",
    "assisted_campaign",
    "incomplete_campaign",
]


@dataclass(frozen=True)
class OutcomeLayers:
    """Keep intervention targets separate from evaluation truth."""

    environment_outcome: Mapping[str, Any]
    agent_visible_observation: Mapping[str, Any]
    evaluation_outcome: Mapping[str, Any]

    def to_dict(self) -> dict[str, dict[str, Any]]:
        return {
            "environment_outcome": dict(self.environment_outcome),
            "agent_visible_observation": dict(self.agent_visible_observation),
            "evaluation_outcome": dict(self.evaluation_outcome),
        }


def normalized_distribution(values: Mapping[str, float]) -> dict[str, float]:
    """Validate and normalize a finite categorical distribution."""

    if len(values) < 2:
        raise ValueError("a mechanism distribution requires at least two candidates")
    normalized: dict[str, float] = {}
    for key, raw in values.items():
        if isinstance(raw, bool) or not isinstance(raw, int | float):
            raise ValueError("mechanism probabilities must be numeric")
        value = float(raw)
        if not math.isfinite(value) or value < 0.0:
            raise ValueError("mechanism probabilities must be finite and non-negative")
        normalized[str(key)] = value
    total = sum(normalized.values())
    if total <= 0.0:
        raise ValueError("mechanism probabilities must have positive total mass")
    return {key: value / total for key, value in normalized.items()}


def declared_change_probability(distribution: Mapping[str, float]) -> float:
    """Derive change probability from the declared no-change mass."""

    values = normalized_distribution(distribution)
    if "no_change" not in values:
        raise ValueError("declared mechanism distribution must include no_change")
    return 1.0 - values["no_change"]


def conditional_changed_family_distribution(
    distribution: Mapping[str, float],
) -> dict[str, float] | None:
    """Return q(family | change), or ``None`` when no change mass is one."""

    values = normalized_distribution(distribution)
    changed = {key: value for key, value in values.items() if key != "no_change"}
    mass = sum(changed.values())
    if mass <= 0.0:
        return None
    return {key: value / mass for key, value in changed.items()}


def categorical_entropy(distribution: Mapping[str, float], *, normalized: bool = False) -> float:
    """Return categorical entropy in nats, optionally divided by log(cardinality)."""

    values = normalized_distribution(distribution)
    entropy = -sum(value * math.log(value) for value in values.values() if value > 0.0)
    if normalized:
        entropy /= math.log(len(values))
    return entropy


def kl_divergence(
    following: Mapping[str, float],
    current: Mapping[str, float],
    *,
    floor: float = 1e-12,
) -> float:
    """Return KL(following || current) with a documented numerical floor."""

    left = normalized_distribution(following)
    right = normalized_distribution(current)
    if set(left) != set(right):
        raise ValueError("distributions must contain identical candidate IDs")
    return sum(
        value * math.log(value / max(right[key], floor))
        for key, value in left.items()
        if value > 0.0
    )


def js_divergence(left: Mapping[str, float], right: Mapping[str, float]) -> float:
    """Return Jensen-Shannon divergence in nats."""

    first = normalized_distribution(left)
    second = normalized_distribution(right)
    if set(first) != set(second):
        raise ValueError("distributions must contain identical candidate IDs")
    midpoint = {key: 0.5 * (first[key] + second[key]) for key in first}
    return 0.5 * kl_divergence(first, midpoint) + 0.5 * kl_divergence(second, midpoint)


def multiclass_brier(distribution: Mapping[str, float], truth: str) -> float:
    """Return the multiclass Brier score for a declared distribution."""

    values = normalized_distribution(distribution)
    if truth not in values:
        raise ValueError("truth must be one of the declared candidates")
    return sum((value - (1.0 if key == truth else 0.0)) ** 2 for key, value in values.items())


def change_detection_summary(
    *,
    changed: Sequence[bool],
    probabilities: Sequence[float],
    detection_delays: Sequence[int | None],
    threshold: float = 0.5,
) -> dict[str, Any]:
    """Score change campaigns together with their required no-change twins."""

    aligned = len(changed) == len(probabilities) == len(detection_delays)
    if not changed or not aligned:
        raise ValueError("change labels, probabilities, and delays must be non-empty and aligned")
    if not 0.0 <= threshold <= 1.0:
        raise ValueError("threshold must be in [0, 1]")
    labels = [bool(item) for item in changed]
    scores = [float(item) for item in probabilities]
    if any(not math.isfinite(item) or not 0.0 <= item <= 1.0 for item in scores):
        raise ValueError("change probabilities must be finite and in [0, 1]")
    positives = sum(labels)
    negatives = len(labels) - positives
    if positives == 0 or negatives == 0:
        raise ValueError("change detection requires changed and no-change campaigns")
    predicted = [score >= threshold for score in scores]
    true_positive = sum(
        label and estimate for label, estimate in zip(labels, predicted, strict=True)
    )
    false_positive = sum(
        not label and estimate for label, estimate in zip(labels, predicted, strict=True)
    )
    observed_delays = [
        int(delay)
        for label, estimate, delay in zip(labels, predicted, detection_delays, strict=True)
        if label and estimate and delay is not None
    ]
    return {
        "campaign_count": len(labels),
        "changed_count": positives,
        "no_change_twin_count": negatives,
        "threshold": threshold,
        "sensitivity": true_positive / positives,
        "false_positive_rate": false_positive / negatives,
        "auroc": _binary_auroc(labels, scores),
        "brier_score": sum(
            (score - (1.0 if label else 0.0)) ** 2
            for label, score in zip(labels, scores, strict=True)
        )
        / len(labels),
        "mean_detection_delay": _mean(observed_delays),
        "detected_changed_count": len(observed_delays),
        "right_censored_changed_count": positives - len(observed_delays),
    }


def declared_distribution_update(
    current: Mapping[str, float],
    following: Mapping[str, float],
    *,
    truth: str,
) -> dict[str, float]:
    """Describe an adjacent public-distribution update without Bayesian claims."""

    first = normalized_distribution(current)
    second = normalized_distribution(following)
    if truth not in first or truth not in second:
        raise ValueError("truth must occur in both declared distributions")
    floor = 1e-12
    return {
        "declared_distribution_js_shift": js_divergence(first, second),
        "declared_distribution_kl_shift": kl_divergence(second, first),
        "declared_normalized_entropy_change": (
            categorical_entropy(second, normalized=True)
            - categorical_entropy(first, normalized=True)
        ),
        "truth_log_probability_change": math.log(max(second[truth], floor))
        - math.log(max(first[truth], floor)),
        "brier_improvement": multiclass_brier(first, truth) - multiclass_brier(second, truth),
    }


def feedback_effect_summary(
    *,
    within_condition_distances: Sequence[float],
    between_condition_distances: Sequence[float],
) -> dict[str, float | int | None]:
    """Separate feedback-condition differences from provider repeat noise."""

    within = _finite_values(within_condition_distances)
    between = _finite_values(between_condition_distances)
    within_mean = _mean(within)
    between_mean = _mean(between)
    return {
        "within_repeat_count": len(within),
        "between_condition_count": len(between),
        "mean_within_provider_variation": within_mean,
        "mean_between_feedback_variation": between_mean,
        "net_feedback_effect": (
            between_mean - within_mean
            if within_mean is not None and between_mean is not None
            else None
        ),
    }


def operation_aware_action_distance(
    left: Mapping[str, Any],
    right: Mapping[str, Any],
    *,
    parameter_bounds: Mapping[str, tuple[float, float]] | None = None,
) -> dict[str, Any]:
    """Compare actions without treating absent operation parameters as zero."""

    left_operation = str(left.get("operation") or "")
    right_operation = str(right.get("operation") or "")
    if left_operation != right_operation:
        return {
            "same_operation": False,
            "operation_distance": 1.0,
            "parameter_distance": None,
            "compared_parameters": [],
        }
    bounds = parameter_bounds or {}
    shared = sorted((set(left) & set(right)) - {"operation", "instrument"})
    squared: list[float] = []
    compared: list[str] = []
    for key in shared:
        first = left[key]
        second = right[key]
        if isinstance(first, bool) or isinstance(second, bool):
            continue
        if isinstance(first, int | float) and isinstance(second, int | float):
            low, high = bounds.get(key, (0.0, max(abs(float(first)), abs(float(second)), 1.0)))
            scale = max(float(high) - float(low), 1e-12)
            squared.append(((float(first) - float(second)) / scale) ** 2)
            compared.append(key)
        elif first != second:
            squared.append(1.0)
            compared.append(key)
        else:
            squared.append(0.0)
            compared.append(key)
    return {
        "same_operation": True,
        "operation_distance": 0.0,
        "parameter_distance": (math.sqrt(sum(squared) / len(squared)) if squared else 0.0),
        "compared_parameters": compared,
    }


def recovery_decomposition(
    *,
    iid_replay_iid_world: float,
    iid_replay_shifted_world: float,
    frozen_policy_shifted_world: float,
    adaptive_policy_shifted_world: float,
    oracle_shifted_world: float,
) -> dict[str, float | None]:
    """Separate world, behavioural-adaptation, and normalized-recovery effects."""

    world_effect = iid_replay_shifted_world - iid_replay_iid_world
    adaptation_gain = adaptive_policy_shifted_world - frozen_policy_shifted_world
    denominator = oracle_shifted_world - frozen_policy_shifted_world
    normalized_recovery = adaptation_gain / denominator if abs(denominator) > 1e-12 else None
    return {
        "world_effect": world_effect,
        "adaptation_gain": adaptation_gain,
        "normalized_recovery": normalized_recovery,
        "normalization_denominator": denominator,
    }


def campaign_autonomy_status(
    *,
    current_experiment_autonomous: bool,
    assisted_history: bool,
    campaign_complete: bool,
) -> AutonomyStatus:
    """Return the frozen three-level campaign autonomy classification."""

    if not campaign_complete:
        return "incomplete_campaign"
    if not current_experiment_autonomous:
        return "assisted_campaign"
    if assisted_history:
        return "autonomous_current_experiment_with_assisted_history"
    return "fully_autonomous_campaign"


@dataclass(frozen=True)
class GaussianCandidatePredictive:
    """Diagonal-Gaussian approximation for one candidate and public action."""

    candidate_id: str
    action_id: str
    mean: np.ndarray
    variance: np.ndarray

    def log_likelihood(self, observation: Sequence[float]) -> float:
        values = np.asarray(observation, dtype=float).reshape(-1)
        if values.shape != self.mean.shape:
            raise ValueError("observation dimension does not match predictive model")
        variance = np.maximum(self.variance, 1e-12)
        return float(
            -0.5 * np.sum(np.log(2.0 * math.pi * variance) + ((values - self.mean) ** 2) / variance)
        )


class GaussianMechanismOracle:
    """Executable Monte-Carlo diagnosis oracle over candidate public generators.

    ``sample_public_observation`` must not reveal the true candidate.  It receives a
    candidate ID, a public action ID, a nuisance/noise seed, and should return the
    public numeric feature vector that an Agent could observe.  A caller may close over
    cloned candidate worlds and the current public history.
    """

    def __init__(
        self,
        *,
        candidate_ids: Sequence[str],
        action_ids: Sequence[str],
        sample_public_observation: Callable[[str, str, int], Sequence[float]],
        samples_per_candidate: int = 128,
        variance_floor: float = 1e-6,
        seed: int = 0,
    ) -> None:
        if len(set(candidate_ids)) < 2:
            raise ValueError("oracle requires at least two candidate IDs")
        if not action_ids:
            raise ValueError("oracle requires at least one public action")
        if samples_per_candidate < 4:
            raise ValueError("samples_per_candidate must be at least four")
        self.candidate_ids = tuple(str(item) for item in candidate_ids)
        self.action_ids = tuple(str(item) for item in action_ids)
        self._sample = sample_public_observation
        self.samples_per_candidate = int(samples_per_candidate)
        self.variance_floor = float(variance_floor)
        self.seed = int(seed)
        uniform = 1.0 / len(self.candidate_ids)
        self.posterior = dict.fromkeys(self.candidate_ids, uniform)
        self._predictives: dict[tuple[str, str], GaussianCandidatePredictive] = {}

    def fit_predictives(self) -> None:
        """Fit held-out-ready predictive approximations for every action/candidate."""

        rng = np.random.default_rng(self.seed)
        fitted: dict[tuple[str, str], GaussianCandidatePredictive] = {}
        for action_id in self.action_ids:
            for candidate_id in self.candidate_ids:
                seeds = rng.integers(0, np.iinfo(np.int32).max, size=self.samples_per_candidate)
                samples = np.asarray(
                    [
                        self._sample(candidate_id, action_id, int(sample_seed))
                        for sample_seed in seeds
                    ],
                    dtype=float,
                )
                if samples.ndim != 2 or samples.shape[0] != self.samples_per_candidate:
                    raise ValueError("candidate generator must return fixed-length vectors")
                fitted[(candidate_id, action_id)] = GaussianCandidatePredictive(
                    candidate_id=candidate_id,
                    action_id=action_id,
                    mean=np.mean(samples, axis=0),
                    variance=np.maximum(np.var(samples, axis=0, ddof=1), self.variance_floor),
                )
        self._predictives = fitted

    def update(self, *, action_id: str, observation: Sequence[float]) -> dict[str, float]:
        """Update the calibrated-reference posterior for one public observation."""

        self._require_fitted()
        if action_id not in self.action_ids:
            raise ValueError("unknown public action ID")
        log_weights = {
            candidate: math.log(max(self.posterior[candidate], 1e-300))
            + self._predictives[(candidate, action_id)].log_likelihood(observation)
            for candidate in self.candidate_ids
        }
        maximum = max(log_weights.values())
        weights = {key: math.exp(value - maximum) for key, value in log_weights.items()}
        self.posterior = normalized_distribution(weights)
        return dict(self.posterior)

    def expected_information_by_action(self, *, draws: int = 256) -> dict[str, float]:
        """Estimate mutual information in nats under the current posterior."""

        self._require_fitted()
        if draws <= 0:
            raise ValueError("draws must be positive")
        rng = np.random.default_rng(self.seed + 1)
        prior_entropy = categorical_entropy(self.posterior)
        candidates = np.asarray(self.candidate_ids)
        probabilities = np.asarray([self.posterior[item] for item in self.candidate_ids])
        result: dict[str, float] = {}
        for action_id in self.action_ids:
            posterior_entropies: list[float] = []
            for _ in range(draws):
                candidate = str(rng.choice(candidates, p=probabilities))
                predictive = self._predictives[(candidate, action_id)]
                observation = rng.normal(predictive.mean, np.sqrt(predictive.variance))
                posterior_entropies.append(
                    categorical_entropy(
                        self._posterior_for_observation(action_id, observation.tolist())
                    )
                )
            result[action_id] = prior_entropy - float(np.mean(posterior_entropies))
        return result

    def select_action(self, *, draws: int = 256) -> str:
        """Select the public action with maximum estimated information value."""

        values = self.expected_information_by_action(draws=draws)
        return max(values, key=values.__getitem__)

    def reset_posterior(self, prior: Mapping[str, float] | None = None) -> None:
        """Reset state between independent world-seed trials."""

        if prior is None:
            uniform = 1.0 / len(self.candidate_ids)
            self.posterior = dict.fromkeys(self.candidate_ids, uniform)
            return
        values = normalized_distribution(prior)
        if set(values) != set(self.candidate_ids):
            raise ValueError("oracle prior must contain exactly the candidate IDs")
        self.posterior = values

    def _posterior_for_observation(
        self,
        action_id: str,
        observation: Sequence[float],
    ) -> dict[str, float]:
        log_weights = {
            candidate: math.log(max(self.posterior[candidate], 1e-300))
            + self._predictives[(candidate, action_id)].log_likelihood(observation)
            for candidate in self.candidate_ids
        }
        maximum = max(log_weights.values())
        return normalized_distribution(
            {key: math.exp(value - maximum) for key, value in log_weights.items()}
        )

    def _require_fitted(self) -> None:
        if not self._predictives:
            raise RuntimeError("fit_predictives must be called before diagnosis")


def wilson_interval(
    successes: int,
    total: int,
    *,
    confidence: float = 0.95,
) -> tuple[float, float]:
    """Return the Wilson binomial confidence interval."""

    if total <= 0 or not 0 <= successes <= total:
        raise ValueError("successes and total must define a non-empty binomial sample")
    if not 0.0 < confidence < 1.0:
        raise ValueError("confidence must be in (0, 1)")
    z = NormalDist().inv_cdf(0.5 + confidence / 2.0)
    rate = successes / total
    denominator = 1.0 + z * z / total
    center = (rate + z * z / (2.0 * total)) / denominator
    radius = (
        z * math.sqrt(rate * (1.0 - rate) / total + z * z / (4.0 * total * total)) / denominator
    )
    return max(center - radius, 0.0), min(center + radius, 1.0)


def identifiability_certificate(
    *,
    truths: Sequence[str],
    predictions: Sequence[str],
    candidate_ids: Sequence[str],
    overall_lower_bound_threshold: float = 0.80,
    family_recall_lower_bound_threshold: float = 0.70,
) -> dict[str, Any]:
    """Build the frozen family-level active/decoder certificate."""

    if len(truths) != len(predictions) or not truths:
        raise ValueError("truths and predictions must be non-empty and aligned")
    candidates = tuple(str(item) for item in candidate_ids)
    if set(truths) - set(candidates) or set(predictions) - set(candidates):
        raise ValueError("truths and predictions must use declared candidate IDs")
    correct = sum(left == right for left, right in zip(truths, predictions, strict=True))
    overall_interval = wilson_interval(correct, len(truths))
    family: dict[str, Any] = {}
    for candidate in candidates:
        indices = [index for index, truth in enumerate(truths) if truth == candidate]
        if not indices:
            family[candidate] = {"count": 0, "recall": None, "recall_interval": None}
            continue
        hits = sum(predictions[index] == candidate for index in indices)
        interval = wilson_interval(hits, len(indices))
        family[candidate] = {
            "count": len(indices),
            "recall": hits / len(indices),
            "recall_interval": list(interval),
        }
    family_pass = all(
        item["recall_interval"] is not None
        and float(item["recall_interval"][0]) >= family_recall_lower_bound_threshold
        for item in family.values()
    )
    return {
        "sample_count": len(truths),
        "top1_accuracy": correct / len(truths),
        "top1_accuracy_interval": list(overall_interval),
        "family_recall": family,
        "overall_lower_bound_threshold": overall_lower_bound_threshold,
        "family_recall_lower_bound_threshold": family_recall_lower_bound_threshold,
        "overall_pass": overall_interval[0] >= overall_lower_bound_threshold,
        "family_pass": family_pass,
        "gate_pass": (overall_interval[0] >= overall_lower_bound_threshold and family_pass),
    }


def fixed_trajectory_decode(
    oracle: GaussianMechanismOracle,
    *,
    action_ids: Sequence[str],
    observations: Sequence[Sequence[float]],
    prior: Mapping[str, float] | None = None,
) -> dict[str, Any]:
    """Decode an Agent-generated public trajectory without selecting its actions."""

    if len(action_ids) != len(observations) or not action_ids:
        raise ValueError("actions and observations must be non-empty and aligned")
    oracle.reset_posterior(prior)
    updates: list[dict[str, float]] = []
    for action_id, observation in zip(action_ids, observations, strict=True):
        updates.append(oracle.update(action_id=action_id, observation=observation))
    return {
        "mode": "fixed_trajectory_decoder",
        "action_count": len(action_ids),
        "posterior": dict(oracle.posterior),
        "prediction": max(oracle.posterior, key=oracle.posterior.__getitem__),
        "updates": updates,
    }


def active_oracle_diagnosis(
    oracle: GaussianMechanismOracle,
    *,
    observe: Callable[[str, int], Sequence[float]],
    budget: int,
    information_draws: int = 256,
    prior: Mapping[str, float] | None = None,
) -> dict[str, Any]:
    """Run one budget-matched active diagnosis trial on public observations."""

    if budget <= 0:
        raise ValueError("diagnosis budget must be positive")
    oracle.reset_posterior(prior)
    actions: list[str] = []
    updates: list[dict[str, float]] = []
    for index in range(budget):
        action_id = oracle.select_action(draws=information_draws)
        actions.append(action_id)
        observation = observe(action_id, index)
        updates.append(oracle.update(action_id=action_id, observation=observation))
    return {
        "mode": "active_budget_matched_diagnosis_oracle",
        "budget": budget,
        "actions": actions,
        "posterior": dict(oracle.posterior),
        "prediction": max(oracle.posterior, key=oracle.posterior.__getitem__),
        "updates": updates,
    }


def validate_mechanism_adaptation_protocol(protocol: Mapping[str, Any]) -> list[str]:
    """Return protocol-freeze errors for the six-Gate mechanism benchmark."""

    errors: list[str] = []
    gates = protocol.get("gates")
    if not isinstance(gates, Mapping):
        return ["gates must be an object containing gate_0 through gate_e"]
    for gate_id in REQUIRED_GATE_IDS:
        gate = gates.get(gate_id)
        if not isinstance(gate, Mapping):
            errors.append(f"missing {gate_id}")
        elif not gate.get("pass_rule"):
            errors.append(f"{gate_id} must freeze a pass_rule")

    design = protocol.get("design")
    if not isinstance(design, Mapping):
        errors.append("design must be an object")
    else:
        if design.get("post_change_checkpoints") != [1, 2, 4, 8]:
            errors.append("post_change_checkpoints must equal [1, 2, 4, 8]")
        changepoints = design.get("change_after_experiments")
        if not isinstance(changepoints, list) or "never" not in changepoints:
            errors.append("change_after_experiments must include the no-change twin 'never'")
        if int(design.get("total_experiment_horizon", 0) or 0) < 8:
            errors.append("total_experiment_horizon must be at least eight")
        repeat_count = int(design.get("provider_repeats_per_paired_cell", 0) or 0)
        order_seeds = design.get("candidate_order_seeds")
        if not isinstance(order_seeds, list) or len(order_seeds) != repeat_count:
            errors.append("candidate_order_seeds must match provider repeat count")

    reporting = protocol.get("reporting")
    if not isinstance(reporting, Mapping):
        errors.append("reporting must be an object")
    else:
        if reporting.get("statistical_unit") != "world_seed_or_paired_cell":
            errors.append("statistical_unit must be world_seed_or_paired_cell")
        if reporting.get("provider_repeats") != "nested_technical_replicates":
            errors.append("provider repeats must be nested technical replicates")

    data_contract = protocol.get("data_contract")
    required_outcomes = {
        "environment_outcome",
        "agent_visible_observation",
        "evaluation_outcome",
    }
    if not isinstance(data_contract, Mapping):
        errors.append("data_contract must be an object")
    elif set(data_contract.get("outcome_layers", [])) != required_outcomes:
        errors.append("data_contract must separate all three outcome layers")

    diagnosis = protocol.get("diagnosis_contract")
    if not isinstance(diagnosis, Mapping):
        errors.append("diagnosis_contract must be an object")
    else:
        if diagnosis.get("change_probability") != "derived_as_1_minus_q_no_change":
            errors.append("change probability must be derived from q(no_change)")
        if not diagnosis.get("candidate_definitions_required"):
            errors.append("operational candidate definitions are required")
        if not diagnosis.get("candidate_order_randomized"):
            errors.append("candidate order randomization is required")

    task_contracts = protocol.get("task_mechanism_contracts")
    expected_tasks = set(design.get("tasks", [])) if isinstance(design, Mapping) else set()
    if not isinstance(task_contracts, Mapping) or set(task_contracts) != expected_tasks:
        errors.append("task_mechanism_contracts must exactly cover design tasks")
    elif isinstance(diagnosis, Mapping):
        definitions = diagnosis.get("candidate_definitions", {})
        for task_id, raw_contract in task_contracts.items():
            if not isinstance(raw_contract, Mapping):
                errors.append(f"task mechanism contract must be an object: {task_id}")
                continue
            candidates = raw_contract.get("candidate_ids")
            interventions = raw_contract.get("interventions")
            if not isinstance(candidates, list) or "no_change" not in candidates:
                errors.append(f"task candidates must include no_change: {task_id}")
                continue
            if not isinstance(interventions, Mapping) or set(interventions) != set(candidates):
                errors.append(f"task interventions must exactly cover candidates: {task_id}")
            if set(candidates) - set(definitions):
                errors.append(f"task candidates lack public definitions: {task_id}")
            if isinstance(interventions, Mapping) and interventions.get("no_change") != []:
                errors.append(f"no_change intervention must be empty: {task_id}")

    return errors


def build_paired_campaign_matrix(
    protocol: Mapping[str, Any],
    *,
    world_seeds: Sequence[int] | None = None,
) -> list[dict[str, Any]]:
    """Expand the frozen changed/no-change twin confirmatory matrix."""

    errors = validate_mechanism_adaptation_protocol(protocol)
    if errors:
        raise ValueError("invalid mechanism-adaptation protocol: " + "; ".join(errors))
    design = protocol["design"]
    task_contracts = protocol["task_mechanism_contracts"]
    seeds = list(world_seeds or design["public_development_seeds"])
    if not seeds or len(set(seeds)) != len(seeds):
        raise ValueError("world seeds must be non-empty and unique")
    change_times = [int(item) for item in design["change_after_experiments"] if item != "never"]
    label_modes = list(protocol["diagnosis_contract"]["candidate_label_modes"])
    order_seeds = [int(item) for item in design["candidate_order_seeds"]]
    rows: list[dict[str, Any]] = []
    for task_id, raw_contract in task_contracts.items():
        candidates = list(raw_contract["candidate_ids"])
        interventions = raw_contract["interventions"]
        for truth_id in candidates:
            if truth_id == "no_change":
                continue
            for change_time in change_times:
                for label_mode in label_modes:
                    for world_seed in seeds:
                        for repeat_id, order_seed in enumerate(order_seeds):
                            pair_payload = {
                                "protocol_id": protocol["protocol_id"],
                                "task_id": task_id,
                                "changed_truth_id": truth_id,
                                "phase_reset_after_experiment": change_time,
                                "candidate_label_mode": label_mode,
                                "world_seed": int(world_seed),
                                "provider_repeat_id": repeat_id,
                                "candidate_order_seed": order_seed,
                            }
                            pair_id = hashlib.sha256(
                                json.dumps(
                                    pair_payload,
                                    sort_keys=True,
                                    separators=(",", ":"),
                                ).encode("utf-8")
                            ).hexdigest()[:20]
                            for arm in ("changed", "no_change_twin"):
                                arm_truth = truth_id if arm == "changed" else "no_change"
                                rows.append(
                                    {
                                        **pair_payload,
                                        "pair_id": pair_id,
                                        "arm": arm,
                                        "truth_id": arm_truth,
                                        "candidate_ids": candidates,
                                        "world_interventions": (
                                            interventions[truth_id]
                                            if arm == "changed"
                                            else interventions["no_change"]
                                        ),
                                        "hidden_law_changes": arm == "changed",
                                        "agent_memory_preserved_across_phase_reset": True,
                                        "total_experiment_horizon": design[
                                            "total_experiment_horizon"
                                        ],
                                        "post_change_checkpoints": design[
                                            "post_change_checkpoints"
                                        ],
                                    }
                                )
    return rows


def evaluate_protocol_gates(
    protocol: Mapping[str, Any],
    evidence: Mapping[str, Any],
) -> dict[str, Any]:
    """Evaluate frozen gates conservatively; absent evidence can never pass."""

    protocol_errors = validate_mechanism_adaptation_protocol(protocol)
    if protocol_errors:
        raise ValueError("invalid mechanism-adaptation protocol: " + "; ".join(protocol_errors))
    gates = protocol["gates"]
    integrity = evidence.get("gate_0")
    gate_0 = bool(isinstance(integrity, Mapping) and integrity.get("all_required_checks_pass"))

    identifiability = evidence.get("gate_a")
    active = identifiability.get("active_oracle") if isinstance(identifiability, Mapping) else None
    decoder = (
        identifiability.get("fixed_trajectory_decoder")
        if isinstance(identifiability, Mapping)
        else None
    )
    gate_a = bool(
        isinstance(active, Mapping) and active.get("gate_pass") and isinstance(decoder, Mapping)
    )

    detection = evidence.get("gate_b")
    gate_b = bool(
        isinstance(detection, Mapping)
        and int(detection.get("no_change_twin_count", 0)) > 0
        and float(detection.get("false_positive_rate", math.inf))
        <= float(gates["gate_b"]["maximum_no_change_false_positive_rate"])
        and _interval_lower(detection.get("auroc_interval"))
        >= float(gates["gate_b"]["minimum_auroc_lower_confidence_bound"])
    )

    feedback = evidence.get("gate_c")
    gate_c = bool(
        isinstance(feedback, Mapping)
        and float(feedback.get("net_local_feedback_effect", -math.inf))
        > float(gates["gate_c"]["minimum_net_local_feedback_effect"])
        and _interval_lower(feedback.get("paired_utility_interval")) > 0.0
    )

    recovery = evidence.get("gate_d")
    gate_d = bool(
        isinstance(recovery, Mapping)
        and _interval_lower(recovery.get("adaptation_gain_interval")) > 0.0
        and _interval_lower(recovery.get("normalized_recovery_interval"))
        >= float(gates["gate_d"]["minimum_normalized_recovery_lower_confidence_bound"])
    )

    autonomy = evidence.get("gate_e")
    gate_e = bool(
        isinstance(autonomy, Mapping)
        and bool(autonomy.get("both_scores_reported"))
        and _interval_upper(autonomy.get("protocol_failure_rate_interval"))
        <= float(gates["gate_e"]["maximum_protocol_failure_rate"])
    )
    results = {
        "gate_0": gate_0,
        "gate_a": gate_a,
        "gate_b": gate_b,
        "gate_c": gate_c,
        "gate_d": gate_d,
        "gate_e": gate_e,
    }
    return {
        "gates": results,
        "all_gates_pass": all(results.values()),
        "publication_ready": all(results.values()),
        "missing_or_failed_gates": [key for key, passed in results.items() if not passed],
    }


def _finite_values(values: Sequence[float]) -> list[float]:
    return [float(value) for value in values if math.isfinite(float(value))]


def _mean(values: Sequence[float]) -> float | None:
    return sum(values) / len(values) if values else None


def _binary_auroc(labels: Sequence[bool], scores: Sequence[float]) -> float:
    wins = 0.0
    total = 0
    for positive_index, positive in enumerate(labels):
        if not positive:
            continue
        for negative_index, negative in enumerate(labels):
            if negative:
                continue
            total += 1
            if scores[positive_index] > scores[negative_index]:
                wins += 1.0
            elif scores[positive_index] == scores[negative_index]:
                wins += 0.5
    if total == 0:
        raise ValueError("AUROC requires both classes")
    return wins / total


def _interval_lower(value: Any) -> float:
    return float(value[0]) if isinstance(value, Sequence) and len(value) == 2 else -math.inf


def _interval_upper(value: Any) -> float:
    return float(value[1]) if isinstance(value, Sequence) and len(value) == 2 else math.inf


__all__ = [
    "MECHANISM_ADAPTATION_ANALYSIS_VERSION",
    "AutonomyStatus",
    "GaussianCandidatePredictive",
    "GaussianMechanismOracle",
    "OutcomeLayers",
    "active_oracle_diagnosis",
    "build_paired_campaign_matrix",
    "campaign_autonomy_status",
    "categorical_entropy",
    "change_detection_summary",
    "conditional_changed_family_distribution",
    "declared_change_probability",
    "declared_distribution_update",
    "evaluate_protocol_gates",
    "feedback_effect_summary",
    "fixed_trajectory_decode",
    "identifiability_certificate",
    "js_divergence",
    "kl_divergence",
    "multiclass_brier",
    "normalized_distribution",
    "operation_aware_action_distance",
    "recovery_decomposition",
    "validate_mechanism_adaptation_protocol",
    "wilson_interval",
]
