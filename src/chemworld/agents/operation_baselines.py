"""Official operation-level controls using only declared public affordances."""

from __future__ import annotations

import math
import random
from collections.abc import Mapping, Sequence
from typing import Any, Literal, cast

import numpy as np

from chemworld.agents.base import BaseAgent, HistoryRecord
from chemworld.agents.interaction import (
    AgentDecisionContext,
    DecisionAuditRecord,
    InteractionCapabilities,
)
from chemworld.agents.task_recipes import (
    task_recipe_dimension,
    task_recipe_event_count,
    task_recipe_from_unit_vector,
)

OperationBaselineId = Literal["operation_random", "observation_blind", "rule_based"]
OPERATION_BASELINE_IDS: tuple[OperationBaselineId, ...] = (
    "operation_random",
    "observation_blind",
    "rule_based",
)

_BLIND_PRIORITY = (
    "add_solvent",
    "add_reagent",
    "add_catalyst",
    "add_phase",
    "add_extractant",
    "set_flow_rate",
    "set_potential",
    "heat",
    "run_flow",
    "electrolyze",
    "mix",
    "wait",
    "settle",
    "quench",
    "separate_phase",
    "wash",
    "dry",
    "concentrate",
    "transfer",
    "seed_crystals",
    "cool_crystallize",
    "filter_crystals",
    "evaporate",
    "distill",
    "collect_fraction",
    "sample",
    "measure",
)

_RULE_RETRY_BY_TASK = {
    "partition-discovery": ("mix", "settle"),
    # Repeating a completed cooling/distillation kernel at its old target can
    # leave the model validity domain.  ``wait`` is a public, replayable way to
    # extend either process without relying on hidden current temperature.
    "reaction-to-crystallization": ("wait",),
    "reaction-to-distillation": ("wait",),
    "flow-reaction-optimization": ("run_flow",),
}

_PRIMARY_PUBLIC_METRICS = {
    "partition-discovery": ("product_in_organic", "recovery", "score"),
    "reaction-to-crystallization": ("crystal_yield", "yield", "score"),
    "reaction-to-distillation": ("distillate_purity", "purity", "score"),
    "flow-reaction-optimization": ("flow_conversion", "conversion", "score"),
}


class OperationBaselineContractError(ValueError):
    """Raised when the public operation-affordance contract is incomplete."""


class OperationBaselineAgent(BaseAgent):
    """One of three frozen operation-level controls.

    ``operation_random`` samples available operations and their public schemas.
    ``observation_blind`` follows a deterministic task-agnostic affordance cycle.
    ``rule_based`` follows a public task recipe and may make one within-experiment
    retry after a public measurement.  No variant consumes spectra or hidden state.
    """

    def __init__(
        self,
        method_id: OperationBaselineId,
        *,
        exploration_multiplier: int = 2,
        numeric_margin: float = 0.15,
        rule_retry_threshold: float = 0.55,
    ) -> None:
        if method_id not in OPERATION_BASELINE_IDS:
            raise OperationBaselineContractError(f"unsupported baseline: {method_id}")
        if exploration_multiplier < 1:
            raise OperationBaselineContractError("exploration_multiplier must be positive")
        if not 0.0 <= numeric_margin < 0.5:
            raise OperationBaselineContractError("numeric_margin must be in [0, 0.5)")
        if not 0.0 <= rule_retry_threshold <= 1.0:
            raise OperationBaselineContractError("rule_retry_threshold must be in [0, 1]")
        self.method_id = method_id
        self.name = method_id
        self.exploration_multiplier = exploration_multiplier
        self.numeric_margin = numeric_margin
        self.rule_retry_threshold = rule_retry_threshold

    def reset(self, task_info: dict[str, Any], seed: int) -> None:
        super().reset(task_info, seed)
        self._rng = random.Random(seed)
        self._blind_cursor = 0
        self._experiment_decisions = 0
        self._executed_operations: set[str] = set()
        self._rule_plan: list[dict[str, Any]] = []
        self._rule_cursor = 0
        self._rule_retry_used = False
        self._last_audit: dict[str, Any] | None = None
        self._closeout_after = max(
            1,
            self.exploration_multiplier * task_recipe_event_count(task_info) - 2,
        )

    def act(self, history: list[HistoryRecord]) -> dict[str, Any]:
        del history
        raise OperationBaselineContractError(
            "operation baselines require the official public-view runner"
        )

    def act_with_public_view(
        self,
        context: AgentDecisionContext,
        public_view: dict[str, Any],
    ) -> dict[str, Any]:
        affordances = _available_affordances(public_view)
        by_operation = {str(item["operation"]): item for item in affordances}
        if context.decision_stage == "experiment_closeout":
            action = _final_assay_action(by_operation)
            return self._record_decision(
                action,
                evidence=("experiment_closeout", "available_operations"),
                hypothesis="the explicitly terminated experiment requires its final assay",
                rationale="select the public final-assay affordance without runner closeout",
                adaptation_source="validator",
            )
        if self._experiment_decisions >= self._closeout_after and "terminate" in by_operation:
            action = {"operation": "terminate"}
            return self._record_decision(
                action,
                evidence=("campaign_step", "available_operations"),
                hypothesis="the frozen per-experiment operation allowance is exhausted",
                rationale="close the experiment explicitly before the campaign budget is lost",
                adaptation_source="validator",
            )
        if self.method_id == "operation_random":
            setup = self._random_setup_action(by_operation)
            if setup is not None:
                return self._record_decision(
                    setup,
                    evidence=("available_operations", "public_action_schema"),
                    hypothesis=(
                        "a minimal public charge is required before random control can "
                        "close an experiment"
                    ),
                    rationale=(
                        "perform the frozen setup guard, then return to uniform affordance sampling"
                    ),
                    adaptation_source="validator",
                )
            action = self._random_action(context, affordances)
            return self._record_decision(
                action,
                evidence=("available_operations", "public_action_schema"),
                hypothesis="uniform affordance sampling is an observation-free stochastic control",
                rationale="sample one currently executable operation and its public parameters",
                adaptation_source="validator",
            )
        if self.method_id == "observation_blind":
            action = self._blind_action(context, by_operation)
            return self._record_decision(
                action,
                evidence=("available_operations", "public_action_schema", "fixed_cycle_index"),
                hypothesis=(
                    "a fixed affordance cycle controls for action access without observations"
                ),
                rationale="take the next available operation in the frozen task-agnostic cycle",
                adaptation_source="validator",
            )
        action, used_measurement = self._rule_action(context, by_operation)
        metric_names = tuple(
            key
            for key in _PRIMARY_PUBLIC_METRICS.get(str(context.task_id), ("score",))
            if key in context.visible_metrics
        )
        return self._record_decision(
            action,
            evidence=(
                "available_operations",
                "public_action_schema",
                *(f"visible_metric:{name}" for name in metric_names),
            ),
            hypothesis=(
                "one public measurement-guided retry may improve the current experiment"
                if used_measurement
                else "the frozen task rule advances the current experiment"
            ),
            rationale=(
                "apply one declared retry because the public endpoint is below threshold"
                if used_measurement
                else "execute the next valid step in the public task rule"
            ),
            adaptation_source="measurement" if used_measurement else "validator",
        )

    def update(
        self,
        action: dict[str, Any],
        observation: dict[str, float | None],
        reward: float,
        info: dict[str, Any],
    ) -> None:
        # Observation-blind policies intentionally ignore observation, reward,
        # and outcome fields.  Rule adaptation is performed from the audited
        # AgentDecisionContext supplied by the public-view runner.
        del observation, reward
        flags = info.get("constraint_flags")
        failed = bool(isinstance(flags, Mapping) and flags.get("precondition_failed", False))
        if not failed and isinstance(action.get("operation"), str):
            self._executed_operations.add(str(action["operation"]))
        self._experiment_decisions += 1
        if info.get("experiment_ended") is True:
            self._experiment_decisions = 0
            self._executed_operations = set()
            self._rule_plan = []
            self._rule_cursor = 0
            self._rule_retry_used = False

    def decision_audit(self) -> dict[str, Any] | None:
        return None if self._last_audit is None else dict(self._last_audit)

    def interaction_capabilities(self) -> InteractionCapabilities:
        reads_public_state = self.method_id == "rule_based"
        return InteractionCapabilities(
            decision_scope="operation",
            consumes_intermediate_observations=reads_public_state,
            consumes_spectra=False,
            adapts_within_experiment=reads_public_state,
            adapts_across_experiments=False,
            emits_structured_decision_audit=True,
        )

    def manifest(self) -> dict[str, Any]:
        return {
            **super().manifest(),
            "method_id": self.method_id,
            "policy_version": "chemworld-operation-baseline-policy-0.4",
            "public_observation_policy": (
                "operation_public_state"
                if self.method_id == "rule_based"
                else "operation_affordance_only"
            ),
            "spectrum_capability": "none",
            "exploration_multiplier": self.exploration_multiplier,
            "numeric_margin": self.numeric_margin,
            "rule_retry_threshold": (
                self.rule_retry_threshold if self.method_id == "rule_based" else None
            ),
            "automatic_action_repair": False,
            "automatic_closeout": False,
        }

    def _random_action(
        self,
        context: AgentDecisionContext,
        affordances: Sequence[Mapping[str, Any]],
    ) -> dict[str, Any]:
        candidates = [item for item in affordances if item.get("operation") != "terminate"]
        if not candidates:
            candidates = list(affordances)
        selected = self._rng.choice(candidates)
        return _action_from_affordance(
            selected,
            mode="random",
            rng=self._rng,
            numeric_margin=self.numeric_margin,
            closeout=context.decision_stage == "experiment_closeout",
        )

    def _random_setup_action(
        self,
        by_operation: Mapping[str, Mapping[str, Any]],
    ) -> dict[str, Any] | None:
        for operation in ("add_solvent", "add_reagent"):
            if operation in self._executed_operations:
                continue
            affordance = by_operation.get(operation)
            if affordance is not None:
                return _action_from_affordance(
                    affordance,
                    mode="random",
                    rng=self._rng,
                    numeric_margin=self.numeric_margin,
                    closeout=False,
                )
        return None

    def _blind_action(
        self,
        context: AgentDecisionContext,
        by_operation: Mapping[str, Mapping[str, Any]],
    ) -> dict[str, Any]:
        del context
        for offset in range(len(_BLIND_PRIORITY)):
            index = (self._blind_cursor + offset) % len(_BLIND_PRIORITY)
            operation = _BLIND_PRIORITY[index]
            if operation in by_operation:
                self._blind_cursor = (index + 1) % len(_BLIND_PRIORITY)
                return _action_from_affordance(
                    by_operation[operation],
                    mode="midpoint",
                    rng=None,
                    numeric_margin=self.numeric_margin,
                    closeout=False,
                )
        if "terminate" in by_operation:
            return {"operation": "terminate"}
        raise OperationBaselineContractError("no blind-control affordance is available")

    def _rule_action(
        self,
        context: AgentDecisionContext,
        by_operation: Mapping[str, Mapping[str, Any]],
    ) -> tuple[dict[str, Any], bool]:
        task_id = str(context.task_id or self.task_info.get("task_id") or "")
        if (
            context.decision_stage == "evidence_update"
            and not self._rule_retry_used
            and _public_metric_below_threshold(
                context.visible_metrics,
                _PRIMARY_PUBLIC_METRICS.get(task_id, ("score",)),
                self.rule_retry_threshold,
            )
        ):
            for operation in _RULE_RETRY_BY_TASK.get(task_id, ("wait",)):
                if operation in by_operation:
                    self._rule_retry_used = True
                    return (
                        _action_from_affordance(
                            by_operation[operation],
                            mode="midpoint",
                            rng=None,
                            numeric_margin=self.numeric_margin,
                            closeout=False,
                        ),
                        True,
                    )
        if not self._rule_plan:
            vector = np.full(task_recipe_dimension(self.task_info), 0.5, dtype=float)
            recipe = task_recipe_from_unit_vector(self.task_info, vector)
            raw_steps = recipe.get("steps", ())
            self._rule_plan = [dict(step) for step in raw_steps if isinstance(step, Mapping)]
            self._rule_cursor = 0
        while self._rule_cursor < len(self._rule_plan):
            planned = self._rule_plan[self._rule_cursor]
            self._rule_cursor += 1
            operation = str(planned.get("operation") or "")
            affordance = by_operation.get(operation)
            if affordance is not None:
                return (
                    _action_from_affordance(
                        affordance,
                        mode="planned",
                        rng=None,
                        numeric_margin=self.numeric_margin,
                        closeout=False,
                        planned=planned,
                    ),
                    False,
                )
        if "terminate" in by_operation:
            return {"operation": "terminate"}, False
        # The recipe may encounter a task-specific state in which its next step
        # is unavailable.  This is an agent decision over the public affordance,
        # not a runner repair: choose a deterministic blind-control fallback.
        return self._blind_action(context, by_operation), False

    def _record_decision(
        self,
        action: dict[str, Any],
        *,
        evidence: tuple[str, ...],
        hypothesis: str,
        rationale: str,
        adaptation_source: Literal["measurement", "validator"],
    ) -> dict[str, Any]:
        audit = DecisionAuditRecord(
            action=dict(action),
            evidence=evidence,
            hypothesis=hypothesis,
            uncertainty=None,
            rationale=rationale,
            adaptation_source=adaptation_source,
        )
        self._last_audit = audit.to_dict()
        return action


def _available_affordances(public_view: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    tool = public_view.get("tool_json")
    raw = tool.get("available_actions") if isinstance(tool, Mapping) else None
    if not isinstance(raw, list):
        raise OperationBaselineContractError("public available_actions are missing")
    affordances = [
        item
        for item in raw
        if isinstance(item, Mapping)
        and isinstance(item.get("operation"), str)
        and item.get("valid") is not False
        and isinstance(item.get("schema"), Mapping)
    ]
    if not affordances:
        raise OperationBaselineContractError("no valid public action affordance is available")
    return affordances


def _final_assay_action(
    by_operation: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    measure = by_operation.get("measure")
    if measure is None:
        raise OperationBaselineContractError("closeout requires a measure affordance")
    schema = measure.get("schema")
    fields = schema.get("fields") if isinstance(schema, Mapping) else None
    instrument = next(
        (
            field
            for field in fields or ()
            if isinstance(field, Mapping) and field.get("field") == "instrument"
        ),
        None,
    )
    choices = instrument.get("choices") if isinstance(instrument, Mapping) else None
    if not isinstance(choices, list) or "final_assay" not in choices:
        raise OperationBaselineContractError("final_assay is not publicly available")
    return {"operation": "measure", "instrument": "final_assay"}


def _action_from_affordance(
    affordance: Mapping[str, Any],
    *,
    mode: Literal["random", "midpoint", "planned"],
    rng: random.Random | None,
    numeric_margin: float,
    closeout: bool,
    planned: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    operation = str(affordance["operation"])
    schema = affordance.get("schema")
    if not isinstance(schema, Mapping):
        raise OperationBaselineContractError(f"{operation} has no public schema")
    fields = schema.get("fields")
    if not isinstance(fields, list):
        raise OperationBaselineContractError(f"{operation} schema fields are invalid")
    action: dict[str, Any] = {"operation": operation}
    for raw_field in fields:
        if not isinstance(raw_field, Mapping) or not isinstance(raw_field.get("field"), str):
            raise OperationBaselineContractError(f"{operation} has an invalid field schema")
        field = str(raw_field["field"])
        candidate = planned.get(field) if planned is not None else None
        action[field] = _field_value(
            operation,
            field,
            raw_field,
            mode=mode,
            rng=rng,
            numeric_margin=numeric_margin,
            closeout=closeout,
            candidate=candidate,
        )
    return action


def _field_value(
    operation: str,
    field: str,
    schema: Mapping[str, Any],
    *,
    mode: Literal["random", "midpoint", "planned"],
    rng: random.Random | None,
    numeric_margin: float,
    closeout: bool,
    candidate: Any,
) -> Any:
    choices = schema.get("choices")
    if isinstance(choices, list) and choices:
        allowed = list(choices)
        if field == "instrument":
            if closeout:
                if "final_assay" not in allowed:
                    raise OperationBaselineContractError("final_assay choice is missing")
                return "final_assay"
            nonfinal = [item for item in allowed if item != "final_assay"]
            if nonfinal:
                allowed = nonfinal
        if mode == "planned" and candidate in allowed:
            return candidate
        if field == "phase" and "aqueous" in allowed:
            return "aqueous"
        if field == "target_phase" and "organic" in allowed:
            return "organic"
        if mode == "random":
            if rng is None:
                raise OperationBaselineContractError("random field sampling requires an RNG")
            return rng.choice(allowed)
        return allowed[0]
    bounds = schema.get("recommended_range", schema.get("bounds"))
    if isinstance(bounds, Mapping):
        low = _finite_number(bounds.get("low"), f"{operation}.{field}.low")
        high = _finite_number(bounds.get("high"), f"{operation}.{field}.high")
        if high < low:
            raise OperationBaselineContractError(f"{operation}.{field} bounds are reversed")
        if mode == "planned" and _number_in_bounds(candidate, low, high):
            return float(candidate)
        span = high - low
        inner_low = low + numeric_margin * span
        inner_high = high - numeric_margin * span
        if mode == "random":
            if rng is None:
                raise OperationBaselineContractError("random field sampling requires an RNG")
            return rng.uniform(inner_low, inner_high)
        return (inner_low + inner_high) / 2.0
    if mode == "planned" and candidate is not None:
        return candidate
    raise OperationBaselineContractError(f"{operation}.{field} has no public domain")


def _public_metric_below_threshold(
    metrics: Mapping[str, Any],
    ordered_keys: Sequence[str],
    threshold: float,
) -> bool:
    for key in ordered_keys:
        value = metrics.get(key)
        if isinstance(value, bool) or not isinstance(value, int | float):
            continue
        scalar = float(value)
        if math.isfinite(scalar):
            return scalar < threshold
    return False


def _finite_number(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise OperationBaselineContractError(f"{label} must be numeric")
    scalar = float(value)
    if not math.isfinite(scalar):
        raise OperationBaselineContractError(f"{label} must be finite")
    return scalar


def _number_in_bounds(value: Any, low: float, high: float) -> bool:
    return bool(
        not isinstance(value, bool)
        and isinstance(value, int | float)
        and math.isfinite(float(value))
        and low <= float(value) <= high
    )


def make_operation_baseline_agent(
    method_id: str,
    *,
    hyperparameters: Mapping[str, Any] | None = None,
) -> OperationBaselineAgent:
    """Construct a named baseline from a frozen method card."""

    if method_id not in OPERATION_BASELINE_IDS:
        raise OperationBaselineContractError(f"unsupported baseline: {method_id}")
    raw = dict(hyperparameters or {})
    allowed = {"exploration_multiplier", "numeric_margin", "rule_retry_threshold"}
    if set(raw) - allowed:
        raise OperationBaselineContractError("unknown operation-baseline hyperparameter")
    return OperationBaselineAgent(
        cast(OperationBaselineId, method_id),
        exploration_multiplier=int(raw.get("exploration_multiplier", 2)),
        numeric_margin=float(raw.get("numeric_margin", 0.15)),
        rule_retry_threshold=float(raw.get("rule_retry_threshold", 0.55)),
    )


__all__ = [
    "OPERATION_BASELINE_IDS",
    "OperationBaselineAgent",
    "OperationBaselineContractError",
    "OperationBaselineId",
    "make_operation_baseline_agent",
]
