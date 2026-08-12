from __future__ import annotations

from typing import Any

from chemworld.eval.work_ii_distillation_additional_rollback_q0 import (
    LAW_IDS,
    analyze,
    registered_cells,
    topology_intervention,
)
from chemworld.world.mechanism_family import MechanismFamilyIntervention
from chemworld.world.scenario import DefaultScenarioGenerator, get_scenario


def _mechanism_audit() -> dict[str, Any]:
    return {
        "native_target_reaction_is_reversible": True,
        "native_target_reaction_preserved": True,
        "added_reaction_count": 1,
        "added_reaction_id": "family_reverse_channel",
        "added_reaction_reactants": {"Ester": 1.0, "Water": 1.0},
        "added_reaction_products": {"Acid": 1.0, "Alcohol": 1.0},
        "effective_reverse_rate_constant_s_inv": 0.0005,
        "mechanism_hash_changed": True,
        "intervention_hash_deterministic": True,
        "execution_mechanism_binding_matches": True,
    }


def _rows() -> list[dict[str, Any]]:
    rows = []
    for cell in registered_cells():
        for law_id in LAW_IDS:
            time_index = int(cell["time_index"])
            rollback_penalty = 0.0 if law_id == LAW_IDS[0] else 0.08 + 0.07 * time_index
            metrics = {
                "yield": 0.78 - rollback_penalty,
                "conversion": 0.74 - rollback_penalty,
                "selectivity": 0.81 - rollback_penalty,
            }
            rows.append(
                {
                    **cell,
                    "task_id": "reaction-to-distillation",
                    "law_id": law_id,
                    "status": "completed",
                    "safe": True,
                    "exact_replay": True,
                    "action_plan_sha256": f"actions-{cell['cell_id']}",
                    "direct_noise_key_sha256": f"noise-{cell['cell_id']}",
                    "direct_metrics": metrics,
                    "direct_observed_mask": dict.fromkeys(metrics, True),
                    "participant_visible_payload": {"observation": metrics},
                }
            )
    return rows


def test_intervention_adds_rollback_to_native_reversible_network() -> None:
    intervention = MechanismFamilyIntervention.from_dict(topology_intervention())
    generator = DefaultScenarioGenerator()
    scenario = get_scenario("reaction-to-distillation")
    native = generator.generate(scenario, 0)
    shifted = generator.generate(scenario, 0, (intervention.to_dict(),))

    native_target = next(
        reaction
        for reaction in native.compiled_mechanism.network.reactions
        if reaction.reaction_id == "esterification"
    )
    shifted_target = next(
        reaction
        for reaction in shifted.compiled_mechanism.network.reactions
        if reaction.reaction_id == "esterification"
    )
    added = shifted.compiled_mechanism.network.reactions[-1]

    assert native_target.reversible is True
    assert shifted_target.to_dict() == native_target.to_dict()
    assert added.reaction_id == "family_reverse_channel"
    assert added.reactants == {"Ester": 1.0, "Water": 1.0}
    assert added.products == {"Acid": 1.0, "Alcohol": 1.0}
    assert added.rate_law.parameters["k"] == 0.0005


def test_analysis_accepts_separated_accumulating_pre_distillation_signal() -> None:
    result = analyze(_rows(), _mechanism_audit())

    assert result["passed"] is True
    assert result["denominators"] == {
        "planned": 18,
        "attempted": 18,
        "completed": 18,
        "exact_replay": 18,
        "physical_failures": 0,
        "platform_failures": 0,
        "unsafe_completed": 0,
    }
    assert result["passing_metric_count"] == 3
    assert result["separated_support"] is True


def test_analysis_rejects_weak_signal_without_lowering_gates() -> None:
    rows = _rows()
    for row in rows:
        row["direct_metrics"] = dict.fromkeys(row["direct_metrics"], 0.5)

    result = analyze(rows, _mechanism_audit())

    assert result["passed"] is False
    assert "at_least_two_direct_metrics_resolve_topology" in result["failures"]
    assert "duration_accumulation_signature" in result["failures"]


def test_analysis_retains_platform_failure_and_partial_denominator() -> None:
    rows = _rows()[:5]
    rows[-1]["status"] = "platform_failure"
    rows[-1]["exact_replay"] = False

    result = analyze(rows, _mechanism_audit())

    assert result["passed"] is False
    assert result["denominators"]["planned"] == 18
    assert result["denominators"]["attempted"] == 5
    assert result["denominators"]["platform_failures"] == 1
    assert "fixed_execution_denominator" in result["failures"]
    assert "zero_platform_failures" in result["failures"]
