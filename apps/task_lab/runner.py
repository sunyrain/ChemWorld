"""DeepSeek-driven task runner with progress events and replayable trajectories."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Callable
from dataclasses import asdict, dataclass
from math import ceil
from pathlib import Path
from typing import Any, Literal

import gymnasium as gym

import chemworld  # noqa: F401
from apps.task_lab.catalog import TASK_BACKGROUNDS
from apps.task_lab.deepseek_client import JsonCompletion, JsonPlannerClient
from apps.task_lab.experiment_audit import audit_experiment_design
from apps.task_lab.interaction_semantics import (
    aligned_affordance,
    operation_semantics,
)
from apps.task_lab.interaction_semantics import (
    validate_interactive_action as _validate_decision,
)
from apps.task_lab.spectral_payload import SpectrumDisclosure, spectral_payload
from chemworld.agent_interface import agent_view_bundle
from chemworld.data.logging import TrajectoryLogger, load_jsonl, observation_to_json, to_builtin
from chemworld.data.submission import git_commit
from chemworld.eval.result_artifacts import build_verified_evaluation_result
from chemworld.tasks import get_task

RunMode = Literal["plan", "adaptive"]
EventCallback = Callable[[dict[str, Any]], None]

SYSTEM_PROMPT = """You are a ChemWorld virtual-laboratory agent.
Work from the public task contract, observations, and listed action schemas.
Return one JSON object using the operation and field names in those schemas.
Private chain-of-thought is not part of the response; provide a concise audit record with public
evidence, any inspected-spectrum interpretation, hypothesis, uncertainty, and action rationale.
"""

MAX_SPECTRUM_RETRIEVALS_PER_DECISION = 3


@dataclass(frozen=True)
class TaskRunResult:
    task_id: str
    seed: int
    model: str
    mode: str
    status: str
    official_score: float | None
    research_score: float | None
    total_score: float | None
    steps: int
    final_assay_count: int
    invalid_plan_actions: int
    model_call_count: int
    verified: bool
    usage: dict[str, Any]
    method_resources: dict[str, Any]
    agent_backend: str
    contract_profile: str
    official_budget: int
    effective_budget: int
    experiment_count: int
    spectrum_disclosure: str
    experiment_design_audit: dict[str, Any]
    trajectory_path: str
    result_path: str | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def run_task(
    *,
    client: JsonPlannerClient,
    task_id: str,
    output_dir: str | Path,
    seed: int | None = None,
    mode: RunMode = "adaptive",
    max_steps: int = 18,
    budget_multiplier: float = 1.0,
    campaign_override: bool = False,
    spectrum_disclosure: SpectrumDisclosure = "unassigned",
    event_callback: EventCallback | None = None,
) -> TaskRunResult:
    """Run one task and emit JSON-safe lifecycle events after every decision."""

    task = get_task(task_id)
    selected_seed = task.seeds[0] if seed is None else seed
    multiplier = float(budget_multiplier)
    if not 1.0 <= multiplier <= 4.0:
        raise ValueError("budget_multiplier must be between 1.0 and 4.0")
    effective_budget = max(task.budget, ceil(task.budget * multiplier))
    step_limit = max(1, min(int(max_steps), effective_budget))
    contract_profile = (
        "extended-research" if effective_budget != task.budget or campaign_override else "official"
    )
    root = Path(output_dir) / task_id
    root.mkdir(parents=True, exist_ok=True)
    trajectory_path = root / "trajectory.jsonl"
    result_path = root / "evaluation_result.json"
    plan_path = root / "agent_plan.json"
    emit = event_callback or (lambda event: None)
    usage = _empty_usage()
    trace: list[dict[str, Any]] = []
    experiment_memory: list[dict[str, Any]] = []
    experiment_trace_start = 0
    spectrum_archive: list[dict[str, Any]] = []
    invalid_plan_actions = 0
    model_call_count = 0
    task_info: dict[str, Any] = {}
    env_kwargs = task.env_kwargs(seed=selected_seed)
    if contract_profile == "extended-research":
        env_kwargs["budget_override"] = effective_budget
        if campaign_override:
            env_kwargs["episode_mode_override"] = "campaign"
    env = gym.make("ChemWorld", **env_kwargs)
    try:
        env.reset(seed=selected_seed)
        base: Any = env.unwrapped
        task_info = base.task_info()
        prompt = base.task_prompt()
        background = TASK_BACKGROUNDS[task_id].to_dict()
        emit(
            {
                "type": "task_started",
                "task_id": task_id,
                "seed": selected_seed,
                "mode": mode,
                "model": client.model,
                "budget": effective_budget,
                "official_budget": task.budget,
                "contract_profile": contract_profile,
                "campaign_override": campaign_override,
                "spectrum_disclosure": spectrum_disclosure,
                "step_limit": step_limit,
                "background": background,
                "success_metrics": list(task.success_metrics),
                "episode_mode": base.campaign_state().get("episode_mode"),
                "state_semantics": _state_semantics(base),
            }
        )

        planned: list[dict[str, Any]] = []
        if mode == "plan":
            completion = _request_plan(
                client=client,
                base=base,
                task_prompt=prompt,
                background=background,
                max_steps=step_limit,
            )
            model_call_count += completion.attempts
            _add_usage(usage, completion.usage)
            planned = _plan_entries(completion.payload)
            plan_path.write_text(
                json.dumps(
                    {
                        "task_id": task_id,
                        "model": completion.model,
                        "strategy_summary": completion.payload.get("strategy_summary"),
                        "actions": planned,
                        "usage": usage,
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )
            emit(
                {
                    "type": "plan_ready",
                    "task_id": task_id,
                    "strategy_summary": completion.payload.get("strategy_summary", ""),
                    "planned_action_count": len(planned),
                    "usage": dict(usage),
                }
            )

        agent_metadata: dict[str, Any] = {
            "agent_name": "deepseek_task_lab",
            "agent_family": "DeepSeekJsonPlanner",
            "model": client.model,
            "mode": mode,
            "thinking_enabled": bool(getattr(client, "thinking", False)),
            "reasoning_effort": getattr(client, "reasoning_effort", None),
            "decision_trace_policy": "structured_public_audit_without_hidden_chain_of_thought",
            "spectrum_disclosure": spectrum_disclosure,
            "contract_profile": contract_profile,
            "official_budget": task.budget,
            "effective_budget": effective_budget,
            "seed": selected_seed,
            "git_commit": git_commit(),
            "api_key_source": "process-local DeepSeek client configuration",
            "usage": usage,
        }
        agent_metadata["method_resources"] = _method_resources(
            client=client,
            usage=usage,
            model_call_count=model_call_count,
        )
        executed_steps = 0
        plan_index = 0
        last_final_assay_step = 0
        consecutive_unrepaired_actions = 0
        done = False
        with TrajectoryLogger(trajectory_path) as logger:
            while executed_steps < step_limit and not done:
                campaign_before = base.campaign_state()
                final_assay_seen = int(campaign_before.get("final_assay_count", 0)) > 0
                current_experiment_has_work = executed_steps > last_final_assay_step
                remaining_steps = step_limit - executed_steps
                if final_assay_seen and not current_experiment_has_work and remaining_steps < 6:
                    break
                closeout_required = current_experiment_has_work and (
                    executed_steps >= max(step_limit - 2, 0)
                    or (mode == "plan" and plan_index >= len(planned))
                )
                decision_spectrum = spectral_payload({}, disclosure=spectrum_disclosure)
                retrieved_spectra: list[dict[str, Any]] = []
                decision_origin = "protocol"
                if closeout_required:
                    decision = _closeout_decision(base)
                    if decision is None:
                        break
                    decision_origin = "protocol_closeout"
                    emit(
                        {
                            "type": "closeout_action",
                            "task_id": task_id,
                            "action": decision["action"],
                            "reason": (
                                "Evaluation limit reached; preserve the model-selected "
                                "state and complete only the required scoring protocol."
                            ),
                        }
                    )
                elif mode == "plan":
                    if plan_index >= len(planned):
                        break
                    decision = _normalize_decision(planned[plan_index])
                    decision_origin = "model_plan"
                    plan_index += 1
                else:
                    try:
                        retrieval_count = 0
                        while True:
                            completion = _request_adaptive_decision(
                                client=client,
                                base=base,
                                task_prompt=prompt,
                                background=background,
                                trace=trace,
                                experiment_memory=experiment_memory,
                                spectrum_archive=spectrum_archive,
                                retrieved_spectra=retrieved_spectra,
                                spectrum_disclosure=spectrum_disclosure,
                            )
                            model_call_count += completion.attempts
                            _add_usage(usage, completion.usage)
                            requested_spectrum_id = _requested_spectrum_id(completion.payload)
                            if requested_spectrum_id is None:
                                decision = _normalize_decision(completion.payload)
                                break
                            if retrieval_count >= MAX_SPECTRUM_RETRIEVALS_PER_DECISION:
                                raise ValueError(
                                    "Model exceeded the per-decision spectrum retrieval limit"
                                )
                            retrieval_count += 1
                            emit(
                                {
                                    "type": "spectrum_requested",
                                    "task_id": task_id,
                                    "step": executed_steps + 1,
                                    "spectrum_id": requested_spectrum_id,
                                    "request_index": retrieval_count,
                                }
                            )
                            retrieved = _spectrum_by_id(spectrum_archive, requested_spectrum_id)
                            if retrieved is None:
                                retrieved_spectra.append(
                                    {
                                        "available": False,
                                        "requested_spectrum_id": requested_spectrum_id,
                                        "request_error": "unknown_spectrum_id",
                                    }
                                )
                                emit(
                                    {
                                        "type": "spectrum_unavailable",
                                        "task_id": task_id,
                                        "step": executed_steps + 1,
                                        "spectrum_id": requested_spectrum_id,
                                    }
                                )
                                continue
                            decision_spectrum = retrieved
                            retrieved_spectra.append(retrieved)
                            emit(
                                {
                                    "type": "spectrum_retrieved",
                                    "task_id": task_id,
                                    "step": executed_steps + 1,
                                    "spectrum_id": requested_spectrum_id,
                                    "request_index": retrieval_count,
                                    "spectrum": to_builtin(retrieved),
                                }
                            )
                        decision_origin = "online_model"
                    except Exception as exc:
                        failed_attempts = max(int(getattr(exc, "attempts", 0)), 0)
                        if failed_attempts:
                            model_call_count += failed_attempts
                            _add_usage(usage, getattr(exc, "usage", {}))
                        emit(
                            {
                                "type": "model_call_failed",
                                "task_id": task_id,
                                "step": executed_steps + 1,
                                "error": str(exc),
                            }
                        )
                        decision = _closeout_decision(base)
                        if decision is None:
                            break
                        decision_origin = "protocol_closeout_after_model_failure"
                        emit(
                            {
                                "type": "closeout_action",
                                "task_id": task_id,
                                "action": decision["action"],
                                "reason": (
                                    "Model call failed; preserve the existing experiment "
                                    "and complete only the required scoring protocol."
                                ),
                            }
                        )

                validation = _validate_decision(base, decision["action"], trace)
                if not validation.get("valid", False):
                    invalid_plan_actions += 1
                    emit(
                        {
                            "type": "action_rejected",
                            "task_id": task_id,
                            "planned_step": plan_index,
                            "action": decision["action"],
                            "reasons": validation.get("invalid_reasons", []),
                        }
                    )
                    repair = _request_repair(
                        client=client,
                        base=base,
                        rejected=decision,
                        validation=validation,
                        spectrum=decision_spectrum,
                        spectrum_archive=spectrum_archive,
                        retrieved_spectra=retrieved_spectra,
                        trace=trace,
                    )
                    model_call_count += repair.attempts
                    _add_usage(usage, repair.usage)
                    decision = _normalize_decision(repair.payload)
                    decision_origin = "online_model_repair"
                    validation = _validate_decision(base, decision["action"], trace)
                    if not validation.get("valid", False):
                        consecutive_unrepaired_actions += 1
                        emit(
                            {
                                "type": "action_skipped",
                                "task_id": task_id,
                                "action": decision["action"],
                                "reasons": validation.get("invalid_reasons", []),
                            }
                        )
                        if consecutive_unrepaired_actions < 3:
                            continue
                        fallback = _closeout_decision(base) if current_experiment_has_work else None
                        if fallback is None:
                            emit(
                                {
                                    "type": "decision_loop_stopped",
                                    "task_id": task_id,
                                    "reason": (
                                        "Three consecutive decisions remained invalid after "
                                        "repair and no legal scoring closeout is available."
                                    ),
                                }
                            )
                            break
                        decision = fallback
                        decision_origin = "protocol_fallback_after_invalid_model"
                        validation = _validate_decision(base, decision["action"], trace)
                        consecutive_unrepaired_actions = 0
                        emit(
                            {
                                "type": "decision_fallback",
                                "task_id": task_id,
                                "action": decision["action"],
                                "reason": (
                                    "Three consecutive decisions remained invalid after repair; "
                                    "close out the current experiment safely."
                                ),
                            }
                        )
                    else:
                        consecutive_unrepaired_actions = 0
                else:
                    consecutive_unrepaired_actions = 0

                emit(
                    {
                        "type": "decision_ready",
                        "task_id": task_id,
                        "step": executed_steps + 1,
                        "action": to_builtin(decision["action"]),
                        "evidence": decision["evidence"],
                        "spectrum_interpretation": decision["spectrum_interpretation"],
                        "rationale": decision["rationale"],
                        "hypothesis": decision["hypothesis"],
                        "experiment_intent": decision["experiment_intent"],
                        "comparison_to_prior": decision["comparison_to_prior"],
                        "uncertainty": decision["uncertainty"],
                        "uncertainty_note": decision["uncertainty_note"],
                        "decision_origin": decision_origin,
                        "experiment_index": campaign_before.get("experiment_index"),
                        "episode_mode": campaign_before.get("episode_mode"),
                        "vessel_state": "cumulative_same_experiment",
                        "spectrum_input": to_builtin(decision_spectrum),
                        "analysis": {
                            "evidence": decision["evidence"],
                            "spectrum_interpretation": decision["spectrum_interpretation"],
                            "hypothesis": decision["hypothesis"],
                            "rationale": decision["rationale"],
                            "experiment_intent": decision["experiment_intent"],
                            "comparison_to_prior": decision["comparison_to_prior"],
                            "uncertainty": decision["uncertainty"],
                            "uncertainty_note": decision["uncertainty_note"],
                        },
                    }
                )

                observation, reward, terminated, truncated, info = env.step(decision["action"])
                executed_steps += 1
                done = bool(terminated or truncated)
                obs_json = observation_to_json(observation)
                report = base.observation_view("lab_report")
                completed_final_assay = (
                    decision["action"].get("operation") == "measure"
                    and decision["action"].get("instrument") == "final_assay"
                    and info.get("leaderboard_score") is not None
                )
                spectrum = spectral_payload(
                    info.get("raw_signal", {}),
                    instrument=report.get("instrument_summary", {}).get("instrument"),
                    disclosure=spectrum_disclosure,
                )
                if spectrum["available"]:
                    spectrum = {
                        **spectrum,
                        "spectrum_id": _spectrum_id(
                            task_id=task_id,
                            experiment_index=int(campaign_before.get("experiment_index", 0)),
                            measurement_step=executed_steps,
                            instrument=str(
                                spectrum.get("instrument") or spectrum.get("kind") or "signal"
                            ),
                        ),
                        "provenance": {
                            "source": "measurement_output",
                            "measurement_step": executed_steps,
                            "experiment_index": int(campaign_before.get("experiment_index", 0)),
                            "vessel_relation": (
                                "completed_previous_experiment"
                                if completed_final_assay
                                and campaign_before.get("episode_mode") == "campaign"
                                else "completed_experiment"
                                if completed_final_assay
                                else "current_experiment"
                            ),
                        },
                    }
                    spectrum_archive.append(spectrum)
                campaign = base.campaign_state()
                if completed_final_assay:
                    last_final_assay_step = executed_steps
                trace_item = {
                    "step": executed_steps,
                    "selected_action": to_builtin(decision["action"]),
                    "reasoning_summary": decision["rationale"],
                    "public_evidence": decision["evidence"],
                    "spectrum_interpretation": decision["spectrum_interpretation"],
                    "hypothesis_note": decision["hypothesis"],
                    "experiment_intent": decision["experiment_intent"],
                    "comparison_to_prior": decision["comparison_to_prior"],
                    "uncertainty": decision["uncertainty"],
                    "uncertainty_note": decision["uncertainty_note"],
                    "decision_origin": decision_origin,
                    "spectrum_input_summary": _spectrum_input_summary(
                        decision_spectrum,
                        decision_origin=decision_origin,
                    ),
                    "validator_result": {
                        "valid": True,
                        "constraint_flags": to_builtin(info.get("constraint_flags", {})),
                    },
                    "observation_summary": {
                        "visible_metrics": report.get("visible_metrics", {}),
                        "leaderboard_score": info.get("leaderboard_score"),
                        "reward": float(reward),
                    },
                }
                trace.append(trace_item)
                if completed_final_assay:
                    experiment_record = _experiment_memory_record(
                        experiment_index=int(campaign_before.get("experiment_index", 0)),
                        score=float(info["leaderboard_score"]),
                        trace=trace[experiment_trace_start:],
                        final_visible_metrics=report.get("visible_metrics", {}),
                    )
                    design_audit = audit_experiment_design([*experiment_memory, experiment_record])
                    experiment_record["design_audit"] = design_audit["comparisons"][-1]
                    experiment_memory.append(experiment_record)
                    experiment_trace_start = len(trace)
                    emit(
                        {
                            "type": "experiment_learned",
                            "task_id": task_id,
                            **experiment_record,
                            "best_score": campaign.get("best_score"),
                        }
                    )
                agent_metadata["usage"] = dict(usage)
                method_resources = _method_resources(
                    client=client,
                    usage=usage,
                    model_call_count=model_call_count,
                )
                agent_metadata["method_resources"] = method_resources
                logger.log(
                    task_info=task_info,
                    step=executed_steps,
                    action=decision["action"],
                    observation=obs_json,
                    reward=float(reward),
                    terminated=terminated,
                    truncated=truncated,
                    info=info,
                    agent_metadata=agent_metadata,
                    explanation={
                        "rationale": decision["rationale"],
                        "hypothesis": decision["hypothesis"],
                        "experiment_intent": decision["experiment_intent"],
                        "comparison_to_prior": decision["comparison_to_prior"],
                        "evidence": decision["evidence"],
                        "spectrum_interpretation": decision["spectrum_interpretation"],
                        "uncertainty": decision["uncertainty"],
                        "uncertainty_note": decision["uncertainty_note"],
                        "decision_origin": decision_origin,
                        "spectrum_input_summary": _spectrum_input_summary(
                            decision_spectrum,
                            decision_origin=decision_origin,
                        ),
                    },
                    agent_view=agent_view_bundle(env, observation, info),
                    agent_trace=trace,
                    method_resources=method_resources,
                )
                emit(
                    {
                        "type": "step_completed",
                        "task_id": task_id,
                        "step": executed_steps,
                        "budget": effective_budget,
                        "step_limit": step_limit,
                        "action": to_builtin(decision["action"]),
                        "rationale": decision["rationale"],
                        "hypothesis": decision["hypothesis"],
                        "evidence": decision["evidence"],
                        "spectrum_interpretation": decision["spectrum_interpretation"],
                        "uncertainty": decision["uncertainty"],
                        "uncertainty_note": decision["uncertainty_note"],
                        "decision_origin": decision_origin,
                        "spectrum_input": to_builtin(decision_spectrum),
                        "spectrum": spectrum,
                        "spectra_summary": _disclose_spectra_summary(
                            report.get("spectra_summary", {}),
                            spectrum_disclosure,
                        ),
                        "reward": float(reward),
                        "leaderboard_score": info.get("leaderboard_score"),
                        "best_score": campaign.get("best_score"),
                        "remaining_budget": campaign.get("remaining_budget"),
                        "experiment_index": campaign.get("experiment_index"),
                        "action_experiment_index": campaign_before.get("experiment_index"),
                        "episode_mode": campaign.get("episode_mode"),
                        "final_assay_count": campaign.get("final_assay_count"),
                        "visible_metrics": report.get("visible_metrics", {}),
                        "constraint_flags": to_builtin(info.get("constraint_flags", {})),
                        "recovery_suggestion": report.get("recovery_suggestion"),
                        "status": report.get("status"),
                        "experiment_transition": (
                            "reset_for_next_experiment"
                            if completed_final_assay
                            and campaign_before.get("episode_mode") == "campaign"
                            else "cumulative_same_experiment"
                        ),
                    }
                )
    finally:
        env.close()

    records = load_jsonl(trajectory_path)
    experiment_design_audit = audit_experiment_design(experiment_memory)
    verified: dict[str, Any] | None = None
    if records:
        verified = build_verified_evaluation_result(
            records,
            trajectory_path=trajectory_path,
            threshold=task.threshold,
        )
        verified["spectrum_disclosure"] = spectrum_disclosure
        verified["experiment_design_audit"] = experiment_design_audit
        result_path.write_text(
            json.dumps(verified, ensure_ascii=False, indent=2, sort_keys=True),
            encoding="utf-8",
        )
    observed_best_score = None
    total_score = None
    final_assay_count = 0
    if verified is not None:
        final_assay_count = int(verified["final_assay_count"])
        total_score = float(verified["total_score"])
        if final_assay_count:
            observed_best_score = float(verified["final_best_score"])
    official_score = observed_best_score if contract_profile == "official" else None
    research_score = observed_best_score if contract_profile == "extended-research" else None
    status = (
        "scored_extended"
        if research_score is not None
        else "scored"
        if official_score is not None
        else "no_final_assay"
    )
    result = TaskRunResult(
        task_id=task_id,
        seed=selected_seed,
        model=client.model,
        mode=mode,
        status=status,
        official_score=official_score,
        research_score=research_score,
        total_score=total_score,
        steps=len(records),
        final_assay_count=final_assay_count,
        invalid_plan_actions=invalid_plan_actions,
        model_call_count=model_call_count,
        verified=bool(verified and verified.get("verified")),
        usage=usage,
        method_resources=_method_resources(
            client=client,
            usage=usage,
            model_call_count=model_call_count,
        ),
        agent_backend="deepseek",
        contract_profile=contract_profile,
        official_budget=task.budget,
        effective_budget=effective_budget,
        experiment_count=final_assay_count,
        spectrum_disclosure=spectrum_disclosure,
        experiment_design_audit=experiment_design_audit,
        trajectory_path=str(trajectory_path.resolve()),
        result_path=str(result_path.resolve()) if verified is not None else None,
    )
    emit({"type": "task_completed", **result.to_dict()})
    return result


def _request_plan(
    *,
    client: JsonPlannerClient,
    base: Any,
    task_prompt: dict[str, Any],
    background: dict[str, str],
    max_steps: int,
) -> JsonCompletion:
    schemas = [
        _compact_schema(
            aligned_affordance(
                {"operation": name, "schema": base.action_schema(name)},
                [],
            )
        )
        for name in task_prompt["allowed_operations"]
    ]
    user_prompt = json.dumps(
        {
            "instruction": (
                "Create one executable plan that satisfies the public task contract. "
                "Use the supplied state semantics and action effects when interpreting "
                "what each operation changes."
            ),
            "max_actions": max_steps,
            "task_background": background,
            "task_contract": task_prompt,
            "state_semantics": _state_semantics(base),
            "action_schemas": schemas,
            "operation_effects": {
                name: {
                    "type": operation_semantics(name)["type"],
                    "summary": operation_semantics(name)["summary"],
                }
                for name in task_prompt["allowed_operations"]
            },
            "required_json_shape": {
                "strategy_summary": "short string",
                "actions": [
                    {
                        "action": {"operation": "exact operation plus required fields"},
                        "rationale": "short audit summary",
                        "hypothesis": "short testable expectation",
                    }
                ],
            },
        },
        ensure_ascii=False,
    )
    return client.complete_json(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=user_prompt,
        max_tokens=16000 if bool(getattr(client, "thinking", False)) else 6000,
    )


def _request_adaptive_decision(
    *,
    client: JsonPlannerClient,
    base: Any,
    task_prompt: dict[str, Any],
    background: dict[str, str],
    trace: list[dict[str, Any]],
    experiment_memory: list[dict[str, Any]],
    spectrum_archive: list[dict[str, Any]],
    retrieved_spectra: list[dict[str, Any]],
    spectrum_disclosure: SpectrumDisclosure,
) -> JsonCompletion:
    lab_report = _disclose_lab_report(
        base.observation_view("lab_report"),
        spectrum_disclosure,
    )
    user_prompt = json.dumps(
        {
            "instruction": (
                "Return either one spectrum_request_id from available_spectra or one "
                "currently valid action. A spectrum is supplied only after you request its "
                "exact id. Base the concise audit fields on public information actually supplied."
            ),
            "task_background": background,
            "task_contract": task_prompt,
            "campaign_state": base.campaign_state(),
            "state_semantics": _state_semantics(base),
            "spectrum_disclosure": spectrum_disclosure,
            "completed_experiment_memory": experiment_memory,
            "latest_lab_report": lab_report,
            "available_spectra": [_spectrum_catalog_entry(item) for item in spectrum_archive],
            "retrieved_spectra": to_builtin(retrieved_spectra),
            "recent_trace": trace[-6:],
            "currently_valid_actions": [
                _compact_affordance(item, trace) for item in base.available_actions()
            ],
            "required_json_shape": {
                "spectrum_request_id": "available id when requesting a spectrum, otherwise null",
                "action": "exact operation object when acting, otherwise null",
                "evidence": ["short public observation or spectral feature"],
                "spectrum_interpretation": (
                    "concise reading of a requested trace, or 'not inspected'"
                ),
                "rationale": "concise evidence-to-action justification",
                "hypothesis": "short testable expectation",
                "experiment_intent": "exploration, exploitation, replication, or measurement",
                "comparison_to_prior": "named prior experiment and controlled change, or none",
                "uncertainty": "number from 0 to 1",
                "uncertainty_note": "main source of uncertainty",
            },
        },
        ensure_ascii=False,
    )
    completion = client.complete_json(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=user_prompt,
        max_tokens=8000 if bool(getattr(client, "thinking", False)) else 2000,
    )
    return completion


def _request_repair(
    *,
    client: JsonPlannerClient,
    base: Any,
    rejected: dict[str, Any],
    validation: dict[str, Any],
    spectrum: dict[str, Any],
    spectrum_archive: list[dict[str, Any]],
    retrieved_spectra: list[dict[str, Any]],
    trace: list[dict[str, Any]],
) -> JsonCompletion:
    user_prompt = json.dumps(
        {
            "instruction": (
                "Repair the rejected action by choosing one currently valid action. Use only "
                "fields declared by that action schema and remove every undeclared observation "
                "or derived-state field."
            ),
            "rejected_decision": rejected,
            "invalid_reasons": validation.get("invalid_reasons", []),
            "retrieved_spectrum": spectrum,
            "available_spectra": [_spectrum_catalog_entry(item) for item in spectrum_archive],
            "retrieved_spectra": to_builtin(retrieved_spectra),
            "campaign_state": base.campaign_state(),
            "state_semantics": _state_semantics(base),
            "currently_valid_actions": [
                _compact_affordance(item, trace) for item in base.available_actions()
            ],
            "required_json_shape": {
                "action": {"operation": "exact operation plus required fields"},
                "evidence": ["public fact supporting the repair"],
                "spectrum_interpretation": "retain only supported spectral conclusion",
                "rationale": "short repair summary",
                "hypothesis": "short testable expectation",
                "uncertainty": "number from 0 to 1",
                "uncertainty_note": "main source of uncertainty",
            },
        },
        ensure_ascii=False,
    )
    return client.complete_json(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=user_prompt,
        max_tokens=6000 if bool(getattr(client, "thinking", False)) else 1200,
    )


def _spectrum_input_summary(
    spectrum: dict[str, Any],
    *,
    decision_origin: str,
) -> dict[str, Any]:
    series = spectrum.get("series")
    safe_series = series if isinstance(series, list) else []
    return {
        "available": bool(spectrum.get("available")),
        "decision_origin": decision_origin,
        "disclosure": spectrum.get("disclosure"),
        "instrument": spectrum.get("instrument"),
        "kind": spectrum.get("kind"),
        "provenance": to_builtin(spectrum.get("provenance", {})),
        "series": [
            {
                "id": item.get("id"),
                "kind": item.get("kind"),
                "point_count": min(
                    len(item.get("x", [])),
                    len(item.get("y", [])),
                ),
                "peak_count": len(item.get("peaks", [])),
            }
            for item in safe_series
            if isinstance(item, dict)
        ],
    }


def _requested_spectrum_id(payload: dict[str, Any]) -> str | None:
    requested = payload.get("spectrum_request_id")
    if not isinstance(requested, str) or not requested.strip():
        return None
    return requested.strip()


def _spectrum_by_id(archive: list[dict[str, Any]], spectrum_id: str) -> dict[str, Any] | None:
    return next(
        (dict(item) for item in archive if str(item.get("spectrum_id") or "") == spectrum_id),
        None,
    )


def _spectrum_catalog_entry(spectrum: dict[str, Any]) -> dict[str, Any]:
    return {
        "spectrum_id": spectrum.get("spectrum_id"),
        "instrument": spectrum.get("instrument"),
        "kind": spectrum.get("kind"),
        "disclosure": spectrum.get("disclosure"),
        "provenance": to_builtin(spectrum.get("provenance", {})),
        "channel_count": len(spectrum.get("series") or []),
    }


def _spectrum_id(
    *,
    task_id: str,
    experiment_index: int,
    measurement_step: int,
    instrument: str,
) -> str:
    safe_instrument = "".join(
        character if character.isalnum() or character in {"-", "_"} else "-"
        for character in instrument.lower()
    ).strip("-")
    return (
        f"{task_id}:experiment-{experiment_index + 1}:"
        f"step-{measurement_step}:{safe_instrument or 'signal'}"
    )


def _state_semantics(base: Any) -> dict[str, Any]:
    campaign = base.campaign_state()
    episode_mode = str(campaign.get("episode_mode") or "single_experiment")
    return {
        "episode_mode": episode_mode,
        "current_experiment_index": int(campaign.get("experiment_index", 0)),
        "current_vessel": "operations apply to the current state until an experiment boundary",
        "experiment_boundary": (
            "successful final_assay ends a single experiment; in campaign mode it also "
            "starts the next experiment from its initial state"
        ),
        "measurement_effect": "instrument measurements can consume sample volume and budget",
    }


def _experiment_memory_record(
    *,
    experiment_index: int,
    score: float,
    trace: list[dict[str, Any]],
    final_visible_metrics: dict[str, Any],
) -> dict[str, Any]:
    actions = [dict(item.get("selected_action") or {}) for item in trace]
    conditions = [
        action
        for action in actions
        if action.get("operation") in {"add_solvent", "add_reagent", "add_catalyst", "heat", "wait"}
    ]
    measurements = [
        str(action.get("instrument"))
        for action in actions
        if action.get("operation") == "measure" and action.get("instrument")
    ]
    interpretations = [
        str(item.get("spectrum_interpretation"))
        for item in trace
        if item.get("spectrum_interpretation")
        and "no spectrum" not in str(item.get("spectrum_interpretation")).lower()
    ]
    return {
        "experiment_index": experiment_index,
        "final_score": score,
        "conditions": to_builtin(conditions),
        "measurements": measurements,
        "spectral_findings": interpretations[-2:],
        "discovery_intents": [
            str(item.get("experiment_intent")) for item in trace if item.get("experiment_intent")
        ][-3:],
        "final_visible_metrics": to_builtin(final_visible_metrics),
    }


def _plan_entries(payload: dict[str, Any]) -> list[dict[str, Any]]:
    actions = payload.get("actions")
    if not isinstance(actions, list) or not actions:
        raise ValueError("DeepSeek plan must contain a non-empty actions list")
    return [entry for entry in actions if isinstance(entry, dict)]


def _closeout_decision(base: Any) -> dict[str, Any] | None:
    final_assay = {"operation": "measure", "instrument": "final_assay"}
    if base.validate_action(final_assay).get("valid", False):
        return {
            "action": final_assay,
            "evidence": ["The model-selected experiment is ready for required scoring."],
            "spectrum_interpretation": "No new spectrum was interpreted by the harness.",
            "rationale": "Harness closeout: obtain the required official final assay.",
            "hypothesis": "The final assay will score the model-selected experimental state.",
            "experiment_intent": "measurement",
            "comparison_to_prior": "Harness closeout; no new condition selected.",
            "uncertainty": 1.0,
            "uncertainty_note": "Official assay result is not yet observed.",
        }
    terminate = {"operation": "terminate"}
    if base.validate_action(terminate).get("valid", False):
        return {
            "action": terminate,
            "evidence": ["Termination is currently valid and final assay is not yet valid."],
            "spectrum_interpretation": "No new spectrum was interpreted by the harness.",
            "rationale": "Harness closeout: terminate before the required final assay.",
            "hypothesis": "Termination will make the model-selected state assay-ready.",
            "experiment_intent": "measurement",
            "comparison_to_prior": "Harness closeout; no new condition selected.",
            "uncertainty": 1.0,
            "uncertainty_note": "The terminal assay has not been observed.",
        }
    return None


def _normalize_decision(payload: dict[str, Any]) -> dict[str, Any]:
    raw_action = payload.get("action")
    action = raw_action if isinstance(raw_action, dict) else payload
    if not isinstance(action, dict) or not action.get("operation"):
        raise ValueError("DeepSeek decision is missing action.operation")
    raw_evidence = payload.get("evidence")
    evidence = (
        [str(item) for item in raw_evidence[:6]]
        if isinstance(raw_evidence, list)
        else ["No structured evidence supplied."]
    )
    raw_uncertainty = payload.get("uncertainty", 1.0)
    uncertainty = (
        float(raw_uncertainty)
        if isinstance(raw_uncertainty, (int, float)) and not isinstance(raw_uncertainty, bool)
        else 1.0
    )
    return {
        "action": dict(action),
        "evidence": evidence,
        "spectrum_interpretation": str(
            payload.get("spectrum_interpretation") or "No spectrum interpretation supplied."
        ),
        "rationale": str(payload.get("rationale") or "No rationale supplied."),
        "hypothesis": str(payload.get("hypothesis") or "No hypothesis supplied."),
        "experiment_intent": str(payload.get("experiment_intent") or "unspecified"),
        "comparison_to_prior": str(
            payload.get("comparison_to_prior") or "No prior comparison supplied."
        ),
        "uncertainty": max(0.0, min(1.0, uncertainty)),
        "uncertainty_note": str(
            payload.get("uncertainty_note") or "Uncertainty was not characterized."
        ),
    }


def _compact_schema(schema: dict[str, Any]) -> dict[str, Any]:
    return {
        "operation": schema.get("operation"),
        "required_fields": schema.get("required_fields", []),
        "fields": schema.get("fields", []),
        "preconditions": schema.get("preconditions", []),
    }


def _compact_affordance(
    affordance: dict[str, Any],
    trace: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    aligned = aligned_affordance(affordance, trace or [])
    return {
        "operation": aligned.get("operation"),
        "schema": _compact_schema(aligned),
        "recipe_lock": aligned.get("recipe_lock"),
        "effect": {
            "type": aligned.get("effect", {}).get("type"),
            "summary": aligned.get("effect", {}).get("summary"),
        },
    }


def _disclose_lab_report(
    report: dict[str, Any],
    disclosure: SpectrumDisclosure,
) -> dict[str, Any]:
    disclosed = dict(report)
    summary = _disclose_spectra_summary(report.get("spectra_summary", {}), disclosure)
    disclosed["spectra_summary"] = {
        "has_spectral_packet": bool(summary.get("has_spectral_packet")),
        "instrument": summary.get("instrument"),
        "retrieval_required": bool(summary.get("has_spectral_packet")),
    }
    return disclosed


def _disclose_spectra_summary(
    summary: object,
    disclosure: SpectrumDisclosure,
) -> dict[str, Any]:
    public = dict(summary) if isinstance(summary, dict) else {}
    if disclosure == "assigned":
        return to_builtin(public)
    allowed = {
        "channel_count",
        "channels",
        "has_spectral_packet",
        "instrument",
        "observed_keys",
        "packet_kind",
        "warnings",
    }
    if disclosure == "unassigned":
        allowed.add("peak_table_count")
    return to_builtin({key: public[key] for key in allowed if key in public})


def _empty_usage() -> dict[str, int]:
    return {
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0,
        "prompt_cache_hit_tokens": 0,
        "prompt_cache_miss_tokens": 0,
    }


def _add_usage(total: dict[str, int], usage: dict[str, Any]) -> None:
    for key in total:
        value = usage.get(key, 0)
        if isinstance(value, int) and not isinstance(value, bool):
            total[key] += value


def _method_resources(
    *,
    client: JsonPlannerClient,
    usage: dict[str, Any],
    model_call_count: int,
) -> dict[str, Any]:
    pricing_factory = getattr(client, "pricing_snapshot", None)
    cost_factory = getattr(client, "estimate_cost_usd", None)
    pricing = pricing_factory() if callable(pricing_factory) else None
    accounting_complete = isinstance(pricing, dict) and callable(cost_factory)
    cost = float(cost_factory(usage)) if accounting_complete else 0.0
    prompt_hash = hashlib.sha256(
        (SYSTEM_PROMPT + "|chemworld-task-lab-adaptive-json-0.2").encode("utf-8")
    ).hexdigest()
    return {
        "schema_version": "chemworld-method-resource-usage-0.1",
        "accounting_complete": accounting_complete,
        "usage_source": "provider_usage_and_frozen_price_snapshot",
        "model_call_count": int(model_call_count),
        "input_token_count": int(usage.get("prompt_tokens", 0)),
        "output_token_count": int(usage.get("completion_tokens", 0)),
        "monetary_cost_usd": cost,
        "training_environment_step_count": 0,
        "cpu_time_s": 0.0,
        "gpu_time_s": 0.0,
        "model_provenance": {
            "provider": "DeepSeek",
            "model_id": client.model,
            "model_snapshot_or_access_date": (
                pricing.get("access_date") if isinstance(pricing, dict) else None
            ),
            "prompt_hash": prompt_hash,
            "request_parameters": {
                "response_format": "json_object",
                "thinking": bool(getattr(client, "thinking", False)),
                "reasoning_effort": getattr(client, "reasoning_effort", None),
            },
            "tokenizer_or_provider_usage_source": "DeepSeek response.usage",
            "pricing": pricing,
            "private_reasoning_retained": False,
        },
    }


__all__ = ["RunMode", "TaskRunResult", "run_task"]
