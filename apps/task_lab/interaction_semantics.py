"""Public interaction semantics shared by the agent and student workspaces.

This module does not change the frozen world law.  It aligns interactive inputs
with the effective ranges of the current runtime and describes state changes
without exposing hidden composition.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from chemworld.data.logging import to_builtin

_OPERATION_EFFECTS: dict[str, dict[str, str]] = {
    "add_reagent": {
        "type": "additive_charge",
        "label_zh": "累计投料",
        "summary": "Adds reagent to the current vessel; existing material remains.",
        "summary_zh": "向当前容器累计加入试剂，已有物料不会被替换。",
        "visual": "feed",
    },
    "add_solvent": {
        "type": "additive_charge",
        "label_zh": "累计加液",
        "summary": "Adds solvent volume to the current vessel.",
        "summary_zh": "向当前容器累计加入溶剂并增加液体体积。",
        "visual": "feed",
    },
    "add_catalyst": {
        "type": "additive_charge",
        "label_zh": "累计加料",
        "summary": "Adds catalyst amount to the current vessel.",
        "summary_zh": "向当前容器累计加入催化剂。",
        "visual": "feed",
    },
    "heat": {
        "type": "cumulative_process",
        "label_zh": "累计反应",
        "summary": "Advances the current composition for the requested thermal interval.",
        "summary_zh": "从当前组成继续积分，时间、热历程和反应进度累计。",
        "visual": "heat",
    },
    "wait": {
        "type": "cumulative_process",
        "label_zh": "继续反应",
        "summary": "Advances the current composition without starting a new experiment.",
        "summary_zh": "当前组成继续随时间演化，不会开始新实验。",
        "visual": "mix",
    },
    "sample": {
        "type": "destructive_withdrawal",
        "label_zh": "取样扣除",
        "summary": "Removes a proportional aliquot from volume and material inventories.",
        "summary_zh": "按比例从当前容器扣除样品体积和其中物料。",
        "visual": "sample",
    },
    "quench": {
        "type": "state_change",
        "label_zh": "淬灭降温",
        "summary": "Changes the current vessel to a quenched, cooler state.",
        "summary_zh": "当前容器进入已淬灭的较低温状态，但不会自动换釜。",
        "visual": "quench",
    },
    "add_phase": {
        "type": "additive_charge",
        "label_zh": "累计加相",
        "summary": "Adds liquid volume to the selected phase in the current phase ledger.",
        "summary_zh": "向当前相账本中的指定液相累计加入体积。",
        "visual": "phase",
    },
    "add_extractant": {
        "type": "additive_charge",
        "label_zh": "加入萃取相",
        "summary": (
            "Adds volume to the organic phase; the current runtime has no "
            "identity-specific extractant effect."
        ),
        "summary_zh": "向有机相加液；当前运行时尚无萃取剂名称对应的独立物性效应。",
        "visual": "phase",
    },
    "mix": {
        "type": "cumulative_process",
        "label_zh": "混合传质",
        "summary": "Repartitions the current phase inventory and accumulates elapsed time.",
        "summary_zh": "对当前相库存重新分配并累计混合时间。",
        "visual": "mix",
    },
    "settle": {
        "type": "cumulative_process",
        "label_zh": "静置分层",
        "summary": "Accumulates settling time and updates the current phase-settled state.",
        "summary_zh": "累计静置时间，并更新当前体系的分层状态。",
        "visual": "settle",
    },
    "separate_phase": {
        "type": "inventory_selection",
        "label_zh": "选择工作相",
        "summary": "Selects one existing phase as the working inventory.",
        "summary_zh": "选择一个现有相作为后续操作的工作库存。",
        "visual": "separate",
    },
    "wash": {
        "type": "cumulative_process",
        "label_zh": "洗涤转移",
        "summary": "Adds wash liquid and repartitions the selected phase with transfer losses.",
        "summary_zh": "加入洗液并重新分配所选相，同时计入夹带与转移损失。",
        "visual": "wash",
    },
    "dry": {
        "type": "cumulative_process",
        "label_zh": "干燥扣留",
        "summary": "Removes water-equivalent material and records retained liquid losses.",
        "summary_zh": "移除水分并记录干燥剂扣留的液体损失。",
        "visual": "dry",
    },
    "concentrate": {
        "type": "cumulative_process",
        "label_zh": "减压浓缩",
        "summary": "Reduces current liquid inventory while accumulating time and losses.",
        "summary_zh": "减少当前液体库存，并累计时间、冷凝与逸散损失。",
        "visual": "evaporate",
    },
    "transfer": {
        "type": "destructive_transfer",
        "label_zh": "转移损失",
        "summary": "Transfers part of the selected inventory and retains heel and line holdup.",
        "summary_zh": "转移所选库存的一部分，并保留釜底残留和管线持液。",
        "visual": "transfer",
    },
    "seed_crystals": {
        "type": "additive_charge",
        "label_zh": "晶种投加",
        "summary": "Adds one seed charge to the current crystallization experiment.",
        "summary_zh": "向当前结晶实验加入一次晶种。",
        "visual": "seed",
    },
    "cool_crystallize": {
        "type": "cumulative_process",
        "label_zh": "冷却结晶",
        "summary": "Recomputes the current solid-liquid state at the requested cooling endpoint.",
        "summary_zh": "按目标冷却终点更新当前固液状态并累计时间。",
        "visual": "crystallize",
    },
    "filter_crystals": {
        "type": "destructive_transfer",
        "label_zh": "过滤收集",
        "summary": "Selects and transfers the current solid phase with recovery losses.",
        "summary_zh": "过滤并转移当前固相，同时计入回收损失。",
        "visual": "filter",
    },
    "evaporate": {
        "type": "cumulative_process",
        "label_zh": "蒸发浓缩",
        "summary": "Removes part of the current liquid volume and accumulates heat exposure.",
        "summary_zh": "移除部分当前液体体积，并累计时间与热负荷。",
        "visual": "evaporate",
    },
    "distill": {
        "type": "inventory_split",
        "label_zh": "蒸馏分流",
        "summary": "Splits the current inventory into distillate and bottoms phase records.",
        "summary_zh": "将当前库存分配为馏出相与釜底相，并累计热负荷。",
        "visual": "distill",
    },
    "collect_fraction": {
        "type": "destructive_transfer",
        "label_zh": "馏分收集",
        "summary": "Transfers a fraction of the current distillate with transfer losses.",
        "summary_zh": "转移当前馏出相的一部分，并计入转移损失。",
        "visual": "collect",
    },
    "set_flow_rate": {
        "type": "configuration_update",
        "label_zh": "更新配置",
        "summary": (
            "Replaces the active flow-rate and residence-time configuration; "
            "it does not run material."
        ),
        "summary_zh": "更新当前流量与停留时间设定，本动作本身不处理物料。",
        "visual": "configure_flow",
    },
    "run_flow": {
        "type": "cumulative_process",
        "label_zh": "流动处理",
        "summary": (
            "Processes the current inventory; repeated calls process the preceding "
            "output, while process metrics describe the latest pass."
        ),
        "summary_zh": "处理当前库存；重复运行会继续处理上一次输出，过程指标描述最近一次运行。",
        "visual": "flow",
    },
    "set_potential": {
        "type": "configuration_update",
        "label_zh": "更新配置",
        "summary": (
            "Replaces the active electrochemical settings; it does not electrolyze material."
        ),
        "summary_zh": "更新当前电化学设定，本动作本身不发生电解。",
        "visual": "configure_electro",
    },
    "electrolyze": {
        "type": "cumulative_process",
        "label_zh": "累计电解",
        "summary": (
            "Advances the current composition under the active cell configuration; "
            "reported process metrics describe the latest run."
        ),
        "summary_zh": "按当前电解池配置继续处理现有组成，过程指标描述最近一次运行。",
        "visual": "electrolyze",
    },
    "terminate": {
        "type": "state_change",
        "label_zh": "终止反应",
        "summary": "Marks the current experiment terminated; it does not itself reset the vessel.",
        "summary_zh": "标记当前实验已终止，但不会自行重置容器。",
        "visual": "terminate",
    },
    "measure": {
        "type": "destructive_measurement",
        "label_zh": "取样测量",
        "summary": (
            "Consumes instrument sample volume and cost; only a successful final assay "
            "creates an experiment boundary."
        ),
        "summary_zh": "消耗仪器样品体积与费用；只有成功的最终检测才形成实验边界。",
        "visual": "measure",
    },
}


# Public schemas are intentionally broad across tasks.  Task Lab narrows them to
# the effective bounds of the currently frozen runtime so accepted inputs are
# never silently clipped to a different value.
_EFFECTIVE_BOUNDS: dict[tuple[str, str], tuple[float, float]] = {
    ("add_phase", "volume_L"): (0.0, 0.060),
    ("add_extractant", "volume_L"): (0.0, 0.060),
    ("seed_crystals", "seed_mass_g"): (0.0, 0.050),
    ("cool_crystallize", "target_temperature_K"): (250.0, 330.0),
    ("evaporate", "target_temperature_K"): (298.15, 390.0),
    ("distill", "target_temperature_K"): (298.15, 430.0),
    ("run_flow", "target_temperature_K"): (298.15, 430.0),
}

_SUPPORTED_CHOICES: dict[tuple[str, str], tuple[Any, ...]] = {
    ("add_phase", "phase"): ("aqueous", "organic"),
    # The frozen runtime records other names but does not couple them to
    # identity-specific partition physics.  Expose the physically active role.
    ("add_extractant", "extractant"): ("organic",),
    ("separate_phase", "target_phase"): ("aqueous", "organic"),
}


def operation_semantics(operation: str) -> dict[str, str]:
    """Return a JSON-safe factual effect description for one operation."""

    return dict(
        _OPERATION_EFFECTS.get(
            str(operation),
            {
                "type": "state_change",
                "label_zh": "状态更新",
                "summary": "Updates the current experiment state.",
                "summary_zh": "更新当前实验状态。",
                "visual": "generic",
            },
        )
    )


def aligned_affordance(
    entry: dict[str, Any],
    history: list[dict[str, Any]],
) -> dict[str, Any]:
    """Align an agent affordance with effective runtime semantics."""

    schema = dict(entry.get("schema") or entry)
    operation = str(entry.get("operation") or schema.get("operation") or "")
    fields = deepcopy(schema.get("fields", []))
    category_field = {
        "add_solvent": "solvent",
        "add_catalyst": "catalyst",
    }.get(operation)
    locked_value = current_recipe_category(
        history,
        operation,
        category_field,
        trace_shape=any("selected_action" in item for item in history),
    )
    for field in fields:
        field_name = str(field.get("field") or "")
        effective_bounds = _EFFECTIVE_BOUNDS.get((operation, field_name))
        if effective_bounds is not None:
            low, high = effective_bounds
            field["bounds"] = {"low": low, "high": high}
            field["recommended_range"] = {"low": low, "high": high}
            field["runtime_aligned"] = True
        supported = _SUPPORTED_CHOICES.get((operation, field_name))
        if supported is not None:
            if "choices" in field:
                field["choices"] = list(supported)
            if "allowed_values" in field:
                field["allowed_values"] = list(supported)
            field["runtime_aligned"] = True
        if category_field == field_name and locked_value is not None:
            if "choices" in field:
                field["choices"] = [locked_value]
            if "allowed_values" in field:
                field["allowed_values"] = [locked_value]
    return {
        "operation": operation,
        "required_fields": schema.get("required_fields", []),
        "fields": fields,
        "preconditions": schema.get("preconditions", []),
        "recipe_lock": (
            None
            if locked_value is None
            else {"field": category_field, "value": to_builtin(locked_value)}
        ),
        "effect": operation_semantics(operation),
    }


def validate_interactive_action(
    base: Any,
    action: dict[str, Any],
    trace: list[dict[str, Any]],
) -> dict[str, Any]:
    """Apply core validation plus fail-closed interactive semantic checks."""

    validation = dict(base.validate_action(action))
    conflicts = semantic_conflicts(base, action, trace)
    if not conflicts:
        return validation
    validation["valid"] = False
    validation["dispatchable_to_runtime"] = False
    validation["invalid_reasons"] = list(
        dict.fromkeys([*validation.get("invalid_reasons", []), *conflicts])
    )
    return validation


def semantic_conflicts(
    base: Any,
    action: dict[str, Any],
    trace: list[dict[str, Any]],
) -> list[str]:
    """Find public/runtime semantic mismatches before state mutation."""

    try:
        canonical = dict(base.action_codec.canonicalize(action))
    except (TypeError, ValueError):
        canonical = dict(action)
    operation = str(canonical.get("operation") or "")
    conflicts = categorical_recipe_conflicts(base, canonical, trace)
    for (candidate_operation, field), (low, high) in _EFFECTIVE_BOUNDS.items():
        if operation != candidate_operation or field not in canonical:
            continue
        value = canonical.get(field)
        if (
            not isinstance(value, int | float)
            or isinstance(value, bool)
            or not low <= value <= high
        ):
            conflicts.append(f"effective_runtime_bounds:{field}:{low}:{high}")
    for (candidate_operation, field), supported in _SUPPORTED_CHOICES.items():
        if operation == candidate_operation and canonical.get(field) not in supported:
            conflicts.append(f"unsupported_runtime_choice:{field}")
    if operation == "seed_crystals" and _operation_seen_in_current_experiment(
        trace, "seed_crystals"
    ):
        conflicts.append("single_seed_charge_per_experiment")
    return list(dict.fromkeys(conflicts))


def categorical_recipe_conflicts(
    base: Any,
    action: dict[str, Any],
    trace: list[dict[str, Any]],
) -> list[str]:
    operation = str(action.get("operation") or "")
    category_field = {
        "add_solvent": "solvent",
        "add_catalyst": "catalyst",
    }.get(operation)
    if category_field is None:
        return []
    try:
        proposed = base.action_codec.canonicalize(action).get(category_field)
    except (TypeError, ValueError):
        proposed = action.get(category_field)
    selected = current_recipe_category(trace, operation, category_field, trace_shape=True)
    if selected is not None and selected != proposed:
        return [f"categorical_recipe_locked:{category_field}"]
    return []


def current_recipe_category(
    history: list[dict[str, Any]],
    operation: str,
    category_field: str | None,
    *,
    trace_shape: bool = False,
) -> Any:
    if category_field is None:
        return None
    for record in reversed(history):
        action_key = "selected_action" if trace_shape else "action"
        action = dict(record.get(action_key) or {})
        if action.get("operation") == "measure" and action.get("instrument") == "final_assay":
            break
        if action.get("operation") == operation:
            return action.get(category_field)
    return None


def public_state_effects(
    action: dict[str, Any],
    info: dict[str, Any],
    *,
    experiment_index: int,
) -> dict[str, Any]:
    """Build an animation-safe effect record from public transaction deltas."""

    delta = dict(info.get("state_delta_summary") or {})
    effect = operation_semantics(str(action.get("operation") or ""))
    return {
        **effect,
        "experiment_index": int(experiment_index),
        "delta_time_s": float(delta.get("delta_time_s", 0.0)),
        "delta_cost": float(delta.get("delta_cost", info.get("cost_delta", 0.0))),
        "delta_risk": float(delta.get("delta_risk", info.get("risk_delta", 0.0))),
        "delta_temperature_K": float(delta.get("delta_temperature_K", 0.0)),
        "delta_volume_L": float(delta.get("delta_volume_L", 0.0)),
        "sample_delta_L": float(info.get("sample_delta", 0.0)),
        "affected_ledgers": list(info.get("affected_ledgers") or []),
        "transaction_status": str(info.get("transaction_status") or "unknown"),
    }


def public_vessel_summary(
    history: list[dict[str, Any]],
    campaign: dict[str, Any],
) -> dict[str, Any]:
    """Summarize only observable state deltas for the current experiment."""

    experiment_index = int(campaign.get("experiment_index", 0))
    current = [
        record for record in history if int(record.get("experiment_index", -1)) == experiment_index
    ]
    effects = [dict(record.get("state_effects") or {}) for record in current]
    latest_action = dict(current[-1].get("action") or {}) if current else {}
    last_temperature_setpoint = next(
        (
            record.get("action", {}).get("target_temperature_K")
            for record in reversed(current)
            if record.get("action", {}).get("target_temperature_K") is not None
        ),
        None,
    )
    return {
        "experiment_index": experiment_index,
        "vessel_relation": "cumulative" if current else "fresh",
        "operation_count": len(current),
        "net_volume_delta_L": sum(float(item.get("delta_volume_L", 0.0)) for item in effects),
        "elapsed_time_delta_s": sum(float(item.get("delta_time_s", 0.0)) for item in effects),
        "sampled_volume_L": sum(float(item.get("sample_delta_L", 0.0)) for item in effects),
        "latest_operation": latest_action.get("operation"),
        "last_temperature_setpoint_K": last_temperature_setpoint,
        "phase_active": any(
            record.get("action", {}).get("operation")
            in {"add_phase", "add_extractant", "mix", "settle", "separate_phase", "wash"}
            for record in current
        ),
        "solid_active": any(
            record.get("action", {}).get("operation")
            in {"seed_crystals", "cool_crystallize", "filter_crystals"}
            for record in current
        ),
    }


def _operation_seen_in_current_experiment(trace: list[dict[str, Any]], operation: str) -> bool:
    for item in reversed(trace):
        previous = dict(item.get("selected_action") or {})
        if previous.get("operation") == "measure" and previous.get("instrument") == "final_assay":
            return False
        if previous.get("operation") == operation:
            return True
    return False


__all__ = [
    "aligned_affordance",
    "categorical_recipe_conflicts",
    "current_recipe_category",
    "operation_semantics",
    "public_state_effects",
    "public_vessel_summary",
    "semantic_conflicts",
    "validate_interactive_action",
]
