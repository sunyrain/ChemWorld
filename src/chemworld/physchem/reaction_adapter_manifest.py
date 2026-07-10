"""WF-10 provider and adapter proposal for rate-law contract diagnostics."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from chemworld.physchem.maturity import (
    MaturityLevel,
    ModelAdapterManifest,
    ModelExecutionRole,
    ModelProviderContract,
)
from chemworld.physchem.reaction_network_specs import ReactionSpec
from chemworld.physchem.reaction_rate_contracts import (
    CANTERA_COMMIT,
    RMG_PY_COMMIT,
    audit_reaction_rate_contract,
)
from chemworld.runtime.kernel_contracts import ModelProviderResult

OWNED_PATHS = (
    "src/chemworld/physchem/reaction_rate_contracts.py",
    "src/chemworld/physchem/reaction_adapter_manifest.py",
    "tests/test_reaction_rate_contracts.py",
)
INTEGRATION_OPERATIONS = ("heat", "wait", "run_flow")


def reaction_rate_provider_contract() -> ModelProviderContract:
    """Return the WF-00-compatible diagnostic provider contract."""

    return ModelProviderContract(
        model_id="chemworld_arrhenius_unit_contract_vnext",
        module_id="reaction_kinetics",
        maturity=MaturityLevel.REFERENCE_VALIDATED,
        role=ModelExecutionRole.DIAGNOSTIC,
        provider_path=("chemworld.physchem.reaction_adapter_manifest.ReactionRateContractProvider"),
        input_fields=("reaction",),
        output_fields=("contract",),
        units={
            "reaction": "ReactionSpec",
            "contract": "JSON dimension contract",
        },
        validity_checks=(
            "reaction is a ReactionSpec",
            "rate law is in the supported Arrhenius family",
            "pre-exponential factors are finite and positive",
            "temperature exponents and activation energies are finite",
            "reversible, third-body, and falloff declarations are complete",
        ),
        diagnostic_fields=(
            "passed",
            "equation_id",
            "forward_order",
            "effective_forward_order",
            "violations",
        ),
        failure_policy=(
            "return an unsuccessful ModelProviderResult with explicit declaration "
            "violations; never infer missing units or mutate the mechanism"
        ),
        provenance=(
            (f"Cantera {CANTERA_COMMIT}: Arrhenius and falloff unit conventions"),
            f"RMG-Py {RMG_PY_COMMIT}: Arrhenius quantity schema",
            "WF-10 analytical dimensional identities",
        ),
        intended_operations=INTEGRATION_OPERATIONS,
    )


class ReactionRateContractProvider:
    """Diagnostic provider that audits one reaction declaration."""

    @property
    def model_contract(self) -> ModelProviderContract:
        return reaction_rate_provider_contract()

    def validate_domain(self, inputs: Mapping[str, Any]) -> tuple[str, ...]:
        reaction = inputs.get("reaction")
        if not isinstance(reaction, ReactionSpec):
            return ("reaction must be a ReactionSpec",)
        return ()

    def evaluate(self, inputs: Mapping[str, Any]) -> ModelProviderResult:
        domain_violations = self.validate_domain(inputs)
        if domain_violations:
            return ModelProviderResult(
                outputs={},
                diagnostics={
                    "passed": False,
                    "equation_id": None,
                    "forward_order": None,
                    "effective_forward_order": None,
                    "violations": list(domain_violations),
                },
                success=False,
                failure_reason="; ".join(domain_violations),
                provenance=self.model_contract.provenance,
            )
        reaction = inputs["reaction"]
        assert isinstance(reaction, ReactionSpec)
        report = audit_reaction_rate_contract(reaction)
        diagnostics = {
            "passed": report.passed,
            "equation_id": report.equation_id,
            "forward_order": report.forward_order,
            "effective_forward_order": report.effective_forward_order,
            "violations": list(report.violations),
        }
        if not report.passed:
            return ModelProviderResult(
                outputs={"contract": report.to_dict()},
                diagnostics=diagnostics,
                success=False,
                failure_reason="; ".join(report.violations),
                provenance=report.provenance,
            )
        return ModelProviderResult(
            outputs={"contract": report.to_dict()},
            diagnostics=diagnostics,
            provenance=report.provenance,
        )


def reaction_rate_adapter_manifest() -> ModelAdapterManifest:
    """Return the claim-bound proposal for later WF-110 intake."""

    return ModelAdapterManifest(
        adapter_id="wf-10-arrhenius-unit-contract",
        adapter_version="0.1",
        owner_workstream="wf-10-reaction-core",
        provider_contract=reaction_rate_provider_contract(),
        owned_paths=OWNED_PATHS,
        integration_operations=INTEGRATION_OPERATIONS,
        target_world_law="chemworld-physical-chemistry-vnext",
        status="proposal",
    )


__all__ = [
    "INTEGRATION_OPERATIONS",
    "OWNED_PATHS",
    "ReactionRateContractProvider",
    "reaction_rate_adapter_manifest",
    "reaction_rate_provider_contract",
]
