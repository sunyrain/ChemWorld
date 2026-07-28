"""Public material identities without overstating benchmark chemistry realism."""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from typing import Any

from chemworld.physchem.component_registry import curated_component_registry
from chemworld.world.actions import CATALYSTS, ELECTROLYTE_PROFILES, SOLVENTS
from chemworld.world.electrochemical_material_family import (
    NOMINAL_PRIOR_MATERIAL_FAMILY,
    electrochemical_material_family,
    normalize_electrochemical_material_family,
)

STATIC_MATERIAL_INFORMATION_VERSION = "chemworld-static-material-information-1.1"
STATIC_MATERIAL_INFORMATION_OPAQUE = "opaque_codes"
STATIC_MATERIAL_INFORMATION_NOMINAL = "anonymous_nominal_properties"
STATIC_MATERIAL_INFORMATION_SHUFFLED = "anonymous_shuffled_properties"
STATIC_MATERIAL_INFORMATION_MODES = frozenset(
    {
        STATIC_MATERIAL_INFORMATION_OPAQUE,
        STATIC_MATERIAL_INFORMATION_NOMINAL,
        STATIC_MATERIAL_INFORMATION_SHUFFLED,
    }
)
_ELECTROCHEMICAL_TASK_ID = "electrochemical-conversion"
_CONTROLLED_MATERIAL_FIELDS = ("electrolyte_profile", "solvent")


def public_material_catalog() -> dict[str, Any]:
    """Return names, reference status, and interpretation policy for task materials."""

    registry = curated_component_registry()
    solvents: list[dict[str, Any]] = []
    for index, solvent_id in enumerate(SOLVENTS):
        try:
            component = registry.resolve(solvent_id)
        except KeyError:
            solvents.append(
                {
                    "index": index,
                    "canonical_id": solvent_id,
                    "display_name": solvent_id.replace("_", " ").title(),
                    "identity_kind": "real_named_component",
                    "reference_status": "identity_only_not_in_curated_property_subset",
                    "formula": None,
                    "cas_number": None,
                    "runtime_coupling": "categorical_benchmark_effect",
                }
            )
            continue
        solvents.append(
            {
                "index": index,
                "canonical_id": component.identifier,
                "display_name": str(
                    component.metadata.get("display_name") or component.identifier.title()
                ),
                "identity_kind": "real_reference_component",
                "reference_status": "curated_identity_and_local_property_correlations",
                "formula": component.hill_formula,
                "cas_number": component.cas_number,
                "runtime_coupling": "categorical_benchmark_effect",
            }
        )
    catalysts = [
        {
            "index": index,
            "canonical_id": catalyst_id,
            "display_name": f"Catalyst {chr(ord('A') + index)}",
            "identity_kind": "anonymous_benchmark_formulation",
            "reference_status": "no_real_material_identity_claimed",
            "runtime_coupling": "latent_categorical_activity_profile",
        }
        for index, catalyst_id in enumerate(CATALYSTS)
    ]
    electrolyte_profiles = [
        {
            "index": index,
            "canonical_id": profile_id,
            "display_name": profile_id.replace("_", " ").title(),
            "identity_kind": "anonymous_aqueous_electrolyte_formulation",
            "reference_status": "bounded_benchmark_formulation_not_a_named_product",
            "runtime_coupling": (
                "conductivity_diffusion_layer_acid_base_and_precipitation_profile"
            ),
        }
        for index, profile_id in enumerate(ELECTROLYTE_PROFILES)
    ]
    return {
        "catalog_version": "chemworld-public-materials-0.2",
        "solvents": solvents,
        "catalysts": catalysts,
        "electrolyte_profiles": electrolyte_profiles,
        "reagent": {
            "canonical_id": "limiting_reagent",
            "display_name": "Anonymous limiting reagent",
            "identity_kind": "mechanism_role",
            "reference_status": "mechanism_specific_not_a_real_identity",
        },
        "interpretation_policy": (
            "Real solvent names identify selectable materials, but current reaction-task "
            "kinetic effects are calibrated categorical benchmark effects rather than "
            "predictions from the curated property correlations. Catalysts and reaction "
            "species remain anonymous; do not infer a real catalyst or named synthesis."
        ),
    }


def material_choice_labels(field: str) -> dict[str, str]:
    """Map stable numeric action values to honest user-facing labels."""

    catalog = public_material_catalog()
    key = (
        "solvents"
        if field in {"solvent", "extractant"}
        else "catalysts"
        if field == "catalyst"
        else "electrolyte_profiles"
        if field == "electrolyte_profile"
        else None
    )
    if key is None:
        return {}
    labels: dict[str, str] = {}
    for item in catalog[key]:
        reference = str(item["reference_status"])
        suffix = "reference identity" if reference.startswith("curated_") else "benchmark"
        formula = f" · {item['formula']}" if item.get("formula") else ""
        labels[str(item["index"])] = f"{item['display_name']}{formula} · {suffix}"
    return labels


def action_material_display(action: dict[str, Any]) -> dict[str, Any]:
    """Return a JSON-safe action copy annotated with public material names."""

    display = dict(action)
    catalog = public_material_catalog()
    for field, key in (
        ("solvent", "solvents"),
        ("extractant", "solvents"),
        ("catalyst", "catalysts"),
        ("electrolyte_profile", "electrolyte_profiles"),
    ):
        value = action.get(field)
        if not isinstance(value, int) or isinstance(value, bool):
            continue
        choices = catalog[key]
        if 0 <= value < len(choices):
            display[f"{field}_name"] = choices[value]["display_name"]
    return display


def normalize_static_material_information_config(
    config: Mapping[str, Any] | None,
    *,
    task_ids: Sequence[str],
    material_family_id: object | None = None,
) -> dict[str, Any]:
    """Validate one S0 information condition without reading hidden world state."""

    if config is None:
        return {"mode": STATIC_MATERIAL_INFORMATION_OPAQUE}
    if not isinstance(config, Mapping):
        raise ValueError("material_information must be an object")
    unknown = set(config) - {"mode", "descriptor_permutation"}
    if unknown:
        raise ValueError(f"material_information has unsupported fields: {sorted(unknown)}")
    mode = config.get("mode")
    if mode not in STATIC_MATERIAL_INFORMATION_MODES:
        raise ValueError(
            f"material_information.mode must be one of {sorted(STATIC_MATERIAL_INFORMATION_MODES)}"
        )
    if mode != STATIC_MATERIAL_INFORMATION_OPAQUE and set(task_ids) != {_ELECTROCHEMICAL_TASK_ID}:
        raise ValueError(
            "nominal material properties are currently audited only for the "
            "electrochemical-conversion task"
        )
    if mode != STATIC_MATERIAL_INFORMATION_OPAQUE:
        family_id = normalize_electrochemical_material_family(material_family_id)
        if family_id != NOMINAL_PRIOR_MATERIAL_FAMILY:
            raise ValueError(
                "nominal material information requires the nominal-prior material family"
            )
    raw_permutation = config.get("descriptor_permutation")
    if mode != STATIC_MATERIAL_INFORMATION_SHUFFLED:
        if raw_permutation is not None:
            raise ValueError(
                "descriptor_permutation is allowed only for anonymous_shuffled_properties"
            )
        return {"mode": str(mode)}
    if not isinstance(raw_permutation, Mapping) or set(raw_permutation) != set(
        _CONTROLLED_MATERIAL_FIELDS
    ):
        raise ValueError(
            "shuffled material information requires permutations for electrolyte_profile "
            "and solvent"
        )
    normalized_permutation: dict[str, list[int]] = {}
    for field in _CONTROLLED_MATERIAL_FIELDS:
        values = raw_permutation[field]
        if not isinstance(values, list) or any(
            isinstance(item, bool) or not isinstance(item, int) for item in values
        ):
            raise ValueError(f"descriptor_permutation.{field} must be an integer list")
        expected = list(range(4))
        if sorted(values) != expected:
            raise ValueError(f"descriptor_permutation.{field} must be a permutation of {expected}")
        if any(index == source for index, source in enumerate(values)):
            raise ValueError(f"descriptor_permutation.{field} must be a derangement")
        normalized_permutation[field] = list(values)
    return {
        "mode": STATIC_MATERIAL_INFORMATION_SHUFFLED,
        "descriptor_permutation": normalized_permutation,
    }


def static_material_information_dossier(
    config: Mapping[str, Any] | None,
    *,
    task_id: str,
    material_family_id: object | None = None,
) -> dict[str, Any] | None:
    """Build the model-visible anonymous property dossier for one S0 task."""

    normalized = normalize_static_material_information_config(
        config,
        task_ids=(task_id,),
        material_family_id=material_family_id,
    )
    mode = normalized["mode"]
    if mode == STATIC_MATERIAL_INFORMATION_OPAQUE:
        return None
    permutations = normalized.get(
        "descriptor_permutation",
        {field: list(range(4)) for field in _CONTROLLED_MATERIAL_FIELDS},
    )
    family = electrochemical_material_family(material_family_id)
    electrolyte_choices = []
    for action_value, source_index in enumerate(permutations["electrolyte_profile"]):
        row = family.electrolyte_profiles[source_index]
        electrolyte_choices.append(
            {
                "action_value": action_value,
                "anonymous_material_id": f"electrolyte-E{action_value}",
                "nominal_properties": {
                    "bulk_conductivity_S_m": row["electrolyte_conductivity_S_m"],
                    "diffusivity_m2_s": row["diffusivity_m2_s"],
                    "diffusion_layer_thickness_mm": (1000.0 * row["diffusion_layer_thickness_m"]),
                    "double_layer_capacitance_F_m2": (row["double_layer_capacitance_F_m2"]),
                    "acid_concentration_mol_L": row["acid_concentration_mol_L"],
                    "supporting_electrolyte_concentration_mol_L": (
                        row["supporting_electrolyte_concentration_mol_L"]
                    ),
                    "precipitating_salt_concentration_mol_L": (
                        row["precipitating_salt_concentration_mol_L"]
                    ),
                    "acid_pKa": row["electrolyte_acid_pka"],
                    "precipitation_log10_Ksp": math.log10(row["electrolyte_ksp"]),
                    "standard_potential_shift_V": row["standard_potential_shift_V"],
                },
            }
        )
    solvent_choices = []
    for action_value, source_index in enumerate(permutations["solvent"]):
        row = family.solvent_profiles[source_index]
        solvent_choices.append(
            {
                "action_value": action_value,
                "anonymous_material_id": f"solvent-S{action_value}",
                "nominal_properties": {
                    "relative_conductivity": row["conductivity_multiplier"],
                    "relative_diffusivity": row["diffusivity_multiplier"],
                    "relative_double_layer_capacitance": row["capacitance_multiplier"],
                    "relative_proton_activity": row["proton_activity_multiplier"],
                    "relative_solubility_product": row["ksp_multiplier"],
                    "standard_potential_shift_V": row["standard_potential_shift_V"],
                    "relative_cost_index": row["relative_cost_index"],
                },
            }
        )
    return {
        "contract_version": STATIC_MATERIAL_INFORMATION_VERSION,
        "presentation": "anonymous_material_ids_with_nominal_properties",
        "identity_policy": (
            "The IDs are benchmark-only labels and do not identify real solvents, "
            "electrolytes, products, or commercial formulations."
        ),
        "property_scope": {
            "electrolyte_profile": (
                "Declared nominal electrolyte properties before bounded world residuals "
                "and solvent coupling."
            ),
            "solvent": (
                "Declared nominal solvent factors before bounded world residuals and "
                "electrolyte coupling."
            ),
        },
        "residual_policy": (
            "World-specific transport, solvation, and interface-kinetics latent factors "
            "generate bounded correlated residuals. They are hidden and fixed for the "
            "entire campaign."
        ),
        "cell_fixture_policy": (
            "Electrode area, electrode gap, and base contact resistance are sampled once "
            "per world and remain identical for every material and experiment in that "
            "campaign. They may differ in another world and are not material descriptors."
        ),
        "interpretation_policy": (
            "Treat these foundational properties as mechanistic prior evidence, not as "
            "an objective ranking or a complete response law. Faradaic efficiency and "
            "product selectivity are intentionally not supplied as material descriptors."
        ),
        "choices": {
            "electrolyte_profile": electrolyte_choices,
            "solvent": solvent_choices,
        },
    }


__all__ = [
    "STATIC_MATERIAL_INFORMATION_MODES",
    "STATIC_MATERIAL_INFORMATION_NOMINAL",
    "STATIC_MATERIAL_INFORMATION_OPAQUE",
    "STATIC_MATERIAL_INFORMATION_SHUFFLED",
    "STATIC_MATERIAL_INFORMATION_VERSION",
    "action_material_display",
    "material_choice_labels",
    "normalize_static_material_information_config",
    "public_material_catalog",
    "static_material_information_dossier",
]
