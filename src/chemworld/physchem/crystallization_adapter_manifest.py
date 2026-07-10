"""WF-50 provider and adapter proposal for crystallization audits."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from chemworld.physchem.crystallization_validation import (
    IDAES_BALANCE_PATH,
    IDAES_COMMIT,
    CrystallizationConvergenceSpec,
    CrystallizationGridCase,
    audit_crystallization_convergence,
)
from chemworld.physchem.maturity import (
    MaturityLevel,
    ModelAdapterManifest,
    ModelExecutionRole,
    ModelProviderContract,
)
from chemworld.runtime.kernel_contracts import ModelProviderResult

OWNED_PATHS = (
    "src/chemworld/physchem/crystallization_validation.py",
    "src/chemworld/physchem/crystallization_adapter_manifest.py",
    "tests/test_crystallization_validation.py",
    "workstreams/world_foundation/adapters/wf-50-crystallization-convergence.json",
)
INTEGRATION_OPERATIONS = ("cool_crystallize",)


def crystallization_convergence_provider_contract() -> ModelProviderContract:
    """Return the WF-00-compatible diagnostic provider contract."""

    return ModelProviderContract(
        model_id="chemworld_crystallization_convergence_audit_vnext",
        module_id="separations",
        maturity=MaturityLevel.REFERENCE_VALIDATED,
        role=ModelExecutionRole.DIAGNOSTIC,
        provider_path=(
            "chemworld.physchem.crystallization_adapter_manifest.CrystallizationConvergenceProvider"
        ),
        input_fields=("case", "audit_spec"),
        output_fields=("report",),
        units={
            "case": "CrystallizationGridCase with explicit SI/L/mol units",
            "audit_spec": "grid and dimensioned residual policy",
            "report": "JSON numerical convergence and closure audit",
        },
        validity_checks=(
            "case is a complete CrystallizationGridCase",
            "audit_spec declares at least two strictly increasing grid levels",
            "all underlying PBM inputs pass cooling_crystallization domain checks",
            "all convergence and ledger thresholds are finite and positive",
        ),
        diagnostic_fields=(
            "passed",
            "grid_converged",
            "material_closed",
            "step_ledger_closed",
            "particle_count_ledger_closed",
            "warnings",
        ),
        failure_policy=(
            "reject invalid cases or policies with an explicit unsuccessful result; "
            "valid non-converged grids return a successful diagnostic whose passed "
            "field is false"
        ),
        provenance=(
            "ChemWorld cooling_crystallization deterministic refinement ladder",
            "analytical component, step-transfer, and particle-count ledgers",
            (
                f"IDAES {IDAES_COMMIT}:{IDAES_BALANCE_PATH} convention boundary; "
                "not a crystallization kinetics backend"
            ),
        ),
        intended_operations=INTEGRATION_OPERATIONS,
    )


class CrystallizationConvergenceProvider:
    """Diagnostic provider for the existing compact crystallization PBM."""

    @property
    def model_contract(self) -> ModelProviderContract:
        return crystallization_convergence_provider_contract()

    def validate_domain(self, inputs: Mapping[str, Any]) -> tuple[str, ...]:
        violations: list[str] = []
        if not isinstance(inputs.get("case"), CrystallizationGridCase):
            violations.append("case must be a CrystallizationGridCase")
        audit_spec = inputs.get("audit_spec")
        if audit_spec is not None and not isinstance(
            audit_spec,
            CrystallizationConvergenceSpec,
        ):
            violations.append("audit_spec must be a CrystallizationConvergenceSpec or None")
        return tuple(violations)

    def evaluate(self, inputs: Mapping[str, Any]) -> ModelProviderResult:
        domain_violations = self.validate_domain(inputs)
        if domain_violations:
            return _failed_result("; ".join(domain_violations), self.model_contract.provenance)
        case = inputs["case"]
        audit_spec = inputs.get("audit_spec")
        assert isinstance(case, CrystallizationGridCase)
        assert audit_spec is None or isinstance(audit_spec, CrystallizationConvergenceSpec)
        try:
            report = audit_crystallization_convergence(case, spec=audit_spec)
        except ValueError as error:
            return _failed_result(str(error), self.model_contract.provenance)
        diagnostics = {
            "passed": report.passed,
            "grid_converged": report.grid_converged,
            "material_closed": report.material_closed,
            "step_ledger_closed": report.step_ledger_closed,
            "particle_count_ledger_closed": report.particle_count_ledger_closed,
            "warnings": list(report.warnings),
        }
        return ModelProviderResult(
            outputs={"report": report.to_dict()},
            diagnostics=diagnostics,
            warnings=report.warnings,
            provenance=report.provenance,
        )


def crystallization_convergence_adapter_manifest() -> ModelAdapterManifest:
    """Return the claim-bound proposal for later WF-110 intake."""

    return ModelAdapterManifest(
        adapter_id="wf-50-crystallization-convergence",
        adapter_version="0.1",
        owner_workstream="wf-50-crystallization-convergence",
        provider_contract=crystallization_convergence_provider_contract(),
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
            "passed": False,
            "grid_converged": False,
            "material_closed": False,
            "step_ledger_closed": False,
            "particle_count_ledger_closed": False,
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
    "CrystallizationConvergenceProvider",
    "crystallization_convergence_adapter_manifest",
    "crystallization_convergence_provider_contract",
]
