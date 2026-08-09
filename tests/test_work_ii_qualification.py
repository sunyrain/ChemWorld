from __future__ import annotations

import json
from pathlib import Path

from chemworld.eval.provenance import canonical_json_sha256, file_sha256
from chemworld.eval.work_ii_formal import build_formal_preflight
from chemworld.eval.work_ii_qualification import (
    METHOD_QUALIFICATION_RECEIPT_VERSION,
    qualification_receipt_sha256,
    validate_method_qualification_receipt,
)

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "configs/benchmark/work_ii_formal_design_v0.1.json"
ANALYSIS = ROOT / "configs/benchmark/work_ii_analysis_plan_v0.1.json"


def _receipt(tmp_path: Path) -> tuple[dict[str, object], dict[str, object]]:
    manifest = build_formal_preflight(ROOT, DESIGN, ANALYSIS)
    report = tmp_path / "qualification-report.json"
    report.write_text(json.dumps({"status": "passed"}), encoding="utf-8")
    receipt: dict[str, object] = {
        "schema_version": METHOD_QUALIFICATION_RECEIPT_VERSION,
        "status": "passed",
        "formal_execution_authorized": True,
        "formal_preflight_sha256": manifest["preflight_sha256"],
        "provider_contract_sha256": canonical_json_sha256(manifest["provider_contract"]),
        "provider_attempt_contract_sha256": canonical_json_sha256(
            manifest["provider_attempt_contract"]
        ),
        "blind_evaluator_contract_sha256": canonical_json_sha256(
            manifest["blind_evaluator_contract"]
        ),
        "qualification_split": "development_seed_0",
        "qualified_prior_arms": [
            "opaque",
            "aligned_nominal",
            "misindexed_nominal",
        ],
        "qualified_cell_count": 3,
        "formal_participant_outcome_count_before_authorization": 0,
        "approved_provider_attempt_hard_cap": manifest["expected_counts"][
            "provider_attempts_hard_cap"
        ],
        "approved_currency_ceiling_usd": 50.0,
        "currency_approval": {
            "approved_by": "user",
            "approved_at": "2026-08-09T00:00:00+08:00",
            "approved_currency_ceiling_usd": 50.0,
            "scope_preflight_sha256": manifest["preflight_sha256"],
        },
        "qualification_report_binding": {
            "path": report.name,
            "sha256": file_sha256(report),
        },
    }
    receipt["receipt_sha256"] = qualification_receipt_sha256(receipt)
    return receipt, manifest


def test_method_qualification_receipt_is_self_hashed_and_cost_bound(tmp_path: Path) -> None:
    receipt, manifest = _receipt(tmp_path)
    assert (
        validate_method_qualification_receipt(
            tmp_path,
            receipt,
            manifest,
            currency_ceiling_usd=50.0,
        )
        == []
    )
    receipt["approved_currency_ceiling_usd"] = 51.0
    errors = validate_method_qualification_receipt(
        tmp_path,
        receipt,
        manifest,
        currency_ceiling_usd=51.0,
    )
    assert "method qualification receipt self-hash mismatch" in errors
    assert "method qualification receipt has invalid user currency approval" in errors
