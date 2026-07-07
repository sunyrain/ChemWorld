"""Foundation-backed ChemWorld reaction and separation module."""

from __future__ import annotations

import os
from dataclasses import dataclass
from hashlib import sha256
from typing import Any

import numpy as np
from scipy.integrate import solve_ivp

from chemworld.core.actions import CATALYSTS, SOLVENTS, canonicalize_action
from chemworld.core.objectives import score_observation
from chemworld.foundation import (
    Instrument,
    Observation,
    Operation,
    OperationRecord,
    PhysicalConstitution,
    Reaction,
    StateVariable,
    Substance,
    TransitionKernel,
    Vessel,
    WorldLawSpec,
    WorldState,
)

R_GAS = 8.31446261815324
WORLD_FAMILY_VERSION = "chemworld-physical-chemistry"
SUPPORTED_SPLITS = ("public-dev", "public-test", "private-eval")
SPECIES = ("A", "P", "B", "D", "E", "Cat_active", "Cat_dead")
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
class ChemWorldParameters:
    world_id: str
    split: str
    provider: str
    family_version: str
    pre_exponential: np.ndarray
    activation_energy: np.ndarray
    catalyst_effects: np.ndarray
    solvent_effects: np.ndarray
    solvent_risks: np.ndarray
    solvent_costs: np.ndarray
    catalyst_costs: np.ndarray
    delta_h_J_per_mol: np.ndarray
    ua_W_per_K: float
    rho_cp_J_per_L_K: float
    environment_temperature_K: float


def _stable_seed(split: str, seed: int, private_salt: str = "") -> int:
    digest = sha256(f"{WORLD_FAMILY_VERSION}:{split}:{seed}:{private_salt}".encode()).digest()
    return int.from_bytes(digest[:8], "little") % (2**32)


def load_chemworld_parameters(
    split: str = "public-dev",
    seed: int = 0,
) -> ChemWorldParameters:
    if split not in SUPPORTED_SPLITS:
        allowed = ", ".join(SUPPORTED_SPLITS)
        raise ValueError(f"Unsupported world_split={split!r}. Allowed: {allowed}")

    private_salt = ""
    provider = "public-registry"
    if split == "private-eval":
        private_salt = os.environ.get("CHEMWORLD_PRIVATE_EVAL_SALT", "")
        provider = "external-private-registry" if private_salt else "public-placeholder-private"

    rng = np.random.default_rng(_stable_seed(split, seed, private_salt))
    split_shift = {"public-dev": 0.0, "public-test": 0.06, "private-eval": -0.05}[split]
    pre_exponential = np.array([90.0, 190.0, 520.0, 65.0, 30.0])
    pre_exponential *= rng.lognormal(mean=split_shift, sigma=[0.10, 0.15, 0.18, 0.18, 0.14])
    activation_energy = np.array([31_000.0, 38_500.0, 45_000.0, 42_000.0, 36_000.0])
    activation_energy *= rng.lognormal(mean=0.0, sigma=[0.03, 0.05, 0.06, 0.06, 0.05])

    catalyst_effects = rng.lognormal(mean=0.0, sigma=0.22, size=(len(CATALYSTS), 5))
    catalyst_effects[:, 0] *= np.array([1.00, 1.30, 0.82, 1.10])
    catalyst_effects[:, 1] *= np.array([1.05, 0.92, 1.32, 0.86])
    catalyst_effects[:, 2] *= np.array([0.92, 1.15, 0.90, 1.22])
    catalyst_effects[:, 3] *= np.array([0.95, 1.08, 1.18, 0.90])
    catalyst_effects[:, 4] *= np.array([0.88, 1.10, 0.94, 1.20])

    solvent_effects = rng.lognormal(mean=0.0, sigma=0.20, size=(len(SOLVENTS), 5))
    solvent_effects[:, 0] *= np.array([0.75, 0.96, 1.20, 1.05])
    solvent_effects[:, 1] *= np.array([0.72, 1.02, 0.98, 1.34])
    solvent_effects[:, 2] *= np.array([0.68, 1.00, 1.12, 1.28])
    solvent_effects[:, 3] *= np.array([0.70, 0.95, 1.15, 1.25])
    solvent_effects[:, 4] *= np.array([0.65, 1.05, 0.98, 1.18])

    provider_label = "external" if provider == "external-private-registry" else "public"
    world_id = f"ChemWorld:{split}:{provider_label}:seed-{seed}"
    return ChemWorldParameters(
        world_id=world_id,
        split=split,
        provider=provider,
        family_version=WORLD_FAMILY_VERSION,
        pre_exponential=pre_exponential,
        activation_energy=activation_energy,
        catalyst_effects=catalyst_effects,
        solvent_effects=solvent_effects,
        solvent_risks=np.array([0.05, 0.18, 0.28, 0.35]),
        solvent_costs=np.array([0.03, 0.08, 0.16, 0.11]),
        catalyst_costs=np.array([0.08, 0.18, 0.12, 0.22]),
        delta_h_J_per_mol=np.array([-42_000.0, -25_000.0, -18_000.0, -35_000.0, -5_000.0]),
        ua_W_per_K=float(rng.uniform(0.05, 0.12)),
        rho_cp_J_per_L_K=float(rng.uniform(3800.0, 4300.0)),
        environment_temperature_K=298.15,
    )


def batch_reactor_substances() -> dict[str, Substance]:
    return {
        "A": Substance("A", "reactant A", {"C": 1}),
        "P": Substance("P", "target product P", {"C": 1}),
        "B": Substance("B", "byproduct B", {"C": 1}),
        "D": Substance("D", "degradation product D", {"C": 1}),
        "E": Substance("E", "coupled impurity E", {"C": 2}),
        "Cat_active": Substance("Cat_active", "active catalyst", {"Cat": 1}, role="catalyst"),
        "Cat_dead": Substance("Cat_dead", "deactivated catalyst", {"Cat": 1}, role="catalyst"),
    }


def batch_reactor_instruments() -> dict[str, Instrument]:
    return {
        "hplc": Instrument(
            "hplc",
            "HPLC",
            (
                "yield",
                "selectivity",
                "byproduct_signal",
                "purity",
                "impurity_signal",
                "crystal_purity",
                "distillate_purity",
            ),
            cost=0.08,
            sample_volume_L=0.00020,
            noise_std={
                "yield": 0.012,
                "selectivity": 0.018,
                "byproduct_signal": 0.012,
                "purity": 0.015,
                "impurity_signal": 0.015,
                "crystal_purity": 0.018,
                "distillate_purity": 0.014,
            },
        ),
        "gc": Instrument(
            "gc",
            "GC",
            ("byproduct_signal", "degradation_warning", "distillate_purity"),
            cost=0.06,
            sample_volume_L=0.00015,
            noise_std={
                "byproduct_signal": 0.018,
                "degradation_warning": 0.018,
                "distillate_purity": 0.020,
            },
        ),
        "uvvis": Instrument(
            "uvvis",
            "UV-vis",
            ("yield", "conversion", "phase_ratio", "flow_conversion", "energy_efficiency"),
            cost=0.025,
            sample_volume_L=0.00005,
            noise_std={
                "yield": 0.045,
                "conversion": 0.035,
                "phase_ratio": 0.040,
                "flow_conversion": 0.040,
                "energy_efficiency": 0.045,
            },
        ),
        "final_assay": Instrument(
            "final_assay",
            "Final assay",
            (
                "yield",
                "selectivity",
                "conversion",
                "byproduct_signal",
                "degradation_warning",
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
            ),
            cost=0.16,
            sample_volume_L=0.00030,
            noise_std={
                "yield": 0.006,
                "selectivity": 0.010,
                "conversion": 0.008,
                "byproduct_signal": 0.008,
                "degradation_warning": 0.008,
                "purity": 0.008,
                "recovery": 0.010,
                "phase_ratio": 0.012,
                "product_in_organic": 0.010,
                "product_in_aqueous": 0.010,
                "impurity_signal": 0.008,
                "solvent_loss": 0.012,
                "process_mass_balance_error": 0.004,
                "crystal_yield": 0.010,
                "crystal_purity": 0.010,
                "crystal_size": 0.025,
                "distillate_purity": 0.010,
                "distillate_recovery": 0.012,
                "flow_conversion": 0.012,
                "electrochemical_selectivity": 0.012,
                "energy_efficiency": 0.016,
            },
            requires_terminated=True,
        ),
    }


def batch_reactor_reactions() -> tuple[Reaction, ...]:
    return (
        Reaction("r1", "A -> P", {"A": -1.0, "P": 1.0}, -42_000.0),
        Reaction("r2", "A -> B", {"A": -1.0, "B": 1.0}, -25_000.0),
        Reaction("r3", "P -> D", {"P": -1.0, "D": 1.0}, -18_000.0),
        Reaction("r4", "A + P -> E", {"A": -1.0, "P": -1.0, "E": 1.0}, -35_000.0),
        Reaction(
            "r5",
            "Cat_active -> Cat_dead",
            {"Cat_active": -1.0, "Cat_dead": 1.0},
            -5_000.0,
        ),
    )


def chemworld_world_law_spec() -> WorldLawSpec:
    """Return the shared physical-chemical law used by all ChemWorld tasks."""

    return WorldLawSpec(
        law_version=WORLD_FAMILY_VERSION,
        ontology_registry={
            "substances": sorted(batch_reactor_substances()),
            "phases": ["reactor_liquid", "aqueous", "organic", "solid"],
            "vessels": ["batch_reactor", "separator", "assay_vial"],
            "instruments": list(INSTRUMENTS),
        },
        physical_constitution="PhysicalConstitutionChecklist",
        operation_registry=OPERATION_TYPES,
        transition_kernel_registry=(
            "reaction_ode",
            "thermal_energy_balance",
            "phase_partition",
            "separation",
            "instrument_cost",
        ),
        observation_kernel_registry=("instrument_observation",),
        instrument_registry={
            key: {
                "instrument_id": instrument.id,
                "observable_keys": list(instrument.observable_keys),
                "cost": instrument.cost,
                "sample_consumption_L": instrument.sample_volume_L,
                "requires_terminated": instrument.requires_terminated,
                "noise_model": instrument.noise_std,
            }
            for key, instrument in batch_reactor_instruments().items()
        },
        module_versions={
            "reaction": "0.2",
            "thermal": "0.2",
            "phase_partition": "0.2",
            "separation": "0.2",
            "observation": "0.2",
        },
        backend={"backend_id": "semi_mechanistic", "fidelity": "qualitative"},
        constitution_rules=(
            "material_conservation",
            "nonnegative_state",
            "unit_consistency",
            "yield_upper_bound",
            "energy_balance",
            "phase_mass_balance",
            "observation_non_omniscient",
            "measurement_has_cost",
            "action_preconditions",
            "safety_constraints",
            "public_private_reproducibility",
        ),
        scenario_generators=("chemworld.scenario.default",),
    )


def batch_reactor_operations() -> tuple[Operation, ...]:
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


def batch_reactor_state_variables() -> tuple[StateVariable, ...]:
    return (
        StateVariable("species_amounts", "mol", hidden=True),
        StateVariable("volume_L", "L", hidden=True),
        StateVariable("temperature_K", "K", hidden=True),
        StateVariable("pressure_Pa", "Pa", hidden=True),
        StateVariable("metadata.stirring_speed_rpm", "rpm", hidden=True),
        StateVariable("ledger.cost", "currency", hidden=False),
        StateVariable("ledger.risk", "risk", hidden=False),
        StateVariable("ledger.time_s", "s", hidden=False),
        StateVariable("metadata.phase_ledger", "dimensionless", hidden=True),
        StateVariable("metadata.purity", "dimensionless", hidden=True),
        StateVariable("metadata.recovery", "dimensionless", hidden=True),
        StateVariable("metadata.process_mass_balance_error", "dimensionless", hidden=True),
        StateVariable("metadata.crystal_yield", "dimensionless", hidden=True),
        StateVariable("metadata.distillate_purity", "dimensionless", hidden=True),
        StateVariable("metadata.flow_conversion", "dimensionless", hidden=True),
        StateVariable("metadata.electrochemical_selectivity", "dimensionless", hidden=True),
    )


def make_chemworld_constitution() -> PhysicalConstitution:
    return PhysicalConstitution(
        substances=batch_reactor_substances(),
        vessel=Vessel(
            "batch_reactor",
            "Virtual 100 mL jacketed batch reactor",
            max_volume_L=0.10,
            max_temperature_K=470.0,
            max_pressure_Pa=550_000.0,
        ),
        instruments=batch_reactor_instruments(),
        max_yield=1.0,
        tolerance=5.0e-7,
    )


def initial_chemworld_state() -> WorldState:
    return WorldState(
        species_amounts=dict.fromkeys(SPECIES, 0.0),
        volume_L=0.0,
        temperature_K=298.15,
        pressure_Pa=101_325.0,
        phase="liquid",
        vessel_id="batch_reactor",
        units={
            "amount": "mol",
            "volume": "L",
            "temperature": "K",
            "pressure": "Pa",
            "time": "s",
            "cost": "currency",
            "risk": "risk",
        },
    ).replace(
        metadata={
            "initial_A_mol": 0.0,
            "solvent": 0,
            "catalyst": 0,
            "stirring_speed_rpm": 600.0,
            "last_observation": {},
            "phase_ledger": {
                "reactor_liquid": {
                    "volume_L": 0.0,
                    "P_mol": 0.0,
                    "impurity_mol": 0.0,
                    "solvent_loss": 0.0,
                }
            },
        }
    )


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


def _action_float(action: dict[str, Any], key: str, default: float) -> float:
    value = action.get(key, default)
    return float(np.asarray(value).reshape(-1)[0])


def _action_index(action: dict[str, Any], key: str, default: int, count: int) -> int:
    return int(np.clip(int(_action_float(action, key, float(default))), 0, count - 1))


class ChemWorldTransitionKernel(TransitionKernel):
    def __init__(
        self,
        world: ChemWorldParameters,
        constitution: PhysicalConstitution,
    ) -> None:
        self.world = world
        self.constitution = constitution

    def transition(
        self,
        state: WorldState,
        action: dict[str, Any],
        rng: np.random.Generator,
    ) -> tuple[WorldState, OperationRecord]:
        del rng
        operation = operation_name(action["operation"])
        before = state
        preconditions = self.constitution.check_preconditions(operation, state, action)
        if not all(preconditions.values()):
            next_state = self._penalize_invalid(state)
            return next_state, self._record(operation, before, next_state, preconditions, action)

        if operation == "add_reagent":
            next_state = self._add_reagent(state, action)
        elif operation == "add_solvent":
            next_state = self._add_solvent(state, action)
        elif operation == "add_catalyst":
            next_state = self._add_catalyst(state, action)
        elif operation == "heat":
            next_state = self._integrate(state, action, heat=True)
        elif operation == "wait":
            next_state = self._integrate(state, action, heat=False)
        elif operation == "sample":
            next_state = self._sample(state, action)
        elif operation == "quench":
            next_state = self._quench(state)
        elif operation == "add_phase":
            next_state = self._add_phase(state, action)
        elif operation == "add_extractant":
            next_state = self._add_extractant(state, action)
        elif operation == "mix":
            next_state = self._mix_phases(state, action)
        elif operation == "settle":
            next_state = self._settle_phases(state, action)
        elif operation == "separate_phase":
            next_state = self._separate_phase(state, action)
        elif operation == "wash":
            next_state = self._wash_phase(state, action)
        elif operation == "dry":
            next_state = self._dry_phase(state)
        elif operation == "concentrate":
            next_state = self._concentrate_phase(state, action)
        elif operation == "transfer":
            next_state = self._transfer_phase(state, action)
        elif operation == "seed_crystals":
            next_state = self._seed_crystals(state, action)
        elif operation == "cool_crystallize":
            next_state = self._cool_crystallize(state, action)
        elif operation == "filter_crystals":
            next_state = self._filter_crystals(state)
        elif operation == "evaporate":
            next_state = self._evaporate(state, action)
        elif operation == "distill":
            next_state = self._distill(state, action)
        elif operation == "collect_fraction":
            next_state = self._collect_fraction(state, action)
        elif operation == "set_flow_rate":
            next_state = self._set_flow_rate(state, action)
        elif operation == "run_flow":
            next_state = self._run_flow(state, action)
        elif operation == "set_potential":
            next_state = self._set_potential(state, action)
        elif operation == "electrolyze":
            next_state = self._electrolyze(state, action)
        elif operation == "terminate":
            next_state = state.replace(terminated=True)
        elif operation == "measure":
            next_state = self._apply_measurement_cost(state, action)
        else:
            raise ValueError(f"Unsupported operation: {operation}")

        next_state = self._with_risk_and_pressure(next_state)
        return next_state, self._record(operation, before, next_state, preconditions, action)

    def _add_reagent(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        amount = float(np.clip(_action_float(action, "amount_mol", 0.003), 0.0, 0.040))
        species = state.species_amounts.copy()
        species["A"] += amount
        metadata = state.metadata.copy()
        metadata["initial_A_mol"] = float(metadata.get("initial_A_mol", 0.0)) + amount
        ledger = state.ledger.with_updates(cost=state.ledger.cost + 0.03 * amount / 0.01)
        return state.replace(species_amounts=species, ledger=ledger, metadata=metadata)

    def _add_solvent(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        volume = float(np.clip(_action_float(action, "volume_L", 0.025), 0.0, 0.080))
        solvent = _action_index(action, "solvent", 0, len(SOLVENTS))
        metadata = state.metadata.copy()
        metadata["solvent"] = solvent
        ledger = state.ledger.with_updates(
            cost=state.ledger.cost + volume * 8.0 * float(self.world.solvent_costs[solvent])
        )
        return state.replace(volume_L=state.volume_L + volume, ledger=ledger, metadata=metadata)

    def _add_catalyst(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        amount = float(np.clip(_action_float(action, "catalyst_amount_mol", 0.00020), 0.0, 0.005))
        catalyst = _action_index(action, "catalyst", 0, len(CATALYSTS))
        species = state.species_amounts.copy()
        species["Cat_active"] += amount
        metadata = state.metadata.copy()
        metadata["catalyst"] = catalyst
        ledger = state.ledger.with_updates(
            cost=state.ledger.cost
            + 4.0 * amount / 0.001 * float(self.world.catalyst_costs[catalyst])
        )
        return state.replace(species_amounts=species, ledger=ledger, metadata=metadata)

    def _sample(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        volume = float(np.clip(_action_float(action, "sample_volume_L", 0.0001), 0.0, 0.002))
        volume = min(volume, max(state.volume_L, 0.0))
        fraction = 0.0 if state.volume_L <= 0 else volume / state.volume_L
        species = {key: value * (1.0 - fraction) for key, value in state.species_amounts.items()}
        ledger = state.ledger.with_updates(
            sample_consumed_L=state.ledger.sample_consumed_L + volume,
            cost=state.ledger.cost + 0.01,
        )
        return state.replace(
            species_amounts=species,
            volume_L=state.volume_L - volume,
            ledger=ledger,
        )

    def _quench(self, state: WorldState) -> WorldState:
        target = max(298.15, state.temperature_K - 45.0)
        ledger = state.ledger.with_updates(cost=state.ledger.cost + 0.03)
        return state.replace(temperature_K=target, quenched=True, ledger=ledger)

    def _phase_ledger(self, state: WorldState) -> dict[str, dict[str, float]]:
        raw = state.metadata.get("phase_ledger", {})
        ledger: dict[str, dict[str, float]] = {}
        for phase_name, values in dict(raw).items():
            ledger[str(phase_name)] = {
                "volume_L": float(values.get("volume_L", 0.0)),
                "P_mol": float(values.get("P_mol", 0.0)),
                "impurity_mol": float(values.get("impurity_mol", 0.0)),
                "solvent_loss": float(values.get("solvent_loss", 0.0)),
            }
        if "reactor_liquid" not in ledger:
            ledger["reactor_liquid"] = {
                "volume_L": state.volume_L,
                "P_mol": state.species_amounts.get("P", 0.0),
                "impurity_mol": state.species_amounts.get("B", 0.0)
                + state.species_amounts.get("D", 0.0)
                + state.species_amounts.get("E", 0.0),
                "solvent_loss": 0.0,
            }
        return ledger

    def _write_phase_metadata(
        self,
        state: WorldState,
        phase_ledger: dict[str, dict[str, float]],
        *,
        updates: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        metadata = state.metadata.copy()
        metadata["phase_ledger"] = phase_ledger
        metadata.update(_downstream_truth_values(state, phase_ledger))
        if updates:
            metadata.update(updates)
        return metadata

    def _add_phase(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        volume = float(np.clip(_action_float(action, "volume_L", 0.015), 0.0, 0.060))
        phase_name = str(action.get("phase", "aqueous"))
        if phase_name not in {"aqueous", "organic"}:
            phase_name = "organic"
        phase_ledger = self._phase_ledger(state)
        phase = phase_ledger.setdefault(
            phase_name,
            {"volume_L": 0.0, "P_mol": 0.0, "impurity_mol": 0.0, "solvent_loss": 0.0},
        )
        phase["volume_L"] += volume
        metadata = self._write_phase_metadata(
            state,
            phase_ledger,
            updates={"phase_system": True, "phase_settled": False, "selected_phase": None},
        )
        ledger = state.ledger.with_updates(cost=state.ledger.cost + 0.015 + 0.35 * volume)
        return state.replace(volume_L=state.volume_L + volume, ledger=ledger, metadata=metadata)

    def _add_extractant(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        volume = float(np.clip(_action_float(action, "volume_L", 0.018), 0.0, 0.060))
        extractant = str(action.get("extractant", "organic"))
        phase_ledger = self._phase_ledger(state)
        organic = phase_ledger.setdefault(
            "organic",
            {"volume_L": 0.0, "P_mol": 0.0, "impurity_mol": 0.0, "solvent_loss": 0.0},
        )
        organic["volume_L"] += volume
        metadata = self._write_phase_metadata(
            state,
            phase_ledger,
            updates={
                "phase_system": True,
                "phase_settled": False,
                "extractant": extractant,
                "selected_phase": None,
            },
        )
        solvent = int(state.metadata.get("solvent", 0))
        risk = min(1.0, state.ledger.risk + 0.04 + 0.05 * float(self.world.solvent_risks[solvent]))
        ledger = state.ledger.with_updates(
            cost=state.ledger.cost + 0.025 + 0.80 * volume,
            risk=risk,
        )
        return state.replace(volume_L=state.volume_L + volume, ledger=ledger, metadata=metadata)

    def _mix_phases(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        duration = float(np.clip(_action_float(action, "duration_s", 180.0), 0.0, 1800.0))
        stirring = float(np.clip(_action_float(action, "stirring_speed_rpm", 700.0), 100.0, 1200.0))
        phase_ledger = self._phase_ledger(state)
        phase_ledger.setdefault(
            "aqueous",
            {
                "volume_L": max(
                    state.volume_L - phase_ledger.get("organic", {}).get("volume_L", 0.0), 0.0
                ),
                "P_mol": 0.0,
                "impurity_mol": 0.0,
                "solvent_loss": 0.0,
            },
        )
        organic = phase_ledger.setdefault(
            "organic",
            {"volume_L": 0.015, "P_mol": 0.0, "impurity_mol": 0.0, "solvent_loss": 0.0},
        )
        aqueous = phase_ledger["aqueous"]
        p_total = state.species_amounts.get("P", 0.0)
        impurity_total = (
            state.species_amounts.get("B", 0.0)
            + state.species_amounts.get("D", 0.0)
            + state.species_amounts.get("E", 0.0)
        )
        solvent = int(state.metadata.get("solvent", 0))
        partition_base = np.array([0.65, 1.25, 2.20, 1.55])
        temperature_factor = 1.0 + 0.0025 * (state.temperature_K - 298.15)
        mix_factor = 0.75 + 0.25 * (1.0 - np.exp(-duration / 240.0)) * (
            0.70 + 0.30 * stirring / 1200.0
        )
        partition = max(0.05, float(partition_base[solvent] * temperature_factor * mix_factor))
        v_org = max(organic["volume_L"], 1.0e-9)
        v_aq = max(aqueous["volume_L"], 1.0e-9)
        product_organic_fraction = float(
            np.clip(partition * v_org / (v_aq + partition * v_org), 0.0, 1.0)
        )
        impurity_organic_fraction = float(
            np.clip(0.35 * product_organic_fraction + 0.10 * solvent, 0.0, 0.85)
        )
        organic["P_mol"] = p_total * product_organic_fraction
        aqueous["P_mol"] = p_total - organic["P_mol"]
        organic["impurity_mol"] = impurity_total * impurity_organic_fraction
        aqueous["impurity_mol"] = impurity_total - organic["impurity_mol"]
        phase_ledger["reactor_liquid"] = {
            "volume_L": state.volume_L,
            "P_mol": p_total,
            "impurity_mol": impurity_total,
            "solvent_loss": 0.0,
        }
        metadata = self._write_phase_metadata(
            state,
            phase_ledger,
            updates={
                "phase_system": True,
                "phase_settled": False,
                "partition_coefficient": partition,
                "stirring_speed_rpm": stirring,
            },
        )
        ledger = state.ledger.with_updates(
            time_s=state.ledger.time_s + duration,
            cost=state.ledger.cost + 0.01 + duration / 3600.0 * 0.015,
        )
        return state.replace(ledger=ledger, metadata=metadata)

    def _settle_phases(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        duration = float(np.clip(_action_float(action, "duration_s", 300.0), 0.0, 3600.0))
        phase_ledger = self._phase_ledger(state)
        metadata = self._write_phase_metadata(
            state,
            phase_ledger,
            updates={"phase_system": True, "phase_settled": duration >= 60.0},
        )
        ledger = state.ledger.with_updates(
            time_s=state.ledger.time_s + duration,
            cost=state.ledger.cost + duration / 3600.0 * 0.006,
        )
        return state.replace(ledger=ledger, metadata=metadata)

    def _separate_phase(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        target = str(action.get("target_phase", "organic"))
        if target not in {"organic", "aqueous"}:
            target = "organic"
        phase_ledger = self._phase_ledger(state)
        selected = phase_ledger.get(
            target,
            {
                "volume_L": state.volume_L,
                "P_mol": state.species_amounts.get("P", 0.0),
                "impurity_mol": 0.0,
                "solvent_loss": 0.0,
            },
        )
        entrainment_loss = 0.025 if target == "organic" else 0.045
        retained_p = selected["P_mol"] * (1.0 - entrainment_loss)
        retained_impurity = selected["impurity_mol"] * (1.0 + 0.20 * entrainment_loss)
        phase_ledger[target] = {
            "volume_L": selected["volume_L"] * (1.0 - 0.015),
            "P_mol": retained_p,
            "impurity_mol": retained_impurity,
            "solvent_loss": selected.get("solvent_loss", 0.0) + entrainment_loss,
        }
        metadata = self._write_phase_metadata(
            state,
            phase_ledger,
            updates={"selected_phase": target, "phase_system": True, "phase_settled": True},
        )
        ledger = state.ledger.with_updates(cost=state.ledger.cost + 0.025)
        return state.replace(
            volume_L=phase_ledger[target]["volume_L"], ledger=ledger, metadata=metadata
        )

    def _wash_phase(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        volume = float(np.clip(_action_float(action, "wash_volume_L", 0.010), 0.0, 0.040))
        phase_ledger = self._phase_ledger(state)
        target = str(state.metadata.get("selected_phase") or "organic")
        phase = phase_ledger.setdefault(
            target,
            {
                "volume_L": state.volume_L,
                "P_mol": state.species_amounts.get("P", 0.0),
                "impurity_mol": 0.0,
                "solvent_loss": 0.0,
            },
        )
        impurity_removal = float(np.clip(0.18 + 8.0 * volume, 0.0, 0.65))
        phase["impurity_mol"] *= 1.0 - impurity_removal
        phase["P_mol"] *= 1.0 - 0.015
        phase["volume_L"] += volume * 0.35
        phase["solvent_loss"] += 0.012
        metadata = self._write_phase_metadata(
            state, phase_ledger, updates={"selected_phase": target}
        )
        ledger = state.ledger.with_updates(cost=state.ledger.cost + 0.02 + 0.25 * volume)
        return state.replace(volume_L=phase["volume_L"], ledger=ledger, metadata=metadata)

    def _dry_phase(self, state: WorldState) -> WorldState:
        phase_ledger = self._phase_ledger(state)
        target = str(state.metadata.get("selected_phase") or "organic")
        phase = phase_ledger.setdefault(
            target,
            {
                "volume_L": state.volume_L,
                "P_mol": state.species_amounts.get("P", 0.0),
                "impurity_mol": 0.0,
                "solvent_loss": 0.0,
            },
        )
        phase["solvent_loss"] = max(0.0, phase.get("solvent_loss", 0.0) * 0.35)
        phase["volume_L"] *= 0.92
        metadata = self._write_phase_metadata(
            state, phase_ledger, updates={"selected_phase": target}
        )
        ledger = state.ledger.with_updates(
            time_s=state.ledger.time_s + 300.0, cost=state.ledger.cost + 0.018
        )
        return state.replace(volume_L=phase["volume_L"], ledger=ledger, metadata=metadata)

    def _concentrate_phase(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        duration = float(np.clip(_action_float(action, "duration_s", 300.0), 0.0, 3600.0))
        phase_ledger = self._phase_ledger(state)
        target = str(state.metadata.get("selected_phase") or "organic")
        phase = phase_ledger.setdefault(
            target,
            {
                "volume_L": state.volume_L,
                "P_mol": state.species_amounts.get("P", 0.0),
                "impurity_mol": 0.0,
                "solvent_loss": 0.0,
            },
        )
        concentration_factor = float(np.clip(1.0 - duration / 7200.0, 0.45, 1.0))
        phase["volume_L"] *= concentration_factor
        phase["P_mol"] *= 1.0 - 0.01 * (1.0 - concentration_factor)
        phase["solvent_loss"] += 0.025 * (1.0 - concentration_factor)
        metadata = self._write_phase_metadata(
            state, phase_ledger, updates={"selected_phase": target}
        )
        ledger = state.ledger.with_updates(
            time_s=state.ledger.time_s + duration,
            cost=state.ledger.cost + duration / 3600.0 * 0.035,
            risk=min(1.0, state.ledger.risk + 0.015 * (1.0 - concentration_factor)),
        )
        return state.replace(volume_L=phase["volume_L"], ledger=ledger, metadata=metadata)

    def _transfer_phase(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        fraction = float(np.clip(_action_float(action, "transfer_fraction", 0.98), 0.0, 1.0))
        phase_ledger = self._phase_ledger(state)
        target = str(state.metadata.get("selected_phase") or "organic")
        phase = phase_ledger.setdefault(
            target,
            {
                "volume_L": state.volume_L,
                "P_mol": state.species_amounts.get("P", 0.0),
                "impurity_mol": 0.0,
                "solvent_loss": 0.0,
            },
        )
        phase["P_mol"] *= fraction
        phase["impurity_mol"] *= fraction
        phase["volume_L"] *= fraction
        phase["solvent_loss"] += 1.0 - fraction
        metadata = self._write_phase_metadata(
            state, phase_ledger, updates={"selected_phase": target}
        )
        ledger = state.ledger.with_updates(cost=state.ledger.cost + 0.01)
        return state.replace(volume_L=phase["volume_L"], ledger=ledger, metadata=metadata)

    def _seed_crystals(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        seed_mass = float(np.clip(_action_float(action, "seed_mass_g", 0.005), 0.0, 0.050))
        metadata = state.metadata.copy()
        metadata["crystal_seeded"] = seed_mass > 0.0
        metadata["crystal_seed_mass_g"] = seed_mass
        ledger = state.ledger.with_updates(cost=state.ledger.cost + 0.012 + 0.20 * seed_mass)
        return state.replace(ledger=ledger, metadata=metadata)

    def _cool_crystallize(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        duration = float(np.clip(_action_float(action, "duration_s", 1200.0), 0.0, 14_400.0))
        target_temperature = float(
            np.clip(_action_float(action, "target_temperature_K", 278.15), 250.0, 330.0)
        )
        cooling_depth = float(np.clip((state.temperature_K - target_temperature) / 55.0, 0.0, 1.0))
        time_factor = float(np.clip(1.0 - np.exp(-duration / 1800.0), 0.0, 1.0))
        seed_factor = 1.08 if bool(state.metadata.get("crystal_seeded", False)) else 0.92
        p_mol = state.species_amounts.get("P", 0.0)
        impurity_mol = (
            state.species_amounts.get("B", 0.0)
            + state.species_amounts.get("D", 0.0)
            + state.species_amounts.get("E", 0.0)
        )
        crystallized = float(np.clip(p_mol * cooling_depth * time_factor * seed_factor, 0.0, p_mol))
        occluded_impurity = float(
            np.clip(impurity_mol * (0.035 + 0.080 * cooling_depth) * time_factor, 0.0, impurity_mol)
        )
        crystal_purity = crystallized / max(crystallized + occluded_impurity, 1.0e-12)
        initial_p = max(
            float(state.metadata.get("pre_separation_product_mol", p_mol)),
            p_mol,
            1.0e-12,
        )
        metadata = state.metadata.copy()
        metadata.update(
            {
                "crystallization_active": True,
                "crystal_product_mol": crystallized,
                "crystal_impurity_mol": occluded_impurity,
                "crystal_yield": float(np.clip(crystallized / initial_p, 0.0, 1.0)),
                "crystal_purity": float(np.clip(crystal_purity, 0.0, 1.0)),
                "crystal_size": float(np.clip(0.25 + 0.65 * time_factor * seed_factor, 0.0, 1.0)),
            }
        )
        ledger = state.ledger.with_updates(
            time_s=state.ledger.time_s + duration,
            cost=state.ledger.cost + 0.018 + duration / 3600.0 * 0.018,
            risk=max(0.0, state.ledger.risk - 0.02 * cooling_depth),
        )
        return state.replace(temperature_K=target_temperature, ledger=ledger, metadata=metadata)

    def _filter_crystals(self, state: WorldState) -> WorldState:
        metadata = state.metadata.copy()
        product = float(metadata.get("crystal_product_mol", 0.0)) * 0.96
        impurity = float(metadata.get("crystal_impurity_mol", 0.0)) * 0.92
        purity = product / max(product + impurity, 1.0e-12)
        initial_p = max(
            float(
                state.metadata.get(
                    "pre_separation_product_mol",
                    state.species_amounts.get("P", 0.0),
                )
            ),
            state.species_amounts.get("P", 0.0),
            1.0e-12,
        )
        metadata.update(
            {
                "selected_phase": "solid",
                "crystals_filtered": True,
                "crystal_product_mol": product,
                "crystal_impurity_mol": impurity,
                "crystal_yield": float(np.clip(product / initial_p, 0.0, 1.0)),
                "crystal_purity": float(np.clip(purity, 0.0, 1.0)),
                "recovery": float(np.clip(product / initial_p, 0.0, 1.0)),
                "purity": float(np.clip(purity, 0.0, 1.0)),
                "solvent_loss": min(1.0, float(metadata.get("solvent_loss", 0.0)) + 0.04),
            }
        )
        ledger = state.ledger.with_updates(
            time_s=state.ledger.time_s + 480.0,
            cost=state.ledger.cost + 0.026,
        )
        return state.replace(ledger=ledger, metadata=metadata)

    def _evaporate(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        duration = float(np.clip(_action_float(action, "duration_s", 600.0), 0.0, 14_400.0))
        target_temperature = float(
            np.clip(_action_float(action, "target_temperature_K", 328.15), 298.15, 390.0)
        )
        removal = float(
            np.clip(
                0.08 + duration / 7200.0 + (target_temperature - 298.15) / 420.0,
                0.0,
                0.70,
            )
        )
        metadata = state.metadata.copy()
        metadata["solvent_loss"] = min(1.0, float(metadata.get("solvent_loss", 0.0)) + removal)
        ledger = state.ledger.with_updates(
            time_s=state.ledger.time_s + duration,
            cost=state.ledger.cost + duration / 3600.0 * 0.040,
            risk=min(1.0, state.ledger.risk + 0.04 * removal),
            energy_jacket_J=state.ledger.energy_jacket_J + 45.0 * duration,
        )
        return state.replace(
            volume_L=state.volume_L * (1.0 - 0.55 * removal),
            temperature_K=target_temperature,
            ledger=ledger,
            metadata=metadata,
        )

    def _distill(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        duration = float(np.clip(_action_float(action, "duration_s", 1200.0), 0.0, 14_400.0))
        target_temperature = float(
            np.clip(_action_float(action, "target_temperature_K", 345.15), 298.15, 430.0)
        )
        reflux = float(np.clip(_action_float(action, "reflux_ratio", 1.5), 0.0, 10.0))
        p_mol = state.species_amounts.get("P", 0.0)
        impurity_mol = (
            state.species_amounts.get("B", 0.0)
            + state.species_amounts.get("D", 0.0)
            + state.species_amounts.get("E", 0.0)
        )
        time_factor = float(np.clip(1.0 - np.exp(-duration / 1500.0), 0.0, 1.0))
        reflux_quality = reflux / (1.0 + reflux)
        distillate_product = p_mol * np.clip(0.35 + 0.42 * time_factor, 0.0, 0.90)
        distillate_impurity = impurity_mol * np.clip(0.26 - 0.18 * reflux_quality, 0.04, 0.30)
        distillate_purity = distillate_product / max(
            distillate_product + distillate_impurity,
            1.0e-12,
        )
        initial_p = max(
            float(state.metadata.get("pre_separation_product_mol", p_mol)),
            p_mol,
            1.0e-12,
        )
        metadata = state.metadata.copy()
        metadata.update(
            {
                "distillation_active": True,
                "distillate_product_mol": float(distillate_product),
                "distillate_impurity_mol": float(distillate_impurity),
                "distillate_purity": float(np.clip(distillate_purity, 0.0, 1.0)),
                "distillate_recovery": float(np.clip(distillate_product / initial_p, 0.0, 1.0)),
            }
        )
        risk = min(1.0, state.ledger.risk + 0.035 + 0.06 * ((target_temperature - 298.15) / 132.0))
        ledger = state.ledger.with_updates(
            time_s=state.ledger.time_s + duration,
            cost=state.ledger.cost + 0.045 + duration / 3600.0 * (0.065 + 0.012 * reflux),
            risk=risk,
            energy_jacket_J=state.ledger.energy_jacket_J + (70.0 + 8.0 * reflux) * duration,
        )
        return state.replace(
            volume_L=max(state.volume_L * 0.62, 0.001),
            temperature_K=target_temperature,
            ledger=ledger,
            metadata=metadata,
        )

    def _collect_fraction(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        fraction = float(np.clip(_action_float(action, "transfer_fraction", 0.90), 0.0, 1.0))
        product = float(state.metadata.get("distillate_product_mol", 0.0)) * fraction
        impurity = float(state.metadata.get("distillate_impurity_mol", 0.0)) * fraction
        purity = product / max(product + impurity, 1.0e-12)
        initial_p = max(
            float(
                state.metadata.get(
                    "pre_separation_product_mol",
                    state.species_amounts.get("P", 0.0),
                )
            ),
            state.species_amounts.get("P", 0.0),
            1.0e-12,
        )
        metadata = state.metadata.copy()
        metadata.update(
            {
                "selected_phase": "distillate",
                "fraction_collected": True,
                "distillate_product_mol": product,
                "distillate_impurity_mol": impurity,
                "distillate_purity": float(np.clip(purity, 0.0, 1.0)),
                "distillate_recovery": float(np.clip(product / initial_p, 0.0, 1.0)),
                "purity": float(np.clip(purity, 0.0, 1.0)),
                "recovery": float(np.clip(product / initial_p, 0.0, 1.0)),
            }
        )
        ledger = state.ledger.with_updates(cost=state.ledger.cost + 0.018)
        return state.replace(volume_L=state.volume_L * fraction, ledger=ledger, metadata=metadata)

    def _set_flow_rate(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        flow_rate = float(np.clip(_action_float(action, "flow_rate_mL_min", 1.0), 0.01, 20.0))
        residence = float(np.clip(_action_float(action, "residence_time_s", 600.0), 1.0, 7200.0))
        metadata = state.metadata.copy()
        metadata["flow_rate_mL_min"] = flow_rate
        metadata["residence_time_s"] = residence
        ledger = state.ledger.with_updates(cost=state.ledger.cost + 0.012)
        return state.replace(ledger=ledger, metadata=metadata)

    def _run_flow(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        residence = float(
            state.metadata.get(
                "residence_time_s",
                _action_float(action, "duration_s", 600.0),
            )
        )
        duration = float(
            np.clip(_action_float(action, "duration_s", residence), residence, 14_400.0)
        )
        target_temperature = float(
            np.clip(_action_float(action, "target_temperature_K", 348.15), 298.15, 430.0)
        )
        effective_action = {
            "duration_s": residence,
            "target_temperature_K": target_temperature,
            "stirring_speed_rpm": 900.0,
        }
        reacted_state = self._integrate(state, effective_action, heat=True)
        initial_a = max(float(state.metadata.get("initial_A_mol", 0.0)), 1.0e-12)
        conversion = float(
            np.clip((initial_a - reacted_state.species_amounts.get("A", 0.0)) / initial_a, 0.0, 1.0)
        )
        metadata = reacted_state.metadata.copy()
        metadata["flow_conversion"] = conversion
        metadata["flow_campaign_time_s"] = duration
        ledger = reacted_state.ledger.with_updates(
            time_s=state.ledger.time_s + duration,
            cost=reacted_state.ledger.cost + duration / 3600.0 * 0.030,
            risk=min(1.0, reacted_state.ledger.risk + 0.015 * (target_temperature > 390.0)),
        )
        return reacted_state.replace(ledger=ledger, metadata=metadata)

    def _set_potential(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        potential = float(np.clip(_action_float(action, "potential_V", 1.20), -3.0, 3.0))
        current = float(np.clip(_action_float(action, "current_mA", 50.0), 0.0, 500.0))
        metadata = state.metadata.copy()
        metadata["potential_V"] = potential
        metadata["current_mA"] = current
        risk = min(1.0, state.ledger.risk + 0.02 * max(abs(potential) - 1.5, 0.0))
        ledger = state.ledger.with_updates(cost=state.ledger.cost + 0.010, risk=risk)
        return state.replace(ledger=ledger, metadata=metadata)

    def _electrolyze(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        duration = float(np.clip(_action_float(action, "duration_s", 900.0), 0.0, 14_400.0))
        potential = float(state.metadata.get("potential_V", 1.20))
        current = float(state.metadata.get("current_mA", 50.0))
        species = state.species_amounts.copy()
        a_mol = species.get("A", 0.0)
        charge_factor = float(np.clip(current * duration / 1_800_000.0, 0.0, 0.85))
        selectivity = float(
            np.clip(
                0.78 - 0.18 * abs(potential - 1.20) + 0.08 * (potential > 0.8),
                0.20,
                0.92,
            )
        )
        converted = min(a_mol, a_mol * charge_factor)
        species["A"] = a_mol - converted
        species["P"] += converted * selectivity
        species["B"] += converted * (1.0 - selectivity)
        energy_j = abs(potential) * current / 1000.0 * duration
        metadata = state.metadata.copy()
        metadata["electrochemical_selectivity"] = selectivity
        metadata["energy_efficiency"] = float(
            np.clip(selectivity * (1.0 - energy_j / 75_000.0), 0.0, 1.0)
        )
        ledger = state.ledger.with_updates(
            time_s=state.ledger.time_s + duration,
            cost=state.ledger.cost + 0.018 + energy_j / 250_000.0,
            risk=min(1.0, state.ledger.risk + 0.02 + 0.03 * abs(potential)),
            energy_jacket_J=state.ledger.energy_jacket_J + energy_j,
        )
        return state.replace(species_amounts=species, ledger=ledger, metadata=metadata)

    def _apply_measurement_cost(self, state: WorldState, action: dict[str, Any]) -> WorldState:
        instrument_id = instrument_name(action.get("instrument", "hplc"))
        instrument = self.constitution.instruments[instrument_id]
        volume = min(instrument.sample_volume_L, max(state.volume_L, 0.0))
        fraction = 0.0 if state.volume_L <= 0 else volume / state.volume_L
        species = {key: value * (1.0 - fraction) for key, value in state.species_amounts.items()}
        ledger = state.ledger.with_updates(
            cost=state.ledger.cost + instrument.cost,
            sample_consumed_L=state.ledger.sample_consumed_L + volume,
        )
        metadata = state.metadata.copy()
        if instrument_id == "final_assay":
            metadata["final_assay_done"] = True
            metadata["final_assay_time_s"] = state.ledger.time_s
        return state.replace(
            species_amounts=species,
            volume_L=state.volume_L - volume,
            ledger=ledger,
            metadata=metadata,
        )

    def _penalize_invalid(self, state: WorldState) -> WorldState:
        ledger = state.ledger.with_updates(
            cost=state.ledger.cost + 0.01,
            risk=min(1.0, state.ledger.risk + 0.08),
        )
        return state.replace(ledger=ledger)

    def _integrate(self, state: WorldState, action: dict[str, Any], *, heat: bool) -> WorldState:
        duration = float(np.clip(_action_float(action, "duration_s", 600.0), 0.0, 14_400.0))
        if duration <= 0.0 or state.volume_L <= 0.0:
            return state

        target_temperature = _action_float(action, "target_temperature_K", state.temperature_K)
        target_temperature = float(np.clip(target_temperature, 250.0, 520.0))
        stirring_speed = _action_float(
            action,
            "stirring_speed_rpm",
            float(state.metadata.get("stirring_speed_rpm", 600.0)),
        )
        stirring_speed = float(np.clip(stirring_speed, 100.0, 1200.0))
        y0 = np.array(
            [state.species_amounts[key] for key in SPECIES] + [state.temperature_K, 0.0, 0.0, 0.0]
        )
        result = solve_ivp(
            lambda _t, y: self._ode_rhs(y, state, target_temperature, heat, stirring_speed),
            (0.0, duration),
            y0,
            method="RK45",
            rtol=1.0e-6,
            atol=1.0e-10,
        )
        y = np.maximum(result.y[:, -1], 0.0)
        species = {key: float(y[index]) for index, key in enumerate(SPECIES)}
        temperature = float(np.clip(y[7], 250.0, 520.0))
        ledger = state.ledger.with_updates(
            time_s=state.ledger.time_s + duration,
            cost=state.ledger.cost + duration / 3600.0 * (0.03 if heat else 0.01),
            energy_jacket_J=state.ledger.energy_jacket_J + float(y[8]),
            heat_reaction_J=state.ledger.heat_reaction_J + float(y[9]),
            heat_loss_J=state.ledger.heat_loss_J + float(y[10]),
        )
        metadata = state.metadata.copy()
        metadata["stirring_speed_rpm"] = stirring_speed
        return state.replace(
            species_amounts=species,
            temperature_K=temperature,
            ledger=ledger,
            metadata=metadata,
        )

    def _ode_rhs(
        self,
        y: np.ndarray,
        state: WorldState,
        target_temperature: float,
        heat: bool,
        stirring_speed_rpm: float,
    ) -> np.ndarray:
        amounts = np.maximum(y[:7], 0.0)
        temperature = float(np.clip(y[7], 250.0, 520.0))
        volume = max(state.volume_L, 1.0e-6)
        catalyst = int(state.metadata.get("catalyst", 0))
        solvent = int(state.metadata.get("solvent", 0))
        concentrations = amounts / volume
        cat_total = max(amounts[5] + amounts[6], 1.0e-12)
        eta_cat = amounts[5] / cat_total

        k = self.world.pre_exponential * np.exp(
            -self.world.activation_energy / (R_GAS * temperature)
        )
        k *= self.world.catalyst_effects[catalyst] * self.world.solvent_effects[solvent]
        stir_factor = 0.70 + 0.30 * (1.0 - np.exp(-stirring_speed_rpm / 420.0))
        low_mixing_side_penalty = 1.0 + 0.15 * (
            1.0 / (1.0 + np.exp((stirring_speed_rpm - 360.0) / 90.0))
        )
        rates = np.array(
            [
                k[0] * concentrations[0] * eta_cat * volume * stir_factor,
                k[1] * concentrations[0] * volume * low_mixing_side_penalty,
                k[2] * concentrations[1] * volume,
                k[3] * concentrations[0] * concentrations[1] * volume * low_mixing_side_penalty,
                k[4] * amounts[5],
            ]
        )
        derivatives = np.zeros(11)
        derivatives[0] = -rates[0] - rates[1] - rates[3]
        derivatives[1] = rates[0] - rates[2] - rates[3]
        derivatives[2] = rates[1]
        derivatives[3] = rates[2]
        derivatives[4] = rates[3]
        derivatives[5] = -rates[4]
        derivatives[6] = rates[4]

        q_jacket = 0.0
        if heat:
            q_jacket = float(np.clip((target_temperature - temperature) * 4.0, -70.0, 90.0))
        heat_loss = self.world.ua_W_per_K * (temperature - self.world.environment_temperature_K)
        heat_reaction = float(np.dot(self.world.delta_h_J_per_mol, rates))
        heat_capacity = max(self.world.rho_cp_J_per_L_K * volume, 1.0e-6)
        derivatives[7] = (q_jacket - heat_loss - heat_reaction) / heat_capacity
        derivatives[8] = q_jacket
        derivatives[9] = heat_reaction
        derivatives[10] = heat_loss
        return derivatives

    def _with_risk_and_pressure(self, state: WorldState) -> WorldState:
        solvent = int(state.metadata.get("solvent", 0))
        total_amount = sum(
            value for key, value in state.species_amounts.items() if not key.startswith("Cat")
        )
        concentration = 0.0 if state.volume_L <= 0 else total_amount / state.volume_L
        pressure = 101_325.0 * (state.temperature_K / 298.15) * (1.0 + 0.025 * concentration)
        exotherm_risk = min(1.0, abs(state.ledger.heat_reaction_J) / 2500.0)
        temperature_risk = 1.0 / (1.0 + np.exp(-(state.temperature_K - 405.0) / 13.0))
        concentration_risk = 1.0 / (1.0 + np.exp(-(concentration - 0.8) / 0.22))
        risk = float(
            np.clip(
                0.30 * temperature_risk
                + 0.20 * concentration_risk
                + 0.20 * exotherm_risk
                + 0.18 * self.world.solvent_risks[solvent]
                + 0.12 * (pressure / 550_000.0),
                0.0,
                1.0,
            )
        )
        return state.replace(pressure_Pa=pressure, ledger=state.ledger.with_updates(risk=risk))

    def _record(
        self,
        operation: str,
        before: WorldState,
        after: WorldState,
        preconditions: dict[str, bool],
        action: dict[str, Any] | None = None,
    ) -> OperationRecord:
        action = action or {}
        report = self.constitution.check_state(after)
        material_check = self.constitution.check_material_conservation(before, after)
        if operation in {
            "add_reagent",
            "add_catalyst",
            "add_solvent",
            "sample",
            "measure",
            "add_phase",
            "add_extractant",
            "mix",
            "settle",
            "separate_phase",
            "wash",
            "dry",
            "concentrate",
            "transfer",
        }:
            material_check = material_check.__class__(
                "material_conservation",
                True,
                "material delta allowed or phase-ledger conserved for operation",
                value=0.0,
                tolerance=self.constitution.tolerance,
            )
        checks = [*report.checks, material_check]
        measurement_cost = 0.0
        sample_consumed = 0.0
        instrument = None
        preconditions_passed = all(preconditions.values())
        if operation == "measure":
            instrument = instrument_name(action.get("instrument", "hplc"))
            if preconditions_passed:
                measurement_cost = self.constitution.instruments[instrument].cost
                sample_consumed = self.constitution.instruments[instrument].sample_volume_L
        return OperationRecord(
            operation_type=operation,
            preconditions=preconditions,
            state_delta_summary={
                "delta_time_s": after.ledger.time_s - before.ledger.time_s,
                "delta_cost": after.ledger.cost - before.ledger.cost,
                "delta_risk": after.ledger.risk - before.ledger.risk,
                "delta_temperature_K": after.temperature_K - before.temperature_K,
                "delta_volume_L": after.volume_L - before.volume_L,
            },
            constitution_checks=[check.to_dict() for check in checks],
            instrument=instrument,
            measurement_cost=measurement_cost,
            sample_consumed_L=sample_consumed,
        )


def _downstream_truth_values(
    state: WorldState,
    phase_ledger: dict[str, dict[str, float]] | None = None,
) -> dict[str, float]:
    phase_ledger = phase_ledger or dict(state.metadata.get("phase_ledger", {}))
    initial_p = max(
        float(
            state.metadata.get(
                "pre_separation_product_mol",
                state.metadata.get("max_product_mol", state.species_amounts.get("P", 0.0)),
            )
        ),
        state.species_amounts.get("P", 0.0),
        1.0e-12,
    )
    organic = phase_ledger.get("organic", {})
    aqueous = phase_ledger.get("aqueous", {})
    selected_phase = str(state.metadata.get("selected_phase") or "organic")
    selected = phase_ledger.get(selected_phase, organic or aqueous or {})
    product_in_organic = float(organic.get("P_mol", 0.0))
    product_in_aqueous = float(aqueous.get("P_mol", 0.0))
    selected_product = float(selected.get("P_mol", state.species_amounts.get("P", 0.0)))
    selected_impurity = float(
        selected.get(
            "impurity_mol",
            state.species_amounts.get("B", 0.0)
            + state.species_amounts.get("D", 0.0)
            + state.species_amounts.get("E", 0.0),
        )
    )
    organic_volume = float(organic.get("volume_L", 0.0))
    aqueous_volume = float(aqueous.get("volume_L", max(state.volume_L - organic_volume, 0.0)))
    total_phase_product = product_in_organic + product_in_aqueous
    purity = selected_product / max(selected_product + selected_impurity, 1.0e-12)
    recovery = selected_product / initial_p
    phase_ratio = organic_volume / max(organic_volume + aqueous_volume, 1.0e-12)
    solvent_loss = float(selected.get("solvent_loss", 0.0))
    mass_balance_error = abs(total_phase_product - state.species_amounts.get("P", 0.0)) / initial_p
    return {
        "purity": float(np.clip(purity, 0.0, 1.0)),
        "recovery": float(np.clip(recovery, 0.0, 1.0)),
        "phase_ratio": float(np.clip(phase_ratio, 0.0, 1.0)),
        "product_in_organic": float(np.clip(product_in_organic / initial_p, 0.0, 1.0)),
        "product_in_aqueous": float(np.clip(product_in_aqueous / initial_p, 0.0, 1.0)),
        "impurity_signal": float(np.clip(selected_impurity / initial_p, 0.0, 1.0)),
        "solvent_loss": float(np.clip(solvent_loss, 0.0, 1.0)),
        "process_mass_balance_error": float(np.clip(mass_balance_error, 0.0, 1.0)),
        "crystal_yield": float(np.clip(float(state.metadata.get("crystal_yield", 0.0)), 0.0, 1.0)),
        "crystal_purity": float(
            np.clip(float(state.metadata.get("crystal_purity", 0.0)), 0.0, 1.0)
        ),
        "crystal_size": float(np.clip(float(state.metadata.get("crystal_size", 0.0)), 0.0, 1.0)),
        "distillate_purity": float(
            np.clip(float(state.metadata.get("distillate_purity", 0.0)), 0.0, 1.0)
        ),
        "distillate_recovery": float(
            np.clip(float(state.metadata.get("distillate_recovery", 0.0)), 0.0, 1.0)
        ),
        "flow_conversion": float(
            np.clip(float(state.metadata.get("flow_conversion", 0.0)), 0.0, 1.0)
        ),
        "electrochemical_selectivity": float(
            np.clip(float(state.metadata.get("electrochemical_selectivity", 0.0)), 0.0, 1.0)
        ),
        "energy_efficiency": float(
            np.clip(float(state.metadata.get("energy_efficiency", 0.0)), 0.0, 1.0)
        ),
    }


class ChemWorldObservationKernel:
    def __init__(self, constitution: PhysicalConstitution, objective: str) -> None:
        self.constitution = constitution
        self.objective = objective

    def observe(
        self,
        state: WorldState,
        action: dict[str, Any],
        rng: np.random.Generator,
    ) -> Observation:
        operation = operation_name(action["operation"])
        if operation != "measure":
            last = dict(state.metadata.get("last_observation", {}))
            last_mask = dict(state.metadata.get("last_observed_mask", {}))
            values = self._base_public_values(state)
            observed_mask = self._base_observed_mask()
            values.update(last)
            observed_mask.update({str(key): bool(value) for key, value in last_mask.items()})
            values["cost"] = min(1.0, state.ledger.cost)
            values["safety_risk"] = state.ledger.risk
            observed_mask["cost"] = True
            observed_mask["safety_risk"] = True
            values["score"] = self._score(values)
            observed_mask["score"] = True
            return Observation(
                values=values,
                units=self._observation_units(),
                observed_mask=observed_mask,
                processed_estimate=self._processed_estimate(values, observed_mask),
            )

        instrument_id = instrument_name(action.get("instrument", "hplc"))
        instrument = self.constitution.instruments[instrument_id]
        truth_values = self._truth_values(state)
        noisy = self._base_public_values(state)
        observed_mask = self._base_observed_mask()
        for key in instrument.observable_keys:
            std = instrument.noise_std.get(key, 0.0)
            noisy[key] = float(np.clip(truth_values[key] + rng.normal(0.0, std), 0.0, 1.0))
            observed_mask[key] = True

        if observed_mask["byproduct_signal"] and observed_mask["degradation_warning"]:
            byproduct_signal = self._observed_value(noisy, "byproduct_signal")
            degradation_warning = self._observed_value(noisy, "degradation_warning")
            noisy["virtual_spectrum_summary"] = float(
                np.clip(
                    0.55 * byproduct_signal + 0.45 * degradation_warning,
                    0.0,
                    1.0,
                )
            )
            observed_mask["virtual_spectrum_summary"] = True
        noisy["cost"] = min(1.0, state.ledger.cost)
        noisy["safety_risk"] = state.ledger.risk
        observed_mask["cost"] = True
        observed_mask["safety_risk"] = True
        noisy["score"] = self._score(noisy)
        observed_mask["score"] = True
        return Observation(
            values=noisy,
            units=self._observation_units(),
            observed_mask=observed_mask,
            raw_signal=self._raw_signal(instrument_id, noisy),
            processed_estimate=self._processed_estimate(noisy, observed_mask),
            uncertainty={
                f"{key}_std": float(std)
                for key, std in instrument.noise_std.items()
                if observed_mask.get(key, False)
            },
            instrument_id=instrument_id,
            cost=instrument.cost,
            sample_consumed_L=instrument.sample_volume_L,
        )

    def failed_observation(self) -> Observation:
        """Return a non-informative observation for failed action preconditions."""

        units = self._observation_units()
        return Observation(
            values=dict.fromkeys(units, None),
            units=units,
            observed_mask=dict.fromkeys(units, False),
            raw_signal={},
            processed_estimate={},
            uncertainty={},
            instrument_id=None,
            cost=0.0,
            sample_consumed_L=0.0,
        )

    @staticmethod
    def _processed_estimate(
        values: dict[str, float | None],
        observed_mask: dict[str, bool],
    ) -> dict[str, float | None]:
        estimate_keys = (
            "yield",
            "selectivity",
            "conversion",
            "byproduct_signal",
            "degradation_warning",
            *DOWNSTREAM_OBSERVATION_KEYS,
        )
        return {key: values.get(key) for key in estimate_keys if observed_mask.get(key, False)}

    @staticmethod
    def _raw_signal(instrument_id: str, values: dict[str, float | None]) -> dict[str, Any]:
        def observed(key: str) -> float:
            value = values.get(key)
            return 0.0 if value is None else float(value)

        if instrument_id == "uvvis":
            yield_value = observed("yield")
            conversion = observed("conversion")
            phase_ratio = observed("phase_ratio")
            flow_conversion = observed("flow_conversion")
            energy_efficiency = observed("energy_efficiency")
            return {
                "kind": "uvvis_spectrum",
                "wavelength_nm": [360, 420, 510, 620, 710],
                "absorbance": [
                    round(0.08 + 0.25 * conversion, 6),
                    round(0.05 + 0.35 * yield_value, 6),
                    round(0.04 + 0.15 * max(conversion - yield_value, 0.0), 6),
                    round(0.03 + 0.10 * phase_ratio, 6),
                    round(0.03 + 0.15 * max(flow_conversion, energy_efficiency), 6),
                ],
            }
        if instrument_id == "hplc":
            yield_value = observed("yield")
            byproduct = observed("byproduct_signal")
            purity = observed("purity")
            impurity = observed("impurity_signal")
            crystal_purity = observed("crystal_purity")
            distillate_purity = observed("distillate_purity")
            return {
                "kind": "hplc_chromatogram",
                "peaks": [
                    {
                        "retention_time_min": 1.18,
                        "peak_area": round(900.0 * max(1.0 - yield_value, 0.0), 6),
                        "assignment": "A_proxy",
                    },
                    {
                        "retention_time_min": 2.74,
                        "peak_area": round(
                            1200.0 * max(yield_value, purity, crystal_purity, distillate_purity),
                            6,
                        ),
                        "assignment": "P_proxy",
                    },
                    {
                        "retention_time_min": 3.52,
                        "peak_area": round(900.0 * max(byproduct, impurity), 6),
                        "assignment": "byproduct_proxy",
                    },
                ],
            }
        if instrument_id == "gc":
            byproduct = observed("byproduct_signal")
            degradation = observed("degradation_warning")
            distillate_purity = observed("distillate_purity")
            return {
                "kind": "gc_chromatogram",
                "peaks": [
                    {
                        "retention_time_min": 0.82,
                        "peak_area": round(800.0 * byproduct, 6),
                        "assignment": "volatile_byproduct_proxy",
                    },
                    {
                        "retention_time_min": 1.65,
                        "peak_area": round(800.0 * degradation, 6),
                        "assignment": "degradation_proxy",
                    },
                    {
                        "retention_time_min": 2.18,
                        "peak_area": round(1000.0 * distillate_purity, 6),
                        "assignment": "distillate_product_proxy",
                    },
                ],
            }
        if instrument_id == "final_assay":
            return {
                "kind": "final_assay_packet",
                "quality": "high",
                "channels": [
                    "hplc",
                    "gc",
                    "calibrated_mass_balance",
                    "phase_partition",
                    "purification_accounting",
                    "crystallization_accounting",
                    "distillation_accounting",
                    "flow_reactor_summary",
                    "electrochemical_summary",
                ],
            }
        return {}

    @staticmethod
    def _observation_units() -> dict[str, str]:
        return {
            "yield": "dimensionless",
            "selectivity": "dimensionless",
            "conversion": "dimensionless",
            "byproduct_signal": "dimensionless",
            "degradation_warning": "dimensionless",
            "virtual_spectrum_summary": "dimensionless",
            **dict.fromkeys(DOWNSTREAM_OBSERVATION_KEYS, "dimensionless"),
            "cost": "currency",
            "safety_risk": "risk",
            "score": "dimensionless",
        }

    @staticmethod
    def _base_public_values(state: WorldState) -> dict[str, float | None]:
        return {
            "yield": None,
            "selectivity": None,
            "conversion": None,
            "byproduct_signal": None,
            "degradation_warning": None,
            "virtual_spectrum_summary": None,
            **dict.fromkeys(DOWNSTREAM_OBSERVATION_KEYS, None),
            "cost": min(1.0, state.ledger.cost),
            "safety_risk": state.ledger.risk,
            "score": 0.0,
        }

    @staticmethod
    def _base_observed_mask() -> dict[str, bool]:
        return {
            "yield": False,
            "selectivity": False,
            "conversion": False,
            "byproduct_signal": False,
            "degradation_warning": False,
            "virtual_spectrum_summary": False,
            **dict.fromkeys(DOWNSTREAM_OBSERVATION_KEYS, False),
            "cost": True,
            "safety_risk": True,
            "score": True,
        }

    @staticmethod
    def _observed_value(values: dict[str, float | None], key: str) -> float:
        value = values.get(key)
        return 0.0 if value is None else float(value)

    def _score(self, values: dict[str, float | None]) -> float:
        return score_observation(
            objective=self.objective,
            product_yield=self._observed_value(values, "yield"),
            selectivity=self._observed_value(values, "selectivity"),
            conversion=self._observed_value(values, "conversion"),
            cost=self._observed_value(values, "cost"),
            safety_risk=self._observed_value(values, "safety_risk"),
        )

    @staticmethod
    def _truth_values(state: WorldState) -> dict[str, float]:
        initial_a = max(float(state.metadata.get("initial_A_mol", 0.0)), 1.0e-12)
        amounts = state.species_amounts
        consumed = max(initial_a - amounts.get("A", 0.0), 1.0e-12)
        yield_value = float(np.clip(amounts.get("P", 0.0) / initial_a, 0.0, 1.0))
        selectivity = float(np.clip(amounts.get("P", 0.0) / consumed, 0.0, 1.0))
        conversion = float(np.clip(consumed / initial_a, 0.0, 1.0))
        byproduct = float(
            np.clip((amounts.get("B", 0.0) + amounts.get("E", 0.0)) / initial_a, 0.0, 1.0)
        )
        degradation = float(np.clip(amounts.get("D", 0.0) / initial_a, 0.0, 1.0))
        return {
            "yield": yield_value,
            "selectivity": selectivity,
            "conversion": conversion,
            "byproduct_signal": byproduct,
            "degradation_warning": degradation,
            **_downstream_truth_values(state),
        }


def recipe_to_event_sequence(action: dict[str, Any]) -> list[dict[str, Any]]:
    """Expand terminal recipe parameters into executable reactor operations."""

    normalized = canonicalize_action(action)
    concentration = float(normalized["initial_concentration"])
    volume = 0.025
    amount = float(np.clip(concentration * volume, 0.0005, 0.040))
    target_temperature = float(normalized["temperature"]) + 273.15
    duration = float(normalized["time"]) * 3600.0
    return [
        {"operation": "add_solvent", "volume_L": volume, "solvent": int(normalized["solvent"])},
        {"operation": "add_reagent", "amount_mol": amount},
        {
            "operation": "add_catalyst",
            "catalyst_amount_mol": 0.00020,
            "catalyst": int(normalized["catalyst"]),
        },
        {
            "operation": "heat",
            "target_temperature_K": target_temperature,
            "duration_s": duration,
            "stirring_speed_rpm": float(normalized["stirring_speed"]),
        },
        {"operation": "terminate"},
        {"operation": "measure", "instrument": "final_assay"},
    ]



