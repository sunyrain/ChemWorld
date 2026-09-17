from __future__ import annotations

from scripts.author_experiment_1_c_structural_redesign import (
    NOTE,
    NOTE_SHA256,
    analyze_world,
    primary_nucleation_intervention,
)

from chemworld.eval.provenance import file_sha256
from chemworld.world.crystallization_material_family import (
    REACTION_CRYSTALLIZATION_LATENT_MATERIAL_FAMILY,
    apply_crystallization_material_family,
)
from chemworld.world.scenario import DefaultScenarioGenerator, get_scenario


def test_c_structural_note_is_bound_and_private_fork_changes_real_physics() -> None:
    assert file_sha256(NOTE) == NOTE_SHA256
    generator = DefaultScenarioGenerator()
    scenario = get_scenario("reaction-to-crystallization")
    parent = apply_crystallization_material_family(
        generator.generate(scenario, 301),
        REACTION_CRYSTALLIZATION_LATENT_MATERIAL_FAMILY,
    )
    child = apply_crystallization_material_family(
        generator.generate(scenario, 301, (primary_nucleation_intervention(),)),
        REACTION_CRYSTALLIZATION_LATENT_MATERIAL_FAMILY,
    )
    assert child.parameters.world_id != parent.parameters.world_id
    assert child.parameters.domain_parameter("crystallization_nucleation_multiplier") > (
        parent.parameters.domain_parameter("crystallization_nucleation_multiplier")
    )
    assert child.parameters.domain_parameter("crystallization_growth_multiplier") < (
        parent.parameters.domain_parameter("crystallization_growth_multiplier")
    )


def test_c_structural_analysis_accepts_interaction_and_decision_change() -> None:
    rows = []
    for seed in (0, 1):
        for temperature in (0, 1):
            for duration in (0, 1):
                cell_id = f"s{seed}-t{temperature}-d{duration}"
                parent_yield = 0.65 + 0.10 * seed + 0.04 * temperature + 0.03 * duration
                gap = 0.02 + 0.10 * seed + 0.06 * temperature - 0.08 * duration
                for law_id in ("seed_growth_parent", "primary_nucleation_dominated"):
                    child = law_id == "primary_nucleation_dominated"
                    metrics = {
                        "crystal_yield": parent_yield - gap if child else parent_yield,
                        "crystal_size": 0.70 - 0.8 * gap if child else 0.70,
                        "crystal_csd_quality": 0.75 - 0.7 * gap if child else 0.75,
                        "crystal_fines_fraction": 0.20 + gap if child else 0.20,
                        "score": 0.68 - 0.6 * gap if child else 0.68,
                    }
                    rows.append(
                        {
                            "cell_id": cell_id,
                            "law_id": law_id,
                            "seed_index": seed,
                            "temperature_index": temperature,
                            "duration_index": duration,
                            "status": "completed",
                            "metrics": metrics,
                            "exact_replay": True,
                            "truth_binding_verified": True,
                            "action_plan_sha256": f"action-{cell_id}",
                            "observation_coordinate_sha256": f"noise-{cell_id}",
                            "participant_visible_leakage_matches": [],
                        }
                    )
    result = analyze_world(
        rows,
        {
            "private_world_hash_changed": True,
            "child_hash_deterministic": True,
            "nucleation_ratio": 4.0,
            "growth_ratio": 0.25,
        },
    )
    assert result["passed"] is True
    assert result["checks"]["non_scalar_interaction_signature"] is True
    assert result["checks"]["task_decision_changes"] is True
