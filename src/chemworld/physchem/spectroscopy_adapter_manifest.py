"""WF-20 provider and adapter proposal for spectral identifiability audits."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from chemworld.physchem.maturity import (
    MaturityLevel,
    ModelAdapterManifest,
    ModelExecutionRole,
    ModelProviderContract,
)
from chemworld.physchem.spectroscopy import SpectralMeasurement
from chemworld.physchem.spectroscopy_identifiability import (
    CHEMICALS_COMMIT,
    RMG_PY_COMMIT,
    SpectralIdentifiabilitySpec,
    evaluate_spectral_identifiability,
)
from chemworld.runtime.kernel_contracts import ModelProviderResult

OWNED_PATHS = (
    "src/chemworld/physchem/spectroscopy_identifiability.py",
    "src/chemworld/physchem/spectroscopy_adapter_manifest.py",
    "tests/test_spectroscopy_identifiability.py",
    "workstreams/world_foundation/adapters/wf-20-spectral-identifiability.json",
)
INTEGRATION_OPERATIONS = ("measure",)


def spectroscopy_identifiability_provider_contract() -> ModelProviderContract:
    """Return the WF-00-compatible diagnostic provider contract."""

    return ModelProviderContract(
        model_id="chemworld_spectral_identifiability_audit_vnext",
        module_id="spectroscopy_instruments",
        maturity=MaturityLevel.REFERENCE_VALIDATED,
        role=ModelExecutionRole.DIAGNOSTIC,
        provider_path=(
            "chemworld.physchem.spectroscopy_adapter_manifest.SpectralIdentifiabilityProvider"
        ),
        input_fields=("reference", "alternative", "audit_spec"),
        output_fields=("report",),
        units={
            "reference": "SpectralMeasurement",
            "alternative": "SpectralMeasurement",
            "audit_spec": "dimensionless policy",
            "report": "JSON signal-level audit",
        },
        validity_checks=(
            "measurements use the same instrument and public signal contract",
            "measurement axes are identical",
            "each state supplies the configured minimum replicate count",
            "replicate arrays are finite and match the public axis",
        ),
        diagnostic_fields=(
            "identifiable",
            "replicate_stable",
            "states_distinct",
            "between_state_rmse",
            "separation_ratio",
            "warnings",
        ),
        failure_policy=(
            "reject invalid signal pairs with an explicit unsuccessful result; "
            "valid but indistinguishable pairs return a successful diagnostic "
            "whose identifiable field is false"
        ),
        provenance=(
            "ChemWorld public replicate-signal RMSE identities",
            f"chemicals {CHEMICALS_COMMIT}: non-instrument reference boundary",
            f"RMG-Py {RMG_PY_COMMIT}: non-instrument reference boundary",
        ),
        intended_operations=INTEGRATION_OPERATIONS,
    )


class SpectralIdentifiabilityProvider:
    """Diagnostic provider for pairwise public instrument signals."""

    @property
    def model_contract(self) -> ModelProviderContract:
        return spectroscopy_identifiability_provider_contract()

    def validate_domain(self, inputs: Mapping[str, Any]) -> tuple[str, ...]:
        violations: list[str] = []
        if not isinstance(inputs.get("reference"), SpectralMeasurement):
            violations.append("reference must be a SpectralMeasurement")
        if not isinstance(inputs.get("alternative"), SpectralMeasurement):
            violations.append("alternative must be a SpectralMeasurement")
        audit_spec = inputs.get("audit_spec")
        if audit_spec is not None and not isinstance(
            audit_spec,
            SpectralIdentifiabilitySpec,
        ):
            violations.append("audit_spec must be a SpectralIdentifiabilitySpec or None")
        return tuple(violations)

    def evaluate(self, inputs: Mapping[str, Any]) -> ModelProviderResult:
        domain_violations = self.validate_domain(inputs)
        if domain_violations:
            return _failed_result("; ".join(domain_violations), self.model_contract.provenance)
        reference = inputs["reference"]
        alternative = inputs["alternative"]
        audit_spec = inputs.get("audit_spec")
        assert isinstance(reference, SpectralMeasurement)
        assert isinstance(alternative, SpectralMeasurement)
        assert audit_spec is None or isinstance(audit_spec, SpectralIdentifiabilitySpec)
        try:
            report = evaluate_spectral_identifiability(
                reference,
                alternative,
                spec=audit_spec,
            )
        except ValueError as error:
            return _failed_result(str(error), self.model_contract.provenance)
        diagnostics = {
            "identifiable": report.identifiable,
            "replicate_stable": report.replicate_stable,
            "states_distinct": report.states_distinct,
            "between_state_rmse": report.between_state_rmse,
            "separation_ratio": report.separation_ratio,
            "warnings": list(report.warnings),
        }
        return ModelProviderResult(
            outputs={"report": report.to_dict()},
            diagnostics=diagnostics,
            warnings=report.warnings,
            provenance=report.provenance,
        )


def spectroscopy_identifiability_adapter_manifest() -> ModelAdapterManifest:
    """Return the claim-bound proposal for later WF-110 intake."""

    return ModelAdapterManifest(
        adapter_id="wf-20-spectral-identifiability",
        adapter_version="0.1",
        owner_workstream="wf-20-spectral-identifiability",
        provider_contract=spectroscopy_identifiability_provider_contract(),
        owned_paths=OWNED_PATHS,
        integration_operations=INTEGRATION_OPERATIONS,
        target_world_law="chemworld-physical-chemistry-vnext",
        status="proposal",
    )


def _failed_result(
    failure_reason: str,
    provenance: tuple[str, ...],
) -> ModelProviderResult:
    return ModelProviderResult(
        outputs={},
        diagnostics={
            "identifiable": False,
            "replicate_stable": False,
            "states_distinct": False,
            "between_state_rmse": None,
            "separation_ratio": None,
            "warnings": [failure_reason],
        },
        warnings=(failure_reason,),
        success=False,
        failure_reason=failure_reason,
        provenance=provenance,
    )


__all__ = [
    "INTEGRATION_OPERATIONS",
    "OWNED_PATHS",
    "SpectralIdentifiabilityProvider",
    "spectroscopy_identifiability_adapter_manifest",
    "spectroscopy_identifiability_provider_contract",
]
