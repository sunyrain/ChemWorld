from __future__ import annotations

import pytest
import scripts.export_work_ii_eq_structural_reports_v0_3 as export


def test_public_guard_rejects_private_provider_fields() -> None:
    with pytest.raises(RuntimeError, match="private field"):
        export._assert_public({"nested": {"thread_id": "secret"}})


def test_recovery_summary_drops_base_paths() -> None:
    rows = export._recovery_summary(
        {
            "recoveries": [
                {
                    "attempt": 1,
                    "kind": "posttests",
                    "base_result": "private-provider/RESULT.json",
                    "resumed_stages": ["K1", "Q", "K2"],
                    "source_experiments_rerun": False,
                    "truth_revealed_to_agent": False,
                    "question_changed": False,
                    "model_changed": False,
                }
            ]
        }
    )

    assert rows[0]["source_experiments_rerun"] is False
    assert "base_result" not in rows[0]


def test_v03_stage_contract_is_exactly_canonical() -> None:
    assert export.STAGES == ("K1", "Q", "K2")

