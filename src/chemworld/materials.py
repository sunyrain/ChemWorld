"""Public material identities without overstating benchmark chemistry realism."""

from __future__ import annotations

from typing import Any

from chemworld.physchem.component_registry import curated_component_registry
from chemworld.world.actions import CATALYSTS, SOLVENTS


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
    return {
        "catalog_version": "chemworld-public-materials-0.1",
        "solvents": solvents,
        "catalysts": catalysts,
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
    ):
        value = action.get(field)
        if not isinstance(value, int) or isinstance(value, bool):
            continue
        choices = catalog[key]
        if 0 <= value < len(choices):
            display[f"{field}_name"] = choices[value]["display_name"]
    return display


__all__ = [
    "action_material_display",
    "material_choice_labels",
    "public_material_catalog",
]
