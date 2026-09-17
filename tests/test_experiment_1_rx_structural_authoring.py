from __future__ import annotations

from scripts.author_experiment_1_rx_structural_redesign import (
    NOTE,
    NOTE_SHA256,
    _analyze_reversible,
    reversible_intervention,
)

from chemworld.eval.provenance import file_sha256
from chemworld.eval.work_ii_catalyst_deactivation_q0 import registered_cells
from chemworld.world.scenario import DefaultScenarioGenerator, get_scenario


def test_rx_structural_authoring_note_is_bound_and_reverse_channel_is_executable() -> None:
    assert file_sha256(NOTE) == NOTE_SHA256
    baseline = DefaultScenarioGenerator().generate(get_scenario("reaction-safety"), 201)
    reversible = DefaultScenarioGenerator().generate(
        get_scenario("reaction-safety"), 201, (reversible_intervention(),)
    )
    baseline_ids = {
        reaction.reaction_id for reaction in baseline.compiled_mechanism.network.reactions
    }
    reversible_ids = {
        reaction.reaction_id for reaction in reversible.compiled_mechanism.network.reactions
    }
    assert reversible_ids - baseline_ids == {"family_reverse_channel"}


def test_reversible_analysis_requires_and_accepts_task_relevant_time_signal() -> None:
    rows = []
    for cell in registered_cells():
        duration = int(cell["duration_index"])
        dose = int(cell["dose_index"])
        baseline_yield = 0.60 + 0.10 * duration - 0.08 * duration**2 + 0.005 * dose
        gap = 0.02 + 0.08 * duration + 0.01 * dose
        for law_id in ("deactivating_baseline", "reversible_target_pathway"):
            offset = 0.0 if law_id == "deactivating_baseline" else gap
            metrics = {
                "yield": baseline_yield - offset,
                "conversion": 0.70 + 0.04 * duration - offset,
                "selectivity": 0.80 - 0.5 * offset,
            }
            rows.append(
                {
                    **cell,
                    "law_id": law_id,
                    "status": "completed",
                    "safe": True,
                    "exact_replay": True,
                    "action_plan_sha256": f"action-{cell['cell_id']}",
                    "direct_noise_key_sha256": f"noise-{cell['cell_id']}",
                    "direct_metrics": metrics,
                    "direct_observed_mask": dict.fromkeys(metrics, True),
                    "participant_visible_leakage_matches": [],
                }
            )
    result = _analyze_reversible(
        rows,
        {
            "added_reaction_count": 1,
            "added_reaction_id": "family_reverse_channel",
            "mechanism_hash_changed": True,
            "reversible_hash_deterministic": True,
            "execution_mechanism_binding_matches": True,
            "opposite_stoichiometric_channel": True,
        },
    )
    assert result["passed"] is True
    assert result["passing_metric_count"] >= 2
    assert result["checks"]["duration_accumulation_signature"] is True
    assert result["checks"]["stopping_decision_changed"] is True
