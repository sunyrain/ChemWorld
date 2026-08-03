"""Freeze the Work I discarded-state latent-terminal estimand contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from chemworld.eval.latent_terminal_contract import (
    build_latent_terminal_contract,
    validate_latent_terminal_contract,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_JSON = ROOT / "configs/benchmark/work_i_latent_terminal_contract_v0.1.json"
DEFAULT_MARKDOWN = (
    ROOT
    / "workstreams/arxiv_v1/reports/"
    "work-i-latent-terminal-contract-v0.1.md"
)


def _json_text(payload: dict[str, Any]) -> str:
    return json.dumps(
        payload,
        ensure_ascii=False,
        allow_nan=False,
        indent=2,
        sort_keys=True,
    ) + "\n"


def build_markdown(contract: dict[str, Any]) -> str:
    population = contract["population"]
    counts = population["counts"]
    reference = contract["quality_reference"]
    lines = [
        "# Work I Discarded-State Latent-Terminal Contract",
        "",
        "Status: **frozen before shadow outcomes**",
        "",
        f"Contract SHA-256: `{contract['contract_sha256']}`",
        "",
        "## Scientific question",
        "",
        contract["purpose"]["question"],
        "",
        "This is a finite-population, evaluator-only counterfactual audit of the "
        "terminal decisions already present in the frozen DeepSeek G2 v0.6 "
        "complete-system demonstration. It is not a model leaderboard.",
        "",
        "## Frozen population",
        "",
        f"The census contains **{counts['closed_lifecycles']} original lifecycles** "
        f"across **{counts['cells']} campaign cells**: "
        f"**{counts['observed_assays']} observed assays + "
        f"{counts['observed_discards']} committed discards**. Exactly "
        f"{counts['shadow_evaluations_planned']} evaluator-only shadow terminal "
        "evaluations are planned; they make zero agent/provider calls.",
        "",
        "| Cell | World | Information arm | Assays | Discards | Observed best | "
        "Terminal sequence |",
        "| --- | ---: | --- | ---: | ---: | ---: | --- |",
    ]
    for cell in population["cells"]:
        sequence = " ".join(
            "A" if item == "assay" else "D"
            for item in cell["terminal_sequence"]
        )
        lines.append(
            f"| `{cell['cell_id']}` | {cell['world_seed']} | "
            f"`{cell['information_arm']}` | {cell['observed_assay_count']} | "
            f"{cell['observed_discard_count']} | "
            f"{cell['campaign_best_assayed_score']:.6f} | `{sequence}` |"
        )
    lines.extend(
        [
            "",
            "Each discard unit is already enumerated by cell, lifecycle, terminal "
            "step, terminal-action hash, public-prefix hash, compact trajectory hash, "
            "and raw source-trajectory hash. No hidden state or latent score was read "
            "while constructing this contract.",
            "",
            "## Counterfactual terminal rule",
            "",
            contract["counterfactual_terminal_rule"]["branch_origin"],
            "",
            contract["counterfactual_terminal_rule"]["intervention"],
            "",
            "The evaluation is read-only with respect to the original campaign. It "
            "may bypass only the agent-facing workflow-readiness gate needed to expose "
            "the frozen final-assay evaluator; it may not advance chemistry, add "
            "material, repair state, or mutate the original resource ledger. Prefix "
            "actions, observations, keyed-noise receipts, hidden state, resource state, "
            "and ordinals must match exactly.",
            "",
            "## Primary quality reference",
            "",
            f"For campaign `c`, `B_c` is the best score among that campaign's original "
            f"assay decisions. The primary near-best threshold is "
            f"**`q_c = {reference['primary_near_best_fraction']:.2f} B_c`**, using the "
            "pre-existing Work I retention fraction. Equality counts as near-best. "
            f"The registered absolute task threshold "
            f"`{reference['registered_absolute_threshold']:.2f}` is sensitivity-only.",
            "",
            "## Frozen estimands",
            "",
            "| Estimand | Role | Unit | Formula | Denominator |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for estimand in contract["estimands"]:
        lines.append(
            f"| `{estimand['estimand_id']}` | `{estimand['role']}` | "
            f"{estimand['unit']} | `{estimand['formula']}` | "
            f"{estimand['denominator']} |"
        )
    lines.extend(
        [
            "",
            "The 60-lifecycle selection table is defined as: TP = assayed and "
            "near-best; FP = assayed and below threshold; FN = discarded with a "
            "near-best shadow score; TN = discarded below threshold. Thus the primary "
            "false-discard fraction is `FN/(FN+TN)`, assay commitment precision is "
            "`TP/(TP+FP)`, and commitment recall is `TP/(TP+FN)`.",
            "",
            "## Aggregation and sensitivity",
            "",
            "- Primary quantities describe the complete frozen finite population; "
            "super-population p-values or confidence intervals are not primary.",
            "- Lifecycle-level micro estimates are reported overall and by arm. "
            "Cell-level macro summaries and paired arm contrasts are separate and "
            "never replace the census estimate.",
            "- Continuous score, signed delta, positive regret, and campaign oracle "
            "regret distributions are mandatory.",
            "- Relative threshold sensitivities at `0.80`, `0.90`, and `1.00` times "
            "the observed campaign best, the registered absolute threshold, and the "
            "decision-time incumbent analysis are all mandatory.",
            "- A discard before any assay has null decision-time regret; a future assay "
            "is never imputed as a past incumbent.",
            "",
            "## Missingness and fail-closed behavior",
            "",
            "All 36 shadow evaluations are required for primary point estimates. A "
            "non-finite score, prefix mismatch, or evaluator failure is retained as an "
            "unresolved receipt: no complete-case substitution, clamping, semantic "
            "repair, or favorable rerun is allowed. The full report must then provide "
            "sharp missing-outcome bounds and remain incomplete.",
            "",
            "## Evidence-entry rule",
            "",
            "The complete 36-row audit, all gates, continuous summaries, selection "
            "tables, sensitivity rows, and failure receipts are published regardless "
            "of direction. Main-text quantitative claims require 36/36 exact prefix "
            "reconstructions, 36/36 valid scores, 36/36 exact shadow replays, zero "
            "agent/provider calls, and no mutation of original trajectories or ledgers. "
            "There is no result-direction, significance, arm-difference, or post-outcome "
            "threshold gate.",
            "",
            "## Claim boundary",
            "",
            "Allowed:",
            "",
        ]
    )
    lines.extend(f"- {item}." for item in contract["claim_boundary"]["allowed"])
    lines.extend(["", "Not allowed:", ""])
    lines.extend(f"- {item}." for item in contract["claim_boundary"]["forbidden"])
    lines.extend(
        [
            "",
            "## Frozen evidence",
            "",
            f"- Campaign audit: `{contract['evidence_bindings']['campaign_audit_sha256']}`",
            f"- Matrix manifest: `{contract['evidence_bindings']['matrix_manifest_sha256']}`",
            f"- Public archive: `{contract['evidence_bindings']['public_archive_sha256']}`",
            f"- Terminal index: `{contract['evidence_bindings']['terminal_file_index_sha256']}`",
            f"- Population manifest: `{population['population_manifest_sha256']}`",
            f"- Source manifest: `{contract['evidence_bindings']['source_manifest_sha256']}`",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json-output", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--markdown-output", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    contract = build_latent_terminal_contract(ROOT)
    errors = validate_latent_terminal_contract(contract, root=ROOT)
    if errors:
        raise SystemExit("latent-terminal contract invalid: " + "; ".join(errors))
    json_text = _json_text(contract)
    markdown_text = build_markdown(contract)
    if args.check:
        if args.json_output.read_text(encoding="utf-8") != json_text:
            raise SystemExit("machine contract differs from deterministic rebuild")
        if args.markdown_output.read_text(encoding="utf-8") != markdown_text:
            raise SystemExit("human contract differs from deterministic rebuild")
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
                "status": "frozen_before_shadow_outcomes",
                "contract_sha256": contract["contract_sha256"],
                "population_manifest_sha256": contract["population"][
                    "population_manifest_sha256"
                ],
                "cells": contract["population"]["counts"]["cells"],
                "observed_assays": contract["population"]["counts"][
                    "observed_assays"
                ],
                "observed_discards": contract["population"]["counts"][
                    "observed_discards"
                ],
                "shadow_evaluations_executed": 0,
                "latent_outcomes_accessed": False,
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
