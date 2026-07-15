from __future__ import annotations

from typing import Any

import gymnasium as gym
import pytest

import chemworld  # noqa: F401
from chemworld.action_codec import ActionCodec


def _material_snapshot(state: Any) -> dict[str, Any]:
    return {
        "species_amounts": state.species_amounts,
        "volume_L": state.volume_L,
        "temperature_K": state.temperature_K,
        "pressure_Pa": state.pressure_Pa,
        "phase": state.phase,
        "vessel_id": state.vessel_id,
        "terminated": state.terminated,
        "quenched": state.quenched,
        "species": None if state.species is None else state.species.to_dict(),
        "phases": None if state.phases is None else state.phases.to_dict(),
        "vessels": None if state.vessels is None else state.vessels.to_dict(),
        "equipment": None if state.equipment is None else state.equipment.to_dict(),
        "thermal": None if state.thermal is None else state.thermal.to_dict(),
    }


def _assert_process_penalty(before: Any, after: Any, info: dict[str, Any]) -> None:
    assert after.ledger.cost > before.ledger.cost
    assert after.ledger.risk > before.ledger.risk
    assert after.ledger.sample_consumed_L == pytest.approx(before.ledger.sample_consumed_L)
    assert after.process is not None
    assert after.process.cost == pytest.approx(after.ledger.cost)
    assert after.process.risk == pytest.approx(after.ledger.risk)
    assert info["cost_delta"] > 0.0
    assert info["risk_delta"] > 0.0
    assert info["sample_delta"] == pytest.approx(0.0)
    assert info["affected_ledgers"] == ["process"]
    assert info["constraint_flags"]["precondition_failed"]
    assert info["state_patches_summary"][-1]["affected_ledgers"] == ["process"]


def test_task_disallowed_action_only_penalizes_process_ledger() -> None:
    env = gym.make("ChemWorld", task_id="reaction-to-assay", seed=0)
    try:
        env.reset(seed=0)
        before = env.unwrapped._state
        before_material = _material_snapshot(before)
        _obs, reward, terminated, truncated, info = env.step(
            {"operation": "add_extractant", "extractant": "organic", "volume_L": 0.010}
        )
        after = env.unwrapped._state

        assert reward == 0.0
        assert not terminated
        assert not truncated
        assert info["transaction_status"] == "validation_failed"
        assert info["rollback_reason"] == "validation_failed"
        assert info["world_events"][0]["event_type"] == "validation_failed"
        assert "operation_allowed_by_task" in info["world_events"][0]["payload"][
            "invalid_reasons"
        ]
        assert _material_snapshot(after) == before_material
        _assert_process_penalty(before, after, info)
    finally:
        env.close()


def test_payload_bounds_failure_only_penalizes_process_ledger() -> None:
    env = gym.make("ChemWorld", task_id="reaction-to-assay", seed=0)
    try:
        env.reset(seed=0)
        before = env.unwrapped._state
        before_material = _material_snapshot(before)
        _obs, reward, terminated, truncated, info = env.step(
            {"operation": "add_solvent", "volume_L": 0.2, "solvent": 1}
        )
        after = env.unwrapped._state

        assert reward == 0.0
        assert not terminated
        assert not truncated
        assert info["transaction_status"] == "validation_failed"
        assert "payload_bounds:volume_L" in info["world_events"][0]["payload"][
            "invalid_reasons"
        ]
        assert _material_snapshot(after) == before_material
        _assert_process_penalty(before, after, info)
    finally:
        env.close()


def test_cooling_schema_matches_the_current_runtime_temperature_domain() -> None:
    env = gym.make("ChemWorld", task_id="reaction-to-crystallization", seed=0)
    try:
        env.reset(seed=0)
        env.step({"operation": "add_solvent", "volume_L": 0.02, "solvent": 1})
        env.step({"operation": "add_reagent", "amount_mol": 0.01})
        env.step({"operation": "seed_crystals", "seed_mass_g": 0.001})
        env.unwrapped._state = env.unwrapped._state.replace(temperature_K=260.0)

        schema = env.unwrapped.action_schema("cool_crystallize")
        temperature = next(
            field for field in schema["fields"] if field["field"] == "target_temperature_K"
        )
        assert temperature["bounds"] == {"low": 250.0, "high": 260.0}
        assert temperature["state_dependent_bounds"] is True
        assert schema["constraints"][1]["id"] == (
            "payload_coupling:maximum_cooling_rate_K_s"
        )

        lower_boundary = env.unwrapped.validate_action(
            {
                "operation": "cool_crystallize",
                "target_temperature_K": 250.0,
                "duration_s": 3600.0,
            }
        )
        heating_through_cooling = env.unwrapped.validate_action(
            {
                "operation": "cool_crystallize",
                "target_temperature_K": 270.0,
                "duration_s": 3600.0,
            }
        )

        assert lower_boundary["valid"] is True
        assert heating_through_cooling["valid"] is False
        assert heating_through_cooling["dispatchable_to_runtime"] is False
        assert "payload_bounds:target_temperature_K" in heating_through_cooling[
            "invalid_reasons"
        ]
    finally:
        env.close()


def test_public_catalyst_display_name_is_a_supported_action_alias() -> None:
    canonical = ActionCodec().canonicalize(
        {
            "operation": "add_catalyst",
            "catalyst": "Catalyst B · benchmark",
            "catalyst_amount_mol": 0.001,
        }
    )

    assert canonical["catalyst"] == 1


def test_unknown_material_label_is_transactionally_rejected() -> None:
    env = gym.make("ChemWorld", task_id="reaction-to-assay", seed=0)
    try:
        env.reset(seed=0)
        before = env.unwrapped._state
        before_material = _material_snapshot(before)

        _obs, reward, terminated, truncated, info = env.step(
            {
                "operation": "add_catalyst",
                "catalyst": "not-a-real-choice",
                "catalyst_amount_mol": 0.001,
            }
        )
        after = env.unwrapped._state

        assert reward == 0.0
        assert not terminated
        assert not truncated
        assert info["transaction_status"] == "validation_failed"
        assert info["rollback_reason"] == "validation_failed"
        assert info["world_events"][0]["payload"]["invalid_reasons"] == [
            "payload_canonicalization_failed"
        ]
        assert _material_snapshot(after) == before_material
        _assert_process_penalty(before, after, info)
    finally:
        env.close()


def test_state_precondition_rollback_only_penalizes_process_ledger() -> None:
    env = gym.make("ChemWorld", task_id="reaction-to-assay", seed=0)
    try:
        env.reset(seed=0)
        before = env.unwrapped._state
        before_material = _material_snapshot(before)
        _obs, reward, terminated, truncated, info = env.step(
            {"operation": "measure", "instrument": "final_assay"}
        )
        after = env.unwrapped._state

        assert reward == 0.0
        assert not terminated
        assert not truncated
        assert info["transaction_status"] == "rolled_back"
        assert info["rollback_reason"] == "precondition_failed"
        assert info["world_events"][0]["event_type"] == "operation_rejected"
        assert info["world_events"][-1]["event_type"] == "transaction_rollback"
        assert _material_snapshot(after) == before_material
        _assert_process_penalty(before, after, info)
    finally:
        env.close()
