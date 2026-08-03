from copy import deepcopy
from pathlib import Path

from scripts.analyze_work_i_latent_terminal_shadow_assays import (
    L05_PREFLIGHT_PATH,
    L05_RESULT_PATH,
    MARKDOWN_PATH,
    OUTPUT_PATH,
    _read_json,
    build_analysis,
    build_markdown,
    validate_analysis,
    validate_formal_input,
)

ROOT = Path(__file__).resolve().parents[1]


def test_formal_analysis_retains_all_units_and_withholds_primary() -> None:
    analysis = build_analysis(ROOT)
    assert validate_analysis(analysis, root=ROOT) == []
    assert analysis["status"] == "incomplete_full_report_required"
    assert analysis["census"]["resolved_shadow_receipts"] == 6
    assert analysis["census"]["unresolved_shadow_receipts"] == 30
    assert len(analysis["unit_rows"]) == 36
    assert len(analysis["selection_and_threshold_sensitivity"]) == 4
    assert analysis["entry_gate"]["main_text_eligible"] is False
    assert analysis["missingness_and_censoring"]["complete_case_primary_used"] is False


def test_all_latent_dependent_point_estimates_are_withheld() -> None:
    estimands = build_analysis(ROOT)["estimands"]
    for name in (
        "latent_terminal_score",
        "discard_to_observed_best_delta",
        "positive_discard_regret",
        "campaign_oracle_regret",
        "false_discard_fraction",
        "assay_commitment_recall",
        "decision_time_discard_regret",
    ):
        assert estimands[name]["point_estimate_status"] == "withheld"
    assert estimands["assay_commitment_precision"]["point_estimate_status"] == (
        "available_observed_exact"
    )
    assert (
        estimands["assay_commitment_precision"]["main_text_promotable_while_shadow_unresolved"]
        is False
    )


def test_formal_input_hash_and_census_tampering_fail_closed() -> None:
    result = _read_json(ROOT / L05_RESULT_PATH)
    preflight = _read_json(ROOT / L05_PREFLIGHT_PATH)
    assert validate_formal_input(result, preflight) == []
    tampered = deepcopy(result)
    tampered["receipts"].pop()
    errors = validate_formal_input(tampered, preflight)
    assert "L05 result identity mismatch" in errors
    assert "L05 does not publish 36 receipts" in errors


def test_committed_formal_reports_match_deterministic_rebuild() -> None:
    analysis = build_analysis(ROOT)
    assert _read_json(ROOT / OUTPUT_PATH) == analysis
    assert (ROOT / MARKDOWN_PATH).read_text(encoding="utf-8") == build_markdown(analysis)
