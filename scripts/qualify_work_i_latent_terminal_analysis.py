"""Synthetically qualify the frozen Work I latent-terminal analyzer."""

from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from chemworld.eval.latent_terminal_analysis import (
    FROZEN_CONTRACT_SHA256,
    analyze_latent_terminal_population,
    finite_population_fraction,
    validate_latent_terminal_analysis,
)
from chemworld.eval.provenance import canonical_json_sha256, file_sha256

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "configs/benchmark/work_i_latent_terminal_contract_v0.1.json"
DEFAULT_JSON = (
    ROOT
    / "workstreams/arxiv_v1/reports/"
    "work-i-latent-terminal-analysis-qualification-v0.1.json"
)
DEFAULT_MARKDOWN = (
    ROOT
    / "workstreams/arxiv_v1/reports/"
    "work-i-latent-terminal-analysis-qualification-v0.1.md"
)
SOURCE_PATHS = (
    Path("configs/benchmark/work_i_latent_terminal_contract_v0.1.json"),
    Path("src/chemworld/eval/latent_terminal_analysis.py"),
    Path("scripts/qualify_work_i_latent_terminal_analysis.py"),
    Path("tests/test_latent_terminal_analysis.py"),
)


def _read_contract() -> dict[str, Any]:
    payload = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("latent-terminal contract must be an object")
    if payload.get("contract_sha256") != FROZEN_CONTRACT_SHA256:
        raise ValueError("qualification is not bound to the frozen L01 contract")
    return payload


def build_synthetic_receipts(contract: dict[str, Any]) -> list[dict[str, Any]]:
    """Create deterministic, visibly synthetic scores for all 36 frozen identities."""

    receipts: list[dict[str, Any]] = []
    population = contract["population"]
    for cell in population["cells"]:
        cell_number = int(str(cell["cell_id"]).split("-")[1])
        for unit in cell["discard_units"]:
            lifecycle = int(unit["lifecycle_index"])
            synthetic_score = ((cell_number * 17 + lifecycle * 23 + 11) % 101) / 100.0
            receipts.append(
                {
                    "contract_sha256": contract["contract_sha256"],
                    "population_manifest_sha256": population[
                        "population_manifest_sha256"
                    ],
                    "fixture_kind": "synthetic_qualification",
                    "discard_id": unit["discard_id"],
                    "cell_id": cell["cell_id"],
                    "world_seed": cell["world_seed"],
                    "information_arm": cell["information_arm"],
                    "lifecycle_index": unit["lifecycle_index"],
                    "terminal_step": unit["terminal_step"],
                    "public_prefix_sha256": unit["public_prefix_sha256"],
                    "terminal_action_sha256": unit["terminal_action_sha256"],
                    "outcome_status": "resolved",
                    "score": synthetic_score,
                    "synthetic_score_rule": (
                        "((cell_number*17 + lifecycle_index*23 + 11) mod 101)/100"
                    ),
                }
            )
    return receipts


def _analyze(contract: dict[str, Any], receipts: list[dict[str, Any]]) -> dict[str, Any]:
    return analyze_latent_terminal_population(
        contract,
        receipts,
        mode="synthetic_qualification",
    )


def _primary_threshold(analysis: dict[str, Any]) -> dict[str, Any]:
    return next(
        row
        for row in analysis["selection_and_threshold_sensitivity"]
        if row["primary"] is True
    )


def _absolute_threshold(analysis: dict[str, Any]) -> dict[str, Any]:
    return next(
        row
        for row in analysis["selection_and_threshold_sensitivity"]
        if row["threshold_id"] == "absolute_0.58"
    )


def _find_cell(contract: dict[str, Any], cell_id: str) -> dict[str, Any]:
    return next(cell for cell in contract["population"]["cells"] if cell["cell_id"] == cell_id)


def _case_record(
    case_id: str,
    analysis: dict[str, Any],
    checks: dict[str, bool],
    evidence: dict[str, Any],
) -> dict[str, Any]:
    validation_errors = validate_latent_terminal_analysis(analysis)
    combined = {"analysis_validator_passed": not validation_errors, **checks}
    return {
        "case_id": case_id,
        "passed": all(combined.values()),
        "checks": combined,
        "validation_errors": validation_errors,
        "analysis_sha256": analysis["analysis_sha256"],
        "evidence": evidence,
    }


def _source_manifest() -> dict[str, str]:
    result: dict[str, str] = {}
    for relative in SOURCE_PATHS:
        path = ROOT / relative
        if not path.is_file():
            raise ValueError(f"qualification source missing: {relative}")
        result[relative.as_posix()] = file_sha256(path)
    return result


def build_qualification_report() -> dict[str, Any]:
    """Build the deterministic synthetic qualification report."""

    contract = _read_contract()
    base_receipts = build_synthetic_receipts(contract)
    complete = _analyze(contract, base_receipts)
    estimand_ids = set(complete["estimands"])
    oracle_cells = complete["estimands"]["campaign_oracle_regret"]["cells"]
    complete_case = _case_record(
        "complete_synthetic_population",
        complete,
        {
            "all_36_resolved": complete["census"]["resolved_shadow_receipts"] == 36,
            "all_eight_estimands_present": len(estimand_ids) == 8,
            "four_registered_threshold_rows": (
                len(complete["selection_and_threshold_sensitivity"]) == 4
            ),
            "finite_population_micro_and_macro_present": all(
                "finite_population_micro"
                in complete["estimands"][estimand]["aggregation"]
                and "cell_macro_average"
                in complete["estimands"][estimand]["aggregation"]
                for estimand in (
                    "latent_terminal_score",
                    "discard_to_observed_best_delta",
                    "positive_discard_regret",
                )
            ),
            "oracle_has_nine_defined_cells": sum(
                row["opportunity"] for row in oracle_cells
            )
            == 9,
            "cell_02_oracle_is_null_not_zero": next(
                row for row in oracle_cells if row["cell_id"] == "cell-02"
            )["point_estimate"]
            is None,
            "no_complete_case_substitution": (
                complete["missingness_and_censoring"]["complete_case_primary_used"]
                is False
            ),
        },
        {
            "status": complete["status"],
            "estimand_ids": sorted(estimand_ids),
            "decision_time_null_count": complete["estimands"][
                "decision_time_discard_regret"
            ]["null_count"],
        },
    )

    equality_receipts = deepcopy(base_receipts)
    equality_id = equality_receipts[0]["discard_id"]
    equality_cell = _find_cell(contract, equality_receipts[0]["cell_id"])
    equality_receipts[0]["score"] = 0.90 * equality_cell[
        "campaign_best_assayed_score"
    ]
    equality = _analyze(contract, equality_receipts)
    equality_row = next(row for row in equality["unit_rows"] if row["discard_id"] == equality_id)
    equality_case = _case_record(
        "threshold_equality_is_near_best",
        equality,
        {
            "equality_classified_fn": equality_row["primary_classification"] == "FN",
            "comparator_is_inclusive": (
                _primary_threshold(equality)["positive_comparator"] == ">="
            ),
        },
        {
            "discard_id": equality_id,
            "score": equality_row["score"],
            "threshold": equality_row["primary_threshold"],
            "classification": equality_row["primary_classification"],
        },
    )

    missing = _analyze(contract, deepcopy(base_receipts[1:]))
    missing_case = _case_record(
        "missing_receipt_retains_fixed_denominator",
        missing,
        {
            "status_is_incomplete": missing["status"] == "incomplete_full_report_required",
            "one_unresolved": missing["census"]["unresolved_shadow_receipts"] == 1,
            "latent_point_withheld": (
                missing["estimands"]["latent_terminal_score"]["point_estimate_status"]
                == "withheld"
            ),
            "fixed_denominator_is_36": (
                missing["estimands"]["latent_terminal_score"]["denominator"] == 36
            ),
            "primary_selection_point_withheld": (
                _primary_threshold(missing)["strata"]["overall"]["point_table"] is None
            ),
        },
        {
            "unresolved_fraction": missing["missingness_and_censoring"][
                "unresolved_fraction"
            ],
            "bound_denominator": missing["estimands"]["latent_terminal_score"][
                "aggregation"
            ]["finite_population_micro"]["overall"]["bounds"]["fixed_denominator"],
        },
    )

    nonfinite_receipts = deepcopy(base_receipts)
    nonfinite_id = nonfinite_receipts[0]["discard_id"]
    nonfinite_receipts[0]["score"] = float("inf")
    nonfinite = _analyze(contract, nonfinite_receipts)
    nonfinite_row = next(
        row for row in nonfinite["unit_rows"] if row["discard_id"] == nonfinite_id
    )
    nonfinite_case = _case_record(
        "nonfinite_score_fails_closed",
        nonfinite,
        {
            "score_not_emitted": nonfinite_row["score"] is None,
            "registered_reason": nonfinite_row["unresolved_category"] == "nonfinite_score",
            "point_withheld": nonfinite["status"] == "incomplete_full_report_required",
        },
        {
            "discard_id": nonfinite_id,
            "outcome_status": nonfinite_row["outcome_status"],
            "reason": nonfinite_row["unresolved_reason"],
        },
    )

    zero_receipts = deepcopy(base_receipts)
    for receipt in zero_receipts:
        receipt["score"] = 0.0
    zero = _analyze(contract, zero_receipts)
    absolute_recall = _absolute_threshold(zero)["strata"]["overall"][
        "point_metrics"
    ]["assay_commitment_recall"]
    zero_case = _case_record(
        "zero_denominator_and_decision_null",
        zero,
        {
            "recall_zero_denominator_is_null": (
                absolute_recall == finite_population_fraction(0, 0)
            ),
            "decision_time_has_null_units": (
                zero["estimands"]["decision_time_discard_regret"]["null_count"] > 0
            ),
            "future_assay_not_imputed": (
                zero["estimands"]["decision_time_discard_regret"][
                    "future_assay_imputed"
                ]
                is False
            ),
        },
        {
            "absolute_recall": absolute_recall,
            "decision_time_null_ids": zero["estimands"][
                "decision_time_discard_regret"
            ]["null_discard_ids"],
        },
    )

    tampered_receipts = deepcopy(base_receipts)
    tampered_id = tampered_receipts[0]["discard_id"]
    tampered_receipts[0]["public_prefix_sha256"] = "0" * 64
    tampered = _analyze(contract, tampered_receipts)
    tampered_row = next(
        row for row in tampered["unit_rows"] if row["discard_id"] == tampered_id
    )
    tampered_case = _case_record(
        "tampered_binding_fails_closed",
        tampered,
        {
            "tampered_unit_unresolved": tampered_row["outcome_status"] == "unresolved",
            "identity_reason": tampered_row["unresolved_category"] == "identity",
            "binding_error_retained": (
                "public_prefix_sha256_mismatch" in tampered_row["binding_errors"]
            ),
            "score_ignored": tampered_row["score"] is None,
        },
        {
            "discard_id": tampered_id,
            "binding_errors": tampered_row["binding_errors"],
        },
    )

    imputed_receipts = deepcopy(base_receipts)
    imputed_id = imputed_receipts[0]["discard_id"]
    imputed_receipts[0].update(
        {
            "outcome_status": "unresolved",
            "failure_category": "evaluator",
            "failure_reason": "synthetic_evaluator_failure",
            "score": 0.99,
        }
    )
    imputed = _analyze(contract, imputed_receipts)
    imputed_row = next(
        row for row in imputed["unit_rows"] if row["discard_id"] == imputed_id
    )
    imputation_case = _case_record(
        "forbidden_imputation_is_ignored",
        imputed,
        {
            "unresolved_score_erased": imputed_row["score"] is None,
            "violation_recorded": (
                "forbidden_unresolved_score" in imputed_row["binding_errors"]
            ),
            "complete_case_not_used": (
                imputed["missingness_and_censoring"]["complete_case_primary_used"]
                is False
            ),
        },
        {
            "discard_id": imputed_id,
            "reason": imputed_row["unresolved_reason"],
            "binding_errors": imputed_row["binding_errors"],
        },
    )

    cases = [
        complete_case,
        equality_case,
        missing_case,
        nonfinite_case,
        zero_case,
        tampered_case,
        imputation_case,
    ]
    sources = _source_manifest()
    report: dict[str, Any] = {
        "schema_id": "chemworld.latent_terminal_analysis_qualification",
        "schema_version": "0.1.0",
        "report_id": "work-i-latent-terminal-analysis-synthetic-qualification-v0.1",
        "status": "qualified" if all(case["passed"] for case in cases) else "failed",
        "purpose": (
            "Qualify the frozen estimand, selection, aggregation, and missingness "
            "implementation using synthetic scores only."
        ),
        "evidence_bindings": {
            "latent_terminal_contract_sha256": contract["contract_sha256"],
            "population_manifest_sha256": contract["population"][
                "population_manifest_sha256"
            ],
            "source_manifest": sources,
            "source_manifest_sha256": canonical_json_sha256(sources),
        },
        "synthetic_fixture": {
            "receipt_count": len(base_receipts),
            "score_rule": (
                "((cell_number*17 + lifecycle_index*23 + 11) mod 101)/100"
            ),
            "formal_shadow_outcomes_accessed": False,
            "formal_shadow_evaluations_executed": 0,
            "agent_provider_calls": 0,
        },
        "qualification_cases": cases,
        "coverage": {
            "all_eight_frozen_estimands": True,
            "selection_table": True,
            "relative_thresholds": [0.8, 0.9, 1.0],
            "absolute_threshold": 0.58,
            "finite_population_micro_cell_macro_and_paired": True,
            "nine_cell_campaign_oracle_rule": True,
            "decision_time_null_rule": True,
            "all_registered_unresolved_bounds": True,
            "unresolved_counts_and_reasons_by_registered_strata": True,
            "all_zero_and_all_one_censoring_endpoints": True,
            "complete_case_primary_forbidden": True,
        },
        "scientific_boundary": {
            "synthetic_qualification_only": True,
            "formal_analysis_authorized": False,
            "shadow_branch_is_agent_choice": False,
            "counts_as_original_agent_experiment": False,
        },
    }
    report["report_sha256"] = _report_sha256(report)
    return report


def _report_sha256(payload: dict[str, Any]) -> str:
    candidate = dict(payload)
    candidate.pop("report_sha256", None)
    return canonical_json_sha256(candidate)


def build_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Work I Latent-Terminal Analysis Synthetic Qualification",
        "",
        f"Status: **{report['status']}**",
        "",
        f"Report SHA-256: `{report['report_sha256']}`",
        "",
        "## Boundary",
        "",
        "This qualification used 36 deterministic synthetic score receipts bound to "
        "the frozen L01 identities. It executed **0 formal shadow evaluations**, "
        "accessed **0 formal shadow outcomes**, and made **0 agent/provider calls**.",
        "",
        "It qualifies analysis code only. It is not a terminal-quality result and is "
        "never eligible for main-text scientific entry.",
        "",
        "## Qualification cases",
        "",
        "| Case | Result | Analysis SHA-256 |",
        "| --- | --- | --- |",
    ]
    for case in report["qualification_cases"]:
        result = "PASS" if case["passed"] else "FAIL"
        lines.append(
            f"| `{case['case_id']}` | **{result}** | `{case['analysis_sha256']}` |"
        )
    lines.extend(
        [
            "",
            "## Qualified surface",
            "",
            "- All eight L01-frozen estimands and their fixed denominators.",
            "- The 60-lifecycle TP/FP/FN/TN table with equality classified near-best.",
            "- Relative threshold rows at 0.80, 0.90 and 1.00, plus absolute 0.58.",
            "- Finite-population micro, cell-macro and descriptive paired-arm outputs.",
            "- The nine discard-opportunity-cell oracle; `cell-02` remains null.",
            "- Decision-time regret with pre-assay discards null and no future imputation.",
            "- Registered unresolved counts, all-zero/all-one endpoints and sharp bounds.",
            "- Fail-closed missing, non-finite, tampered-binding and imputation handling.",
            "",
            "Observed-only diagnostics never replace a registered point estimate. Any "
            "unresolved shadow receipt retains the frozen denominator and withholds all "
            "affected point estimates.",
            "",
            "## Evidence binding",
            "",
            "- Frozen contract: "
            f"`{report['evidence_bindings']['latent_terminal_contract_sha256']}`",
            "- Population manifest: "
            f"`{report['evidence_bindings']['population_manifest_sha256']}`",
            "- Source manifest: "
            f"`{report['evidence_bindings']['source_manifest_sha256']}`",
            "",
        ]
    )
    return "\n".join(lines)


def _json_text(payload: dict[str, Any]) -> str:
    return json.dumps(
        payload,
        ensure_ascii=False,
        allow_nan=False,
        indent=2,
        sort_keys=True,
    ) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json-output", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--markdown-output", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = build_qualification_report()
    if report["status"] != "qualified":
        raise SystemExit("latent-terminal analysis synthetic qualification failed")
    if report["report_sha256"] != _report_sha256(report):
        raise SystemExit("qualification report self-hash mismatch")
    json_text = _json_text(report)
    markdown_text = build_markdown(report)
    if args.check:
        if args.json_output.read_text(encoding="utf-8") != json_text:
            raise SystemExit("machine qualification differs from deterministic rebuild")
        if args.markdown_output.read_text(encoding="utf-8") != markdown_text:
            raise SystemExit("human qualification differs from deterministic rebuild")
    else:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(json_text, encoding="utf-8", newline="\n")
        args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
        args.markdown_output.write_text(
            markdown_text,
            encoding="utf-8",
            newline="\n",
        )
    print(
        json.dumps(
            {
                "status": report["status"],
                "report_sha256": report["report_sha256"],
                "qualification_case_count": len(report["qualification_cases"]),
                "formal_shadow_evaluations_executed": 0,
                "formal_shadow_outcomes_accessed": False,
                "check": bool(args.check),
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
