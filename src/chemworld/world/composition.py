"""Declarative world-composition entry point for the ChemWorld v1 surface."""

from __future__ import annotations

from collections.abc import Mapping
from copy import deepcopy
from dataclasses import dataclass
from typing import Any

from chemworld.tasks import TaskSpec, default_kernel_maturity, get_task
from chemworld.world.operations import INSTRUMENTS
from chemworld.world.parameters import SUPPORTED_SPLITS
from chemworld.world.scenario import ScenarioSpec, get_scenario

WORLD_COMPOSITION_SCHEMA_VERSION = "chemworld-world-composition-0.1"
SUPPORTED_COMPONENT_KINDS = (
    "reaction",
    "thermal",
    "phase",
    "separation",
    "crystallization",
    "distillation",
    "continuous_flow",
    "electrochemistry",
    "observation",
)

_COMPONENT_ORDER = {kind: index for index, kind in enumerate(SUPPORTED_COMPONENT_KINDS)}
_TOP_LEVEL_KEYS = frozenset(
    {"schema_version", "composition_id", "world_split", "components", "task"}
)
_COMPONENT_KEYS = frozenset({"kind", "role", "parameters"})
_TASK_KEYS = frozenset(
    {
        "objective",
        "budget",
        "operations",
        "instruments",
        "observations",
        "resources",
        "termination",
        "evaluation",
        "seeds",
        "episode_mode",
        "safety_limit",
        "difficulty",
        "description",
        "tags",
    }
)
_EVALUATION_KEYS = frozenset({"metrics", "threshold"})

_INTERFACES_BY_COMPONENT = {
    "reaction": ("material", "reaction_event"),
    "thermal": ("temperature", "time", "energy", "safety"),
    "phase": ("phase", "volume", "composition", "state_identity"),
    "separation": ("material", "phase", "volume", "sample_identity"),
    "crystallization": ("temperature", "phase", "crystal_state", "sample"),
    "distillation": ("temperature", "phase", "volatility", "fraction"),
    "continuous_flow": ("flow_rate", "residence_time", "temperature", "material"),
    "electrochemistry": ("potential", "current", "charge", "energy", "material"),
    "observation": ("public_measurement", "missingness", "cost", "latency", "sample"),
}


class WorldCompositionError(ValueError):
    """Raised when a declarative composition cannot be compiled."""


def _require_exact_keys(
    payload: Mapping[str, Any],
    expected: frozenset[str],
    label: str,
) -> None:
    unknown = sorted(set(payload) - expected)
    if unknown:
        raise WorldCompositionError(f"{label} contains unsupported fields: {unknown}")


def _string_tuple(value: Any, label: str) -> tuple[str, ...]:
    if not isinstance(value, (list, tuple)) or not value:
        raise WorldCompositionError(f"{label} must be a non-empty list of strings")
    result = tuple(str(item) for item in value)
    if any(not item.strip() for item in result):
        raise WorldCompositionError(f"{label} must contain non-empty strings")
    if len(set(result)) != len(result):
        raise WorldCompositionError(f"{label} must not contain duplicates")
    return result


@dataclass(frozen=True)
class WorldComponentRequest:
    """One reader-facing component declaration."""

    kind: str
    role: str
    parameters: dict[str, Any]

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> WorldComponentRequest:
        _require_exact_keys(payload, _COMPONENT_KEYS, "component")
        kind = str(payload.get("kind", "")).strip()
        if kind not in SUPPORTED_COMPONENT_KINDS:
            raise WorldCompositionError(f"unsupported component kind: {kind!r}")
        role = str(payload.get("role", kind)).strip()
        if not role:
            raise WorldCompositionError("component role must be non-empty")
        parameters = payload.get("parameters", {})
        if not isinstance(parameters, Mapping):
            raise WorldCompositionError("component parameters must be an object")
        return cls(kind=kind, role=role, parameters=deepcopy(dict(parameters)))

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "role": self.role,
            "parameters": deepcopy(self.parameters),
        }


@dataclass(frozen=True)
class CompositionTaskRequest:
    """Reader-facing task surface attached to a composed world."""

    objective: str | None
    budget: int | None
    operations: tuple[str, ...] | None
    instruments: tuple[str, ...] | None
    observations: str | None
    resources: dict[str, Any]
    termination: str | None
    evaluation_metrics: tuple[str, ...] | None
    evaluation_threshold: float | None
    seeds: tuple[int, ...] | None
    episode_mode: str | None
    safety_limit: float | None
    difficulty: str | None
    description: str | None
    tags: tuple[str, ...]

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> CompositionTaskRequest:
        _require_exact_keys(payload, _TASK_KEYS, "task")
        budget_value = payload.get("budget")
        budget = None if budget_value is None else int(budget_value)
        if budget is not None and budget <= 0:
            raise WorldCompositionError("task budget must be positive")
        operations_value = payload.get("operations")
        operations = (
            None
            if operations_value is None
            else _string_tuple(operations_value, "task operations")
        )
        instruments_value = payload.get("instruments")
        instruments = (
            None
            if instruments_value is None
            else _string_tuple(instruments_value, "task instruments")
        )
        if instruments is not None:
            unknown_instruments = sorted(set(instruments) - set(INSTRUMENTS))
            if unknown_instruments:
                raise WorldCompositionError(
                    f"task instruments are unsupported: {unknown_instruments}"
                )
        resources_value = payload.get("resources", {})
        if not isinstance(resources_value, Mapping):
            raise WorldCompositionError("task resources must be an object")
        evaluation_value = payload.get("evaluation", {})
        if not isinstance(evaluation_value, Mapping):
            raise WorldCompositionError("task evaluation must be an object")
        _require_exact_keys(evaluation_value, _EVALUATION_KEYS, "task evaluation")
        metrics_value = evaluation_value.get("metrics")
        evaluation_metrics = (
            None
            if metrics_value is None
            else _string_tuple(metrics_value, "task evaluation metrics")
        )
        threshold_value = evaluation_value.get("threshold")
        evaluation_threshold = (
            None if threshold_value is None else float(threshold_value)
        )
        if evaluation_threshold is not None and not 0.0 <= evaluation_threshold <= 1.0:
            raise WorldCompositionError("task evaluation threshold must be in [0, 1]")
        seeds_value = payload.get("seeds")
        seeds = None
        if seeds_value is not None:
            if not isinstance(seeds_value, (list, tuple)) or not seeds_value:
                raise WorldCompositionError("task seeds must be a non-empty list")
            seeds = tuple(int(seed) for seed in seeds_value)
            if any(seed < 0 for seed in seeds) or len(set(seeds)) != len(seeds):
                raise WorldCompositionError(
                    "task seeds must be unique non-negative integers"
                )
        episode_mode_value = payload.get("episode_mode")
        episode_mode = None if episode_mode_value is None else str(episode_mode_value)
        if episode_mode not in {None, "single_experiment", "campaign"}:
            raise WorldCompositionError(
                "task episode_mode must be single_experiment or campaign"
            )
        safety_limit_value = payload.get("safety_limit")
        safety_limit = None if safety_limit_value is None else float(safety_limit_value)
        if safety_limit is not None and not 0.0 < safety_limit <= 1.0:
            raise WorldCompositionError("task safety_limit must be in (0, 1]")
        tags_value = payload.get("tags", ())
        tags = (
            ()
            if tags_value is None or tags_value == () or tags_value == []
            else _string_tuple(tags_value, "task tags")
        )
        return cls(
            objective=(
                None if payload.get("objective") is None else str(payload["objective"])
            ),
            budget=budget,
            operations=operations,
            instruments=instruments,
            observations=(
                None
                if payload.get("observations") is None
                else str(payload["observations"])
            ),
            resources=deepcopy(dict(resources_value)),
            termination=(
                None
                if payload.get("termination") is None
                else str(payload["termination"])
            ),
            evaluation_metrics=evaluation_metrics,
            evaluation_threshold=evaluation_threshold,
            seeds=seeds,
            episode_mode=episode_mode,
            safety_limit=safety_limit,
            difficulty=(
                None if payload.get("difficulty") is None else str(payload["difficulty"])
            ),
            description=(
                None if payload.get("description") is None else str(payload["description"])
            ),
            tags=tags,
        )


@dataclass(frozen=True)
class WorldCompositionSpec:
    """Validated declarative request before runtime compilation."""

    schema_version: str
    composition_id: str
    world_split: str
    components: tuple[WorldComponentRequest, ...]
    task: CompositionTaskRequest

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> WorldCompositionSpec:
        _require_exact_keys(payload, _TOP_LEVEL_KEYS, "world composition")
        schema_version = str(payload.get("schema_version", ""))
        if schema_version != WORLD_COMPOSITION_SCHEMA_VERSION:
            raise WorldCompositionError("unsupported world-composition schema")
        composition_id = str(payload.get("composition_id", "")).strip()
        if not composition_id:
            raise WorldCompositionError("composition_id must be non-empty")
        world_split = str(payload.get("world_split", "public-dev"))
        if world_split not in SUPPORTED_SPLITS:
            raise WorldCompositionError(f"unsupported world_split: {world_split!r}")
        components_value = payload.get("components")
        if not isinstance(components_value, list) or not components_value:
            raise WorldCompositionError("components must be a non-empty list")
        components = tuple(
            WorldComponentRequest.from_dict(component)
            for component in components_value
            if isinstance(component, Mapping)
        )
        if len(components) != len(components_value):
            raise WorldCompositionError("every component must be an object")
        kinds = tuple(component.kind for component in components)
        if len(set(kinds)) != len(kinds):
            raise WorldCompositionError("component kinds must not be duplicated")
        components = tuple(sorted(components, key=lambda item: _COMPONENT_ORDER[item.kind]))
        task_value = payload.get("task")
        if not isinstance(task_value, Mapping):
            raise WorldCompositionError("task must be an object")
        return cls(
            schema_version=schema_version,
            composition_id=composition_id,
            world_split=world_split,
            components=components,
            task=CompositionTaskRequest.from_dict(task_value),
        )

    @property
    def component_kinds(self) -> tuple[str, ...]:
        return tuple(component.kind for component in self.components)


@dataclass(frozen=True)
class _CompositionPattern:
    component_kinds: frozenset[str]
    template_task_id: str


_COMPOSITION_PATTERNS = (
    _CompositionPattern(
        frozenset({"reaction", "thermal", "observation"}),
        "reaction-to-assay",
    ),
    _CompositionPattern(
        frozenset({"reaction", "thermal", "phase", "separation", "observation"}),
        "reaction-to-purification",
    ),
    _CompositionPattern(
        frozenset({"phase", "separation", "observation"}),
        "partition-discovery",
    ),
    _CompositionPattern(
        frozenset({"reaction", "thermal", "crystallization", "observation"}),
        "reaction-to-crystallization",
    ),
    _CompositionPattern(
        frozenset({"reaction", "thermal", "distillation", "observation"}),
        "reaction-to-distillation",
    ),
    _CompositionPattern(
        frozenset({"reaction", "thermal", "continuous_flow", "observation"}),
        "flow-reaction-optimization",
    ),
    _CompositionPattern(
        frozenset({"reaction", "electrochemistry", "observation"}),
        "electrochemical-conversion",
    ),
    _CompositionPattern(
        frozenset({"phase", "observation"}),
        "equilibrium-characterization",
    ),
)
_PATTERN_BY_COMPONENT_SET = {
    pattern.component_kinds: pattern for pattern in _COMPOSITION_PATTERNS
}


@dataclass(frozen=True)
class CompiledWorldComposition:
    """Runtime-ready task/scenario pair plus the reader-facing public surface."""

    spec: WorldCompositionSpec
    task_spec: TaskSpec
    scenario_spec: ScenarioSpec
    public_surface: dict[str, Any]

    def to_public_dict(self) -> dict[str, Any]:
        return deepcopy(self.public_surface)

    def env_kwargs(self, *, seed: int | None = None) -> dict[str, Any]:
        return {
            "composition": self,
            "seed": self.task_spec.seeds[0] if seed is None else int(seed),
        }


def _resolve_pattern(spec: WorldCompositionSpec) -> _CompositionPattern:
    component_set = frozenset(spec.component_kinds)
    pattern = _PATTERN_BY_COMPONENT_SET.get(component_set)
    if pattern is None:
        rendered = ", ".join(spec.component_kinds)
        raise WorldCompositionError(
            "component combination is not registered in the v1 runtime surface: "
            f"[{rendered}]"
        )
    return pattern


def compile_world_composition(
    value: Mapping[str, Any] | WorldCompositionSpec | CompiledWorldComposition,
) -> CompiledWorldComposition:
    """Compile one declarative request into a runtime-ready public contract."""

    if isinstance(value, CompiledWorldComposition):
        return value
    spec = (
        value
        if isinstance(value, WorldCompositionSpec)
        else WorldCompositionSpec.from_dict(value)
    )
    pattern = _resolve_pattern(spec)
    template = get_task(pattern.template_task_id)
    request = spec.task
    operations = request.operations or template.allowed_operations
    invalid_operations = sorted(set(operations) - set(template.allowed_operations))
    if invalid_operations:
        raise WorldCompositionError(
            "task operations are outside the compiled component surface: "
            f"{invalid_operations}"
        )
    if not {"terminate", "measure"}.issubset(operations):
        raise WorldCompositionError(
            "task operations must include terminate and measure for lifecycle closure"
        )
    instruments = request.instruments or template.allowed_instruments
    invalid_instruments = sorted(set(instruments) - set(template.allowed_instruments))
    if invalid_instruments:
        raise WorldCompositionError(
            "task instruments are outside the compiled component surface: "
            f"{invalid_instruments}"
        )
    if "final_assay" not in instruments:
        raise WorldCompositionError("task instruments must include final_assay")
    budget = request.budget or template.budget
    resources = {
        "operation_budget": budget,
        "stock_accounting": "task-and-constitution",
        "sample_accounting": "per-instrument",
        "time_accounting": "per-operation-and-instrument",
        **deepcopy(request.resources),
    }
    if int(resources.get("operation_budget", budget)) != budget:
        raise WorldCompositionError(
            "task resources.operation_budget must match task budget"
        )
    metrics = request.evaluation_metrics or template.success_metrics
    threshold = (
        template.threshold
        if request.evaluation_threshold is None
        else request.evaluation_threshold
    )
    scenario_spec = get_scenario(template.scenario_id, split=spec.world_split)
    task_spec = TaskSpec(
        task_id=spec.composition_id,
        env_id=template.env_id,
        world_law_id=template.world_law_id,
        scenario_id=scenario_spec.scenario_id,
        initial_state_id=scenario_spec.initial_state_id,
        world_split=spec.world_split,
        objective=request.objective or template.objective,
        budget=budget,
        seeds=request.seeds or template.seeds,
        threshold=threshold,
        episode_mode=request.episode_mode or template.episode_mode,
        allowed_operations=operations,
        allowed_instruments=instruments,
        observation_policy=request.observations or template.observation_policy,
        termination_policy=request.termination or template.termination_policy,
        success_metrics=metrics,
        safety_limit=(
            template.safety_limit if request.safety_limit is None else request.safety_limit
        ),
        difficulty=request.difficulty or template.difficulty,
        description=(
            request.description
            or f"Declaratively composed ChemWorld world: {spec.composition_id}."
        ),
        tags=tuple(dict.fromkeys((*template.tags, "composed-world", *request.tags))),
        kernel_maturity=default_kernel_maturity(
            operations,
            allowed_instruments=instruments,
        ),
    )
    interfaces = tuple(
        sorted(
            {
                interface
                for component in spec.components
                for interface in _INTERFACES_BY_COMPONENT[component.kind]
            }
        )
    )
    public_surface = {
        "schema_version": WORLD_COMPOSITION_SCHEMA_VERSION,
        "composition_id": spec.composition_id,
        "world": {
            "components": [component.to_dict() for component in spec.components],
            "interfaces": list(interfaces),
            "family": scenario_spec.family,
            "split": spec.world_split,
            "initial_state": scenario_spec.initial_state_id,
        },
        "task": {
            "objective": task_spec.objective,
            "operations": list(task_spec.allowed_operations),
            "instruments": list(task_spec.allowed_instruments),
            "observations": task_spec.observation_policy,
            "resources": resources,
            "termination": task_spec.termination_policy,
            "evaluation": {
                "metrics": list(task_spec.success_metrics),
                "threshold": task_spec.threshold,
            },
            "episode_mode": task_spec.episode_mode,
            "safety_limit": task_spec.safety_limit,
        },
    }
    return CompiledWorldComposition(
        spec=spec,
        task_spec=task_spec,
        scenario_spec=scenario_spec,
        public_surface=public_surface,
    )


__all__ = [
    "SUPPORTED_COMPONENT_KINDS",
    "WORLD_COMPOSITION_SCHEMA_VERSION",
    "CompiledWorldComposition",
    "CompositionTaskRequest",
    "WorldComponentRequest",
    "WorldCompositionError",
    "WorldCompositionSpec",
    "compile_world_composition",
]
