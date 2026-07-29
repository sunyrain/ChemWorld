from __future__ import annotations

import json
from pathlib import Path

LEDGER = Path(
    "workstreams/flagship_tasks/reports/pre-arxiv-claim-evidence-ledger-v1.json"
)


def test_pre_arxiv_claim_ledger_separates_results_from_stronger_claims() -> None:
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    claims = {row["claim_id"]: row for row in ledger["claims"]}

    assert ledger["current_formal_evidence"]["formal_results_present"] is True
    assert ledger["current_formal_evidence"]["benchmark_claim_allowed"] is False
    assert claims["C02"]["status"] == "supported_descriptive_only"
    assert claims["C04"]["status"] == "contradicted_by_current_formal_result"
    assert claims["C06"]["status"] == "not_supported"
    assert claims["C11"]["status"] == "supported_internal_exact_replay"
    assert (
        claims["C12"]["status"]
        == "supported_for_electrochemical_inconclusive_for_crystallization"
    )
    assert (
        claims["C13"]["status"]
        == "not_supported_by_preregistered_joint_recovery_rule"
    )
    assert (
        ledger["current_formal_evidence"][
            "material_information_all_sixty_cells_exact_replay_verified"
        ]
        is True
    )

    decision = ledger["first_arxiv_decision"]
    assert (
        decision[
            "narrow_descriptive_submission_can_proceed_without_new_scientific_experiments"
        ]
        is True
    )
    assert decision["experiments_required_before_any_stronger_claim"]
