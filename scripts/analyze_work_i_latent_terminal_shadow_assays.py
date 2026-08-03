"""Analyze the frozen W1-L05 receipts under the L01 missingness rules."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from collections.abc import Mapping
from copy import deepcopy
from pathlib import Path
from typing import Any, cast

from chemworld.eval.latent_terminal_analysis import (
    analyze_latent_terminal_population,
    latent_terminal_analysis_sha256,
    validate_latent_terminal_analysis,
)
from chemworld.eval.latent_terminal_contract import (
    latent_terminal_contract_sha256,
    validate_latent_terminal_contract,
)
from chemworld.eval.provenance import canonical_json_sha256, file_sha256

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = Path("configs/benchmark/work_i_latent_terminal_contract_v0.1.json")
L04_PATH = Path(
    "workstreams/arxiv_v1/reports/work-i-latent-terminal-analysis-qualification-v0.1.json"
)
L05_PREFLIGHT_PATH = Path(
    "workstreams/arxiv_v1/reports/work-i-latent-terminal-shadow-assay-preflight-v0.1.json"
)
L05_RESULT_PATH = Path(
    "workstreams/arxiv_v1/reports/work-i-latent-terminal-shadow-assays-v0.1.json"
)
OUTPUT_PATH = Path("workstreams/arxiv_v1/reports/work-i-latent-terminal-analysis-v0.1.json")
MARKDOWN_PATH = Path("workstreams/arxiv_v1/reports/work-i-latent-terminal-analysis-v0.1.md")
SOURCE_PATHS = (
    CONTRACT_PATH,
    L04_PATH,
    L05_PREFLIGHT_PATH,
    L05_RESULT_PATH,
    Path("src/chemworld/eval/latent_terminal_analysis.py"),
    Path("scripts/analyze_work_i_latent_terminal_shadow_assays.py"),
    Path("tests/test_work_i_latent_terminal_formal_analysis.py"),
)
EXPECTED_L04_SHA256 = "f2113e77d8b3bca66f80ddd1e88d48c87bc25443ab52c29129f4aca4271747be"
EXPECTED_L05_SHA256 = "bf76788777c7bf100c213ddc258f987adca8734cd545fa56d0bb7f4a598a4314"
EXPECTED_PREFLIGHT_SHA256 = "7dbbf824c4aa14be10c28b2a500a316b129fe5da92ef99f7c2612dbc3a296128"


def _read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected JSON object: {path}")
    return payload


def _without(payload: Mapping[str, Any], field: str) -> dict[str, Any]:
    result = deepcopy(dict(payload))
    result.pop(field, None)
    return result


def _embedded_hash(payload: Mapping[str, Any], field: str) -> str:
    return canonical_json_sha256(_without(payload, field))


def _source_manifest(root: Path) -> dict[str, str]:
    return {path.as_posix(): file_sha256(root / path) for path in SOURCE_PATHS}


def validate_formal_input(
    result: Mapping[str, Any],
    preflight: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []
    if (
        result.get("report_sha256") != EXPECTED_L05_SHA256
        or _embedded_hash(result, "report_sha256") != EXPECTED_L05_SHA256
    ):
        errors.append("L05 result identity mismatch")
    if (
        preflight.get("report_sha256") != EXPECTED_PREFLIGHT_SHA256
        or _embedded_hash(preflight, "report_sha256") != EXPECTED_PREFLIGHT_SHA256
    ):
        errors.append("L05 preflight identity mismatch")
    receipts = result.get("receipts")
    if not isinstance(receipts, list) or len(receipts) != 36:
        errors.append("L05 does not publish 36 receipts")
        receipts = []
    if len({row.get("discard_id") for row in receipts}) != len(receipts):
        errors.append("L05 receipt identities are not unique")
    if sum(row.get("outcome_status") == "resolved" for row in receipts) != 6:
        errors.append("L05 resolved census changed")
    if sum(row.get("outcome_status") == "unresolved" for row in receipts) != 30:
        errors.append("L05 unresolved census changed")
    counts = result.get("counting_rule")
    if not isinstance(counts, Mapping) or counts.get("agent_provider_calls") != 0:
        errors.append("L05 provider-call boundary changed")
    gates = result.get("gates")
    if not isinstance(gates, Mapping) or gates.get("raw_sources_unchanged") is not True:
        errors.append("L05 raw-source mutation gate failed")
    return errors


def _execution_gates(
    result: Mapping[str, Any],
    preflight: Mapping[str, Any],
) -> dict[str, Any]:
    receipts = cast(list[Mapping[str, Any]], result["receipts"])
    resolved = [row for row in receipts if row.get("outcome_status") == "resolved"]
    preflight_census = cast(Mapping[str, Any], preflight["census"])
    result_gates = cast(Mapping[str, Any], result["gates"])
    counts = cast(Mapping[str, Any], result["counting_rule"])
    return {
        "exact_prefix_reconstruction_count": preflight_census["reconstructable_discard_units"],
        "valid_shadow_score_count": len(resolved),
        "exact_same_identity_replay_count": sum(
            row.get("same_identity_replay", {}).get("passed") is True for row in resolved
        ),
        "agent_provider_calls": counts["agent_provider_calls"],
        "original_trajectory_mutated": not result_gates["raw_sources_unchanged"],
        "original_resource_ledger_mutated": not result_gates["original_resource_ledger_unmodified"],
    }


def build_analysis(root: Path) -> dict[str, Any]:
    contract = _read_json(root / CONTRACT_PATH)
    contract_errors = validate_latent_terminal_contract(contract, root=root)
    if contract_errors:
        raise ValueError("invalid L01 contract: " + "; ".join(contract_errors))
    if contract.get("contract_sha256") != latent_terminal_contract_sha256(contract):
        raise ValueError("L01 contract self-hash mismatch")
    l04 = _read_json(root / L04_PATH)
    if (
        l04.get("report_sha256") != EXPECTED_L04_SHA256
        or _embedded_hash(l04, "report_sha256") != EXPECTED_L04_SHA256
        or l04.get("status") != "qualified"
    ):
        raise ValueError("L04 analysis qualification identity mismatch")
    preflight = _read_json(root / L05_PREFLIGHT_PATH)
    result = _read_json(root / L05_RESULT_PATH)
    input_errors = validate_formal_input(result, preflight)
    if input_errors:
        raise ValueError("invalid L05 formal input: " + "; ".join(input_errors))
    receipts = cast(list[Mapping[str, Any]], result["receipts"])
    analysis = analyze_latent_terminal_population(
        contract,
        receipts,
        mode="formal_shadow_analysis",
        execution_gates=_execution_gates(result, preflight),
    )
    source_failures = Counter(
        (str(row.get("failure_category")), str(row.get("failure_reason")))
        for row in receipts
        if row.get("outcome_status") == "unresolved"
    )
    analysis["report_id"] = "work-i-latent-terminal-analysis-v0.1"
    analysis["evidence_bindings"].update(
        {
            "l04_qualification_report_sha256": EXPECTED_L04_SHA256,
            "l05_preflight_report_sha256": EXPECTED_PREFLIGHT_SHA256,
            "l05_formal_report_sha256": EXPECTED_L05_SHA256,
            "source_manifest": _source_manifest(root),
        }
    )
    analysis["formal_execution_failure"] = {
        "l05_status": result["status"],
        "resolved_receipts": 6,
        "unresolved_receipts": 30,
        "source_failure_counts": [
            {
                "failure_category": category,
                "failure_reason": reason,
                "count": count,
            }
            for (category, reason), count in sorted(source_failures.items())
        ],
        "raw_sources_unchanged": True,
        "formal_rerun_or_result_replacement_performed": False,
    }
    analysis["analysis_sha256"] = latent_terminal_analysis_sha256(analysis)
    return analysis


def _number(value: Any) -> str:
    if value is None:
        return "withheld"
    return f"{float(value):.6g}"


def _fraction_value(value: Mapping[str, Any]) -> str:
    point = value.get("value")
    if point is None:
        return f"null ({value.get('numerator')}/{value.get('denominator')})"
    return f"{float(point):.6g} ({value['numerator']}/{value['denominator']})"


def _fraction_bound(value: Mapping[str, Any]) -> str:
    return f"{_fraction_value(value['lower'])} to {_fraction_value(value['upper'])}"


def _mean_bound(estimand: Mapping[str, Any]) -> str:
    overall = estimand["aggregation"]["finite_population_micro"]["overall"]
    bound = overall["bounds"]["mean_and_order_statistic_bounds"]["mean"]
    return f"[{_number(bound['lower'])}, {_number(bound['upper'])}]"


def build_markdown(analysis: Mapping[str, Any]) -> str:
    census = cast(Mapping[str, Any], analysis["census"])
    estimands = cast(Mapping[str, Any], analysis["estimands"])
    missingness = cast(Mapping[str, Any], analysis["missingness_and_censoring"])
    lines = [
        "# Work I Latent-Terminal Formal Analysis",
        "",
        f"Status: **{analysis['status']}**",
        "",
        f"Analysis SHA-256: `{analysis['analysis_sha256']}`",
        "",
        "## Frozen result",
        "",
        f"The formal gate did not pass: {census['resolved_shadow_receipts']} of 36 "
        f"shadow receipts resolved and {census['unresolved_shadow_receipts']} remain "
        "unresolved. Terminal quality is therefore unresolved. All latent-dependent "
        "primary point estimates are withheld; the six resolved rows are retained only "
        "inside registered observed-only diagnostics and bounds.",
        "",
        "No formal assay was rerun or replaced. The analyzer made zero agent/provider "
        "calls and executed zero shadow evaluations.",
        "",
        "## Registered continuous bounds",
        "",
        "| Estimand | Fixed denominator | Primary point | Sharp mean bound |",
        "| --- | ---: | --- | --- |",
        "| Latent terminal score | 36 | withheld | "
        f"{_mean_bound(estimands['latent_terminal_score'])} |",
        "| Discard - observed-best delta | 36 | withheld | "
        f"{_mean_bound(estimands['discard_to_observed_best_delta'])} |",
        "| Positive discard regret | 36 | withheld | "
        f"{_mean_bound(estimands['positive_discard_regret'])} |",
        "| Decision-time discard regret | "
        f"{estimands['decision_time_discard_regret']['denominator']} | withheld | "
        f"{_mean_bound(estimands['decision_time_discard_regret'])} |",
        "",
    ]
    oracle = estimands["campaign_oracle_regret"]
    oracle_mean = oracle["bounds"]["mean_and_order_statistic_bounds"]["mean"]
    lines.extend(
        [
            "Campaign-oracle regret is also withheld over its nine opportunity cells; "
            f"its registered mean bound is [{_number(oracle_mean['lower'])}, "
            f"{_number(oracle_mean['upper'])}].",
            "",
            "## Threshold sensitivity",
            "",
            "All rows use the frozen 60-lifecycle population. Point tables are withheld.",
            "",
            "| Threshold | Primary | False-discard bound | Precision bound | Recall bound |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in analysis["selection_and_threshold_sensitivity"]:
        overall = row["strata"]["overall"]
        bounds = overall["bounds"]
        lines.append(
            f"| `{row['threshold_id']}` | {'yes' if row['primary'] else 'no'} | "
            f"{_fraction_bound(bounds['false_discard_fraction'])} | "
            f"{_fraction_bound(bounds['assay_commitment_precision'])} | "
            f"{_fraction_bound(bounds['assay_commitment_recall'])} |"
        )
    lines.extend(
        [
            "",
            "## Missingness and execution boundary",
            "",
            f"Unresolved fraction: {_fraction_value(missingness['unresolved_fraction'])}.",
            "",
            "The analyzer conservatively maps unregistered L05 exception-class labels "
            "to the registered evaluator category while retaining every literal failure "
            "reason in the 36-row machine report. The frozen L05 source artifacts were "
            "unchanged on disk, but its original-resource-ledger execution gate failed.",
            "",
            "This bounded result is not eligible for a main-text latent-terminal quality "
            "claim. It does not imply that discarding saved laboratory resources, that "
            "the shadow branch was agent-selected, or that either information arm is "
            "generally superior.",
            "",
        ]
    )
    return "\n".join(lines)


def validate_analysis(analysis: Mapping[str, Any], *, root: Path) -> list[str]:
    errors = validate_latent_terminal_analysis(analysis)
    if analysis.get("status") != "incomplete_full_report_required":
        errors.append("formal incomplete status changed")
    census = analysis.get("census")
    if not isinstance(census, Mapping) or (
        census.get("resolved_shadow_receipts") != 6
        or census.get("unresolved_shadow_receipts") != 30
    ):
        errors.append("formal 6/30 census changed")
    entry = analysis.get("entry_gate")
    if not isinstance(entry, Mapping) or entry.get("main_text_eligible") is not False:
        errors.append("failed formal result became main-text eligible")
    estimands = analysis.get("estimands")
    if isinstance(estimands, Mapping):
        forbidden_available = [
            name
            for name, payload in estimands.items()
            if name != "assay_commitment_precision"
            and isinstance(payload, Mapping)
            and payload.get("point_estimate_status") not in {"withheld", None}
        ]
        if forbidden_available:
            errors.append("latent-dependent primary point estimate was not withheld")
    bindings = analysis.get("evidence_bindings")
    if not isinstance(bindings, Mapping) or bindings.get("source_manifest") != _source_manifest(
        root
    ):
        errors.append("analysis source manifest is stale")
    return list(dict.fromkeys(errors))


def _json_text(payload: Mapping[str, Any]) -> str:
    return (
        json.dumps(
            payload,
            ensure_ascii=False,
            allow_nan=False,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    analysis = build_analysis(ROOT)
    errors = validate_analysis(analysis, root=ROOT)
    if errors:
        raise SystemExit("formal analysis invalid: " + "; ".join(errors))
    json_text = _json_text(analysis)
    markdown_text = build_markdown(analysis)
    if args.check:
        if (ROOT / OUTPUT_PATH).read_text(encoding="utf-8") != json_text:
            raise SystemExit("committed analysis differs from deterministic rebuild")
        if (ROOT / MARKDOWN_PATH).read_text(encoding="utf-8") != markdown_text:
            raise SystemExit("committed markdown differs from deterministic rebuild")
    else:
        (ROOT / OUTPUT_PATH).write_text(json_text, encoding="utf-8", newline="\n")
        (ROOT / MARKDOWN_PATH).write_text(
            markdown_text,
            encoding="utf-8",
            newline="\n",
        )
    print(
        json.dumps(
            {
                "status": analysis["status"],
                "analysis_sha256": analysis["analysis_sha256"],
                "resolved": analysis["census"]["resolved_shadow_receipts"],
                "unresolved": analysis["census"]["unresolved_shadow_receipts"],
                "main_text_eligible": analysis["entry_gate"]["main_text_eligible"],
                "check": bool(args.check),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
