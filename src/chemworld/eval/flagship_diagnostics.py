# ruff: noqa: RUF001
"""Exploratory flagship diagnostics for feedback use and mechanism adaptation."""

from __future__ import annotations

import copy
import hashlib
import itertools
import json
import math
from collections import defaultdict
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, Literal, Protocol

from chemworld.agents.base import Agent, HistoryRecord
from chemworld.agents.interaction import AgentDecisionContext, InteractionCapabilities
from chemworld.agents.task_recipes import task_recipe_event_count
from chemworld.eval.artifact_paths import repository_relative_reference
from chemworld.eval.runner import run_agent
from chemworld.tasks import get_task

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_PROTOCOL_PATH = (
    ROOT / "configs/benchmark/flagship_mechanism_diagnostics_v0.1.1.json"
)
DIAGNOSTIC_REPORT_VERSION = "chemworld-flagship-mechanism-diagnostics-0.1.1"

FeedbackCondition = Literal[
    "true_feedback",
    "permuted_feedback",
    "delayed_feedback",
    "critical_measurement_deleted",
]


class PublicViewAgent(Protocol):
    def act_with_public_view(
        self,
        context: AgentDecisionContext,
        public_view: dict[str, Any],
    ) -> dict[str, Any]: ...


@dataclass(frozen=True)
class FeedbackOutcomePacket:
    instrument: str
    experiment_index: int
    observation: dict[str, float | None]
    reward: float
    info: dict[str, Any]


@dataclass(frozen=True)
class FeedbackViewPacket:
    instrument: str
    experiment_index: int
    context: AgentDecisionContext
    public_view: dict[str, Any]


class _ContinuingAgentBase:
    """Preserve agent memory across two environment instances."""

    def __init__(self, delegate: Agent, *, method_id: str) -> None:
        self.delegate = delegate
        self.name = method_id
        self.method_id = method_id
        self._initialized = False
        self._phase = "iid"
        self._experiment_offset = 0
        self._operation_offset = 0
        self._usage_baseline: dict[str, Any] = {}
        self._per_experiment_action_limit: int | None = None
        self._experiment_action_count = 0
        self._pending_guardrail_audit: dict[str, Any] | None = None
        self._pending_guardrail_trace: list[dict[str, Any]] | None = None
        self.lifecycle_guardrail_log: list[dict[str, Any]] = []

    def configure_lifecycle_guardrail(self, per_experiment_action_limit: int) -> None:
        if per_experiment_action_limit < 2:
            raise ValueError("per_experiment_action_limit must be at least two")
        self._per_experiment_action_limit = int(per_experiment_action_limit)

    def begin_phase(
        self,
        phase: Literal["iid", "shifted"],
        *,
        experiment_offset: int,
        operation_offset: int,
    ) -> None:
        self._phase = phase
        self._experiment_offset = int(experiment_offset)
        self._operation_offset = int(operation_offset)
        self._experiment_action_count = 0
        self._pending_guardrail_audit = None
        self._pending_guardrail_trace = None

    def reset(self, task_info: dict[str, Any], seed: int) -> None:
        if not self._initialized:
            self.delegate.reset(task_info, seed)
            self._initialized = True
        else:
            # Preserve learned state and public experiment memory while updating
            # only the current task contract reference used by official agents.
            if hasattr(self.delegate, "task_info"):
                self.delegate.task_info = task_info
        usage_factory = getattr(self.delegate, "method_resource_usage", None)
        self._usage_baseline = copy.deepcopy(usage_factory()) if callable(usage_factory) else {}

    def update(
        self,
        action: dict[str, Any],
        observation: dict[str, float | None],
        reward: float,
        info: dict[str, Any],
    ) -> None:
        self.delegate.update(action, observation, reward, info)
        self._experiment_action_count += 1
        if bool(info.get("experiment_ended")):
            self._experiment_action_count = 0

    def act(self, history: list[HistoryRecord]) -> dict[str, Any]:
        del history
        raise RuntimeError("this diagnostic adapter requires a specialized act method")

    def manifest(self) -> dict[str, Any]:
        payload = dict(self.delegate.manifest())
        payload.update(
            {
                "diagnostic_adapter": "two_phase_memory_preserving",
                "diagnostic_method_id": self.method_id,
                "diagnostic_phase": self._phase,
                "environment_instance_reset_between_phases": True,
                "agent_memory_reset_between_phases": False,
                "benchmark_claim_allowed": False,
                "diagnostic_per_experiment_action_limit": (self._per_experiment_action_limit),
                "lifecycle_guardrail": (
                    "force terminate and final_assay only in the final two per-experiment "
                    "action slots"
                ),
            }
        )
        return payload

    def method_resource_usage(self) -> dict[str, Any]:
        usage_factory = getattr(self.delegate, "method_resource_usage", None)
        if not callable(usage_factory):
            return {}
        current = copy.deepcopy(usage_factory())
        if not current.get("model_call_count") and not current.get("input_token_count"):
            return current
        for key in (
            "model_call_count",
            "input_token_count",
            "output_token_count",
            "monetary_cost_usd",
            "cpu_time_s",
            "gpu_time_s",
        ):
            if key in current:
                current[key] = max(
                    float(current[key]) - float(self._usage_baseline.get(key, 0.0)),
                    0.0,
                )
                if key not in {
                    "monetary_cost_usd",
                    "cpu_time_s",
                    "gpu_time_s",
                }:
                    current[key] = int(current[key])
        return current

    def interaction_capabilities(self) -> InteractionCapabilities:
        factory = getattr(self.delegate, "interaction_capabilities", None)
        return factory() if callable(factory) else InteractionCapabilities()

    def decision_audit(self) -> dict[str, Any] | None:
        if self._pending_guardrail_audit is not None:
            return copy.deepcopy(self._pending_guardrail_audit)
        factory = getattr(self.delegate, "decision_audit", None)
        return factory() if callable(factory) else None

    def agent_trace(self) -> list[dict[str, Any]]:
        if self._pending_guardrail_trace is not None:
            trace = copy.deepcopy(self._pending_guardrail_trace)
            self._pending_guardrail_trace = None
            return trace
        factory = getattr(self.delegate, "agent_trace", None)
        trace = factory() if callable(factory) else []
        return [dict(item) for item in trace]

    def _guardrail_action(
        self,
        context: AgentDecisionContext,
    ) -> dict[str, Any] | None:
        self._pending_guardrail_audit = None
        self._pending_guardrail_trace = None
        limit = self._per_experiment_action_limit
        if limit is None:
            return None
        action: dict[str, Any] | None = None
        reason = ""
        previous_action = getattr(self, "_previous_action", None)
        closeout_ready = context.decision_stage == "experiment_closeout" or (
            isinstance(previous_action, Mapping)
            and previous_action.get("operation") == "terminate"
            and bool(getattr(self, "_previous_action_committed", False))
        )
        if closeout_ready and self._experiment_action_count >= limit - 2:
            action = {"operation": "measure", "instrument": "final_assay"}
            reason = "final_assay_reserved_slot"
        elif self._experiment_action_count >= limit - 2:
            action = {"operation": "terminate"}
            reason = "terminate_reserved_slot"
        if action is None:
            return None
        event = {
            "phase": self._phase,
            "experiment_index": int(context.campaign_state.get("experiment_index", 0))
            + self._experiment_offset,
            "actions_used_before_override": self._experiment_action_count,
            "per_experiment_action_limit": limit,
            "decision_stage": context.decision_stage,
            "selected_action": copy.deepcopy(action),
            "reason": reason,
        }
        self.lifecycle_guardrail_log.append(event)
        self._pending_guardrail_audit = {
            "action": copy.deepcopy(action),
            "evidence": [
                "The public per-experiment action limit reached its reserved closeout slots."
            ],
            "hypothesis": "Lifecycle closeout is required for a scoreable experiment.",
            "uncertainty": None,
            "rationale": (
                "The protocol-reserved closeout action replaces an optional model decision."
            ),
            "adaptation_source": "validator",
            "spectrum_interpretation": "",
            "request_historical_spectrum_id": None,
            "status": "provided",
        }
        self._pending_guardrail_trace = [
            {
                "status": "lifecycle_guardrail",
                "action": copy.deepcopy(action),
                "reason": reason,
                "per_experiment_action_limit": limit,
                "actions_used_before_override": self._experiment_action_count,
                "private_reasoning_retained": False,
            }
        ]
        return action

    def consume_historical_spectrum_request(self) -> str | None:
        factory = getattr(self.delegate, "consume_historical_spectrum_request", None)
        return factory() if callable(factory) else None

    def full_method_resource_usage(self) -> dict[str, Any]:
        factory = getattr(self.delegate, "method_resource_usage", None)
        return copy.deepcopy(factory()) if callable(factory) else {}

    def provider_receipts(self) -> list[dict[str, Any]]:
        factory = getattr(self.delegate, "provider_receipts", None)
        receipts = factory() if callable(factory) else []
        return [dict(item) for item in receipts if isinstance(item, Mapping)]


class ContinuingHistoryAgent(_ContinuingAgentBase):
    """Memory-preserving adapter for recipe/history agents."""

    def act(self, history: list[HistoryRecord]) -> dict[str, Any]:
        return self.delegate.act(history)


class ContinuingPublicViewAgent(_ContinuingAgentBase):
    """Memory-preserving adapter with optional causal feedback intervention."""

    def __init__(
        self,
        delegate: Agent,
        *,
        method_id: str,
        feedback_condition: FeedbackCondition = "true_feedback",
        critical_instrument: str,
    ) -> None:
        super().__init__(delegate, method_id=method_id)
        if feedback_condition not in {
            "true_feedback",
            "permuted_feedback",
            "delayed_feedback",
            "critical_measurement_deleted",
        }:
            raise ValueError(f"unsupported feedback condition: {feedback_condition}")
        self.feedback_condition = feedback_condition
        self.critical_instrument = critical_instrument
        self._previous_action: dict[str, Any] | None = None
        self._iid_outcomes: dict[str, list[FeedbackOutcomePacket]] = defaultdict(list)
        self._iid_views: dict[str, list[FeedbackViewPacket]] = defaultdict(list)
        self._shifted_outcomes: dict[str, list[FeedbackOutcomePacket]] = defaultdict(list)
        self._shifted_views: dict[str, list[FeedbackViewPacket]] = defaultdict(list)
        self._outcome_cursors: dict[str, int] = defaultdict(int)
        self._view_cursors: dict[str, int] = defaultdict(int)
        self.feedback_intervention_log: list[dict[str, Any]] = []
        self._previous_action_committed = False

    def act_with_public_view(
        self,
        context: AgentDecisionContext,
        public_view: dict[str, Any],
    ) -> dict[str, Any]:
        guarded = self._guardrail_action(context)
        if guarded is not None:
            return guarded
        method = getattr(self.delegate, "act_with_public_view", None)
        if not callable(method):
            raise TypeError("delegate does not implement act_with_public_view")
        current_context = self._offset_context(context)
        current_view = copy.deepcopy(public_view)
        instrument = _measurement_instrument(self._previous_action)
        if self._phase == "iid":
            if instrument is not None:
                self._iid_views[instrument].append(
                    FeedbackViewPacket(
                        instrument=instrument,
                        experiment_index=max(
                            int(context.campaign_state.get("experiment_index", 0)) - 1,
                            0,
                        ),
                        context=current_context,
                        public_view=current_view,
                    )
                )
        elif instrument is not None:
            donor = self._view_donor(instrument)
            transformed = self._transform_view_feedback(
                current_context,
                current_view,
                instrument=instrument,
                donor=donor,
            )
            current_context, current_view = transformed
            self._shifted_views[instrument].append(
                FeedbackViewPacket(
                    instrument=instrument,
                    experiment_index=int(context.campaign_state.get("experiment_index", 0)),
                    context=self._offset_context(context),
                    public_view=copy.deepcopy(public_view),
                )
            )
        return method(current_context, current_view)

    def update(
        self,
        action: dict[str, Any],
        observation: dict[str, float | None],
        reward: float,
        info: dict[str, Any],
    ) -> None:
        instrument = _measurement_instrument(action)
        packet: FeedbackOutcomePacket | None = None
        if instrument is not None:
            packet = FeedbackOutcomePacket(
                instrument=instrument,
                experiment_index=int(info.get("experiment_index", 0)),
                observation=copy.deepcopy(observation),
                reward=float(reward),
                info=copy.deepcopy(info),
            )
        delivered_observation = observation
        delivered_reward = reward
        delivered_info = info
        if packet is not None and self._phase == "iid":
            self._iid_outcomes[packet.instrument].append(packet)
        elif packet is not None and self._phase == "shifted":
            donor = self._outcome_donor(packet.instrument)
            (
                delivered_observation,
                delivered_reward,
                delivered_info,
            ) = self._transform_outcome_feedback(packet, donor=donor)
            self._shifted_outcomes[packet.instrument].append(packet)
        self.delegate.update(
            action,
            delivered_observation,
            float(delivered_reward),
            delivered_info,
        )
        self._previous_action = dict(action)
        self._previous_action_committed = info.get("transaction_status") == "committed"
        self._experiment_action_count += 1
        if bool(info.get("experiment_ended")):
            self._experiment_action_count = 0

    def manifest(self) -> dict[str, Any]:
        payload = super().manifest()
        payload.update(
            {
                "feedback_condition": self.feedback_condition,
                "critical_instrument": self.critical_instrument,
                "feedback_intervention_scope": "agent-visible evidence only",
                "environment_state_and_scoring_intervened": False,
            }
        )
        return payload

    def _offset_context(self, context: AgentDecisionContext) -> AgentDecisionContext:
        campaign = copy.deepcopy(context.campaign_state)
        campaign["diagnostic_actions_used_current_experiment"] = self._experiment_action_count
        campaign["diagnostic_per_experiment_action_limit"] = self._per_experiment_action_limit
        for key in ("experiment_index", "final_assay_count"):
            if isinstance(campaign.get(key), int) and not isinstance(campaign.get(key), bool):
                campaign[key] = int(campaign[key]) + self._experiment_offset
        if isinstance(campaign.get("operation_count"), int) and not isinstance(
            campaign.get("operation_count"), bool
        ):
            campaign["operation_count"] = int(campaign["operation_count"]) + self._operation_offset
        return replace(context, campaign_state=campaign)

    def _view_donor(self, instrument: str) -> FeedbackViewPacket | None:
        condition = self.feedback_condition
        if condition == "true_feedback":
            return None
        if condition == "critical_measurement_deleted":
            return None
        if condition == "delayed_feedback":
            candidates = self._shifted_views[instrument]
            return candidates[-1] if candidates else None
        candidates = self._iid_views[instrument]
        if not candidates:
            return None
        cursor = self._view_cursors[instrument]
        self._view_cursors[instrument] += 1
        return candidates[(cursor + 1) % len(candidates)]

    def _outcome_donor(self, instrument: str) -> FeedbackOutcomePacket | None:
        condition = self.feedback_condition
        if condition == "true_feedback":
            return None
        if condition == "critical_measurement_deleted":
            return None
        if condition == "delayed_feedback":
            candidates = self._shifted_outcomes[instrument]
            return candidates[-1] if candidates else None
        candidates = self._iid_outcomes[instrument]
        if not candidates:
            return None
        cursor = self._outcome_cursors[instrument]
        self._outcome_cursors[instrument] += 1
        return candidates[(cursor + 1) % len(candidates)]

    def _transform_view_feedback(
        self,
        context: AgentDecisionContext,
        public_view: dict[str, Any],
        *,
        instrument: str,
        donor: FeedbackViewPacket | None,
    ) -> tuple[AgentDecisionContext, dict[str, Any]]:
        condition = self.feedback_condition
        if condition == "true_feedback" or (
            condition == "critical_measurement_deleted" and instrument != self.critical_instrument
        ):
            return context, public_view
        if donor is None:
            transformed_context = replace(
                context,
                visible_metrics={},
                latest_spectra={"has_spectral_packet": False},
                uncertainty={},
            )
            transformed_view = _mask_public_feedback(public_view)
            source = "masked_no_eligible_donor"
            donor_experiment = None
        else:
            transformed_context = replace(
                context,
                visible_metrics=copy.deepcopy(donor.context.visible_metrics),
                latest_spectra=copy.deepcopy(donor.context.latest_spectra),
                uncertainty=copy.deepcopy(donor.context.uncertainty),
            )
            transformed_view = _replace_public_feedback(
                public_view,
                donor.public_view,
            )
            source = "iid_permuted" if condition == "permuted_feedback" else "one_event_delayed"
            donor_experiment = donor.experiment_index
        self.feedback_intervention_log.append(
            {
                "surface": "decision_view",
                "condition": condition,
                "instrument": instrument,
                "source": source,
                "donor_experiment_index": donor_experiment,
            }
        )
        return transformed_context, transformed_view

    def _transform_outcome_feedback(
        self,
        packet: FeedbackOutcomePacket,
        *,
        donor: FeedbackOutcomePacket | None,
    ) -> tuple[dict[str, float | None], float, dict[str, Any]]:
        condition = self.feedback_condition
        if condition == "true_feedback" or (
            condition == "critical_measurement_deleted"
            and packet.instrument != self.critical_instrument
        ):
            return packet.observation, packet.reward, packet.info
        if donor is None:
            observation: dict[str, float | None] = {
                key: None if value is not None else value
                for key, value in packet.observation.items()
            }
            info = copy.deepcopy(packet.info)
            info["observed_keys"] = []
            info["observed_mask"] = dict.fromkeys(info.get("observed_mask", {}), False)
            info["leaderboard_score"] = None
            reward = 0.0
            source = "masked_no_eligible_donor"
            donor_experiment = None
        else:
            observation = copy.deepcopy(donor.observation)
            info = _replace_outcome_feedback(packet.info, donor.info)
            reward = donor.reward
            source = "iid_permuted" if condition == "permuted_feedback" else "one_event_delayed"
            donor_experiment = donor.experiment_index
        self.feedback_intervention_log.append(
            {
                "surface": "agent_update",
                "condition": condition,
                "instrument": packet.instrument,
                "source": source,
                "donor_experiment_index": donor_experiment,
                "true_environment_score_retained_for_evaluation": packet.info.get(
                    "leaderboard_score"
                ),
            }
        )
        return observation, reward, info


def load_flagship_diagnostic_protocol(
    path: str | Path = DEFAULT_PROTOCOL_PATH,
) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("flagship diagnostic protocol must be a JSON object")
    if payload.get("schema_version") != DIAGNOSTIC_REPORT_VERSION:
        raise ValueError("unsupported flagship diagnostic protocol schema")
    return payload


def run_two_phase_campaign(
    *,
    task_id: str,
    adapter: _ContinuingAgentBase,
    seed: int,
    pre_change_experiments: int,
    post_change_experiments: int,
    shifted_interventions: Sequence[Mapping[str, Any]],
    output_root: str | Path,
    campaign_id: str,
    closeout_headroom_per_experiment: int = 6,
) -> dict[str, Any]:
    """Run IID and shifted phases while preserving only the agent's memory."""

    if closeout_headroom_per_experiment < 0:
        raise ValueError("closeout_headroom_per_experiment must be non-negative")
    task = get_task(task_id)
    per_experiment = task_recipe_event_count(task.to_dict())
    root = Path(output_root)
    root.mkdir(parents=True, exist_ok=True)
    iid_path = root / f"{campaign_id}--iid.jsonl"
    shifted_path = root / f"{campaign_id}--shifted.jsonl"
    per_experiment_limit = per_experiment + closeout_headroom_per_experiment
    iid_limit = per_experiment_limit * pre_change_experiments
    shifted_limit = per_experiment_limit * post_change_experiments
    adapter.configure_lifecycle_guardrail(per_experiment_limit)
    adapter.begin_phase("iid", experiment_offset=0, operation_offset=0)
    iid_history = run_agent(
        env_id=task.env_id,
        agent=adapter,
        world_split=task.world_split,
        budget=task.budget,
        objective=task.objective,
        seed=seed,
        task_id=task.task_id,
        output_path=iid_path,
        budget_override=iid_limit,
        episode_mode_override="campaign",
        method_resource_limits=_diagnostic_resource_limits(
            iid_limit,
            pre_change_experiments,
        ),
        evaluation_policy="vnext_risk_cost",
    )
    iid_complete = sum(record.event_type == "experiment_end" for record in iid_history)
    adapter.begin_phase(
        "shifted",
        experiment_offset=iid_complete,
        operation_offset=len(iid_history),
    )
    shifted_history = run_agent(
        env_id=task.env_id,
        agent=adapter,
        world_split=task.world_split,
        budget=task.budget,
        objective=task.objective,
        seed=seed,
        task_id=task.task_id,
        output_path=shifted_path,
        budget_override=shifted_limit,
        episode_mode_override="campaign",
        method_resource_limits=_diagnostic_resource_limits(
            shifted_limit,
            post_change_experiments,
        ),
        evaluation_policy="vnext_risk_cost",
        world_interventions=tuple(dict(item) for item in shifted_interventions),
    )
    return {
        "campaign_id": campaign_id,
        "task_id": task_id,
        "method_id": adapter.method_id,
        "seed": seed,
        "iid": summarize_phase(iid_history, path=iid_path),
        "shifted": summarize_phase(shifted_history, path=shifted_path),
        "shifted_interventions": [dict(item) for item in shifted_interventions],
        "agent_memory_reset_between_phases": False,
        "environment_instance_reset_between_phases": True,
        "recipe_event_count": per_experiment,
        "closeout_headroom_per_experiment": closeout_headroom_per_experiment,
        "phase_operation_limit_per_experiment": per_experiment_limit,
        "full_method_resources": adapter.full_method_resource_usage(),
        "provider_receipts": adapter.provider_receipts(),
        "feedback_intervention_log": list(getattr(adapter, "feedback_intervention_log", ())),
        "lifecycle_guardrail_log": list(adapter.lifecycle_guardrail_log),
    }


def summarize_phase(
    history: Sequence[HistoryRecord],
    *,
    path: Path,
) -> dict[str, Any]:
    terminal = [record for record in history if record.event_type == "experiment_end"]
    scores = [
        float(record.info["leaderboard_score"])
        for record in terminal
        if record.info.get("leaderboard_score") is not None
    ]
    try:
        trajectory_reference = repository_relative_reference(path)
        trajectory_reference_kind = "repository_relative"
    except ValueError:
        trajectory_reference = str(path)
        trajectory_reference_kind = "external_ephemeral"
    return {
        "trajectory_path": trajectory_reference,
        "trajectory_reference_kind": trajectory_reference_kind,
        "trajectory_sha256": _file_sha256(path),
        "operation_count": len(history),
        "complete_experiment_count": len(terminal),
        "scores": scores,
        "mean_score": sum(scores) / len(scores) if scores else None,
        "best_score": max(scores) if scores else None,
        "failure_count": sum(
            record.info.get("transaction_status") != "committed" for record in history
        ),
        "operation_counts": _counts(
            str(record.action.get("operation") or "unknown") for record in history
        ),
    }


def _diagnostic_resource_limits(
    operation_limit: int,
    complete_experiment_limit: int,
) -> dict[str, Any]:
    """Bound live calls generously while retaining exact phase accounting."""

    return {
        "operation_limit": operation_limit,
        "complete_experiment_limit": complete_experiment_limit,
        "wall_time_limit_s": float(operation_limit * 150),
        "model_call_limit": operation_limit * 2,
        "input_token_limit": operation_limit * 12_000,
        "output_token_limit": operation_limit * 1_500,
        "monetary_cost_limit_usd": operation_limit * 0.01,
        "training_environment_step_limit": 0,
        "checkpoint_complete_experiments": tuple(range(1, complete_experiment_limit + 1)),
    }


def build_flagship_diagnostic_report(
    protocol: Mapping[str, Any],
    campaigns: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Derive the four requested diagnostics from completed campaign artifacts."""

    threshold = float(protocol["analysis"]["change_detection_threshold"])
    recovery_fraction = float(protocol["analysis"]["recovery_fraction_of_iid_best"])
    analyzed: list[dict[str, Any]] = []
    for raw in campaigns:
        campaign = copy.deepcopy(dict(raw))
        truth_id = str(campaign.get("shifted_truth_id") or "")
        diagnostic = (
            analyze_deepseek_campaign(
                campaign,
                shifted_truth_id=truth_id,
                change_detection_threshold=threshold,
                recovery_fraction=recovery_fraction,
            )
            if campaign.get("method_id") == "deepseek_v4_flash"
            else None
        )
        campaign["deepseek_diagnostic"] = diagnostic
        analyzed.append(campaign)

    ranking = _ranking_analysis(
        [item for item in analyzed if item.get("experiment_id") == "ranking_shift"]
    )
    feedback = _feedback_analysis(
        [item for item in analyzed if item.get("experiment_id") == "feedback_ablation"]
    )
    counterfactual = _counterfactual_analysis(
        [item for item in analyzed if item.get("experiment_id") == "material_law_swap"]
    )
    outcome_understanding = _outcome_understanding_analysis(analyzed)
    coverage = _coverage_audit(protocol, analyzed)
    completed = bool(coverage["complete"])
    return {
        "schema_version": DIAGNOSTIC_REPORT_VERSION,
        "protocol_id": protocol.get("protocol_id"),
        "protocol_sha256": _canonical_sha256(protocol),
        "status": "exploratory_complete" if completed else "exploratory_incomplete",
        "candidate_diagnostic_only": True,
        "benchmark_claim_allowed": False,
        "publication_ready": False,
        "completion_audit": coverage,
        "model": copy.deepcopy(protocol.get("deepseek")),
        "experiment_1_ranking_shift": ranking,
        "experiment_2_feedback_ablation": feedback,
        "experiment_3_material_law_counterfactual": counterfactual,
        "experiment_4_outcome_understanding": outcome_understanding,
        "campaigns": analyzed,
        "resource_summary": _resource_summary(analyzed),
        "limitations": [
            "This is a one-seed exploratory diagnostic, not a formal method ranking.",
            (
                "DeepSeek responses are provider-sampled; feedback conditions are not "
                "deterministic replay clones."
            ),
            (
                "PPO was excluded before evaluation because its legacy failed-smoke "
                "checkpoint is incompatible with the current observation contract."
            ),
            (
                "The UCB baseline explores optimistic performance, not a dedicated "
                "Bayesian information-gain objective."
            ),
            "Two post-change experiments provide only a right-censored recovery diagnostic.",
            (
                "Material-law swaps are benchmark interventions, not claims about real "
                "named chemical materials."
            ),
            (
                "A public lifecycle guardrail forces terminate and final_assay only in "
                "the final two per-experiment action slots; those forced closeout actions "
                "are not unconstrained agent decisions."
            ),
        ],
    }


def render_flagship_diagnostic_markdown(report: Mapping[str, Any]) -> str:
    """Render the exploratory diagnostic report as a self-contained Chinese brief."""

    ranking = report.get("experiment_1_ranking_shift", {})
    feedback = report.get("experiment_2_feedback_ablation", {})
    counterfactual = report.get("experiment_3_material_law_counterfactual", {})
    understanding = report.get("experiment_4_outcome_understanding", {})
    resources = report.get("resource_summary", {})
    coverage = report.get("completion_audit", {})
    type_counts = json.dumps(
        understanding.get("type_counts", {}),
        ensure_ascii=False,
        sort_keys=True,
    )
    deepseek_rank: Mapping[str, Any] = next(
        (row for row in ranking.get("rows", []) if row.get("method_id") == "deepseek_v4_flash"),
        {},
    )
    true_diagnostics = [
        task.get("diagnostics", {}).get("true_feedback", {})
        for task in feedback.get("tasks", {}).values()
    ]
    true_mechanism_correct = sum(
        bool(item.get("mechanism_identified")) for item in true_diagnostics
    )
    true_recovered = sum(item.get("recovery_experiment") is not None for item in true_diagnostics)
    counterfactual_rows = counterfactual.get("rows", [])
    counterfactual_correct = sum(
        bool(item.get("mechanism_identified")) for item in counterfactual_rows
    )
    information = understanding.get("aggregate_information_value", {})
    lines = [
        "# DeepSeek 旗舰任务机制诊断（探索性）",
        "",
        f"- 状态：`{report.get('status')}`",
        f"- 协议：`{report.get('protocol_id')}`",
        f"- 协议 SHA-256：`{report.get('protocol_sha256')}`",
        "- 定位：Agent 能力测试环境；不训练、不微调、不更新模型权重。",
        "- 声明边界：单种子探索性诊断，不构成正式排行榜或可发表的确认性结论。",
        "",
        "## 完整性审计",
        "",
        f"- 覆盖是否完整：`{coverage.get('complete')}`",
        (
            f"- 预期单元：{coverage.get('expected_cell_count')}；"
            f"观测单元：{coverage.get('observed_cell_count')}"
        ),
        (
            f"- 缺失单元：{len(coverage.get('missing_cells', []))}；"
            f"未完成阶段：{len(coverage.get('incomplete_phases', []))}"
        ),
        "",
        "## 核心发现",
        "",
        (
            f"- 排名迁移很弱：IID/切换排名 Spearman = "
            f"{_fmt(ranking.get('spearman_rank_correlation'))}，"
            f"共 {ranking.get('rank_inversion_count')} 对反转。DeepSeek 的 IID/适应排名为 "
            f"{deepseek_rank.get('iid_rank')}/{deepseek_rank.get('adaptation_rank')}。"
        ),
        (
            f"- 没有观察到正的证据依赖：平均 `J_true - J_permuted` = "
            f"{_fmt(feedback.get('mean_evidence_reliance'))}。负值不能证明错误反馈有益，"
            "但说明本轮没有稳定的真实反馈优势。"
        ),
        (
            f"- 真反馈下机制识别 {true_mechanism_correct}/{len(true_diagnostics)}，"
            f"在两个切换实验内恢复 {true_recovered}/{len(true_diagnostics)}；"
            "模型虽报告变化概率上升，最终仍倾向 no_change。"
        ),
        (
            f"- 名称—规律反事实识别 {counterfactual_correct}/"
            f"{len(counterfactual_rows)}；两项最佳得分都提高，但真值概率都很低，"
            "属于结果与机制理解分离。"
        ),
        (
            f"- 信息价值明显高估：加权声明值 "
            f"{_fmt(information.get('mean_expected_information_gain'))}，"
            f"下一步实际熵下降 {_fmt(information.get('mean_realized_entropy_reduction'))}，"
            f"绝对校准误差 {_fmt(information.get('mean_absolute_calibration_error'))}。"
        ),
        f"- 独立 campaign 分类：`{type_counts}`。",
        "",
        "## 实验一：IID 排名与未见机制切换排名",
        "",
        (
            "该实验检验静态任务得分能否代表机制变化后的适应能力。"
            f"Spearman 排名相关为 {_fmt(ranking.get('spearman_rank_correlation'))}，"
            f"排名反转 {ranking.get('rank_inversion_count')} 对。"
        ),
        "",
        _md_table(
            ["方法", "IID", "切换后", "IID 排名", "适应排名", "排名变化"],
            [
                [
                    row.get("method_id"),
                    _fmt(row.get("iid_performance")),
                    _fmt(row.get("adaptation_performance")),
                    row.get("iid_rank"),
                    row.get("adaptation_rank"),
                    row.get("rank_change"),
                ]
                for row in ranking.get("rows", [])
            ],
        ),
        "",
        "解释：这里比较的是同一公开种子、两个旗舰任务上的描述性均值；它能发现排序错位，但不能估计跨种子显著性。",
        "",
        "## 实验二：反馈置换与证据依赖",
        "",
        (
            "环境状态和真实评分始终不变，只修改 Agent 可见的测量反馈。"
            "证据依赖定义为 `J_true - J_permuted`；正值表示真实反馈对结果有帮助。"
        ),
        "",
        _md_table(
            ["任务", "真实", "跨实验置换", "延迟", "关键测量删除", "证据依赖"],
            [
                [
                    task_id,
                    _fmt(task.get("condition_scores", {}).get("true_feedback")),
                    _fmt(task.get("condition_scores", {}).get("permuted_feedback")),
                    _fmt(task.get("condition_scores", {}).get("delayed_feedback")),
                    _fmt(task.get("condition_scores", {}).get("critical_measurement_deleted")),
                    _fmt(task.get("evidence_reliance")),
                ]
                for task_id, task in feedback.get("tasks", {}).items()
            ],
        ),
        "",
        f"跨任务平均证据依赖：{_fmt(feedback.get('mean_evidence_reliance'))}。由于各条件是独立采样调用而非确定性轨迹克隆，差值同时包含模型采样噪声。",
        "",
        "## 实验三：名称—规律反事实",
        "",
        "材料名称、说明、动作编码、成本与风险保持不变，仅交换隐藏材料效应行；因此该实验测试模型是否依赖观测到的物理化学反馈，而不是记住名称先验。",
        "",
        _md_table(
            ["任务", "IID 最佳", "反事实最佳", "得分变化", "机制识别", "真值概率"],
            [
                [
                    row.get("task_id"),
                    _fmt(row.get("iid_best_score")),
                    _fmt(row.get("counterfactual_best_score")),
                    _fmt(row.get("score_change")),
                    row.get("mechanism_identified"),
                    _fmt(row.get("truth_probability")),
                ]
                for row in counterfactual.get("rows", [])
            ],
        ),
        "",
        "## 实验四：结果与机制理解解耦",
        "",
        (
            "分类规则：相对结果达到本 campaign IID 最佳值的 90% 且正确识别为 "
            "genuine_experimental；"
            "高结果但未识别为 accidental_optimizer；"
            "低结果但正确识别为 theoretical_explainer；"
            "两者皆低为 joint_failure。"
        ),
        "",
        f"类型计数：`{type_counts}`",
        "",
        _md_table(
            [
                "实验",
                "任务",
                "反馈",
                "最终目标",
                "机制识别",
                "真值概率",
                "变化检测",
                "Brier",
                "恢复实验",
                "分类",
            ],
            [
                [
                    row.get("experiment_id"),
                    row.get("task_id"),
                    row.get("feedback_condition"),
                    _fmt(row.get("final_objective")),
                    row.get("mechanism_identified"),
                    _fmt(row.get("truth_probability")),
                    row.get("change_detected"),
                    _fmt(row.get("multiclass_brier_score")),
                    row.get("recovery_experiment"),
                    row.get("type"),
                ]
                for row in understanding.get("rows", [])
            ],
        ),
        "",
        "信息价值校准使用模型声明的预期信息增益与下一步归一化熵下降比较；它衡量公开概率报告的一致性，不等同于访问或评判私有思维链。",
        (
            "这里的高/低结果是相对各 campaign 的 IID 基线定义，不代表绝对分数"
            "高/低；因此绝对分数很低的轨迹仍可能被标为 accidental_optimizer。"
        ),
        "",
        "## 综合判断",
        "",
        (
            "这组结果支持 ChemWorld 作为“反馈驱动的物理化学 world-model Agent 评测环境”"
            "的故事：静态优化排名不能代表机制切换后的表现，任务还能把变化检测、机制识别、"
            "结果恢复和信息价值校准彼此拆开。"
        ),
        "",
        (
            "它不支持把当前 DeepSeek 控制器称为已具备可靠机制发现能力。真反馈下两个机制"
            "切换都未被正确识别，材料反事实也未识别；多个相对高结果被归为 accidental_optimizer。"
            "唯一 genuine_experimental 出现在电化学延迟反馈条件，属于单种子、采样型孤立结果。"
        ),
        "",
        (
            "负 Evidence Reliance 与严重的信息价值高估表明：当前控制器尚未展示稳定、可校准的"
            "反馈使用。下一步确认性研究应冻结协议后增加种子、使用确定性或配对重放设计，并为"
            "信息增益策略加入真正的专用基线。"
        ),
        "",
        "## 资源与可复现性",
        "",
        f"- DeepSeek 独立活动 campaign：{resources.get('deepseek_campaign_count')}",
        f"- 模型调用：{resources.get('model_call_count')}",
        f"- 计费响应后决策失败：{resources.get('provider_failure_count')}",
        f"- Provider 重试：{resources.get('retry_count')}",
        f"- 生命周期收尾覆盖：{resources.get('lifecycle_guardrail_override_count')}",
        (
            f"- 输入 / 输出 token：{resources.get('input_token_count')} / "
            f"{resources.get('output_token_count')}"
        ),
        f"- 估算费用（USD）：{_fmt(resources.get('monetary_cost_usd'), digits=6)}",
        "- 私有推理保留：否；报告只保留公开决策、概率诊断、请求回执和环境轨迹。",
        "",
        "## 限制",
        "",
    ]
    lines.extend(
        (
            "- 仅使用一个公开种子，属于探索性诊断，不是正式方法排名。",
            "- DeepSeek 响应由 provider 采样；不同反馈条件不是确定性轨迹克隆。",
            "- PPO 旧 failed-smoke checkpoint 与当前 observation contract 不兼容，已在评估前排除。",
            "- UCB 基线是乐观探索策略，不是专用 Bayesian information-gain 基线。",
            "- 切换后只有两个实验，恢复时间是右删失诊断，不能估计长期样本效率。",
            "- 材料规律交换是 benchmark 环境干预，不是对真实命名化学材料的断言。",
            "- 生命周期护栏只覆盖每实验最后两个动作槽；被强制收尾的动作不是 Agent 的自由决策。",
        )
    )
    return "\n".join(lines).rstrip() + "\n"


def _coverage_audit(
    protocol: Mapping[str, Any],
    campaigns: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    tasks = tuple(str(item) for item in protocol.get("tasks", {}))
    expected: set[str] = set()
    for task_id in tasks:
        for method_id in protocol.get("ranking_methods", []):
            expected.add(f"ranking_shift|{task_id}|{method_id}|true_feedback")
        for condition in protocol.get("feedback_conditions", []):
            expected.add(f"feedback_ablation|{task_id}|deepseek_v4_flash|{condition}")
        expected.add(f"material_law_swap|{task_id}|deepseek_v4_flash|true_feedback")
    observed_counts: dict[str, int] = defaultdict(int)
    incomplete_phases: list[dict[str, Any]] = []
    expected_iid = int(protocol.get("pre_change_experiments", 0))
    expected_shifted = int(protocol.get("post_change_experiments", 0))
    for campaign in campaigns:
        cell = "|".join(
            (
                str(campaign.get("experiment_id")),
                str(campaign.get("task_id")),
                str(campaign.get("method_id")),
                str(campaign.get("feedback_condition")),
            )
        )
        observed_counts[cell] += 1
        iid_count = int(campaign.get("iid", {}).get("complete_experiment_count", 0))
        shifted_count = int(campaign.get("shifted", {}).get("complete_experiment_count", 0))
        if iid_count != expected_iid or shifted_count != expected_shifted:
            incomplete_phases.append(
                {
                    "cell": cell,
                    "iid_complete": iid_count,
                    "iid_expected": expected_iid,
                    "shifted_complete": shifted_count,
                    "shifted_expected": expected_shifted,
                }
            )
    observed = set(observed_counts)
    duplicate_cells = sorted(cell for cell, count in observed_counts.items() if count != 1)
    missing = sorted(expected - observed)
    unexpected = sorted(observed - expected)
    complete = not (missing or unexpected or duplicate_cells or incomplete_phases)
    return {
        "complete": complete,
        "expected_cell_count": len(expected),
        "observed_cell_count": len(observed),
        "missing_cells": missing,
        "unexpected_cells": unexpected,
        "duplicate_cells": duplicate_cells,
        "incomplete_phases": incomplete_phases,
    }


def _fmt(value: Any, *, digits: int = 4) -> str:
    if value is None:
        return "NA"
    if isinstance(value, bool):
        return str(value)
    if isinstance(value, int | float):
        return f"{float(value):.{digits}f}"
    return str(value)


def _md_table(headers: Sequence[str], rows: Sequence[Sequence[Any]]) -> str:
    def cell(value: Any) -> str:
        return str(value).replace("|", "\\|").replace("\n", " ")

    rendered = ["| " + " | ".join(cell(item) for item in headers) + " |"]
    rendered.append("| " + " | ".join("---" for _ in headers) + " |")
    rendered.extend("| " + " | ".join(cell(item) for item in row) + " |" for row in rows)
    return "\n".join(rendered)


def analyze_deepseek_campaign(
    campaign: Mapping[str, Any],
    *,
    shifted_truth_id: str,
    change_detection_threshold: float,
    recovery_fraction: float,
) -> dict[str, Any] | None:
    iid_path = Path(str(campaign.get("iid", {}).get("trajectory_path", "")))
    shifted_path = Path(str(campaign.get("shifted", {}).get("trajectory_path", "")))
    if not iid_path.is_file() or not shifted_path.is_file():
        return None
    iid_trace = _diagnostic_trace(iid_path)
    shifted_trace = _diagnostic_trace(shifted_path)
    if not iid_trace or not shifted_trace:
        return None
    iid_final = iid_trace[-1]
    shifted_final = shifted_trace[-1]
    iid_best = campaign.get("iid", {}).get("best_score")
    shifted_scores = [float(value) for value in campaign.get("shifted", {}).get("scores", [])]
    recovery_target = float(iid_best) * recovery_fraction if iid_best is not None else None
    recovery_experiment = next(
        (
            index
            for index, score in enumerate(shifted_scores, start=1)
            if recovery_target is not None and score >= recovery_target
        ),
        None,
    )
    detection = next(
        (
            item
            for item in shifted_trace
            if float(item["change_probability"]) >= change_detection_threshold
        ),
        None,
    )
    final_belief = shifted_final["mechanism_belief"]
    truth_probability = float(final_belief.get(shifted_truth_id, 0.0))
    mechanism_identified = shifted_final["mechanism_prediction"] == shifted_truth_id
    outcome_high = bool(
        recovery_target is not None
        and campaign.get("shifted", {}).get("best_score") is not None
        and float(campaign["shifted"]["best_score"]) >= recovery_target
    )
    understanding_high = mechanism_identified and truth_probability >= 0.5
    return {
        "iid_final_prediction": iid_final["mechanism_prediction"],
        "iid_no_change_probability": float(iid_final["mechanism_belief"].get("no_change", 0.0)),
        "iid_max_change_probability": max(float(item["change_probability"]) for item in iid_trace),
        "shifted_truth_id": shifted_truth_id,
        "shifted_final_prediction": shifted_final["mechanism_prediction"],
        "shifted_truth_probability": truth_probability,
        "mechanism_identified": mechanism_identified,
        "multiclass_brier_score": _brier_score(final_belief, shifted_truth_id),
        "change_detected": detection is not None,
        "change_detection_operation": (
            int(detection["operation_index"]) if detection is not None else None
        ),
        "change_detection_experiment": (
            int(detection["experiment_index"]) + 1 if detection is not None else None
        ),
        "recovery_target": recovery_target,
        "recovery_experiment": recovery_experiment,
        "recovery_right_censored": recovery_experiment is None,
        "information_value": _information_value_summary(shifted_trace),
        "final_outcome_high": outcome_high,
        "mechanism_understanding_high": understanding_high,
        "outcome_understanding_type": _quadrant(outcome_high, understanding_high),
    }


def _diagnostic_trace(path: Path) -> list[dict[str, Any]]:
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]
    trace: list[dict[str, Any]] = []
    for index, row in enumerate(rows, start=1):
        raw_trace = row.get("agent_trace")
        decision = raw_trace[-1] if isinstance(raw_trace, list) and raw_trace else None
        if not isinstance(decision, dict):
            continue
        belief = decision.get("mechanism_belief")
        if not isinstance(belief, dict):
            continue
        try:
            normalized_belief = {str(key): float(value) for key, value in belief.items()}
            change_probability = float(decision["change_probability"])
            expected_information_gain = float(decision["expected_information_gain"])
        except (KeyError, TypeError, ValueError):
            continue
        trace.append(
            {
                "operation_index": index,
                "experiment_index": int(row.get("experiment_index", 0)),
                "operation": row.get("operation_type"),
                "instrument": row.get("instrument"),
                "mechanism_belief": normalized_belief,
                "mechanism_prediction": str(decision.get("mechanism_prediction")),
                "change_probability": change_probability,
                "expected_information_gain": expected_information_gain,
                "entropy": _normalized_entropy(normalized_belief),
            }
        )
    return trace


def _information_value_summary(trace: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    pairs: list[dict[str, Any]] = []
    for current, following in itertools.pairwise(trace):
        expected = float(current["expected_information_gain"])
        realized = max(float(current["entropy"]) - float(following["entropy"]), 0.0)
        pairs.append(
            {
                "operation_index": int(current["operation_index"]),
                "operation": current.get("operation"),
                "expected": expected,
                "realized_entropy_reduction": realized,
                "absolute_error": abs(expected - realized),
            }
        )
    return {
        "pair_count": len(pairs),
        "mean_expected_information_gain": _mean([float(item["expected"]) for item in pairs]),
        "mean_realized_entropy_reduction": _mean(
            [float(item["realized_entropy_reduction"]) for item in pairs]
        ),
        "mean_absolute_calibration_error": _mean([float(item["absolute_error"]) for item in pairs]),
        "top_expected_operations": sorted(
            pairs,
            key=lambda item: float(item["expected"]),
            reverse=True,
        )[:5],
    }


def _ranking_analysis(campaigns: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    by_method: dict[str, dict[str, list[float]]] = defaultdict(lambda: {"iid": [], "shifted": []})
    for campaign in campaigns:
        method = str(campaign.get("method_id"))
        for phase in ("iid", "shifted"):
            value = campaign.get(phase, {}).get("mean_score")
            if value is not None:
                by_method[method][phase].append(float(value))
    rows: list[dict[str, Any]] = [
        {
            "method_id": method,
            "iid_performance": _mean(values["iid"]),
            "adaptation_performance": _mean(values["shifted"]),
            "task_count": min(len(values["iid"]), len(values["shifted"])),
        }
        for method, values in sorted(by_method.items())
        if values["iid"] and values["shifted"]
    ]
    iid_order = sorted(rows, key=lambda item: float(item["iid_performance"]), reverse=True)
    shifted_order = sorted(
        rows,
        key=lambda item: float(item["adaptation_performance"]),
        reverse=True,
    )
    iid_rank = {str(item["method_id"]): index for index, item in enumerate(iid_order, start=1)}
    shifted_rank = {
        str(item["method_id"]): index for index, item in enumerate(shifted_order, start=1)
    }
    for row in rows:
        method = str(row["method_id"])
        row["iid_rank"] = iid_rank[method]
        row["adaptation_rank"] = shifted_rank[method]
        row["rank_change"] = iid_rank[method] - shifted_rank[method]
    inversions = _rank_inversions(rows)
    iid_values = [float(row["iid_performance"]) for row in rows]
    shifted_values = [float(row["adaptation_performance"]) for row in rows]
    return {
        "agent_count": len(rows),
        "rows": sorted(rows, key=lambda item: int(item["iid_rank"])),
        "iid_order": [str(item["method_id"]) for item in iid_order],
        "adaptation_order": [str(item["method_id"]) for item in shifted_order],
        "spearman_rank_correlation": _spearman(iid_values, shifted_values),
        "rank_inversion_count": len(inversions),
        "rank_inversions": inversions,
        "interpretation_boundary": (
            "descriptive one-seed panel; correlation is not an inferential estimate"
        ),
    }


def _feedback_analysis(campaigns: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    by_task: dict[str, dict[str, Mapping[str, Any]]] = defaultdict(dict)
    for campaign in campaigns:
        by_task[str(campaign.get("task_id"))][str(campaign.get("feedback_condition"))] = campaign
    tasks: dict[str, Any] = {}
    reliance_values: list[float] = []
    for task_id, conditions in sorted(by_task.items()):
        true = conditions.get("true_feedback")
        permuted = conditions.get("permuted_feedback")
        true_score = _phase_score(true, "shifted")
        permuted_score = _phase_score(permuted, "shifted")
        evidence_reliance = (
            true_score - permuted_score
            if true_score is not None and permuted_score is not None
            else None
        )
        if evidence_reliance is not None:
            reliance_values.append(evidence_reliance)
        tasks[task_id] = {
            "condition_scores": {
                condition: _phase_score(campaign, "shifted")
                for condition, campaign in sorted(conditions.items())
            },
            "evidence_reliance": evidence_reliance,
            "diagnostics": {
                condition: campaign.get("deepseek_diagnostic")
                for condition, campaign in sorted(conditions.items())
            },
        }
    return {
        "definition": "J_true_feedback - J_permuted_feedback",
        "mean_evidence_reliance": _mean(reliance_values),
        "tasks": tasks,
        "causal_boundary": (
            "environment state and scoring are true in every condition; only "
            "agent-visible feedback changes"
        ),
    }


def _counterfactual_analysis(campaigns: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    rows = []
    for campaign in campaigns:
        diagnostic = campaign.get("deepseek_diagnostic")
        rows.append(
            {
                "task_id": campaign.get("task_id"),
                "iid_best_score": campaign.get("iid", {}).get("best_score"),
                "counterfactual_best_score": campaign.get("shifted", {}).get("best_score"),
                "score_change": _difference(
                    campaign.get("shifted", {}).get("best_score"),
                    campaign.get("iid", {}).get("best_score"),
                ),
                "mechanism_identified": (
                    diagnostic.get("mechanism_identified")
                    if isinstance(diagnostic, Mapping)
                    else None
                ),
                "truth_probability": (
                    diagnostic.get("shifted_truth_probability")
                    if isinstance(diagnostic, Mapping)
                    else None
                ),
                "feedback_condition": campaign.get("feedback_condition"),
            }
        )
    return {
        "public_names_descriptions_and_action_codes_held_fixed": True,
        "hidden_material_effect_rows_swapped": True,
        "rows": rows,
    }


def _outcome_understanding_analysis(
    campaigns: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    rows = []
    counts: dict[str, int] = defaultdict(int)
    for campaign in campaigns:
        if campaign.get("resource_reused_from_campaign") is not None:
            continue
        diagnostic = campaign.get("deepseek_diagnostic")
        if not isinstance(diagnostic, Mapping):
            continue
        row = {
            "campaign_id": campaign.get("campaign_id"),
            "experiment_id": campaign.get("experiment_id"),
            "task_id": campaign.get("task_id"),
            "feedback_condition": campaign.get("feedback_condition"),
            "final_objective": campaign.get("shifted", {}).get("best_score"),
            "mechanism_identified": diagnostic.get("mechanism_identified"),
            "truth_probability": diagnostic.get("shifted_truth_probability"),
            "change_detected": diagnostic.get("change_detected"),
            "multiclass_brier_score": diagnostic.get("multiclass_brier_score"),
            "information_value": diagnostic.get("information_value"),
            "recovery_experiment": diagnostic.get("recovery_experiment"),
            "type": diagnostic.get("outcome_understanding_type"),
        }
        counts[str(row["type"])] += 1
        rows.append(row)
    return {
        "axes": {
            "x": "final objective relative to 90% of IID best",
            "y": "correct mechanism argmax with truth probability at least 0.5",
        },
        "type_counts": dict(sorted(counts.items())),
        "aggregate_information_value": _aggregate_information_value(rows),
        "rows": rows,
    }


def _aggregate_information_value(
    rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    total_pairs = sum(int(row.get("information_value", {}).get("pair_count", 0)) for row in rows)

    def weighted(field: str) -> float | None:
        if total_pairs == 0:
            return None
        return (
            sum(
                float(row.get("information_value", {}).get(field, 0.0))
                * int(row.get("information_value", {}).get("pair_count", 0))
                for row in rows
            )
            / total_pairs
        )

    return {
        "pair_count": total_pairs,
        "mean_expected_information_gain": weighted("mean_expected_information_gain"),
        "mean_realized_entropy_reduction": weighted("mean_realized_entropy_reduction"),
        "mean_absolute_calibration_error": weighted("mean_absolute_calibration_error"),
    }


def _resource_summary(campaigns: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    deepseek_campaigns = [
        campaign
        for campaign in campaigns
        if campaign.get("method_id") == "deepseek_v4_flash"
        and campaign.get("resource_reused_from_campaign") is None
    ]
    deepseek = [campaign.get("full_method_resources", {}) for campaign in deepseek_campaigns]
    return {
        "deepseek_campaign_count": len(deepseek),
        "model_call_count": sum(int(item.get("model_call_count", 0)) for item in deepseek),
        "input_token_count": sum(int(item.get("input_token_count", 0)) for item in deepseek),
        "output_token_count": sum(int(item.get("output_token_count", 0)) for item in deepseek),
        "provider_failure_count": sum(
            int(item.get("model_provenance", {}).get("provider_failure_count", 0))
            for item in deepseek
        ),
        "retry_count": sum(
            int(item.get("model_provenance", {}).get("retry_count", 0)) for item in deepseek
        ),
        "lifecycle_guardrail_override_count": sum(
            len(campaign.get("lifecycle_guardrail_log", [])) for campaign in deepseek_campaigns
        ),
        "monetary_cost_usd": sum(float(item.get("monetary_cost_usd", 0.0)) for item in deepseek),
        "private_reasoning_retained": False,
    }


def _phase_score(campaign: Mapping[str, Any] | None, phase: str) -> float | None:
    if not isinstance(campaign, Mapping):
        return None
    value = campaign.get(phase, {}).get("best_score")
    return float(value) if value is not None else None


def _normalized_entropy(belief: Mapping[str, float]) -> float:
    if len(belief) <= 1:
        return 0.0
    entropy = -sum(value * math.log(value) for value in belief.values() if value > 0.0)
    return entropy / math.log(len(belief))


def _brier_score(belief: Mapping[str, float], truth: str) -> float:
    return sum(
        (float(probability) - (1.0 if candidate == truth else 0.0)) ** 2
        for candidate, probability in belief.items()
    )


def _quadrant(outcome_high: bool, understanding_high: bool) -> str:
    if outcome_high and understanding_high:
        return "genuine_experimental"
    if outcome_high:
        return "accidental_optimizer"
    if understanding_high:
        return "theoretical_explainer"
    return "joint_failure"


def _rank_inversions(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, str]]:
    inversions = []
    for index, left in enumerate(rows):
        for right in rows[index + 1 :]:
            iid_delta = float(left["iid_performance"]) - float(right["iid_performance"])
            shifted_delta = float(left["adaptation_performance"]) - float(
                right["adaptation_performance"]
            )
            if iid_delta * shifted_delta < 0.0:
                inversions.append(
                    {
                        "method_a": str(left["method_id"]),
                        "method_b": str(right["method_id"]),
                    }
                )
    return inversions


def _spearman(left: Sequence[float], right: Sequence[float]) -> float | None:
    if len(left) != len(right) or len(left) < 2:
        return None
    return _pearson(_ranks(left), _ranks(right))


def _ranks(values: Sequence[float]) -> list[float]:
    order = sorted(range(len(values)), key=values.__getitem__)
    ranks = [0.0] * len(values)
    cursor = 0
    while cursor < len(order):
        end = cursor + 1
        while end < len(order) and values[order[end]] == values[order[cursor]]:
            end += 1
        average = (cursor + 1 + end) / 2.0
        for position in range(cursor, end):
            ranks[order[position]] = average
        cursor = end
    return ranks


def _pearson(left: Sequence[float], right: Sequence[float]) -> float | None:
    left_mean = _mean(left)
    right_mean = _mean(right)
    if left_mean is None or right_mean is None:
        return None
    numerator = sum((a - left_mean) * (b - right_mean) for a, b in zip(left, right, strict=True))
    denominator = math.sqrt(
        sum((value - left_mean) ** 2 for value in left)
        * sum((value - right_mean) ** 2 for value in right)
    )
    return numerator / denominator if denominator > 0.0 else None


def _mean(values: Sequence[float]) -> float | None:
    return sum(values) / len(values) if values else None


def _difference(left: Any, right: Any) -> float | None:
    return float(left) - float(right) if left is not None and right is not None else None


def _canonical_sha256(payload: Mapping[str, Any]) -> str:
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _measurement_instrument(action: Mapping[str, Any] | None) -> str | None:
    if not isinstance(action, Mapping) or action.get("operation") != "measure":
        return None
    instrument = action.get("instrument")
    return str(instrument) if isinstance(instrument, str) and instrument else None


def _replace_public_feedback(
    current: Mapping[str, Any],
    donor: Mapping[str, Any],
) -> dict[str, Any]:
    replaced = copy.deepcopy(dict(current))
    donor_copy = copy.deepcopy(dict(donor))
    for key in ("observation", "raw_signal", "processed_estimate", "uncertainty", "lab_report"):
        if key in donor_copy:
            replaced[key] = donor_copy[key]
    current_tool = replaced.get("tool_json")
    donor_tool = donor_copy.get("tool_json")
    if isinstance(current_tool, dict) and isinstance(donor_tool, dict):
        for key in ("observation", "raw_signal", "processed_estimate", "uncertainty", "lab_report"):
            if key in donor_tool:
                current_tool[key] = copy.deepcopy(donor_tool[key])
    return replaced


def _mask_public_feedback(current: Mapping[str, Any]) -> dict[str, Any]:
    masked = copy.deepcopy(dict(current))
    for container in (masked, masked.get("tool_json")):
        if not isinstance(container, dict):
            continue
        observation = container.get("observation")
        if isinstance(observation, dict):
            container["observation"] = dict.fromkeys(observation)
        container["raw_signal"] = {}
        container["processed_estimate"] = {}
        container["uncertainty"] = {}
        report = container.get("lab_report")
        if isinstance(report, dict):
            report["visible_metrics"] = {}
            report["spectra_summary"] = {"has_spectral_packet": False}
    return masked


def _replace_outcome_feedback(
    current: Mapping[str, Any],
    donor: Mapping[str, Any],
) -> dict[str, Any]:
    replaced = copy.deepcopy(dict(current))
    for key in (
        "leaderboard_score",
        "observed_keys",
        "observed_mask",
        "processed_estimate",
        "raw_signal",
        "uncertainty",
        "measurement_cost",
    ):
        if key in donor:
            replaced[key] = copy.deepcopy(donor[key])
    # Lifecycle and transaction validity always come from the true current world.
    for key in (
        "experiment_ended",
        "next_experiment_ready",
        "operation_type",
        "transaction_status",
        "preconditions",
        "constraint_flags",
    ):
        if key in current:
            replaced[key] = copy.deepcopy(current[key])
    return replaced


def _counts(values: Sequence[str] | Any) -> dict[str, int]:
    counts: dict[str, int] = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items()))


def _file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


__all__ = [
    "DEFAULT_PROTOCOL_PATH",
    "DIAGNOSTIC_REPORT_VERSION",
    "ContinuingHistoryAgent",
    "ContinuingPublicViewAgent",
    "FeedbackCondition",
    "analyze_deepseek_campaign",
    "build_flagship_diagnostic_report",
    "load_flagship_diagnostic_protocol",
    "render_flagship_diagnostic_markdown",
    "run_two_phase_campaign",
    "summarize_phase",
]
