"""Formal benchmark task registry for the unified ChemWorld."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from chemworld.physchem.maturity import (
    MaturityLevel,
    ModuleMaturity,
    TaskMaturitySpec,
    validate_task_maturity_policy,
)
from chemworld.registration import ENV_ID
from chemworld.world.operations import (
    CRYSTALLIZATION_OPERATIONS,
    DISTILLATION_OPERATIONS,
    ELECTROCHEMISTRY_OPERATIONS,
    FLOW_OPERATIONS,
    INSTRUMENTS,
    OPERATION_TYPES,
    REACTION_OPERATIONS,
)
from chemworld.world.scenario import get_scenario_card

WORLD_LAW_ID = "chemworld-physical-chemistry"
REACTION_ALLOWED = REACTION_OPERATIONS
REACTION_SEPARATION_ALLOWED = OPERATION_TYPES
REACTION_CRYSTALLIZATION_ALLOWED = (*REACTION_OPERATIONS, *CRYSTALLIZATION_OPERATIONS)
REACTION_DISTILLATION_ALLOWED = (*REACTION_OPERATIONS, *DISTILLATION_OPERATIONS)
FLOW_REACTION_ALLOWED = (
    "add_solvent",
    "add_reagent",
    "add_catalyst",
    *FLOW_OPERATIONS,
    "measure",
    "terminate",
)
ELECTROCHEMISTRY_ALLOWED = (
    "add_solvent",
    "add_reagent",
    *ELECTROCHEMISTRY_OPERATIONS,
    "measure",
    "terminate",
)
PARTITION_ALLOWED = (
    "add_solvent",
    "add_reagent",
    "add_phase",
    "add_extractant",
    "mix",
    "settle",
    "separate_phase",
    "measure",
    "terminate",
)
REFERENCE_BASELINES = (
    "random",
    "lhs",
    "scripted_chemistry",
    "gp_bo",
    "safe_gp_bo",
)


@dataclass(frozen=True)
class TaskSpec:
    task_id: str
    env_id: str
    world_law_id: str
    scenario_id: str
    initial_state_id: str
    world_split: str
    objective: str
    budget: int
    seeds: tuple[int, ...]
    threshold: float
    episode_mode: str
    allowed_operations: tuple[str, ...]
    allowed_instruments: tuple[str, ...]
    observation_policy: str
    termination_policy: str
    success_metrics: tuple[str, ...]
    safety_limit: float
    difficulty: str
    description: str
    tags: tuple[str, ...]
    kernel_maturity: TaskMaturitySpec

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "env_id": self.env_id,
            "world_law_id": self.world_law_id,
            "scenario_id": self.scenario_id,
            "initial_state_id": self.initial_state_id,
            "world_split": self.world_split,
            "objective": self.objective,
            "budget": self.budget,
            "seeds": list(self.seeds),
            "threshold": self.threshold,
            "episode_mode": self.episode_mode,
            "allowed_operations": list(self.allowed_operations),
            "allowed_instruments": list(self.allowed_instruments),
            "observation_policy": self.observation_policy,
            "termination_policy": self.termination_policy,
            "success_metrics": list(self.success_metrics),
            "safety_limit": self.safety_limit,
            "difficulty": self.difficulty,
            "description": self.description,
            "tags": list(self.tags),
            "kernel_maturity": self.kernel_maturity.to_dict(),
            "physics_maturity": self.kernel_maturity.lowest_level.value,
            "proxy_allowed": self.kernel_maturity.proxy_allowed,
        }

    def __post_init__(self) -> None:
        validate_task_maturity_policy(
            task_id=self.task_id,
            tags=self.tags,
            maturity=self.kernel_maturity,
        )

    def env_kwargs(self, *, seed: int | None = None) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "world_split": self.world_split,
            "budget": self.budget,
            "objective": self.objective,
            "seed": self.seeds[0] if seed is None else seed,
        }

    def to_card(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "scientific_motivation": self.description,
            "world_law_id": self.world_law_id,
            "scenario_id": self.scenario_id,
            "allowed_operations": list(self.allowed_operations),
            "allowed_instruments": list(self.allowed_instruments),
            "budget": self.budget,
            "episode_mode": self.episode_mode,
            "reward_leaderboard_metric": {
                "online_reward": "observed score from instrument-visible estimates",
                "leaderboard_score": "final-assay score only",
                "success_metrics": list(self.success_metrics),
            },
            "observation_policy": self.observation_policy,
            "termination_policy": self.termination_policy,
            "public_seeds": list(self.seeds)
            if self.world_split != "private-eval"
            else "maintainer-controlled",
            "private_seeds": "maintainer-controlled",
            "baseline_reference_scores": dict.fromkeys(REFERENCE_BASELINES),
            "reference_baselines": list(REFERENCE_BASELINES),
            "recommended_agent_families": self._recommended_agent_families(),
            "scenario_card": get_scenario_card(self.scenario_id, split=self.world_split),
            "kernel_maturity": self.kernel_maturity.to_dict(),
            "physics_maturity": self.kernel_maturity.lowest_level.value,
            "proxy_allowed": self.kernel_maturity.proxy_allowed,
            "failure_modes": self._failure_modes(),
            "recommended_use": self._recommended_use(),
            "safety_limit": self.safety_limit,
            "difficulty": self.difficulty,
            "tags": list(self.tags),
        }

    def _failure_modes(self) -> list[str]:
        modes = ["invalid operation preconditions", "unsafe or high-cost trajectory"]
        if "separation" in self.tags or "purification" in self.tags:
            modes.extend(["poor phase split", "low recovery", "mass-balance drift"])
        if "explanation" in self.tags or "mechanism" in self.tags:
            modes.append("weak or unsupported mechanism explanation")
        if "private-eval" in self.tags:
            modes.append("public-world overfitting")
        return modes

    def _recommended_use(self) -> list[str]:
        use = ["benchmark"]
        if "smoke" in self.tags:
            use.append("teaching")
        if "llm-agent" in self.tags or "explanation" in self.tags:
            use.append("LLM-agent")
        if "optimization" in self.tags or "sample-efficiency" in self.tags:
            use.extend(["BO", "RL"])
        return sorted(set(use))

    def _recommended_agent_families(self) -> list[str]:
        families = ["random", "scripted"]
        if "optimization" in self.tags or "sample-efficiency" in self.tags:
            families.extend(["lhs", "gp_bo", "safe_gp_bo"])
        if "separation" in self.tags or "purification" in self.tags:
            families.append("scripted_reaction_to_purification")
        if "llm-agent" in self.tags or "explanation" in self.tags:
            families.extend(["llm_replay", "tool_using_llm_stub"])
        return sorted(set(families))


def _task(
    task_id: str,
    *,
    scenario_id: str,
    world_split: str,
    objective: str = "balanced",
    budget: int,
    seeds: tuple[int, ...],
    threshold: float,
    episode_mode: str = "single_experiment",
    allowed_operations: tuple[str, ...],
    success_metrics: tuple[str, ...],
    safety_limit: float = 0.65,
    difficulty: str = "standard",
    description: str,
    tags: tuple[str, ...],
    instruments: tuple[str, ...] = INSTRUMENTS,
    observation_policy: str = "partial-instrument-observation",
    termination_policy: str | None = None,
    kernel_maturity: TaskMaturitySpec | None = None,
) -> TaskSpec:
    resolved_termination_policy = (
        termination_policy
        if termination_policy is not None
        else ("budget" if episode_mode == "campaign" else "final-assay-or-budget")
    )
    resolved_kernel_maturity = kernel_maturity or default_kernel_maturity(
        allowed_operations
    )
    resolved_tags = ("chemworld", *tags)
    if (
        resolved_kernel_maturity.contains_proxy
        and not set(resolved_tags).intersection({"teaching", "smoke", "exploratory"})
    ):
        resolved_tags = (*resolved_tags, "exploratory")
    return TaskSpec(
        task_id=task_id,
        env_id=ENV_ID,
        world_law_id=WORLD_LAW_ID,
        scenario_id=scenario_id,
        initial_state_id=f"{scenario_id}:default",
        world_split=world_split,
        objective=objective,
        budget=budget,
        seeds=seeds,
        threshold=threshold,
        episode_mode=episode_mode,
        allowed_operations=allowed_operations,
        allowed_instruments=instruments,
        observation_policy=observation_policy,
        termination_policy=resolved_termination_policy,
        success_metrics=success_metrics,
        safety_limit=safety_limit,
        difficulty=difficulty,
        description=description,
        tags=resolved_tags,
        kernel_maturity=resolved_kernel_maturity,
    )


def default_kernel_maturity(
    allowed_operations: tuple[str, ...],
) -> TaskMaturitySpec:
    operations = set(allowed_operations)
    modules = [
        ModuleMaturity(
            "reaction_kinetics",
            MaturityLevel.LITE,
            model_ids=("chemworld_reaction_network_lite",),
            notes=(
                "Local stoichiometric reaction-network and rate-law engine; "
                "not yet Cantera-comparable.",
            ),
        ),
        ModuleMaturity(
            "reactors",
            MaturityLevel.LITE,
            model_ids=("chemworld_reactor_lite",),
            notes=("Batch/CSTR/PFR kernels are benchmark ODE models.",),
        ),
        ModuleMaturity(
            "spectroscopy_instruments",
            MaturityLevel.LITE,
            model_ids=("chemworld_synthetic_instruments", "beer_lambert_uvvis"),
            notes=(
                "State-coupled synthetic observations with a reference-validated "
                "Beer-Lambert UV-vis slice; not empirical spectral prediction.",
            ),
        ),
    ]
    if operations.intersection({"add_phase", "add_extractant", "mix", "settle"}):
        modules.append(
            ModuleMaturity(
                "phase_equilibrium",
                MaturityLevel.LITE,
                model_ids=("chemworld_phase_equilibrium_lite",),
                notes=("Raoult/Rachford-Rice/LLE-lite models with partial validation.",),
            )
        )
    if operations.intersection(CRYSTALLIZATION_OPERATIONS):
        modules.append(
            ModuleMaturity(
                "crystallization",
                MaturityLevel.PROXY,
                model_ids=("chemworld_crystallization_proxy",),
                notes=("Crystallization is a material-conserving benchmark proxy.",),
            )
        )
    if operations.intersection(DISTILLATION_OPERATIONS):
        modules.append(
            ModuleMaturity(
                "distillation",
                MaturityLevel.REFERENCE_VALIDATED,
                model_ids=("vle_shortcut_distillation",),
                notes=(
                    "Distillation uses a VLE-coupled constant-relative-volatility "
                    "shortcut model with analytical Fenske identity tests.",
                ),
            )
        )
    if operations.intersection(FLOW_OPERATIONS):
        modules.append(
            ModuleMaturity(
                "continuous_flow",
                MaturityLevel.PROXY,
                model_ids=("chemworld_continuous_flow_proxy",),
                notes=("Continuous-flow behavior is a projection of the shared reaction law.",),
            )
        )
    if operations.intersection(ELECTROCHEMISTRY_OPERATIONS):
        modules.append(
            ModuleMaturity(
                "electrochemistry",
                MaturityLevel.PROXY,
                model_ids=("chemworld_electrochemistry_proxy",),
                notes=("Electrochemistry lacks Butler-Volmer and charge accounting.",),
            )
        )
    if operations.intersection({"separate_phase", "wash", "dry", "concentrate"}):
        modules.append(
            ModuleMaturity(
                "separations",
                MaturityLevel.PROXY,
                model_ids=("chemworld_separation_proxy",),
                notes=("Downstream purification uses material-conserving proxy units.",),
            )
        )
    proxy_allowed = any(module.level is MaturityLevel.PROXY for module in modules)
    notes = (
        "Current task maturity is alpha/lite; professional hardening is tracked in "
        "TODO_PROFESSIONAL.md.",
    )
    return TaskMaturitySpec(
        modules=tuple(modules),
        proxy_allowed=proxy_allowed,
        notes=notes,
    )


TASK_REGISTRY: dict[str, TaskSpec] = {
    "reaction-optimization-standard": _task(
        "reaction-optimization-standard",
        scenario_id="reaction-optimization",
        world_split="public-test",
        budget=72,
        seeds=(0, 1, 2, 3, 4),
        threshold=0.75,
        episode_mode="campaign",
        allowed_operations=REACTION_ALLOWED,
        success_metrics=("score", "yield", "selectivity", "sample_efficiency"),
        description="Primary reaction optimization task in the shared ChemWorld law.",
        tags=("reaction", "optimization", "public-test"),
    ),
    "reaction-safety-constrained": _task(
        "reaction-safety-constrained",
        scenario_id="reaction-safety",
        world_split="public-test",
        objective="safe",
        budget=72,
        seeds=(0, 1, 2, 3, 4),
        threshold=0.70,
        episode_mode="campaign",
        allowed_operations=REACTION_ALLOWED,
        success_metrics=("score", "safety_risk", "constraint_violations"),
        safety_limit=0.35,
        description="Reaction optimization under a stricter safety-risk target.",
        tags=("reaction", "safety", "public-test"),
    ),
    "reaction-mechanism-explanation": _task(
        "reaction-mechanism-explanation",
        scenario_id="reaction-mechanism",
        world_split="public-test",
        budget=36,
        seeds=(0, 1, 2),
        threshold=0.68,
        episode_mode="campaign",
        allowed_operations=REACTION_ALLOWED,
        success_metrics=("score", "mechanism_explanation", "failure_analysis"),
        description="Optimize while producing structured hypotheses about hidden kinetics.",
        tags=("reaction", "explanation", "mechanism"),
    ),
    "reaction-to-assay": _task(
        "reaction-to-assay",
        scenario_id="reaction-to-assay",
        world_split="public-dev",
        budget=18,
        seeds=(0,),
        threshold=0.55,
        episode_mode="single_experiment",
        allowed_operations=REACTION_ALLOWED,
        success_metrics=("final_assay_score", "trajectory_validity"),
        difficulty="smoke",
        description="Short event-sequence task from charging the reactor to final assay.",
        tags=("reaction", "assay", "smoke"),
    ),
    "reaction-to-purification": _task(
        "reaction-to-purification",
        scenario_id="reaction-to-purification",
        world_split="public-test",
        budget=90,
        seeds=(0, 1, 2, 3, 4),
        threshold=0.70,
        episode_mode="single_experiment",
        allowed_operations=REACTION_SEPARATION_ALLOWED,
        success_metrics=("score", "purity", "recovery", "process_mass_balance_error"),
        description="Closed-loop reaction, extraction, phase separation, purification, and assay.",
        tags=("reaction", "separation", "purification"),
    ),
    "reaction-to-crystallization": _task(
        "reaction-to-crystallization",
        scenario_id="reaction-to-crystallization",
        world_split="public-test",
        budget=72,
        seeds=(0, 1, 2),
        threshold=0.66,
        episode_mode="single_experiment",
        allowed_operations=REACTION_CRYSTALLIZATION_ALLOWED,
        success_metrics=("score", "crystal_yield", "crystal_purity", "crystal_size"),
        description="Run a reaction and isolate product through seeded cooling crystallization.",
        tags=("reaction", "crystallization", "purification", "year2"),
    ),
    "reaction-to-distillation": _task(
        "reaction-to-distillation",
        scenario_id="reaction-to-distillation",
        world_split="public-test",
        budget=72,
        seeds=(0, 1, 2),
        threshold=0.64,
        episode_mode="single_experiment",
        allowed_operations=REACTION_DISTILLATION_ALLOWED,
        success_metrics=("score", "distillate_purity", "distillate_recovery", "solvent_loss"),
        description="Run a reaction and evaluate volatile-product recovery through distillation.",
        tags=("reaction", "distillation", "purification", "year2"),
    ),
    "flow-reaction-optimization": _task(
        "flow-reaction-optimization",
        scenario_id="flow-reaction-optimization",
        world_split="public-test",
        budget=60,
        seeds=(0, 1, 2),
        threshold=0.64,
        episode_mode="campaign",
        allowed_operations=FLOW_REACTION_ALLOWED,
        success_metrics=("score", "flow_conversion", "yield", "safety_risk"),
        description="Optimize a continuous-flow projection of the shared reaction law.",
        tags=("reaction", "continuous-flow", "optimization", "year2"),
    ),
    "electrochemical-conversion": _task(
        "electrochemical-conversion",
        scenario_id="electrochemical-conversion",
        world_split="public-test",
        budget=48,
        seeds=(0, 1, 2),
        threshold=0.58,
        episode_mode="campaign",
        allowed_operations=ELECTROCHEMISTRY_ALLOWED,
        success_metrics=(
            "score",
            "electrochemical_selectivity",
            "energy_efficiency",
            "safety_risk",
        ),
        description="Probe potential/current choices for a virtual electrochemical conversion.",
        tags=("reaction", "electrochemistry", "optimization", "year2"),
    ),
    "partition-discovery": _task(
        "partition-discovery",
        scenario_id="partition-discovery",
        world_split="public-test",
        budget=48,
        seeds=(0, 1, 2),
        threshold=0.60,
        episode_mode="campaign",
        allowed_operations=PARTITION_ALLOWED,
        success_metrics=("phase_ratio", "product_in_organic", "product_in_aqueous"),
        description="Learn unknown solvent/product partition behavior through instruments.",
        tags=("phase", "partition", "world-model-learning"),
    ),
    "purity-yield-tradeoff": _task(
        "purity-yield-tradeoff",
        scenario_id="purity-yield-tradeoff",
        world_split="public-test",
        budget=90,
        seeds=(0, 1, 2, 3, 4),
        threshold=0.70,
        episode_mode="campaign",
        allowed_operations=REACTION_SEPARATION_ALLOWED,
        success_metrics=("yield", "purity", "recovery", "cost"),
        description="Optimize the downstream tradeoff between product purity, recovery, and cost.",
        tags=("separation", "multi-objective", "purification"),
    ),
    "public-private-generalization": _task(
        "public-private-generalization",
        scenario_id="generalization",
        world_split="private-eval",
        budget=72,
        seeds=(0, 1, 2, 3, 4),
        threshold=0.72,
        episode_mode="campaign",
        allowed_operations=REACTION_ALLOWED,
        success_metrics=("score", "public_private_gap", "rank_confidence"),
        description="Private-split task for evaluating overfitting to public worlds.",
        tags=("reaction", "private-eval", "generalization"),
    ),
    "low-budget-characterization": _task(
        "low-budget-characterization",
        scenario_id="low-budget-characterization",
        world_split="public-test",
        budget=18,
        seeds=(0, 1, 2),
        threshold=0.55,
        episode_mode="campaign",
        allowed_operations=REACTION_ALLOWED,
        success_metrics=("sample_efficiency", "uncertainty", "local_model_quality"),
        difficulty="hard",
        description="Build a useful local world model with very few measurements.",
        tags=("reaction", "sample-efficiency", "low-budget"),
    ),
    "tool-agent-planning": _task(
        "tool-agent-planning",
        scenario_id="tool-agent-planning",
        world_split="public-dev",
        budget=48,
        seeds=(0, 1),
        threshold=0.62,
        episode_mode="single_experiment",
        allowed_operations=REACTION_SEPARATION_ALLOWED,
        success_metrics=("trajectory_validity", "validator_use", "score", "explanation"),
        description=(
            "Task slice for LLM/tool agents that use validators, instruments, "
            "and surrogates."
        ),
        tags=("llm-agent", "tool-use", "planning"),
    ),
}


def list_tasks() -> list[TaskSpec]:
    return [TASK_REGISTRY[key] for key in sorted(TASK_REGISTRY)]


def list_task_cards() -> list[dict[str, Any]]:
    return [task.to_card() for task in list_tasks()]


def get_task(task_id: str) -> TaskSpec:
    try:
        return TASK_REGISTRY[task_id]
    except KeyError as exc:
        allowed = ", ".join(sorted(TASK_REGISTRY))
        raise ValueError(f"Unknown task_id={task_id!r}. Allowed: {allowed}") from exc


def get_task_card(task_id: str) -> dict[str, Any]:
    return get_task(task_id).to_card()
