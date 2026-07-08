"""Operation registry for the unified ChemWorld language."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

from chemworld.foundation import Operation
from chemworld.world.ontology import chemworld_state_variables

REACTION_OPERATIONS = (
    "add_reagent",
    "add_solvent",
    "add_catalyst",
    "heat",
    "wait",
    "sample",
    "quench",
    "terminate",
    "measure",
)
SEPARATION_OPERATIONS = (
    "add_phase",
    "add_extractant",
    "mix",
    "settle",
    "separate_phase",
    "wash",
    "dry",
    "concentrate",
    "transfer",
)
CRYSTALLIZATION_OPERATIONS = ("seed_crystals", "cool_crystallize", "filter_crystals")
DISTILLATION_OPERATIONS = ("evaporate", "distill", "collect_fraction")
FLOW_OPERATIONS = ("set_flow_rate", "run_flow")
ELECTROCHEMISTRY_OPERATIONS = ("set_potential", "electrolyze")
MACRO_OPERATIONS = ("wash", "dry", "concentrate")
TERMINAL_OPERATIONS = ("terminate",)
DOMAIN_OPERATIONS = (
    *CRYSTALLIZATION_OPERATIONS,
    *DISTILLATION_OPERATIONS,
    *FLOW_OPERATIONS,
    *ELECTROCHEMISTRY_OPERATIONS,
)
PRIMITIVE_OPERATIONS = tuple(
    operation
    for operation in (
        *REACTION_OPERATIONS,
        *SEPARATION_OPERATIONS,
        *DOMAIN_OPERATIONS,
        *TERMINAL_OPERATIONS,
    )
    if operation not in (*MACRO_OPERATIONS, *DOMAIN_OPERATIONS, *TERMINAL_OPERATIONS)
)
PROCESS_OPERATIONS = (
    *CRYSTALLIZATION_OPERATIONS,
    *DISTILLATION_OPERATIONS,
    *FLOW_OPERATIONS,
    *ELECTROCHEMISTRY_OPERATIONS,
)
OPERATION_TYPES = (
    *REACTION_OPERATIONS[:-2],
    *SEPARATION_OPERATIONS,
    *PROCESS_OPERATIONS,
    "terminate",
    "measure",
)
INSTRUMENTS = ("hplc", "gc", "uvvis", "final_assay")
DOWNSTREAM_OBSERVATION_KEYS = (
    "purity",
    "recovery",
    "phase_ratio",
    "product_in_organic",
    "product_in_aqueous",
    "impurity_signal",
    "solvent_loss",
    "process_mass_balance_error",
    "crystal_yield",
    "crystal_purity",
    "crystal_size",
    "distillate_purity",
    "distillate_recovery",
    "flow_conversion",
    "electrochemical_selectivity",
    "energy_efficiency",
)


@dataclass(frozen=True)
class OperationContract:
    operation_id: str
    module: str
    kind: str
    required_fields: tuple[str, ...]
    preconditions: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "operation_id": self.operation_id,
            "module": self.module,
            "kind": self.kind,
            "required_fields": list(self.required_fields),
            "preconditions": list(self.preconditions),
        }


def chemworld_operations() -> tuple[Operation, ...]:
    """Return operation contracts for the shared event language."""

    return (
        Operation("add_reagent", "Add reagent", ("amount_mol",), ("not_terminated",)),
        Operation("add_solvent", "Add solvent", ("volume_L", "solvent"), ("not_terminated",)),
        Operation(
            "add_catalyst",
            "Add catalyst",
            ("catalyst_amount_mol", "catalyst"),
            ("not_terminated",),
        ),
        Operation(
            "heat",
            "Heat",
            ("target_temperature_K", "duration_s", "stirring_speed_rpm"),
            ("has_volume", "has_material"),
        ),
        Operation(
            "wait",
            "Wait",
            ("duration_s", "stirring_speed_rpm"),
            ("has_volume", "has_material"),
        ),
        Operation("sample", "Sample", ("sample_volume_L",), ("has_volume",)),
        Operation("quench", "Quench", (), ("has_volume",)),
        Operation("add_phase", "Add phase", ("phase", "volume_L"), ("not_terminated",)),
        Operation(
            "add_extractant",
            "Add extractant",
            ("extractant", "volume_L"),
            ("has_volume", "has_material", "not_terminated"),
        ),
        Operation("mix", "Mix phases", ("duration_s", "stirring_speed_rpm"), ("has_phase_system",)),
        Operation("settle", "Settle phases", ("duration_s",), ("has_phase_system",)),
        Operation(
            "separate_phase",
            "Separate phase",
            ("target_phase",),
            ("has_phase_system", "phase_settled"),
        ),
        Operation("wash", "Wash product phase", ("wash_volume_L",), ("has_phase_system",)),
        Operation("dry", "Dry product phase", (), ("has_phase_system",)),
        Operation(
            "concentrate", "Concentrate product phase", ("duration_s",), ("has_phase_system",)
        ),
        Operation(
            "transfer", "Transfer product phase", ("transfer_fraction",), ("has_phase_system",)
        ),
        Operation("seed_crystals", "Seed crystallization", ("seed_mass_g",), ("has_volume",)),
        Operation(
            "cool_crystallize",
            "Cool crystallization",
            ("target_temperature_K", "duration_s"),
            ("has_volume", "has_material"),
        ),
        Operation(
            "filter_crystals",
            "Filter crystals",
            (),
            ("has_material", "filter_requires_crystallization"),
        ),
        Operation(
            "evaporate",
            "Evaporate solvent",
            ("target_temperature_K", "duration_s"),
            ("has_volume",),
        ),
        Operation(
            "distill",
            "Distill volatile fraction",
            ("target_temperature_K", "duration_s", "reflux_ratio"),
            ("has_volume", "has_material"),
        ),
        Operation(
            "collect_fraction",
            "Collect distillation fraction",
            ("transfer_fraction",),
            ("collect_fraction_requires_distillation",),
        ),
        Operation(
            "set_flow_rate",
            "Configure continuous-flow residence time",
            ("flow_rate_mL_min", "residence_time_s"),
            ("not_terminated",),
        ),
        Operation(
            "run_flow",
            "Run continuous-flow reaction",
            ("target_temperature_K", "duration_s"),
            ("has_volume", "has_material", "run_flow_requires_flow_setup"),
        ),
        Operation(
            "set_potential",
            "Configure electrochemical cell",
            ("potential_V", "current_mA"),
            ("has_volume", "has_material"),
        ),
        Operation(
            "electrolyze",
            "Run electrolysis",
            ("duration_s",),
            ("has_volume", "has_material", "electrolyze_requires_potential"),
        ),
        Operation("terminate", "Terminate", (), ("has_material",)),
        Operation("measure", "Measure", ("instrument",), ("has_volume", "instrument_specific")),
    )


def chemworld_state_variable_contracts() -> tuple[Any, ...]:
    return chemworld_state_variables()


def operation_contracts() -> dict[str, OperationContract]:
    reaction = set(REACTION_OPERATIONS)
    separation = set(SEPARATION_OPERATIONS)
    crystallization = set(CRYSTALLIZATION_OPERATIONS)
    distillation = set(DISTILLATION_OPERATIONS)
    flow = set(FLOW_OPERATIONS)
    electrochemistry = set(ELECTROCHEMISTRY_OPERATIONS)
    macros = set(MACRO_OPERATIONS)
    terminals = set(TERMINAL_OPERATIONS)
    domains = set(DOMAIN_OPERATIONS)
    contracts: dict[str, OperationContract] = {}
    for operation in chemworld_operations():
        if operation.id in separation:
            module = "separation"
        elif operation.id in crystallization:
            module = "crystallization"
        elif operation.id in distillation:
            module = "distillation"
        elif operation.id in flow:
            module = "continuous_flow"
        elif operation.id in electrochemistry:
            module = "electrochemistry"
        elif operation.id == "measure":
            module = "observation"
        elif operation.id in reaction:
            module = "reaction"
        else:
            module = "general"
        if operation.id in macros:
            kind = "macro"
        elif operation.id in terminals:
            kind = "terminal"
        elif operation.id in domains:
            kind = "domain"
        else:
            kind = "primitive"
        contracts[operation.id] = OperationContract(
            operation_id=operation.id,
            module=module,
            kind=kind,
            required_fields=operation.required_fields,
            preconditions=operation.preconditions,
        )
    return contracts


def operation_name(value: Any) -> str:
    if isinstance(value, str):
        if value not in OPERATION_TYPES:
            raise ValueError(f"Unsupported operation: {value}")
        return value
    index = int(np.asarray(value).reshape(-1)[0])
    return OPERATION_TYPES[int(np.clip(index, 0, len(OPERATION_TYPES) - 1))]


def instrument_name(value: Any) -> str:
    if isinstance(value, str):
        if value not in INSTRUMENTS:
            raise ValueError(f"Unsupported instrument: {value}")
        return value
    index = int(np.asarray(value).reshape(-1)[0])
    return INSTRUMENTS[int(np.clip(index, 0, len(INSTRUMENTS) - 1))]


__all__ = [
    "CRYSTALLIZATION_OPERATIONS",
    "DISTILLATION_OPERATIONS",
    "DOMAIN_OPERATIONS",
    "DOWNSTREAM_OBSERVATION_KEYS",
    "ELECTROCHEMISTRY_OPERATIONS",
    "FLOW_OPERATIONS",
    "INSTRUMENTS",
    "MACRO_OPERATIONS",
    "OPERATION_TYPES",
    "PRIMITIVE_OPERATIONS",
    "PROCESS_OPERATIONS",
    "REACTION_OPERATIONS",
    "SEPARATION_OPERATIONS",
    "TERMINAL_OPERATIONS",
    "OperationContract",
    "chemworld_operations",
    "chemworld_state_variable_contracts",
    "instrument_name",
    "operation_contracts",
    "operation_name",
]
