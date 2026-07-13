"""Official runner for benchmark agents."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from time import perf_counter
from typing import Any, Literal

import gymnasium as gym

import chemworld  # noqa: F401
from chemworld.agent_interface import agent_view_bundle
from chemworld.agents import (
    CodexSubagentOnlineAgent,
    CodexSubagentReplayAgent,
    GaussianProcessBOAgent,
    GaussianProcessPIAgent,
    GaussianProcessUCBAgent,
    GreedyLocalAgent,
    LatinHypercubeAgent,
    LLMReplayAgent,
    RandomAgent,
    RandomForestEIAgent,
    RandomRecipeAgent,
    SafetyConstrainedBOAgent,
    ScriptedChemistryAgent,
    StructuredGaussianProcessBOAgent,
    StructuredGaussianProcessPIAgent,
    StructuredGaussianProcessUCBAgent,
    StructuredRandomForestEIAgent,
    StructuredSafetyConstrainedBOAgent,
    ToolUsingLLMStubAgent,
)
from chemworld.agents.base import Agent, HistoryRecord
from chemworld.agents.interaction import (
    INTERACTION_CONTRACT_VERSION,
    DecisionAuditRecord,
    build_decision_context,
)
from chemworld.data.logging import TrajectoryLogger, action_payload, observation_to_json
from chemworld.data.submission import git_commit
from chemworld.eval.method_protocol import (
    MethodResourceLedger,
    MethodResourceLimits,
    evaluation_resource_limits,
    load_method_protocol,
)
from chemworld.eval.risk_policy import (
    RiskCostTaskPolicy,
    load_risk_cost_protocol,
)

EvaluationPolicy = Literal["task_contract", "vnext_risk_cost"]

AGENT_REGISTRY: dict[str, Callable[[], Agent]] = {
    "random": RandomAgent,
    "lhs": LatinHypercubeAgent,
    "latin_hypercube": LatinHypercubeAgent,
    "greedy": GreedyLocalAgent,
    "greedy_local": GreedyLocalAgent,
    "gp_bo": GaussianProcessBOAgent,
    "gp_pi": GaussianProcessPIAgent,
    "gp_ucb": GaussianProcessUCBAgent,
    "rf_ei": RandomForestEIAgent,
    "safe_gp_bo": SafetyConstrainedBOAgent,
    "structured_gp_bo": StructuredGaussianProcessBOAgent,
    "structured_gp_pi": StructuredGaussianProcessPIAgent,
    "structured_gp_ucb": StructuredGaussianProcessUCBAgent,
    "structured_rf_ei": StructuredRandomForestEIAgent,
    "structured_safe_gp_bo": StructuredSafetyConstrainedBOAgent,
    "random_recipe": RandomRecipeAgent,
    "scripted_chemistry": ScriptedChemistryAgent,
    "scripted_reaction_to_purification": ScriptedChemistryAgent,
    "partition_discovery_heuristic": ScriptedChemistryAgent,
    "heuristic": ScriptedChemistryAgent,
    "tool_using_llm_stub": ToolUsingLLMStubAgent,
    "llm_replay": LLMReplayAgent,
    "codex_subagent_replay": CodexSubagentReplayAgent,
    "codex_subagent_online": CodexSubagentOnlineAgent,
}


def make_agent(name: str) -> Agent:
    if name not in AGENT_REGISTRY:
        allowed = ", ".join(sorted(AGENT_REGISTRY))
        raise ValueError(f"Unknown agent={name!r}. Allowed: {allowed}")
    return AGENT_REGISTRY[name]()


def run_agent(
    *,
    env_id: str,
    agent: Agent,
    world_split: str,
    budget: int,
    objective: str,
    seed: int,
    agent_seed: int | None = None,
    task_id: str | None = None,
    output_path: str | Path | None = None,
    budget_override: int | None = None,
    episode_mode_override: str | None = None,
    step_callback: Callable[[HistoryRecord, list[dict[str, Any]]], None] | None = None,
    method_resource_limits: dict[str, Any] | None = None,
    evaluation_policy: EvaluationPolicy = "task_contract",
    world_interventions: tuple[dict[str, Any], ...] | list[dict[str, Any]] | None = None,
    safety_limit_override: float | None = None,
) -> list[HistoryRecord]:
    """Run one benchmark episode and optionally write a JSONL trajectory."""

    if evaluation_policy not in {"task_contract", "vnext_risk_cost"}:
        raise ValueError("evaluation_policy must be task_contract or vnext_risk_cost")
    if safety_limit_override is not None:
        if evaluation_policy != "task_contract":
            raise ValueError(
                "safety_limit_override cannot be combined with a named evaluation policy"
            )
        if not 0.0 < float(safety_limit_override) < 1.0:
            raise ValueError("safety_limit_override must be in (0, 1)")
    risk_policy: RiskCostTaskPolicy | None = None
    if evaluation_policy == "vnext_risk_cost":
        if task_id is None:
            raise ValueError("vnext_risk_cost requires a registered serious task_id")
        risk_policy = RiskCostTaskPolicy.from_protocol(
            task_id,
            load_risk_cost_protocol(),
        )

    env_kwargs: dict[str, Any] = {
        "world_split": world_split,
        "budget": budget,
        "objective": objective,
        "seed": seed,
    }
    if task_id is not None:
        env_kwargs["task_id"] = task_id
    if world_interventions:
        env_kwargs["world_interventions"] = list(world_interventions)
    if risk_policy is not None:
        env_kwargs["safety_limit_override"] = risk_policy.risk_limit
    elif safety_limit_override is not None:
        env_kwargs["safety_limit_override"] = float(safety_limit_override)
    if budget_override is not None:
        env_kwargs["budget_override"] = budget_override
    if episode_mode_override is not None:
        env_kwargs["episode_mode_override"] = episode_mode_override
    effective_budget = budget_override if budget_override is not None else budget
    env = gym.make(
        env_id,
        **env_kwargs,
    )
    initial_obs, task_info = env.reset(seed=seed)
    if not hasattr(env.unwrapped, "task_info"):
        raise RuntimeError(f"{env_id} does not expose task_info()")
    base_env: Any = env.unwrapped
    task_info = base_env.task_info()
    if risk_policy is not None:
        task_info.update(risk_policy.task_info_overlay())
        task_info["risk_policy_hash"] = risk_policy.policy_hash

    resolved_agent_seed = seed if agent_seed is None else int(agent_seed)
    agent.reset(task_info, resolved_agent_seed)
    agent_metadata = agent.manifest()
    if agent_seed is not None:
        # Formal method RNG streams are committed privately and must not be copied
        # into public trajectory metadata. The world seed remains in task_info for
        # replay binding, while the policy receives only resolved_agent_seed.
        agent_metadata.pop("seed", None)
        agent_metadata["agent_seed_disclosure"] = "private_committed"
    agent_metadata["git_commit"] = git_commit()
    agent_metadata["evaluation_policy"] = evaluation_policy
    agent_metadata["risk_policy_hash"] = (
        risk_policy.policy_hash if risk_policy is not None else None
    )
    agent_metadata["safety_limit_override"] = (
        float(safety_limit_override) if safety_limit_override is not None else None
    )
    agent_metadata["official_runner_policy"] = {
        "one_agent_decision_per_operation": True,
        "automatic_action_repair": False,
        "automatic_terminate": False,
        "automatic_final_assay": False,
        "failed_or_invalid_actions_retained": True,
    }
    requires_online_model = bool(agent_metadata.get("requires_online_model", False))
    resource_limits = (
        MethodResourceLimits.from_payload(
            method_resource_limits,
            operation_limit=effective_budget,
        )
        if method_resource_limits is not None
        else evaluation_resource_limits(
            load_method_protocol(),
            operation_limit=effective_budget,
            requires_online_model=requires_online_model,
        )
    )
    resource_ledger = MethodResourceLedger(
        limits=resource_limits,
        requires_online_model=requires_online_model,
    )
    agent_metadata["method_resource_contract_version"] = resource_ledger.snapshot()[
        "schema_version"
    ]

    history: list[HistoryRecord] = []
    current_observation = initial_obs
    current_info: dict[str, Any] = {}
    previous_event_type: str | None = None
    logger_context = TrajectoryLogger(output_path) if output_path is not None else None
    try:
        logger = logger_context.__enter__() if logger_context is not None else None
        for step in range(1, effective_budget + 1):
            pre_decision_view = agent_view_bundle(env, current_observation, current_info)
            decision_context = build_decision_context(
                step=step,
                task_info=task_info,
                campaign_state=base_env.campaign_state(),
                public_view=pre_decision_view,
                previous_event_type=previous_event_type,
            )
            public_view_act = getattr(agent, "act_with_public_view", None)
            context_act = getattr(agent, "act_with_context", None)
            decision_started = perf_counter()
            if callable(public_view_act):
                action = public_view_act(decision_context, pre_decision_view)
            elif callable(context_act):
                action = context_act(decision_context)
            else:
                action = agent.act(history)
            decision_elapsed_s = perf_counter() - decision_started
            normalized_action = action_payload(action)
            if not isinstance(normalized_action, dict):
                raise TypeError("agent action must normalize to a JSON object")
            action = normalized_action
            usage_factory = getattr(agent, "method_resource_usage", None)
            agent_usage = usage_factory() if callable(usage_factory) else {}
            resource_ledger.record_decision(
                elapsed_s=decision_elapsed_s,
                agent_usage=agent_usage,
            )
            decision_audit_factory = getattr(agent, "decision_audit", None)
            decision_audit = DecisionAuditRecord.from_payload(
                decision_audit_factory() if callable(decision_audit_factory) else None,
                action=action,
            )
            observation, reward, terminated, truncated, info = env.step(action)
            obs_json = observation_to_json(observation)
            update_started = perf_counter()
            agent.update(action, obs_json, float(reward), info)
            update_elapsed_s = perf_counter() - update_started
            public_view = agent_view_bundle(env, observation, info)
            final_assay_ended = bool(
                terminated
                and action.get("operation") == "measure"
                and action.get("instrument") == "final_assay"
            )
            if info.get("experiment_ended") or final_assay_ended:
                event_type = "experiment_end"
            elif info.get("operation_type") == "measure":
                event_type = "measurement_result"
            else:
                event_type = "operation_result"
            resource_ledger.record_outcome(
                experiment_ended=event_type == "experiment_end",
                update_elapsed_s=update_elapsed_s,
            )
            method_resources = resource_ledger.snapshot()
            interaction_evidence = {
                "interaction_contract_version": INTERACTION_CONTRACT_VERSION,
                "decision_context": decision_context.to_dict(),
                "decision_audit": decision_audit.to_dict(),
                "outcome": {
                    "event_type": event_type,
                    "observed_keys": list(info.get("observed_keys", [])),
                    "has_spectral_packet": bool(
                        public_view.get("lab_report", {})
                        .get("spectra_summary", {})
                        .get("has_spectral_packet", False)
                    ),
                    "experiment_ended": bool(
                        info.get("experiment_ended", False) or final_assay_ended
                    ),
                    "constraint_flags": info.get("constraint_flags", {}),
                },
                "method_resources": method_resources,
            }
            record = HistoryRecord(
                step=step,
                action=dict(action),
                observation=obs_json,
                reward=float(reward),
                info=info,
                public_view=public_view,
                decision_context=decision_context.to_dict(),
                decision_audit=decision_audit.to_dict(),
                event_type=event_type,
                method_resources=method_resources,
            )
            history.append(record)
            agent_trace_factory = getattr(agent, "agent_trace", None)
            agent_trace = agent_trace_factory() if callable(agent_trace_factory) else []
            if logger is not None:
                logger.log(
                    task_info=task_info,
                    step=step,
                    action=action,
                    observation=obs_json,
                    reward=float(reward),
                    terminated=terminated,
                    truncated=truncated,
                    info=info,
                    agent_metadata=agent_metadata,
                    explanation=interaction_evidence,
                    agent_view=public_view,
                    agent_trace=agent_trace,
                    method_resources=method_resources,
                )
            if step_callback is not None:
                step_callback(record, agent_trace)
            current_observation = observation
            current_info = info
            previous_event_type = event_type
            if terminated or truncated:
                break
    finally:
        if logger_context is not None:
            logger_context.__exit__(None, None, None)
        env.close()
    return history
