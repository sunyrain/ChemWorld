from __future__ import annotations

import pytest

from chemworld.foundation import (
    DimensionContract,
    canonical_dimensions,
    check_unit_dimension,
    core_dimension_contracts,
    unmapped_supported_unit_dimensions,
)
from chemworld.physchem import (
    ComponentConflictPolicy,
    ComponentDataConflictReport,
    ComponentFieldCandidate,
    ComponentIdentityRegistry,
    ComponentSpec,
    ComponentUncertainty,
    DatasetProvenanceCard,
    DataSourceProvenance,
    audit_component_data_conflicts,
    build_dataset_provenance_card,
    curated_component_registry,
    data_foundation_model_cards,
    validate_model_card,
)


def test_curated_component_registry_resolves_all_identity_forms_and_roundtrips() -> None:
    registry = curated_component_registry()
    water = registry.resolve("water")

    assert registry.resolve("dihydrogen oxide") == water
    assert registry.resolve("7732185") == water
    assert registry.resolve("InChI=1S/H2O/h1H2") == water
    assert registry.resolve("XLYOFNOQVPJJNP-UHFFFAOYSA-N") == water
    assert water.formula == "H2O"
    assert water.charge == 0
    assert water.molecular_weight_g_mol == pytest.approx(18.015, rel=2e-4)
    assert water.provenance

    payload = registry.to_dict()
    restored = ComponentIdentityRegistry.from_dict(payload)
    assert restored.to_dict() == payload
    assert restored.digest == registry.digest


def test_component_registry_rejects_duplicate_and_tampered_identities() -> None:
    water = ComponentSpec(
        identifier="water",
        formula="H2O",
        cas_number="7732-18-5",
        inchi="InChI=1S/H2O/h1H2",
        inchi_key="XLYOFNOQVPJJNP-UHFFFAOYSA-N",
    )
    with pytest.raises(ValueError, match="duplicate component identifiers"):
        ComponentIdentityRegistry("duplicate", "1", (water, water), "test")

    collision = ComponentSpec(
        identifier="water_copy",
        formula="H2O",
        aliases=("water",),
    )
    with pytest.raises(ValueError, match="alias conflict"):
        ComponentIdentityRegistry("collision", "1", (water, collision), "test")

    payload = ComponentIdentityRegistry("valid", "1", (water,), "test").to_dict()
    payload["digest"] = "0" * 64
    with pytest.raises(ValueError, match="digest mismatch"):
        ComponentIdentityRegistry.from_dict(payload)

    with pytest.raises(ValueError, match="InChI=1"):
        ComponentSpec(identifier="bad", formula="H2O", inchi="H2O")
    with pytest.raises(ValueError, match="14-10-1"):
        ComponentSpec(identifier="bad", formula="H2O", inchi_key="bad-key")


def test_dimension_catalog_is_closed_and_obeys_dimension_algebra() -> None:
    dimensions = canonical_dimensions()
    required = {
        "amount",
        "mass",
        "volume",
        "temperature",
        "pressure",
        "energy",
        "dynamic_viscosity",
        "thermal_conductivity",
        "diffusivity",
        "detector_response",
        "chemical_shift",
        "mass_to_charge",
    }
    assert required <= set(dimensions)
    assert unmapped_supported_unit_dimensions() == ()
    assert dimensions["pressure"].vector == (
        dimensions["energy"].vector / dimensions["volume"].vector
    )
    assert dimensions["electric_charge"].vector == (
        dimensions["electrical_current"].vector * dimensions["time"].vector
    )


def test_dimension_checker_keeps_instrument_semantics_distinct() -> None:
    assert check_unit_dimension("mPa*s", "dynamic_viscosity").compatible
    assert check_unit_dimension("ppm", "chemical_shift").compatible
    assert check_unit_dimension("m/z", "mass_to_charge").compatible

    mismatch = check_unit_dimension("dimensionless", "chemical_shift")
    assert not mismatch.compatible
    assert mismatch.actual_dimension == "dimensionless"
    with pytest.raises(ValueError, match="expects dimension"):
        check_unit_dimension("bar", "temperature", field_id="temperature_K", strict=True)


def test_dimension_field_contracts_are_json_roundtrip_safe() -> None:
    contracts = core_dimension_contracts()
    assert contracts
    restored = DimensionContract.from_dict(contracts[0].to_dict())
    assert restored == contracts[0]
    assert restored.check("mmol").compatible
    strict_contract = DimensionContract("strict_amount", "amount", ("mmol",))
    with pytest.raises(ValueError, match="not allowed"):
        strict_contract.check("mol", strict=True)


def _sources() -> tuple[DataSourceProvenance, ...]:
    return (
        DataSourceProvenance(
            "thermo",
            0,
            "thermo property package",
            version="0.6",
            license="MIT",
        ),
        DataSourceProvenance(
            "chemicals",
            1,
            "chemicals property tables",
            version="1.5",
            license="MIT",
        ),
    )


def _uncertainty(source_id: str) -> ComponentUncertainty:
    return ComponentUncertainty(
        field_id="normal_boiling_point_K",
        unit="K",
        standard_uncertainty=0.01,
        source_id=source_id,
    )


def test_data_conflict_resolution_is_priority_ordered_and_auditable() -> None:
    candidates = (
        ComponentFieldCandidate(
            "normal_boiling_point_K",
            373.124,
            "chemicals",
            uncertainty=_uncertainty("chemicals"),
        ),
        ComponentFieldCandidate(
            "normal_boiling_point_K",
            373.125,
            "thermo",
            uncertainty=_uncertainty("thermo"),
        ),
    )
    policy = ComponentConflictPolicy(
        mode="warn",
        source_priority=("thermo", "chemicals"),
        field_atol={"normal_boiling_point_K": 0.01},
        required_uncertainty_fields=("normal_boiling_point_K",),
        missing_uncertainty_mode="raise",
    )
    report = audit_component_data_conflicts(
        tuple(reversed(candidates)),
        policy,
        sources=tuple(reversed(_sources())),
    )

    assert report.accepted
    assert report.resolutions[0].resolved_source_id == "thermo"
    assert report.resolutions[0].status == "consistent"
    assert report.sources[0].source_id == "thermo"
    restored = ComponentDataConflictReport.from_dict(report.to_dict())
    assert restored.to_dict() == report.to_dict()


def test_data_conflict_reports_warning_and_hard_fail_modes() -> None:
    candidates = (
        ComponentFieldCandidate("critical_temperature_K", 500.0, "chemicals"),
        ComponentFieldCandidate("critical_temperature_K", 510.0, "thermo"),
    )
    warning_policy = ComponentConflictPolicy(
        mode="warn",
        source_priority=("thermo", "chemicals"),
        required_uncertainty_fields=("critical_temperature_K",),
        missing_uncertainty_mode="warn",
    )
    warning = audit_component_data_conflicts(
        candidates,
        warning_policy,
        sources=_sources(),
    )
    assert warning.accepted
    assert warning.warning_count == 2
    assert {finding.severity for finding in warning.findings} == {"warning"}

    hard_policy = ComponentConflictPolicy(
        mode="raise",
        source_priority=("thermo", "chemicals"),
        required_uncertainty_fields=("critical_temperature_K",),
        missing_uncertainty_mode="raise",
    )
    hard = audit_component_data_conflicts(candidates, hard_policy, sources=_sources())
    assert not hard.accepted
    assert hard.error_count == 2


def test_data_conflict_rejects_undefined_sources_and_card_tampering() -> None:
    report = audit_component_data_conflicts(
        (ComponentFieldCandidate("density", 998.0, "unknown"),),
        ComponentConflictPolicy(mode="warn"),
        sources=_sources(),
    )
    assert not report.accepted
    assert "undefined source" in report.findings[0].message

    card = build_dataset_provenance_card(
        report,
        dataset_id="curated-component-data-v1",
        registry_digest=curated_component_registry().digest,
    )
    payload = card.to_dict()
    assert DatasetProvenanceCard.from_dict(payload).to_dict() == payload
    payload["digest"] = "f" * 64
    with pytest.raises(ValueError, match="digest mismatch"):
        DatasetProvenanceCard.from_dict(payload)


def test_data_foundation_model_cards_are_auditable() -> None:
    cards = data_foundation_model_cards()
    assert {card.model_id for card in cards} == {
        "component_identity_registry_v1",
        "canonical_dimension_checker_v1",
        "deterministic_data_conflict_policy_v1",
    }
    assert all(validate_model_card(card) == [] for card in cards)
