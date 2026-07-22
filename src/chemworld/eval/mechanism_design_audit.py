"""Fail-closed action/intervention audit for mechanism-adaptation protocols.

The protocol is scientifically meaningful only when every hidden intervention can be
probed through public actions at the frozen budget.  This module checks that invariant
before an identifiability certificate or provider campaign is allowed to run.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from typing import Any

import numpy as np

from chemworld.agents.interaction import AgentDecisionContext
from chemworld.agents.mechanism_adaptation_live_llm import (
    MechanismAdaptationLiveLLMAgent,
    MechanismCandidateSpec,
)
from chemworld.agents.task_recipes import task_recipe_from_unit_vector
from chemworld.envs.chemworld_env import ChemWorldEnv
from chemworld.tasks import get_task

DESIGN_AUDIT_SCHEMA_VERSION = "chemworld-mechanism-design-audit-0.2.1"

MATERIAL_FIELD_ACTIONS: dict[str, tuple[str, str]] = {
    "catalyst": ("add_catalyst", "catalyst"),
    "solvent": ("add_solvent", "solvent"),
    "electrolyte_profile": ("set_potential", "electrolyte_profile"),
}

_MECHANISM_CONTROL_GROUPS: dict[str, tuple[tuple[str, str], ...]] = {
    "rate_law_family": (
        ("heat", "target_temperature_K"),
        ("heat", "duration_s"),
    ),
    "topology_family": (
        ("add_catalyst", "catalyst"),
        ("heat", "target_temperature_K"),
    ),
    "constitutive_law_family": (
        ("set_potential", "potential_V"),
        ("set_potential", "current_mA"),
        ("set_potential", "electrolyte_profile"),
    ),
}

_FORBIDDEN_PUBLIC_KEYS = {
    "public_to_baseline",
    "world_interventions",
    "mechanism_family_intervention_hash",
    "material_law_counterfactual_hash",
    "_hidden_material_law_counterfactual_field",
    "_hidden_material_law_public_to_baseline",
}


class _PromptOnlyClient:
    model = "prompt-only-audit"
    thinking = False


def audit_mechanism_design(
    protocol: Mapping[str, Any],
    gate_a_plan: Mapping[str, Any],
    *,
    action_libraries: Mapping[str, Mapping[str, np.ndarray]],
) -> dict[str, Any]:
    """Audit reachability, recipe coverage, observability, and prompt secrecy."""

    findings: list[dict[str, Any]] = []
    task_reports: dict[str, Any] = {}
    definitions = protocol.get("diagnosis_contract", {}).get(
        "candidate_definitions", {}
    )
    contracts = protocol.get("task_mechanism_contracts", {})

    for task_id in protocol.get("design", {}).get("tasks", []):
        task_id = str(task_id)
        task_info = get_task(task_id).to_dict()
        contract = contracts.get(task_id, {})
        interventions = contract.get("interventions", {})
        action_library = action_libraries.get(task_id, {})
        recipes = {
            action_id: task_recipe_from_unit_vector(task_info, vector)
            for action_id, vector in action_library.items()
        }
        recipe_values = _recipe_field_values(recipes)
        task_findings: list[dict[str, Any]] = []

        if not action_library:
            _add(
                task_findings,
                "action_library_present",
                False,
                "The frozen Gate A action library is empty.",
            )
        _add(
            task_findings,
            "diagnostic_measurement_present",
            bool(recipes)
            and all(_has_preterminal_measurement(recipe) for recipe in recipes.values()),
            "Every frozen recipe must contain a public measurement before termination.",
        )

        for candidate_id in contract.get("candidate_ids", []):
            candidate_id = str(candidate_id)
            candidate_interventions = interventions.get(candidate_id)
            if candidate_id == "no_change":
                _add(
                    task_findings,
                    f"{candidate_id}:empty_intervention",
                    candidate_interventions == [],
                    "The no-change twin must have no hidden intervention.",
                )
                continue
            _add(
                task_findings,
                f"{candidate_id}:single_intervention",
                isinstance(candidate_interventions, list)
                and len(candidate_interventions) == 1,
                "Each certification cell must change exactly one hidden law family.",
            )
            if not isinstance(candidate_interventions, list) or len(candidate_interventions) != 1:
                continue
            intervention = candidate_interventions[0]
            _audit_environment_reset(
                task_findings,
                task_id=task_id,
                candidate_id=candidate_id,
                intervention=intervention,
            )
            if intervention.get("kind") == "material_law_counterfactual":
                _audit_material_alignment(
                    task_findings,
                    task_id=task_id,
                    candidate_id=candidate_id,
                    intervention=intervention,
                    recipe_values=recipe_values,
                )
            else:
                mode = str(intervention.get("mode", ""))
                controls = _MECHANISM_CONTROL_GROUPS.get(mode, ())
                varied = [
                    {"operation": operation, "field": field}
                    for operation, field in controls
                    if len(recipe_values.get((operation, field), set())) >= 2
                ]
                _add(
                    task_findings,
                    f"{candidate_id}:diagnostic_control_variation",
                    bool(varied),
                    "At least one public control implicated by the hidden law must vary "
                    f"across frozen recipes; varied={varied}.",
                )

        prompt_check = _audit_prompt_boundary(
            task_id=task_id,
            task_info=task_info,
            definitions=definitions,
            candidate_ids=[str(item) for item in contract.get("candidate_ids", [])],
        )
        task_findings.append(prompt_check)
        findings.extend({"task_id": task_id, **item} for item in task_findings)
        task_reports[task_id] = {
            "action_count": len(action_library),
            "recipe_field_values": {
                f"{operation}.{field}": sorted(values, key=str)
                for (operation, field), values in sorted(recipe_values.items())
            },
            "checks": task_findings,
            "pass": all(item["pass"] for item in task_findings),
        }

    failures = [item for item in findings if not item["pass"]]
    return {
        "schema_version": DESIGN_AUDIT_SCHEMA_VERSION,
        "status": "passed" if not failures else "failed",
        "protocol_id": protocol.get("protocol_id"),
        "gate_a_plan_id": gate_a_plan.get("plan_id"),
        "material_field_action_contract": {
            key: {"operation": value[0], "public_field": value[1]}
            for key, value in MATERIAL_FIELD_ACTIONS.items()
        },
        "task_reports": task_reports,
        "check_count": len(findings),
        "failure_count": len(failures),
        "failures": failures,
        "pass": not failures,
        "interpretation": (
            "A pass means each frozen hidden target is publicly manipulable, covered by "
            "the Gate A recipes, observable before termination, instantiable, and absent "
            "from the mechanism-Agent prompt. It does not establish identifiability."
        ),
    }


def _audit_environment_reset(
    findings: list[dict[str, Any]],
    *,
    task_id: str,
    candidate_id: str,
    intervention: Mapping[str, Any],
) -> None:
    environment: ChemWorldEnv | None = None
    error: str | None = None
    try:
        environment = ChemWorldEnv(
            task_id=task_id,
            seed=0,
            world_interventions=(dict(intervention),),
        )
        environment.reset(seed=0)
    except Exception as exc:  # pragma: no cover - error text is reported to the caller
        error = f"{type(exc).__name__}: {exc}"
    finally:
        if environment is not None:
            environment.close()
    _add(
        findings,
        f"{candidate_id}:environment_instantiation",
        error is None,
        "The task must reset under the declared intervention."
        + (f" error={error}" if error else ""),
    )


def _audit_material_alignment(
    findings: list[dict[str, Any]],
    *,
    task_id: str,
    candidate_id: str,
    intervention: Mapping[str, Any],
    recipe_values: Mapping[tuple[str, str], set[Any]],
) -> None:
    field = str(intervention.get("material_field", ""))
    action_contract = MATERIAL_FIELD_ACTIONS.get(field)
    _add(
        findings,
        f"{candidate_id}:supported_material_field",
        action_contract is not None,
        f"Supported material targets are {sorted(MATERIAL_FIELD_ACTIONS)}.",
    )
    if action_contract is None:
        return
    operation, public_field = action_contract
    environment = ChemWorldEnv(task_id=task_id, seed=0)
    try:
        environment.reset(seed=0)
        schema = environment.action_schema(operation)
    finally:
        environment.close()
    field_schema: Mapping[str, Any] = next(
        (item for item in schema.get("fields", []) if item.get("field") == public_field),
        {},
    )
    choices = set(field_schema.get("choices", []))
    permutation = intervention.get("public_to_baseline")
    moved = (
        {index for index, value in enumerate(permutation) if index != value}
        if isinstance(permutation, list)
        else set()
    )
    _add(
        findings,
        f"{candidate_id}:public_operation_allowed",
        bool(schema.get("valid_operation_type")) and bool(schema.get("task_allowed")),
        f"{operation}.{public_field} must be available to the Agent in {task_id}.",
    )
    _add(
        findings,
        f"{candidate_id}:public_choice_cardinality",
        len(choices) >= 2,
        "A relational counterfactual needs at least two public choices; "
        f"choices={sorted(choices, key=str)}.",
    )
    _add(
        findings,
        f"{candidate_id}:moved_indices_publicly_reachable",
        bool(moved) and moved <= choices,
        "All moved public indices must be legal; "
        f"moved={sorted(moved)}, choices={sorted(choices, key=str)}.",
    )
    covered = recipe_values.get((operation, public_field), set())
    _add(
        findings,
        f"{candidate_id}:moved_indices_recipe_covered",
        bool(moved) and moved <= covered,
        "Frozen Gate A recipes must exercise every moved index; "
        f"moved={sorted(moved)}, covered={sorted(covered, key=str)}.",
    )


def _audit_prompt_boundary(
    *,
    task_id: str,
    task_info: dict[str, Any],
    definitions: Mapping[str, Any],
    candidate_ids: list[str],
) -> dict[str, Any]:
    specs = tuple(
        MechanismCandidateSpec(candidate_id=item, public_definition=str(definitions[item]))
        for item in candidate_ids
        if item in definitions
    )
    if len(specs) < 2 or "no_change" not in {item.candidate_id for item in specs}:
        return _finding(
            "private_truth_absent_from_agent_prompt",
            False,
            "Prompt audit requires complete candidate definitions including no_change.",
        )
    agent = MechanismAdaptationLiveLLMAgent(
        _PromptOnlyClient(),
        role_id="mechanism-design-audit",
        candidate_specs=specs,
        candidate_order_seed=0,
        randomize_candidate_order=True,
    )
    agent.reset(task_info, 0)
    context = AgentDecisionContext(
        step=0,
        task_id=task_id,
        decision_stage="experiment_setup",
        campaign_state={"remaining_budget": 1},
        visible_metrics={},
        latest_spectra={},
        uncertainty={},
        constraint_flags={},
        available_operations=tuple(task_info.get("allowed_operations", ())),
        previous_event_type=None,
    )
    prompt = json.loads(agent._build_prompt(context, {"tool_json": {}}))
    exposed = sorted(_collect_keys(prompt) & _FORBIDDEN_PUBLIC_KEYS)
    return _finding(
        "private_truth_absent_from_agent_prompt",
        not exposed,
        f"Forbidden intervention keys in prompt={exposed}.",
    )


def _recipe_field_values(
    recipes: Mapping[str, Mapping[str, Any]],
) -> dict[tuple[str, str], set[Any]]:
    values: dict[tuple[str, str], set[Any]] = {}
    for recipe in recipes.values():
        for step in recipe.get("steps", []):
            if not isinstance(step, Mapping):
                continue
            operation = str(step.get("operation", ""))
            for field, value in step.items():
                if field != "operation" and isinstance(value, str | int | float):
                    values.setdefault((operation, str(field)), set()).add(value)
    return values


def _has_preterminal_measurement(recipe: Mapping[str, Any]) -> bool:
    operations = [
        str(step.get("operation", ""))
        for step in recipe.get("steps", [])
        if isinstance(step, Mapping)
    ]
    try:
        terminate_index = operations.index("terminate")
    except ValueError:
        return False
    return "measure" in operations[:terminate_index]


def _collect_keys(value: Any) -> set[str]:
    if isinstance(value, Mapping):
        return {str(key) for key in value} | {
            nested
            for item in value.values()
            for nested in _collect_keys(item)
        }
    if isinstance(value, list | tuple):
        return {nested for item in value for nested in _collect_keys(item)}
    return set()


def _finding(check: str, passed: bool, detail: str) -> dict[str, Any]:
    return {"check": check, "pass": bool(passed), "detail": detail}


def _add(findings: list[dict[str, Any]], check: str, passed: bool, detail: str) -> None:
    findings.append(_finding(check, passed, detail))


__all__ = [
    "DESIGN_AUDIT_SCHEMA_VERSION",
    "MATERIAL_FIELD_ACTIONS",
    "audit_mechanism_design",
]
