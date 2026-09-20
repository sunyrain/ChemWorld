from __future__ import annotations

import pytest
import scripts.export_work_ii_eq_entity_reports_v0_2 as export


def test_public_guard_rejects_private_provider_fields() -> None:
    with pytest.raises(RuntimeError, match="private field"):
        export._assert_public({"nested": {"thread_id": "secret"}})


def test_eq_e_stage_contract_is_exactly_canonical() -> None:
    assert export.STAGES == ("K1", "Q", "K2")


def test_eq_e_macro_keeps_entity_and_scale_errors() -> None:
    row = {
        "prediction_evaluation": {
            "metrics": {
                metric: {
                    "mae_to_five_repeat_mean": 0.1,
                    "empirical_coverage80": 0.8,
                    "mean_width80": 0.2,
                    "mean_interval_score_alpha_0_2": 0.3,
                }
                for metric in export.METRICS
            },
            "entity_mapping": {
                "entity_contrast": [{"pairwise_contrast_mae": 0.04}],
                "same_concentration_scale_transfer": [{"scale_gap_mae": 0.02}],
            },
        }
    }

    macro = export._cell_macro(row)

    assert macro["entity_contrast_mae"] == pytest.approx(0.04)
    assert macro["scale_gap_mae"] == pytest.approx(0.02)
