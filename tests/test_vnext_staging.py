from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from scripts.manage_claims import complete_claim, create_claim

from chemworld.physchem.maturity import (
    MaturityLevel,
    ModelAdapterManifest,
    ModelExecutionRole,
    ModelProviderContract,
)
from chemworld.runtime.vnext_staging import (
    AdapterIntegrationClass,
    build_vnext_integration_plan,
    classify_adapter,
)


def _prepare(root: Path) -> None:
    (root / "claims" / "active").mkdir(parents=True)
    (root / "claims" / "completed").mkdir(parents=True)


def _manifest(
    *,
    role: ModelExecutionRole,
    model_id: str,
    replaces: tuple[str, ...] = (),
) -> ModelAdapterManifest:
    contract = ModelProviderContract(
        model_id=model_id,
        module_id="reaction_kinetics",
        maturity=MaturityLevel.REFERENCE_VALIDATED,
        role=role,
        provider_path="chemworld.runtime.kernel_contracts.ContractModelProviderStub",
        input_fields=("reaction",),
        output_fields=("result",),
        units={"reaction": "ReactionSpec", "result": "JSON"},
        validity_checks=("typed reaction",),
        diagnostic_fields=("residual",),
        failure_policy="return a typed failed result",
        provenance=("reference-case",),
        intended_operations=("heat",),
    )
    return ModelAdapterManifest(
        adapter_id=f"{model_id}-adapter",
        adapter_version="0.1",
        owner_workstream="wf-10-test-provider",
        provider_contract=contract,
        owned_paths=("src/example/provider.py",),
        integration_operations=("heat",),
        target_world_law="chemworld-physical-chemistry-vnext",
        replaces_model_ids=replaces,
    )


def _write(root: Path, manifest: ModelAdapterManifest) -> Path:
    path = root / f"{manifest.adapter_id}.json"
    path.write_text(json.dumps(manifest.to_dict()), encoding="utf-8")
    return path


def _claim(root: Path, *, complete: bool) -> None:
    create_claim(
        root,
        task_id="wf-10-test-provider",
        owner="test-team",
        branch="team/wf-10-test-provider",
        scope="Test provider",
        owned_paths=["src/example/provider.py"],
    )
    if complete:
        complete_claim(
            root,
            task_id="wf-10-test-provider",
            owner="test-team",
            summary="Provider delivered",
        )


def test_classification_separates_diagnostics_additions_and_replacements() -> None:
    diagnostic = _manifest(
        role=ModelExecutionRole.DIAGNOSTIC,
        model_id="diagnostic_vnext",
    )
    addition = _manifest(
        role=ModelExecutionRole.RUNTIME,
        model_id="runtime_addition_vnext",
    )
    replacement = _manifest(
        role=ModelExecutionRole.RUNTIME,
        model_id="runtime_replacement_vnext",
        replaces=("chemworld_reaction_network_lite",),
    )
    assert classify_adapter(diagnostic) is AdapterIntegrationClass.DIAGNOSTIC_ADDITION
    assert classify_adapter(addition) is AdapterIntegrationClass.RUNTIME_ADDITION
    assert classify_adapter(replacement) is AdapterIntegrationClass.RUNTIME_REPLACEMENT


def test_active_claim_stages_but_does_not_become_integration_ready(tmp_path: Path) -> None:
    _prepare(tmp_path)
    _claim(tmp_path, complete=False)
    path = _write(
        tmp_path,
        _manifest(
            role=ModelExecutionRole.RUNTIME,
            model_id="runtime_replacement_vnext",
            replaces=("chemworld_reaction_network_lite",),
        ),
    )
    report = build_vnext_integration_plan([path], repository_root=tmp_path)
    assert report["passed"] is True
    assert report["plan_integrity_passed"] is True
    assert report["planning_error_count"] == 0
    assert report["staged_count"] == 1
    assert report["integration_ready_count"] == 0
    assert report["pending_delivery_count"] == 1
    assert report["runtime_replacement_count"] == 1
    assert report["proposals"][0]["blockers"][0]["check_id"] == (
        "delivery_claim_incomplete"
    )
    assert report["proposals"][0]["readiness_blockers"]
    assert report["proposals"][0]["planning_errors"] == []


def test_cli_default_allows_pending_but_explicit_readiness_requirement_fails(
    tmp_path: Path,
) -> None:
    _prepare(tmp_path)
    _claim(tmp_path, complete=False)
    path = _write(
        tmp_path,
        _manifest(
            role=ModelExecutionRole.RUNTIME,
            model_id="runtime_addition_vnext",
        ),
    )
    output = tmp_path / "plan.json"
    command = [
        sys.executable,
        "scripts/build_vnext_integration_plan.py",
        str(path),
        "--root",
        str(tmp_path),
        "--manifest-dir",
        str(tmp_path / "no-discovery"),
        "--output",
        str(output),
    ]
    default = subprocess.run(command, check=False, capture_output=True, text=True)
    assert default.returncode == 0
    assert json.loads(output.read_text(encoding="utf-8"))["pending_delivery_count"] == 1

    required = subprocess.run(
        [*command, "--require-integration-ready"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert required.returncode == 1
    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["plan_integrity_passed"] is True
    assert report["requirement_errors"] == [
        "no completed adapter proposal is integration-ready"
    ]


def test_completed_runtime_replacement_is_ready_but_cannot_raise_maturity_yet(
    tmp_path: Path,
) -> None:
    _prepare(tmp_path)
    _claim(tmp_path, complete=True)
    path = _write(
        tmp_path,
        _manifest(
            role=ModelExecutionRole.RUNTIME,
            model_id="runtime_replacement_vnext",
            replaces=("chemworld_reaction_network_lite",),
        ),
    )
    report = build_vnext_integration_plan([path], repository_root=tmp_path)
    assert report["passed"] is True
    assert report["integration_ready_count"] == 1
    assert report["runtime_replacement_count"] == 1
    proposal = report["proposals"][0]
    assert proposal["runtime_maturity_upgrade_allowed"] is False
    assert proposal["can_remove_replaced_models"] is False
    assert report["v0_3_runtime_changed"] is False


def test_diagnostic_provider_cannot_claim_a_runtime_replacement(tmp_path: Path) -> None:
    _prepare(tmp_path)
    _claim(tmp_path, complete=True)
    path = _write(
        tmp_path,
        _manifest(
            role=ModelExecutionRole.DIAGNOSTIC,
            model_id="diagnostic_vnext",
            replaces=("chemworld_reaction_network_lite",),
        ),
    )
    report = build_vnext_integration_plan([path], repository_root=tmp_path)
    assert report["passed"] is False
    assert report["diagnostic_only_count"] == 1
    proposal = report["proposals"][0]
    assert proposal["runtime_maturity_effect"] == "none_on_runtime"
    assert proposal["blockers"][0]["check_id"] == "diagnostic_replacement_forbidden"
    assert proposal["readiness_blockers"] == []
    assert proposal["planning_errors"][0]["check_id"] == (
        "diagnostic_replacement_forbidden"
    )


def test_current_wf10_proposal_is_ready_diagnostic_evidence_only() -> None:
    root = Path(__file__).resolve().parents[1]
    path = (
        root
        / "workstreams"
        / "world_foundation"
        / "adapters"
        / "wf-10-rate-law-unit-contracts.json"
    )
    report = build_vnext_integration_plan([path], repository_root=root)
    assert report["passed"] is True
    assert report["integration_ready_count"] == 1
    assert report["diagnostic_only_count"] == 1
    assert report["runtime_replacement_count"] == 0
    assert report["runtime_maturity_upgrade_count"] == 0
    proposal = report["proposals"][0]
    assert proposal["provider_model_id"] == "chemworld_arrhenius_unit_contract_vnext"
    assert proposal["runtime_maturity_effect"] == "none_on_runtime"
