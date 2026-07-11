"""World parameter generation and split handling."""

from __future__ import annotations

import os
from dataclasses import dataclass
from hashlib import sha256

import numpy as np

from chemworld.world.actions import CATALYSTS, SOLVENTS

WORLD_FAMILY_VERSION = "chemworld-physical-chemistry-v0.4"
SUPPORTED_SPLITS = ("public-dev", "public-test", "private-eval")

DEFAULT_DOMAIN_PARAMETERS: dict[str, float] = {
    "partition_coefficient_multiplier": 1.0,
    "partition_coefficient_exponent": 1.0,
    "partition_phase_volume_multiplier": 1.0,
    "crystallization_nucleation_multiplier": 1.0,
    "crystallization_solubility_multiplier": 1.0,
    "distillation_relative_volatility_multiplier": 1.0,
    "flow_rate_multiplier": 1.0,
    "flow_residence_multiplier": 1.0,
    "flow_boundary_ua_multiplier": 1.0,
    "electro_exchange_current_multiplier": 1.0,
    "electro_resistance_multiplier": 1.0,
    "electro_selectivity_decay_multiplier": 1.0,
    "electro_standard_potential_multiplier": 1.0,
    "electro_transfer_asymmetry_multiplier": 1.0,
    "observation_noise_multiplier": 1.0,
}


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
    domain_parameters: dict[str, float]

    def __post_init__(self) -> None:
        domain_parameters = {
            str(key): float(value) for key, value in self.domain_parameters.items()
        }
        missing = sorted(set(DEFAULT_DOMAIN_PARAMETERS) - set(domain_parameters))
        unknown = sorted(set(domain_parameters) - set(DEFAULT_DOMAIN_PARAMETERS))
        invalid = sorted(
            key
            for key, value in domain_parameters.items()
            if not np.isfinite(value) or value <= 0.0
        )
        if missing or unknown or invalid:
            raise ValueError(
                "invalid domain parameters: "
                f"missing={missing}, unknown={unknown}, nonpositive_or_nonfinite={invalid}"
            )
        object.__setattr__(self, "domain_parameters", domain_parameters)

    def domain_parameter(self, key: str) -> float:
        """Return a typed vNext provider parameter and fail on unknown keys."""

        try:
            return float(self.domain_parameters[key])
        except KeyError as exc:
            raise KeyError(f"Unknown domain parameter: {key}") from exc


def stable_parameter_seed(split: str, seed: int, private_salt: str = "") -> int:
    digest = sha256(f"{WORLD_FAMILY_VERSION}:{split}:{seed}:{private_salt}".encode()).digest()
    return int.from_bytes(digest[:8], "little") % (2**32)


def load_chemworld_parameters(
    split: str = "public-dev",
    seed: int = 0,
) -> ChemWorldParameters:
    """Generate deterministic hidden world parameters for a split and seed."""

    if split not in SUPPORTED_SPLITS:
        allowed = ", ".join(SUPPORTED_SPLITS)
        raise ValueError(f"Unsupported world_split={split!r}. Allowed: {allowed}")

    private_salt = ""
    provider = "public-registry"
    if split == "private-eval":
        private_salt = os.environ.get("CHEMWORLD_PRIVATE_EVAL_SALT", "")
        provider = "external-private-registry" if private_salt else "public-placeholder-private"

    rng = np.random.default_rng(stable_parameter_seed(split, seed, private_salt))
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
        domain_parameters=dict(DEFAULT_DOMAIN_PARAMETERS),
    )


__all__ = [
    "DEFAULT_DOMAIN_PARAMETERS",
    "SUPPORTED_SPLITS",
    "WORLD_FAMILY_VERSION",
    "ChemWorldParameters",
    "load_chemworld_parameters",
    "stable_parameter_seed",
]
