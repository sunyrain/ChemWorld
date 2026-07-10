"""Task Lab adapter for classical surrogate-model optimization agents."""

from __future__ import annotations

import json
from math import ceil, sqrt
from pathlib import Path
from typing import Any

from apps.task_lab.catalog import TASK_BACKGROUNDS
from apps.task_lab.experiment_audit import (
    audit_experiment_design,
    experiments_from_trajectory,
)
from apps.task_lab.runner import EventCallback, TaskRunResult
from apps.task_lab.spectral_payload import SpectrumDisclosure, spectral_payload
from chemworld.agents.base import HistoryRecord
from chemworld.data.logging import load_jsonl, to_builtin
from chemworld.eval.result_artifacts import build_verified_evaluation_result
from chemworld.eval.runner import make_agent, run_agent
from chemworld.tasks import TaskSpec, get_task

CLASSIC_AGENT_IDS = (
    "random_recipe",
    "latin_hypercube",
    "greedy_local",
    "gp_pi",
    "gp_ucb",
    "gp_bo",
    "rf_ei",
    "safe_gp_bo",
)
_RECIPE_OPERATIONS = {
    "add_solvent",
    "add_reagent",
    "add_catalyst",
    "heat",
    "terminate",
    "measure",
}


def run_classic_task(
    *,
    agent_id: str,
    task_id: str,
    output_dir: str | Path,
    seed: int | None = None,
    max_steps: int = 72,
    budget_multiplier: float = 1.0,
    campaign_override: bool = False,
    spectrum_disclosure: SpectrumDisclosure = "unassigned",
    event_callback: EventCallback | None = None,
) -> TaskRunResult:
    """Run one recipe-level active-learning baseline with Task Lab events."""

    if agent_id not in CLASSIC_AGENT_IDS:
        allowed = ", ".join(CLASSIC_AGENT_IDS)
        raise ValueError(f"agent_id must be one of: {allowed}")
    task = get_task(task_id)
    _validate_recipe_task(task)
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
    emit = event_callback or (lambda event: None)
    agent = make_agent(agent_id)
    background = TASK_BACKGROUNDS[task_id].to_dict()
    emit(
        {
            "type": "task_started",
            "task_id": task_id,
            "seed": selected_seed,
            "mode": "active_learning",
            "agent_backend": agent_id,
            "model": agent_id,
            "budget": effective_budget,
            "official_budget": task.budget,
            "contract_profile": contract_profile,
            "campaign_override": campaign_override,
            "spectrum_disclosure": spectrum_disclosure,
            "step_limit": step_limit,
            "background": background,
            "success_metrics": list(task.success_metrics),
        }
    )

    best_score: float | None = None
    final_assay_count = 0
    invalid_actions = 0
    emitted_trace_count = 0

    def on_step(record: HistoryRecord, agent_trace: list[dict[str, Any]]) -> None:
        nonlocal best_score, final_assay_count, invalid_actions, emitted_trace_count
        if len(agent_trace) > emitted_trace_count:
            for decision in agent_trace[emitted_trace_count:]:
                emit(_surrogate_event(task_id, decision))
            emitted_trace_count = len(agent_trace)
        info = record.info
        flags = dict(info.get("constraint_flags") or {})
        if flags.get("precondition_failed"):
            invalid_actions += 1
        score = info.get("leaderboard_score")
        if score is not None:
            final_assay_count += 1
            numeric_score = float(score)
            best_score = numeric_score if best_score is None else max(best_score, numeric_score)
        spectrum = spectral_payload(
            info.get("raw_signal", {}),
            instrument=info.get("instrument"),
            disclosure=spectrum_disclosure,
        )
        summaries = list(info.get("experiment_summaries") or [])
        emit(
            {
                "type": "step_completed",
                "task_id": task_id,
                "step": record.step,
                "budget": effective_budget,
                "step_limit": step_limit,
                "action": to_builtin(record.action),
                "rationale": "Execute the current recipe proposed by the active-learning policy.",
                "hypothesis": "This recipe will add a scored observation to the surrogate dataset.",
                "evidence": [
                    f"{len(summaries)} completed experiment summaries are publicly available.",
                    f"Current policy: {agent_id}.",
                ],
                "spectrum_interpretation": (
                    "The classical optimizer learns from final-assay responses; this signal "
                    "is displayed for audit but is not featurized by the surrogate."
                ),
                "uncertainty": None,
                "uncertainty_note": (
                    "See the acquisition value and trained recipe count in the "
                    "surrogate decision event."
                ),
                "spectrum": spectrum,
                "spectra_summary": to_builtin(info.get("processed_estimate", {})),
                "reward": float(record.reward),
                "leaderboard_score": score,
                "best_score": best_score,
                "remaining_budget": info.get("remaining_budget"),
                "experiment_index": info.get("experiment_index"),
                "final_assay_count": final_assay_count,
                "visible_metrics": to_builtin(info.get("processed_estimate", {})),
                "constraint_flags": to_builtin(flags),
                "recovery_suggestion": info.get("error_message"),
                "status": "rejected" if flags.get("precondition_failed") else "accepted",
            }
        )

    run_agent(
        env_id="ChemWorld",
        agent=agent,
        world_split=task.world_split,
        budget=step_limit,
        objective=task.objective,
        seed=selected_seed,
        task_id=task_id,
        output_path=trajectory_path,
        budget_override=effective_budget if contract_profile == "extended-research" else None,
        episode_mode_override="campaign" if campaign_override else None,
        step_callback=on_step,
    )

    records = load_jsonl(trajectory_path)
    experiment_design_audit = audit_experiment_design(experiments_from_trajectory(records))
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
    total_score = float(verified["total_score"]) if verified is not None else None
    final_assay_count = int(verified["final_assay_count"]) if verified is not None else 0
    observed_best = (
        float(verified["final_best_score"]) if verified is not None and final_assay_count else None
    )
    official_score = observed_best if contract_profile == "official" else None
    research_score = observed_best if contract_profile == "extended-research" else None
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
        model=agent_id,
        mode="active_learning",
        status=status,
        official_score=official_score,
        research_score=research_score,
        total_score=total_score,
        steps=len(records),
        final_assay_count=final_assay_count,
        invalid_plan_actions=invalid_actions,
        model_call_count=0,
        verified=bool(verified and verified.get("verified")),
        usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
        agent_backend=agent_id,
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


def _validate_recipe_task(task: TaskSpec) -> None:
    missing = sorted(_RECIPE_OPERATIONS - set(task.allowed_operations))
    if missing or "final_assay" not in task.allowed_instruments:
        detail = f" missing operations={missing}" if missing else ""
        raise ValueError(
            f"{task.task_id} is not compatible with recipe-level active learning;{detail}. "
            "Choose a reaction task whose contract supports solvent, reagent, catalyst, "
            "heat, terminate, and final assay."
        )


def supports_classic_task(task_id: str) -> bool:
    """Return whether the fixed recipe compiler satisfies a task contract."""

    task = get_task(task_id)
    return (
        _RECIPE_OPERATIONS.issubset(task.allowed_operations)
        and "final_assay" in task.allowed_instruments
    )


def _surrogate_event(task_id: str, decision: dict[str, Any]) -> dict[str, Any]:
    trained = int(decision.get("trained_recipe_count") or 0)
    phase = str(decision.get("phase") or "initial")
    policy = str(decision.get("selected_policy") or "unknown")
    acquisition = decision.get("acquisition_value")
    recipe = to_builtin(decision.get("selected_recipe") or {})
    if phase == "acquisition":
        rationale = f"Fit the surrogate to {trained} completed recipes and maximize {policy}."
    else:
        rationale = "Collect an initial design point before fitting the surrogate model."
    return {
        "type": "surrogate_decision",
        "task_id": task_id,
        "phase": phase,
        "trained_recipe_count": trained,
        "used_surrogate": bool(decision.get("used_surrogate")),
        "selected_policy": policy,
        "best_observed_score": decision.get("best_observed_score"),
        "acquisition_value": acquisition,
        "selected_recipe": recipe,
        "evidence": [
            f"Training set: {trained} completed recipes.",
            "Best observed score: "
            f"{decision.get('best_observed_score') if trained else 'not available yet'}.",
        ],
        "spectrum_interpretation": (
            "No spectral features are used by this classical baseline; it models the "
            "recipe-to-final-assay response."
        ),
        "hypothesis": f"The selected recipe is informative under {policy}.",
        "rationale": rationale,
        "uncertainty": min(1.0, 1.0 / sqrt(trained + 1)),
        "uncertainty_note": (
            f"Acquisition value: {float(acquisition):.6g}."
            if isinstance(acquisition, int | float)
            else "Initial-design phase; no fitted acquisition value yet."
        ),
    }


__all__ = ["CLASSIC_AGENT_IDS", "run_classic_task", "supports_classic_task"]
