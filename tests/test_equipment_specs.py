from __future__ import annotations

import json

import pytest

from chemworld.physchem import (
    EquipmentCardSpec,
    MaturityLevel,
    column_equipment_card,
    condenser_equipment_card,
    equipment_spec_model_cards,
    evaluate_equipment_constraints,
    heat_exchanger_equipment_card,
    mixer_equipment_card,
    pump_equipment_card,
    validate_model_card,
    vessel_equipment_card,
)


def test_vessel_card_round_trip_and_hard_constraints() -> None:
    card = vessel_equipment_card(
        equipment_id="V-101",
        total_volume_m3=2.0,
        maximum_working_fraction=0.8,
        design_pressure_Pa=600_000.0,
        design_temperature_K=450.0,
        heat_transfer_area_m2=4.0,
        provenance_id="vessel-datasheet-rev-a",
    )
    restored = EquipmentCardSpec.from_dict(json.loads(json.dumps(card.to_dict())))
    feasible = evaluate_equipment_constraints(
        restored,
        {"liquid_volume_m3": 1.5, "pressure_Pa": 500_000.0, "temperature_K": 400.0},
    )
    overfilled = evaluate_equipment_constraints(
        card,
        {"liquid_volume_m3": 1.7, "pressure_Pa": 500_000.0, "temperature_K": 400.0},
    )

    assert restored == card
    assert feasible.feasible
    assert not overfilled.feasible
    assert overfilled.hard_violation_ids == ("working_volume",)


def test_pump_card_checks_flow_head_and_npsh_margin() -> None:
    card = pump_equipment_card(
        equipment_id="P-101",
        maximum_flow_m3_s=0.01,
        maximum_differential_pressure_Pa=500_000.0,
        minimum_npsh_margin_m=1.0,
        rated_efficiency=0.72,
        provenance_id="pump-curve-rev-b",
    )
    report = evaluate_equipment_constraints(
        card,
        {
            "volumetric_flow_m3_s": 0.008,
            "differential_pressure_Pa": 450_000.0,
            "npsh_margin_m": 0.5,
        },
    )

    assert not report.feasible
    assert report.hard_violation_ids == ("npsh_margin",)
    npsh = next(item for item in report.checks if item.constraint_id == "npsh_margin")
    assert npsh.margin == pytest.approx(-0.5)
    assert npsh.utilization == pytest.approx(2.0)


def test_mixer_warning_does_not_make_card_infeasible() -> None:
    card = mixer_equipment_card(
        equipment_id="M-101",
        minimum_liquid_volume_m3=0.2,
        maximum_liquid_volume_m3=1.5,
        maximum_rotational_speed_rev_s=20.0,
        maximum_power_W=5000.0,
        maximum_power_density_W_m3=3000.0,
        impeller_diameter_m=0.35,
        provenance_id="mixer-datasheet-rev-a",
    )
    report = evaluate_equipment_constraints(
        card,
        {
            "liquid_volume_m3": 1.0,
            "rotational_speed_rev_s": 15.0,
            "power_W": 3500.0,
            "power_density_W_m3": 3500.0,
        },
    )

    assert report.feasible
    assert report.warning_ids == ("maximum_power_density",)
    assert report.hard_violation_ids == ()


def test_condenser_and_heat_exchanger_share_thermal_constraint_contract() -> None:
    condenser = condenser_equipment_card(
        equipment_id="E-101",
        heat_transfer_area_m2=12.0,
        overall_u_W_m2_K=500.0,
        maximum_duty_W=200_000.0,
        design_pressure_Pa=800_000.0,
        maximum_process_temperature_K=450.0,
        provenance_id="condenser-datasheet",
    )
    exchanger = heat_exchanger_equipment_card(
        equipment_id="E-102",
        heat_transfer_area_m2=10.0,
        overall_u_W_m2_K=350.0,
        maximum_duty_W=150_000.0,
        design_pressure_Pa=700_000.0,
        maximum_process_temperature_K=430.0,
        lmtd_correction_factor=0.85,
        provenance_id="exchanger-datasheet",
    )

    assert condenser.equipment_type == "condenser"
    assert exchanger.equipment_type == "heat_exchanger"
    assert exchanger.parameters["lmtd_correction_factor"] == pytest.approx(0.85)
    assert {item.field_name for item in condenser.constraints} == {
        "duty_W",
        "pressure_Pa",
        "process_temperature_K",
    }


def test_column_card_checks_flooding_and_thermal_duties() -> None:
    card = column_equipment_card(
        equipment_id="T-101",
        diameter_m=1.2,
        height_m=18.0,
        stage_count=30,
        maximum_flood_fraction=0.8,
        design_pressure_Pa=400_000.0,
        design_temperature_K=420.0,
        maximum_reboiler_duty_W=300_000.0,
        maximum_condenser_duty_W=250_000.0,
        provenance_id="column-mechanical-card",
    )
    report = evaluate_equipment_constraints(
        card,
        {
            "flood_fraction": 0.9,
            "pressure_Pa": 350_000.0,
            "temperature_K": 390.0,
            "reboiler_duty_W": 250_000.0,
            "condenser_duty_W": 200_000.0,
        },
    )

    assert report.feasible
    assert report.warning_ids == ("flood_fraction",)
    assert card.parameters["stage_count"] == 30


def test_constraint_evaluator_rejects_missing_operating_fields() -> None:
    card = pump_equipment_card(
        equipment_id="P-102",
        maximum_flow_m3_s=0.01,
        maximum_differential_pressure_Pa=500_000.0,
        minimum_npsh_margin_m=1.0,
        rated_efficiency=0.72,
        provenance_id="pump-curve",
    )

    with pytest.raises(ValueError, match="missing"):
        evaluate_equipment_constraints(card, {"volumetric_flow_m3_s": 0.005})


def test_equipment_card_model_card_is_professional_candidate() -> None:
    card = equipment_spec_model_cards()[0]

    assert card.model_id == "typed_equipment_card_constraints_v1"
    assert card.maturity is MaturityLevel.PROFESSIONAL_CANDIDATE
    assert validate_model_card(card) == []
