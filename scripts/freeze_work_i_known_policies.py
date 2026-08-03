"""Freeze the Work I known-policy construct-validity controls."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from chemworld.eval.known_policy_contract import (
    build_known_policy_contract,
    known_policy_contract_sha256,
    validate_known_policy_contract,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_JSON = ROOT / "configs/benchmark/work_i_known_policy_contract_v0.1.json"
DEFAULT_MARKDOWN = (
    ROOT / "workstreams/arxiv_v1/reports/work-i-known-policy-contract-v0.1.md"
)


def build_artifact() -> dict[str, Any]:
    contract = build_known_policy_contract()
    errors = validate_known_policy_contract(contract)
    if errors:
        raise ValueError("invalid known-policy contract: " + "; ".join(errors))
    artifact = {**contract, "contract_sha256": known_policy_contract_sha256(contract)}
    return json.loads(json.dumps(artifact))


def build_markdown(artifact: dict[str, Any]) -> str:
    matrix = artifact["formal_matrix"]
    signatures = artifact["expected_profile_signatures"]
    exact = signatures["exact_by_policy"]
    lines = [
        "# Work I Known-Policy Construct-Validity Contract",
        "",
        f"Schema: `{artifact['schema_id']}@{artifact['schema_version']}`",
        "",
        f"Contract SHA-256: `{artifact['contract_sha256']}`",
        "",
        f"Bound profile contract SHA-256: `{artifact['depends_on']['profile_contract_sha256']}`",
        "",
        "## What these controls establish",
        "",
        artifact["purpose"]["primary_question"],
        "",
        "The three policies are **construct-validity positive controls**, not endpoint "
        "baselines. They deliberately differ in terminal commitment, evidence acquisition, "
        "and evidence-conditioned investment while making zero provider calls.",
        "",
        "They do not establish:",
        "",
    ]
    lines.extend(f"- {claim}." for claim in artifact["purpose"]["not_a_claim_about"])
    lines.extend(
        [
            "",
            "## Formal matrix",
            "",
            f"The formal matrix contains **{matrix['campaign_count']} campaigns** and "
            f"**{matrix['closed_lifecycle_count']} closed lifecycles**: "
            f"{len(matrix['world_seeds'])} worlds x {len(matrix['information_arms'])} "
            f"information arms x {len(matrix['policy_ids'])} policies x "
            f"{matrix['lifecycles_per_cell']} lifecycles. Provider calls: "
            f"**{matrix['provider_call_count']}**.",
            "",
            "All policies receive the same six cards in the same order. The material "
            "dossier is never read, so matched arms are an exact interface-and-pairing "
            "check rather than a material-information experiment.",
            "",
            "## Frozen policy grammar",
            "",
            "| Policy | Evidence | Terminal policy | Operations per lifecycle |",
            "| --- | --- | --- | ---: |",
            "| `assay_all` | none | terminate and final assay every vessel | 6 |",
            "| `start_then_discard` | none | discard immediately after vessel start | 2 |",
            "| `measure_then_threshold` | one UV-vis conversion signal | below "
            "threshold: discard; at/above: one additional electrolysis then final "
            "assay | 6 or 8 |",
            "",
            "## Six-probe schedule",
            "",
            "| Probe | Solvent | Electrolyte | Reagent (mol) | Potential (V) | "
            "Current (mA) | Probe (s) | Post-measure (s) |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for probe in artifact["probe_schedule"]["cards"]:
        lines.append(
            f"| `{probe['probe_id']}` | {probe['solvent']} | "
            f"{probe['electrolyte_profile']} | {probe['reagent_amount_mol']:.3f} | "
            f"{probe['potential_V']:.2f} | {probe['current_mA']:.1f} | "
            f"{probe['probe_duration_s']:.0f} | "
            f"{probe['post_measure_duration_s']:.0f} |"
        )
    lines.extend(
        [
            "",
            "## Exact signatures",
            "",
            "These identities are evaluated after the all-commit execution-validity gate: "
            + signatures["execution_validity_gate"],
            "",
            "| Metric | `assay_all` | `start_then_discard` | `measure_then_threshold` |",
            "| --- | ---: | ---: | ---: |",
        ]
    )
    metric_ids = (
        "closed_lifecycle_fraction",
        "assay_fraction",
        "discard_fraction",
        "measured_lifecycle_fraction",
        "nonfinal_instrument_uses_per_closed_lifecycle",
        "continued_after_measurement_fraction",
        "threshold_eligible_fraction",
        "threshold_decision_concordance",
        "attempted_operations_per_closed_lifecycle",
    )
    for metric_id in metric_ids:
        values = []
        for policy_id in ("assay_all", "start_then_discard", "measure_then_threshold"):
            value = exact[policy_id].get(metric_id, "see p algebra")
            values.append("null" if value is None else str(value))
        lines.append(
            f"| `{metric_id}` | {values[0]} | {values[1]} | {values[2]} |"
        )
    algebra = signatures["threshold_policy_algebra"]
    lines.extend(
        [
            "",
            "For the threshold policy, " + algebra["symbol"] + ". After the formal "
            f"non-degeneracy gate, `{algebra['domain_after_formal_non_degeneracy_gate']}`. "
            f"Its assay fraction is `{algebra['assay_fraction']}`, continued-investment "
            f"fraction is `{algebra['continued_after_measurement_fraction']}`, and attempted "
            "operations per lifecycle are "
            f"`{algebra['attempted_operations_per_closed_lifecycle']}`.",
            "",
            "## Preregistered partial orderings",
            "",
        ]
    )
    lines.extend(
        f"- `{ordering}`" for ordering in signatures["strict_partial_orderings_after_gate"]
    )
    lines.extend(
        [
            "",
            "No ordering is asserted for endpoint score, outcome-trajectory metrics, or "
            "cost/risk between `assay_all` and `measure_then_threshold`. Those quantities "
            "are not controlled policy identities.",
            "",
            "## Threshold firewall",
            "",
            artifact["threshold_qualification"]["selection_rule"],
            "",
            "Only independent qualification worlds may supply candidate signals. Formal "
            "world seeds 0-4 are forbidden for threshold selection. W1-V03 must freeze the "
            "value and source-manifest hash before implementation. If the resulting formal "
            "matrix does not contain both branches, the complete result remains published "
            "and the positive-control gate is marked unestablished; the threshold is never "
            "retuned on formal data.",
            "",
            "## Reliability",
            "",
            artifact["reliability"]["test_retest_rule"],
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
    artifact = build_artifact()
    json_text = json.dumps(artifact, indent=2, sort_keys=True) + "\n"
    markdown_text = build_markdown(artifact)
    if args.check:
        if args.json_output.read_text(encoding="utf-8") != json_text:
            raise SystemExit("machine known-policy contract does not match rebuild")
        if args.markdown_output.read_text(encoding="utf-8") != markdown_text:
            raise SystemExit("human known-policy contract does not match rebuild")
    else:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(json_text, encoding="utf-8")
        args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
        args.markdown_output.write_text(markdown_text, encoding="utf-8")
    print(
        json.dumps(
            {
                "campaign_count": artifact["formal_matrix"]["campaign_count"],
                "closed_lifecycle_count": artifact["formal_matrix"][
                    "closed_lifecycle_count"
                ],
                "contract_sha256": artifact["contract_sha256"],
                "policy_count": len(artifact["policies"]),
                "probe_count": len(artifact["probe_schedule"]["cards"]),
                "provider_call_count": artifact["formal_matrix"][
                    "provider_call_count"
                ],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
