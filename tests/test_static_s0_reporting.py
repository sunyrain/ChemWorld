from __future__ import annotations

from pathlib import Path

import pytest

from chemworld.eval.static_s0_reporting import build_static_s0_reportable_results


def test_static_s0_report_uses_world_clusters_for_baseline_comparison() -> None:
    root = Path(__file__).resolve().parents[1]
    required_raw_report = (
        root
        / "runs/formal/"
        "static_scientific_optimization_s0_v041_single_stage_high_20_5seed_20260727/"
        "multiseed_report.json"
    )
    if not required_raw_report.exists():
        pytest.skip("raw formal S0 run reports are intentionally distributed separately")
    report = build_static_s0_reportable_results(root)

    assert report["formal_result"] is True
    assert report["benchmark_claim_allowed"] is False
    assert report["reporting_unit"] == "world_seed_cluster"
    assert report["combined_resources"] == {
        "formal_llm_world_cells": 10,
        "provider_call_count": 214,
        "provider_attempt_count": 222,
        "provider_reported_total_tokens": 2_589_950,
        "physical_experiment_count": 380,
        "all_replay_verified": True,
        "monetary_accounting_complete": False,
    }

    electro = report["tasks"]["electrochemical-conversion"]
    assert electro["best_classic_calibration"]["algorithm_id"] == "structured_rf_ei"
    assert electro["llm"]["blind_final_score"]["mean"] == pytest.approx(0.3902, abs=5e-5)
    assert electro["paired_llm_vs_best_classic"]["llm_world_win_count"] == 2
    assert electro["llm"]["positive_final_synthesis_gain_count"] == 0
    assert electro["llm"]["zero_final_synthesis_gain_count"] == 3
    assert electro["llm"]["negative_final_synthesis_gain_count"] == 2

    crystallization = report["tasks"]["reaction-to-crystallization"]
    assert (
        crystallization["best_classic_calibration"]["algorithm_id"]
        == "structured_gp_ei"
    )
    assert crystallization["llm"]["blind_final_score"]["mean"] == pytest.approx(
        0.4828944714
    )
    assert crystallization["paired_llm_vs_best_classic"]["llm_world_win_count"] == 0
    assert crystallization["llm"]["zero_final_synthesis_gain_count"] == 5
