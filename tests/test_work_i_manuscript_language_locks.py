from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest
from scripts.audit_work_i_manuscript_language_locks import (
    G2_COMPARISON_PATH,
    REPORT_JSON_PATH,
    REPORT_MD_PATH,
    ManuscriptLanguageLockError,
    _read_json,
    _validate_g2_evidence,
    build_markdown_report,
    receipt_sha256,
)

ROOT = Path(__file__).resolve().parents[1]


def _receipt() -> dict[str, object]:
    return _read_json(ROOT / REPORT_JSON_PATH)


def test_committed_audit_is_self_hashed_and_frozen() -> None:
    receipt = _receipt()
    assert receipt["receipt_sha256"] == receipt_sha256(receipt)
    assert (ROOT / REPORT_MD_PATH).read_text(encoding="utf-8") == build_markdown_report(receipt)


def test_frozen_counts_and_sensitivity_roles_are_preserved() -> None:
    receipt = _receipt()
    assert receipt["frozen_counting_evidence"] == {
        "closed_lifecycles": 120,
        "distinct_complete_agent_systems": 2,
        "explicit_discards": 36,
        "final_assays": 84,
        "system_partition": {
            "codex": {"assays": 60, "closed": 60, "discards": 0},
            "deepseek": {"assays": 24, "closed": 60, "discards": 36},
        },
    }
    contract = receipt["frozen_figure_and_sensitivity_contract"]
    assert contract["two_of_eight_role"] == "endpoint_diagnostic"
    assert contract["six_of_eight_role"] == "threshold_sensitive_supporting_evidence"
    assert contract["fresh_complete_pairs"] == 8
    assert contract["selected_worlds"] == 2


def test_current_manuscript_findings_are_complete_and_line_addressed() -> None:
    receipt = _receipt()
    assert receipt["status"] == "integration_changes_required"
    audit = receipt["current_manuscript_audit"]
    assert audit["figure_first_references"]["observed_sequence"] == [1, 6, 3, 4, 5]
    assert audit["figure_first_references"]["expected_sequence"] == [1, 2, 3, 4, 5, 6]
    assert audit["counting_lock"]["first_120_line"] == 28
    assert audit["counting_lock"]["explicit_84_lines"] == []
    assert audit["sensitivity_lock"]["passed"] is True
    finding_ids = {row["finding_id"] for row in audit["findings"]}
    assert finding_ids == {
        "FIGURE_FIRST_REFERENCE_ORDER",
        "FIRST_120_COUNT_LOCK",
        "TERMINOLOGY_ARBITRARY_RECOMBINATION",
        "TERMINOLOGY_CLOSED_VESSELS",
        "TERMINOLOGY_INDEPENDENTLY_CONFIGURED",
    }
    assert all(row["lines"] for row in audit["findings"])
    assert receipt["write_boundary"]["manuscript_edited"] is False


def test_g2_or_receipt_tampering_fails_closed() -> None:
    g2 = _read_json(ROOT / G2_COMPARISON_PATH)
    g2["systems"]["deepseek_v4_flash_direct"]["discarded_batch_count"] = 35
    with pytest.raises(ManuscriptLanguageLockError, match="self-hash mismatch"):
        _validate_g2_evidence(g2)

    receipt = deepcopy(_receipt())
    receipt["claim_boundary"]["six_of_eight_promoted_to_primary_result"] = True
    assert receipt["receipt_sha256"] != receipt_sha256(receipt)
