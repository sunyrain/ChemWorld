"""Operation precondition checks for the executable physical constitution."""

from __future__ import annotations

from typing import Any

from chemworld.foundation.state import (
    WorldState,
    equipment_settings,
    has_phase_system,
    instrument_completed,
    phases_are_settled,
)


def check_operation_preconditions(
    constitution: Any,
    operation_type: str,
    state: WorldState,
    payload: dict[str, Any],
) -> dict[str, bool]:
    has_volume = state.volume_L > constitution.tolerance
    has_material = sum(state.species_amounts.values()) > constitution.tolerance
    is_terminated = state.terminated
    instrument_id = str(payload.get("instrument", "hplc"))
    instrument = constitution.instruments.get(instrument_id)
    if instrument is None and instrument_id.isdigit():
        instruments = list(constitution.instruments.values())
        instrument = instruments[int(instrument_id) % len(instruments)]
    requires_terminated = (
        bool(instrument.requires_terminated) if instrument is not None else False
    )
    final_assay_done = instrument_completed(state.equipment, "final_assay")
    is_final_assay = operation_type == "measure" and instrument_id == "final_assay"
    phase_system = has_phase_system(state.phases)
    phase_settled = phases_are_settled(state.phases)
    crystallized = (
        state.phases is not None
        and "solid" in state.phases.phases
        and sum(state.phases.phases["solid"].species_amounts_mol.values())
        > constitution.tolerance
    )
    distillate_ready = (
        state.phases is not None
        and "distillate" in state.phases.phases
        and sum(state.phases.phases["distillate"].species_amounts_mol.values())
        > constitution.tolerance
    )
    flow_settings = equipment_settings(state.equipment, "flow_reactor")
    potential_settings = equipment_settings(state.equipment, "electrochemical_cell")
    flow_ready = {"flow_rate_mL_min", "residence_time_s"} <= set(flow_settings)
    potential_ready = {"potential_V", "current_mA"} <= set(potential_settings)
    phase_operations = {
        "add_extractant",
        "mix",
        "settle",
        "separate_phase",
        "wash",
        "dry",
        "concentrate",
        "transfer",
    }
    needs_volume = operation_type in {
        "heat",
        "wait",
        "sample",
        "quench",
        "measure",
        "add_extractant",
        "mix",
        "settle",
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
        "set_potential",
        "run_flow",
        "electrolyze",
    }
    needs_material = operation_type in {
        "heat",
        "wait",
        "terminate",
        "add_extractant",
        "mix",
        "settle",
        "separate_phase",
        "wash",
        "dry",
        "concentrate",
        "transfer",
        "cool_crystallize",
        "filter_crystals",
        "distill",
        "collect_fraction",
        "set_potential",
        "run_flow",
        "electrolyze",
    }
    needs_not_terminated = operation_type in {
        "add_reagent",
        "add_solvent",
        "add_catalyst",
        "heat",
        "wait",
        "sample",
        "quench",
        "add_phase",
        "add_extractant",
        "mix",
        "settle",
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
        "set_flow_rate",
        "run_flow",
        "set_potential",
        "electrolyze",
    }
    return {
        "instrument_available": operation_type != "measure" or instrument is not None,
        "has_volume": not needs_volume or has_volume,
        "has_material": not needs_material or has_material,
        "not_terminated": not needs_not_terminated or not state.terminated,
        "has_phase_system": operation_type not in phase_operations or phase_system,
        "phase_settled": operation_type != "separate_phase" or phase_settled,
        "measure_final_requires_terminated": operation_type != "measure"
        or not requires_terminated
        or is_terminated,
        "measure_final_not_repeated": not is_final_assay or not final_assay_done,
        "terminate_requires_material": operation_type != "terminate" or has_material,
        "filter_requires_crystallization": operation_type != "filter_crystals"
        or crystallized,
        "collect_fraction_requires_distillation": operation_type != "collect_fraction"
        or distillate_ready,
        "run_flow_requires_flow_setup": operation_type != "run_flow" or flow_ready,
        "electrolyze_requires_potential": operation_type != "electrolyze"
        or potential_ready,
    }


__all__ = ["check_operation_preconditions"]
