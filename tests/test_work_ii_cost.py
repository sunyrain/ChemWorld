from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from chemworld.eval.provenance import canonical_json_sha256
from chemworld.eval.work_ii_cost import (
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
    manifest = build_formal_preflight(ROOT, DESIGN, ANALYSIS)
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
    assert validate_qualification_cost_ledger(manifest, contract, ledger) == []


def test_formal_cost_contract_rejects_rehashed_semantic_tampering() -> None:
    manifest, contract = _contract()
    tampered = deepcopy(contract)
    tampered["all_infrastructure_resumes"]["cost_cap_usd"] = 1.0
    tampered["formal_cost_contract_sha256"] = formal_cost_contract_sha256(tampered)

    assert (
        "Work II formal cost contract differs from deterministic rebuild"
        in validate_formal_cost_contract(ROOT, manifest, tampered)
    )


def test_formal_cost_reservations_survive_runtime_manifest_authorization() -> None:
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
    authorized = authorize_formal_preflight(
        base,
        qualification_receipt_sha256="a" * 64,
        preregistration_freeze_receipt_sha256="b" * 64,
        formal_cost_contract_sha256=contract["formal_cost_contract_sha256"],
    )
    first = authorized["cells"][0]
    ledger = build_formal_cost_ledger(
        authorized,
        contract,
        {first["cell_key_sha256"]: 1},
    )

    assert validate_formal_cost_contract(ROOT, authorized, contract) == []
    assert ledger["provider_attempt_count"] == 1
    assert ledger["reserved_cost_usd"] == 0.057344
    assert ledger["remaining_unreserved_usd"] == 19.942656
    assert ledger["within_ceiling"] is True
    assert ledger["formal_preflight_sha256"] == base["preflight_sha256"]

    with pytest.raises(ValueError, match="non-integer attempt count"):
        build_formal_cost_ledger(
            authorized,
            contract,
            {first["cell_key_sha256"]: 1.5},
        )
