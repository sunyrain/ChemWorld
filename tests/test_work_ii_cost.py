from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

import chemworld.eval.work_ii_formal as work_ii_formal
from chemworld.eval.provenance import canonical_json_sha256
from chemworld.eval.work_ii_cost import (
    METHOD_QUALIFICATION_LOCAL_MANIFEST_VERSION,
    build_formal_cost_contract,
    build_formal_cost_ledger,
    build_qualification_cost_contract,
    build_qualification_cost_ledger,
    formal_cost_contract_sha256,
    validate_formal_cost_contract,
    validate_qualification_cost_contract,
    validate_qualification_cost_ledger,
)
from chemworld.eval.work_ii_formal import (
    authorize_formal_preflight,
    build_formal_preflight,
    validate_formal_preflight,
)

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "configs/benchmark/work_ii_formal_design_v0.1.json"
ANALYSIS = ROOT / "configs/benchmark/work_ii_analysis_plan_v0.1.json"


@pytest.fixture(autouse=True)
def _qualified_formal_prerequisites(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(work_ii_formal, "_validate_environment_binding", lambda *_: [])

    def ready_c2(_root, _plan, _design, cells):
        report = {
            "schema_version": "chemworld-work-ii-c2-admission-report-0.1",
            "status": "ready_for_formal_authorization",
            "formal_execution_allowed": True,
            "blocking_requirements": [],
            "evidence_validation_errors": [],
            "plan_binding": {
                "path": Path(_plan).resolve().relative_to(_root).as_posix(),
            },
            "blocks": {"A_E": {"public_schedule": {
                "public_schedule_cell_count": len(cells),
                "public_schedule_sha256": canonical_json_sha256(cells),
            }}},
        }
        report["admission_sha256"] = canonical_json_sha256(report)
        return report

    monkeypatch.setattr(work_ii_formal, "build_c2_admission_report", ready_c2)
    monkeypatch.setattr(work_ii_formal, "validate_c2_admission_report", lambda *_: [])


def _authorization_evidence(
    manifest: dict[str, object], contract: dict[str, object]
) -> dict[str, object]:
    base = manifest["preflight_sha256"]
    qualification = {
        "schema_version": "chemworld-work-ii-method-qualification-receipt-0.4",
        "status": "passed",
        "formal_execution_authorized": True,
        "formal_preflight_sha256": base,
    }
    qualification["receipt_sha256"] = canonical_json_sha256(qualification)
    freeze = {
        "schema_version": "chemworld-work-ii-preregistration-freeze-receipt-0.1",
        "status": "passed_final_freeze",
        "formal_execution_authorized": True,
        "bindings": {
            "formal_preflight_sha256": base,
            "method_qualification": {
                "receipt_sha256": qualification["receipt_sha256"]
            },
        },
        "formal_currency_budget": contract,
    }
    freeze["receipt_sha256"] = canonical_json_sha256(freeze)
    return {
        "qualification_receipt": qualification,
        "preregistration_freeze_receipt": freeze,
        "formal_cost_contract": contract,
    }


def _contract(*, ceiling: float = 20.0) -> tuple[dict[str, object], dict[str, object]]:
    manifest = build_formal_preflight(ROOT, DESIGN, ANALYSIS)
    contract = build_formal_cost_contract(
        ROOT,
        manifest,
        formal_currency_ceiling_usd=ceiling,
        pricing_source="https://api-docs.deepseek.com/quick_start/pricing",
        pricing_observed_at="2026-08-10T12:00:00+08:00",
        cache_hit_input_usd_per_million=0.0028,
        cache_miss_input_usd_per_million=0.14,
        output_usd_per_million=0.28,
    )
    return manifest, contract


def _local_qualification_manifest() -> dict[str, object]:
    formal = build_formal_preflight(ROOT, DESIGN, ANALYSIS)
    manifest: dict[str, object] = {
        "schema_version": METHOD_QUALIFICATION_LOCAL_MANIFEST_VERSION,
        "status": "passed",
        "formal_result": False,
        "formal_execution_authorized": False,
        "provider_contract": formal["provider_contract"],
        "method_qualification_contract": formal["method_qualification_contract"],
        "method_qualification_contract_sha256": formal[
            "method_qualification_contract_sha256"
        ],
        "task_bindings": formal["task_bindings"],
        "errors": [],
    }
    manifest["manifest_sha256"] = canonical_json_sha256(manifest)
    return manifest


def test_formal_cost_contract_covers_initial_and_all_resume_token_envelopes() -> None:
    manifest, contract = _contract()

    assert validate_formal_cost_contract(ROOT, manifest, contract) == []
    assert contract["initial_schedule"] == {
        "provider_attempt_count": 75,
        "token_caps": {
            "input_tokens": 324_000_000,
            "uncached_input_tokens": 43_200_000,
            "output_tokens": 3_240_000,
        },
        "cost_cap_usd": 7.74144,
    }
    assert contract["all_infrastructure_resumes"] == {
        "provider_attempt_count": 150,
        "token_caps": {
            "input_tokens": 648_000_000,
            "uncached_input_tokens": 86_400_000,
            "output_tokens": 6_480_000,
        },
        "cost_cap_usd": 15.48288,
    }
    assert contract["formal_currency_ceiling_usd"] == 20.0
    assert contract["currency_headroom_over_all_attempts_usd"] == 4.51712


def test_formal_cost_contract_rejects_ceiling_below_retry_hard_cap() -> None:
    with pytest.raises(ValueError, match="below the frozen all-attempt cost cap"):
        _contract(ceiling=15.0)


def test_qualification_cost_contract_and_attempt_ledger_cover_all_resumes() -> None:
    manifest = _local_qualification_manifest()
    contract = build_qualification_cost_contract(
        ROOT,
        manifest,
        qualification_currency_ceiling_usd=0.5,
        pricing_source="https://provider.example/pricing",
        pricing_observed_at="2026-08-10T12:00:00+08:00",
        cache_hit_input_usd_per_million=0.0028,
        cache_miss_input_usd_per_million=0.14,
        output_usd_per_million=0.28,
    )
    ledger = build_qualification_cost_ledger(
        manifest,
        contract,
        {"opaque": 2, "aligned_nominal": 2, "misindexed_nominal": 2},
    )

    assert validate_qualification_cost_contract(ROOT, manifest, contract) == []
    assert contract["initial_schedule"] == {
        "provider_attempt_count": 3,
        "token_caps": {
            "input_tokens": 7_200_000,
            "uncached_input_tokens": 960_000,
            "output_tokens": 72_000,
        },
        "cost_cap_usd": 0.172032,
    }
    assert contract["all_infrastructure_resumes"]["cost_cap_usd"] == 0.344064
    assert ledger["provider_attempt_count"] == 6
    assert ledger["reserved_cost_usd"] == 0.344064
    assert ledger["qualification_manifest_sha256"] == manifest["manifest_sha256"]
    assert validate_qualification_cost_ledger(manifest, contract, ledger) == []


def test_unlimited_qualification_cost_contract_keeps_token_and_attempt_caps() -> None:
    manifest = _local_qualification_manifest()
    reason = "provider contract exposes no attributable per-run USD price"
    contract = build_qualification_cost_contract(
        ROOT,
        manifest,
        qualification_currency_ceiling_usd=None,
        pricing_source="provider_pricing_unavailable",
        pricing_observed_at="2026-08-14T00:00:00+08:00",
        cache_hit_input_usd_per_million=None,
        cache_miss_input_usd_per_million=None,
        output_usd_per_million=None,
        unlimited_spend_authorized=True,
        pricing_unavailable_reason=reason,
    )
    ledger = build_qualification_cost_ledger(
        manifest,
        contract,
        {"opaque": 2, "aligned_nominal": 2, "misindexed_nominal": 2},
    )

    assert validate_qualification_cost_contract(ROOT, manifest, contract) == []
    assert contract["all_infrastructure_resumes"]["provider_attempt_count"] == 6
    assert contract["all_infrastructure_resumes"]["token_caps"] == {
        "input_tokens": 14_400_000,
        "uncached_input_tokens": 1_920_000,
        "output_tokens": 144_000,
    }
    assert contract["all_infrastructure_resumes"]["cost_cap_usd"] is None
    assert contract["qualification_currency_ceiling_usd"] is None
    assert contract["pricing"]["pricing_unavailable_reason"] == reason
    assert ledger["within_ceiling"] is None
    assert ledger["within_authorized_spend"] is True
    assert ledger["reserved_cost_usd"] is None
    assert validate_qualification_cost_ledger(manifest, contract, ledger) == []

    with pytest.raises(ValueError, match="attempt cap exceeded"):
        build_qualification_cost_ledger(
            manifest,
            contract,
            {"opaque": 3},
        )


def test_qualification_cost_rejects_formal_preflight_identity() -> None:
    formal = build_formal_preflight(ROOT, DESIGN, ANALYSIS)
    with pytest.raises(ValueError, match="requires the W2-27 local manifest"):
        build_qualification_cost_contract(
            ROOT,
            formal,
            qualification_currency_ceiling_usd=None,
            pricing_source="provider_pricing_unavailable",
            pricing_observed_at="2026-08-14T00:00:00+08:00",
            cache_hit_input_usd_per_million=None,
            cache_miss_input_usd_per_million=None,
            output_usd_per_million=None,
            unlimited_spend_authorized=True,
            pricing_unavailable_reason=(
                "provider contract exposes no attributable per-run USD price"
            ),
        )


def test_formal_cost_contract_rejects_rehashed_semantic_tampering() -> None:
    manifest, contract = _contract()
    tampered = deepcopy(contract)
    tampered["all_infrastructure_resumes"]["cost_cap_usd"] = 1.0
    tampered["formal_cost_contract_sha256"] = formal_cost_contract_sha256(tampered)

    assert (
        "Work II formal cost contract differs from deterministic rebuild"
        in validate_formal_cost_contract(ROOT, manifest, tampered)
    )


def test_incomplete_c2_schedule_cost_contract_cannot_authorize_runtime() -> None:
    base, contract = _contract()
    forged = deepcopy(base)
    forged["status"] = "passed_execution_authorized"
    forged["formal_execution_allowed"] = True
    forged["blocking_requirements"] = []
    forged["preflight_sha256"] = canonical_json_sha256(
        {key: value for key, value in forged.items() if key != "preflight_sha256"}
    )
    assert (
        "formal execution manifest lacks exact authorization bindings"
        in validate_formal_preflight(forged)
    )
    with pytest.raises(ValueError, match="unresolved prerequisite failures"):
        authorize_formal_preflight(
            base,
            **_authorization_evidence(base, contract),
        )
    first = base["cells"][0]
    ledger = build_formal_cost_ledger(
        base,
        contract,
        {first["cell_key_sha256"]: 1},
    )

    assert validate_formal_cost_contract(ROOT, base, contract) == []
    assert ledger["provider_attempt_count"] == 1
    assert ledger["reserved_cost_usd"] == 0.057344
    assert ledger["remaining_unreserved_usd"] == 19.942656
    assert ledger["within_ceiling"] is True
    assert ledger["formal_preflight_sha256"] == base["preflight_sha256"]

    with pytest.raises(ValueError, match="non-integer attempt count"):
        build_formal_cost_ledger(
            base,
            contract,
            {first["cell_key_sha256"]: 1.5},
        )
