"""Machine-readable readiness contracts for serious benchmark tasks."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from chemworld.physchem.maturity import MaturityLevel
from chemworld.tasks import SERIOUS_TASK_IDS, TaskSpec, get_task
from chemworld.world.operations import PUBLIC_OBSERVATION_KEYS
from chemworld.world.parameters import WORLD_FAMILY_VERSION

TASK_DESIGN_VERSION = "chemworld-serious-task-design-0.1"
SERIOUS_GENERALIZATION_CONTRACTS: dict[str, tuple[dict[str, Any], ...]] = {
    "partition-discovery": (
        {
            "label": "distribution coefficient",
            "hidden_drivers": ("solvent family", "partition-law seed"),
            "evaluation": "frozen-seed stratification and private-salt shift",
        },
        {
            "label": "phase-volume ratio",
            "hidden_drivers": ("aqueous volume", "organic volume"),
            "evaluation": "task-recipe response-surface audit",
        },
    ),
    "reaction-to-crystallization": (
        {
            "label": "kinetic profile",
            "hidden_drivers": ("rate constants", "catalyst and solvent effects"),
            "evaluation": "frozen-seed stratification and private-salt shift",
        },
        {
            "label": "solubility and cooling profile",
            "hidden_drivers": ("solubility curve", "cooling duration and endpoint"),
            "evaluation": "task-recipe response-surface audit",
        },
    ),
    "reaction-to-distillation": (
        {
            "label": "relative volatility",
            "hidden_drivers": ("VLE policy", "temperature and reflux"),
            "evaluation": "frozen-seed stratification and response-surface audit",
        },
        {
            "label": "reaction selectivity",
            "hidden_drivers": ("rate constants", "catalyst and solvent effects"),
            "evaluation": "frozen-seed stratification and private-salt shift",
        },
    ),
    "flow-reaction-optimization": (
        {
            "label": "reaction kinetics",
            "hidden_drivers": ("rate constants", "activation energies"),
            "evaluation": "frozen-seed stratification and private-salt shift",
        },
        {
            "label": "residence time and thermal boundary",
            "hidden_drivers": ("flow rate", "residence time", "heat transfer"),
            "evaluation": "task-recipe response-surface audit",
        },
    ),
    "electrochemical-conversion": (
        {
            "label": "redox kinetics",
            "hidden_drivers": ("redox scenario seed", "potential and current"),
            "evaluation": "frozen-seed stratification and private-salt shift",
        },
        {
            "label": "mass-transfer and resistance regime",
            "hidden_drivers": ("transport policy", "cell resistance"),
            "evaluation": "task-recipe response-surface audit",
        },
    ),
    "equilibrium-characterization": (
        {
            "label": "acid-base constants",
            "hidden_drivers": ("hidden pKa", "solution composition"),
            "evaluation": "frozen-seed stratification and private-salt shift",
        },
        {
            "label": "solubility-product regime",
            "hidden_drivers": ("hidden Ksp", "concentration"),
            "evaluation": "task-recipe response-surface audit",
        },
    ),
}
EXECUTABLE_EVALUATION_METRICS = frozenset(
    {
        *PUBLIC_OBSERVATION_KEYS,
        "total_score",
        "safety_aware_score",
        "cost_aware_score",
        "sample_efficiency_step",
        "invalid_action_rate",
        "area_under_best_score",
        "campaign_area_under_best_score",
    }
)


@dataclass(frozen=True)
class SeriousTaskDesign:
    task_id: str
    research_question: str
    capability_claim: str
    primary_metric: str
    secondary_metrics: tuple[str, ...]
    generalization_axes: tuple[str, ...]
    required_baselines: tuple[str, ...]
    required_evidence: tuple[str, ...]
    anti_gaming_checks: tuple[str, ...]
    minimum_maturity: MaturityLevel = MaturityLevel.LITE
    allow_proxy: bool = False
    status: str = "candidate"

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "minimum_maturity",
            MaturityLevel.normalize(self.minimum_maturity),
        )
        for name in ("task_id", "research_question", "capability_claim", "primary_metric"):
            if not str(getattr(self, name)).strip():
                raise ValueError(f"{name} cannot be empty")
        if self.status not in {"candidate", "validated"}:
            raise ValueError("status must be 'candidate' or 'validated'")

    def to_dict(self) -> dict[str, Any]:
        return {
            "design_version": TASK_DESIGN_VERSION,
            "task_id": self.task_id,
            "research_question": self.research_question,
            "capability_claim": self.capability_claim,
            "primary_metric": self.primary_metric,
            "secondary_metrics": list(self.secondary_metrics),
            "generalization_axes": list(self.generalization_axes),
            "required_baselines": list(self.required_baselines),
            "required_evidence": list(self.required_evidence),
            "anti_gaming_checks": list(self.anti_gaming_checks),
            "minimum_maturity": self.minimum_maturity.value,
            "allow_proxy": self.allow_proxy,
            "status": self.status,
        }


@dataclass(frozen=True)
class TaskDesignCheck:
    check_id: str
    passed: bool
    message: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "check_id": self.check_id,
            "passed": self.passed,
            "message": self.message,
        }


@dataclass(frozen=True)
class TaskDesignReview:
    task_id: str
    checks: tuple[TaskDesignCheck, ...]
    empirical_status: str

    @property
    def contract_ready(self) -> bool:
        return all(check.passed for check in self.checks)

    @property
    def benchmark_ready(self) -> bool:
        return self.contract_ready and self.empirical_status == "validated"

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "contract_ready": self.contract_ready,
            "benchmark_ready": self.benchmark_ready,
            "empirical_status": self.empirical_status,
            "checks": [check.to_dict() for check in self.checks],
        }


def review_task_design(
    task: TaskSpec,
    design: SeriousTaskDesign,
    *,
    empirical_status: str | None = None,
) -> TaskDesignReview:
    """Evaluate whether a task has an executable, non-proxy research contract."""

    success_metrics = set(task.success_metrics)
    declared_metrics = {design.primary_metric, *design.secondary_metrics}
    unsupported_metrics = sorted(success_metrics - EXECUTABLE_EVALUATION_METRICS)
    missing_declared_metrics = sorted(declared_metrics - success_metrics)
    maturity = task.kernel_maturity.lowest_level
    generalization_contract = SERIOUS_GENERALIZATION_CONTRACTS.get(task.task_id, ())
    checks = (
        TaskDesignCheck(
            "identity",
            task.task_id == design.task_id,
            "design and task ids must match",
        ),
        TaskDesignCheck(
            "world_law",
            task.world_law_id == WORLD_FAMILY_VERSION,
            "task must use the current frozen world law",
        ),
        TaskDesignCheck(
            "public_evaluation_split",
            task.world_split == "public-test",
            "candidate tasks require a reproducible public-test split",
        ),
        TaskDesignCheck(
            "seed_depth",
            len(task.seeds) >= 5,
            "at least five frozen seeds are required for the serious suite",
        ),
        TaskDesignCheck(
            "decision_horizon",
            task.budget >= 24,
            "budget must support a non-trivial decision horizon",
        ),
        TaskDesignCheck(
            "campaign_learning",
            task.episode_mode == "campaign",
            "serious tasks must permit observation, learning, and a later experiment",
        ),
        TaskDesignCheck(
            "metric_implementation",
            not unsupported_metrics,
            f"unsupported success metrics: {unsupported_metrics}",
        ),
        TaskDesignCheck(
            "metric_alignment",
            not missing_declared_metrics,
            f"design metrics absent from task contract: {missing_declared_metrics}",
        ),
        TaskDesignCheck(
            "final_assay",
            "final_assay" in task.allowed_instruments,
            "serious tasks require a final hidden-state assay boundary",
        ),
        TaskDesignCheck(
            "maturity_floor",
            maturity.rank >= design.minimum_maturity.rank,
            f"task maturity {maturity.value} must meet {design.minimum_maturity.value}",
        ),
        TaskDesignCheck(
            "proxy_policy",
            design.allow_proxy or not task.kernel_maturity.proxy_allowed,
            "proxy modules are excluded from the serious candidate suite",
        ),
        TaskDesignCheck(
            "baseline_diversity",
            len(design.required_baselines) >= 3
            and "random" in design.required_baselines
            and any(
                name in design.required_baselines
                for name in ("gp_bo", "safe_gp_bo", "scripted_chemistry")
            ),
            "require random plus at least two informative baselines",
        ),
        TaskDesignCheck(
            "generalization_axes",
            len(design.generalization_axes) >= 2,
            "at least two explicit generalization axes are required",
        ),
        TaskDesignCheck(
            "generalization_contract",
            tuple(item.get("label") for item in generalization_contract)
            == design.generalization_axes
            and all(item.get("hidden_drivers") for item in generalization_contract)
            and all(item.get("evaluation") for item in generalization_contract),
            "generalization axes require hidden drivers and an executable audit mode",
        ),
        TaskDesignCheck(
            "evidence_plan",
            len(design.required_evidence) >= 3,
            "task design requires baseline, replay, and failure-analysis evidence",
        ),
        TaskDesignCheck(
            "anti_gaming",
            len(design.anti_gaming_checks) >= 2,
            "at least two anti-gaming checks are required",
        ),
    )
    return TaskDesignReview(
        task.task_id,
        checks,
        design.status if empirical_status is None else empirical_status,
    )


_COMMON_BASELINES = (
    "random",
    "lhs",
    "gp_bo",
    "structured_gp_bo",
    "structured_safe_gp_bo",
)
_COMMON_EVIDENCE = (
    "multi-seed baseline confidence intervals",
    "deterministic replay verification",
    "per-task failure and constraint analysis",
)
_COMMON_ANTI_GAMING = (
    "reject hidden-state access and contract-hash drift",
    "score final-assay results separately from intermediate observations",
)

SERIOUS_TASK_DESIGNS: dict[str, SeriousTaskDesign] = {
    "partition-discovery": SeriousTaskDesign(
        task_id="partition-discovery",
        research_question="Can an agent identify a hidden partition law with few contacts?",
        capability_claim="active phase-equilibrium characterization under a budget",
        primary_metric="product_in_organic",
        secondary_metrics=("phase_ratio", "product_in_aqueous"),
        generalization_axes=("distribution coefficient", "phase-volume ratio"),
        required_baselines=_COMMON_BASELINES,
        required_evidence=_COMMON_EVIDENCE,
        anti_gaming_checks=_COMMON_ANTI_GAMING,
    ),
    "reaction-to-crystallization": SeriousTaskDesign(
        task_id="reaction-to-crystallization",
        research_question="Can an agent balance reaction quality, recovery, purity, and CSD?",
        capability_claim="closed-loop reaction and cooling-crystallization planning",
        primary_metric="crystal_yield",
        secondary_metrics=("score", "crystal_purity", "crystal_size"),
        generalization_axes=("kinetic profile", "solubility and cooling profile"),
        required_baselines=_COMMON_BASELINES,
        required_evidence=_COMMON_EVIDENCE,
        anti_gaming_checks=_COMMON_ANTI_GAMING,
    ),
    "reaction-to-distillation": SeriousTaskDesign(
        task_id="reaction-to-distillation",
        research_question="Can an agent choose reaction and cut conditions jointly?",
        capability_claim="reaction-distillation trade-off reasoning",
        primary_metric="distillate_purity",
        secondary_metrics=("score", "distillate_recovery", "solvent_loss"),
        generalization_axes=("relative volatility", "reaction selectivity"),
        required_baselines=_COMMON_BASELINES,
        required_evidence=_COMMON_EVIDENCE,
        anti_gaming_checks=_COMMON_ANTI_GAMING,
    ),
    "flow-reaction-optimization": SeriousTaskDesign(
        task_id="flow-reaction-optimization",
        research_question="Can an agent optimize conversion without ignoring flow risk?",
        capability_claim="geometry-aware continuous-flow optimization",
        primary_metric="flow_conversion",
        secondary_metrics=("score", "yield", "safety_risk"),
        generalization_axes=("reaction kinetics", "residence time and thermal boundary"),
        required_baselines=_COMMON_BASELINES,
        required_evidence=_COMMON_EVIDENCE,
        anti_gaming_checks=_COMMON_ANTI_GAMING,
    ),
    "electrochemical-conversion": SeriousTaskDesign(
        task_id="electrochemical-conversion",
        research_question="Can an agent trade selectivity against electrical efficiency?",
        capability_claim="electrochemical control under transport and energy constraints",
        primary_metric="electrochemical_selectivity",
        secondary_metrics=("score", "energy_efficiency", "safety_risk"),
        generalization_axes=("redox kinetics", "mass-transfer and resistance regime"),
        required_baselines=_COMMON_BASELINES,
        required_evidence=_COMMON_EVIDENCE,
        anti_gaming_checks=_COMMON_ANTI_GAMING,
    ),
    "equilibrium-characterization": SeriousTaskDesign(
        task_id="equilibrium-characterization",
        research_question="Can an agent characterize hidden aqueous equilibrium efficiently?",
        capability_claim="instrument-budgeted equilibrium identification",
        primary_metric="equilibrium_confidence",
        secondary_metrics=(
            "pH_normalized",
            "acid_dissociation_fraction",
            "precipitation_signal",
            "equilibrium_residual",
        ),
        generalization_axes=("acid-base constants", "solubility-product regime"),
        required_baselines=_COMMON_BASELINES,
        required_evidence=_COMMON_EVIDENCE,
        anti_gaming_checks=_COMMON_ANTI_GAMING,
    ),
}


def serious_task_readiness_manifest() -> dict[str, Any]:
    from chemworld.eval.benchmark_validation import official_empirical_statuses

    empirical_statuses = official_empirical_statuses()
    reviews = {
        task_id: review_task_design(
            get_task(task_id),
            SERIOUS_TASK_DESIGNS[task_id],
            empirical_status=empirical_statuses[task_id],
        )
        for task_id in SERIOUS_TASK_IDS
    }
    benchmark_ready_count = sum(review.benchmark_ready for review in reviews.values())
    return {
        "schema_version": TASK_DESIGN_VERSION,
        "suite_status": (
            "validated" if benchmark_ready_count == len(SERIOUS_TASK_IDS) else "candidate"
        ),
        "task_ids": list(SERIOUS_TASK_IDS),
        "contract_ready_count": sum(review.contract_ready for review in reviews.values()),
        "benchmark_ready_count": benchmark_ready_count,
        "designs": {
            task_id: {
                **SERIOUS_TASK_DESIGNS[task_id].to_dict(),
                "status": reviews[task_id].empirical_status,
                "generalization_contract": [
                    {
                        **axis,
                        "hidden_drivers": list(axis["hidden_drivers"]),
                    }
                    for axis in SERIOUS_GENERALIZATION_CONTRACTS[task_id]
                ],
            }
            for task_id in SERIOUS_TASK_IDS
        },
        "reviews": {
            task_id: reviews[task_id].to_dict() for task_id in SERIOUS_TASK_IDS
        },
    }


__all__ = [
    "EXECUTABLE_EVALUATION_METRICS",
    "SERIOUS_GENERALIZATION_CONTRACTS",
    "SERIOUS_TASK_DESIGNS",
    "TASK_DESIGN_VERSION",
    "SeriousTaskDesign",
    "TaskDesignCheck",
    "TaskDesignReview",
    "review_task_design",
    "serious_task_readiness_manifest",
]
