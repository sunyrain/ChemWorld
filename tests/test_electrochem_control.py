from __future__ import annotations

import pytest

from chemworld.physchem import (
    ElectrochemicalControlLimits,
    ElectrochemicalControlRecipe,
    ElectrochemicalControlSegment,
    MaturityLevel,
    electrochemistry_model_cards,
    execute_electrochemical_control_recipe,
    validate_model_card,
    verify_electrochemical_control_replay,
)


def _limits() -> ElectrochemicalControlLimits:
    return ElectrochemicalControlLimits(
        minimum_potential_V=-1.5,
        maximum_potential_V=1.5,
        minimum_current_A=-0.2,
        maximum_current_A=0.2,
        maximum_potential_slew_V_s=0.1,
        maximum_current_slew_A_s=0.05,
        provenance_id="potentiostat-datasheet",
    )


def test_ramp_and_hold_recipe_clips_range_and_slew_with_operation_logs() -> None:
    recipe = ElectrochemicalControlRecipe(
        recipe_id="mixed_control",
        segments=(
            ElectrochemicalControlSegment("potential_ramp", "potentiostatic", "ramp", 2.0, 5.0),
            ElectrochemicalControlSegment("potential_hold", "potentiostatic", "hold", 0.5, 2.0),
            ElectrochemicalControlSegment("current_ramp", "galvanostatic", "ramp", 0.3, 2.0),
            ElectrochemicalControlSegment("current_hold", "galvanostatic", "hold", 0.1, 3.0),
        ),
        sample_interval_s=1.0,
        provenance_id="mixed-control-recipe",
    )
    result = execute_electrochemical_control_recipe(
        recipe,
        _limits(),
        initial_potential_V=0.0,
        initial_current_A=0.0,
    )

    assert result.final_potential_V == pytest.approx(0.5)
    assert result.final_current_A == pytest.approx(0.1)
    assert result.total_duration_s == pytest.approx(12.0)
    assert result.clipping_event_count == 4
    potential_ramp = result.operation_logs[0]
    assert potential_ramp.range_clipped
    assert potential_ramp.slew_clipped
    assert potential_ramp.range_clipped_target_value == pytest.approx(1.5)
    assert potential_ramp.applied_end_value == pytest.approx(0.5)
    current_ramp = result.operation_logs[2]
    assert current_ramp.range_clipped
    assert current_ramp.slew_clipped
    assert current_ramp.applied_end_value == pytest.approx(0.1)


def test_ramp_trace_is_linear_and_hold_trace_is_constant() -> None:
    recipe = ElectrochemicalControlRecipe(
        recipe_id="potential_ramp_hold",
        segments=(
            ElectrochemicalControlSegment("ramp", "potentiostatic", "ramp", 0.4, 4.0),
            ElectrochemicalControlSegment("hold", "potentiostatic", "hold", 0.4, 2.0),
        ),
        sample_interval_s=1.0,
        provenance_id="linear-trace-recipe",
    )
    result = execute_electrochemical_control_recipe(
        recipe,
        _limits(),
        initial_potential_V=0.0,
        initial_current_A=0.0,
    )
    ramp_points = [point for point in result.trace if point.segment_id == "ramp"]
    hold_points = [point for point in result.trace if point.segment_id == "hold"]

    assert [point.applied_value for point in ramp_points] == pytest.approx(
        [0.0, 0.1, 0.2, 0.3, 0.4]
    )
    assert {point.applied_value for point in hold_points} == {0.4}
    assert not result.operation_logs[1].hold_step_exceeds_slew_limit


def test_hold_step_beyond_sample_slew_is_flagged_without_hidden_ramp() -> None:
    recipe = ElectrochemicalControlRecipe(
        recipe_id="step_hold",
        segments=(
            ElectrochemicalControlSegment("step", "galvanostatic", "hold", 0.2, 2.0),
        ),
        sample_interval_s=0.5,
        provenance_id="step-recipe",
    )
    result = execute_electrochemical_control_recipe(
        recipe,
        _limits(),
        initial_potential_V=0.0,
        initial_current_A=0.0,
    )

    assert result.operation_logs[0].hold_step_exceeds_slew_limit
    assert result.operation_logs[0].applied_end_value == pytest.approx(0.2)
    assert all(point.applied_value == pytest.approx(0.2) for point in result.trace)


def test_execution_hash_and_replay_contract_detect_recipe_change() -> None:
    recipe = ElectrochemicalControlRecipe(
        recipe_id="replayable",
        segments=(
            ElectrochemicalControlSegment("ramp", "potentiostatic", "ramp", 0.2, 2.0),
        ),
        sample_interval_s=0.5,
        provenance_id="replay-recipe",
    )
    execution = execute_electrochemical_control_recipe(
        recipe,
        _limits(),
        initial_potential_V=0.0,
        initial_current_A=0.0,
    )
    changed = ElectrochemicalControlRecipe(
        recipe_id="replayable",
        segments=(
            ElectrochemicalControlSegment("ramp", "potentiostatic", "ramp", 0.3, 2.0),
        ),
        sample_interval_s=0.5,
        provenance_id="replay-recipe",
    )

    assert len(execution.recipe_hash) == 64
    assert len(execution.execution_hash) == 64
    assert verify_electrochemical_control_replay(execution, recipe, _limits())
    assert not verify_electrochemical_control_replay(execution, changed, _limits())


def test_controller_contract_rejects_duplicate_segment_ids() -> None:
    with pytest.raises(ValueError, match="unique"):
        ElectrochemicalControlRecipe(
            recipe_id="duplicate",
            segments=(
                ElectrochemicalControlSegment("same", "potentiostatic", "hold", 0.0, 1.0),
                ElectrochemicalControlSegment("same", "galvanostatic", "hold", 0.0, 1.0),
            ),
            sample_interval_s=1.0,
            provenance_id="invalid-recipe",
        )


def test_electrochemical_controller_model_card_is_reference_validated() -> None:
    card = {
        item.model_id: item for item in electrochemistry_model_cards()
    }["electrochemical_setpoint_recipe_controller_v1"]

    assert card.maturity is MaturityLevel.REFERENCE_VALIDATED
    assert validate_model_card(card) == []
