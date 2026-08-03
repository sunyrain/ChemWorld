"""Execute and freeze the Work I known-policy threshold qualification."""

from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path
from typing import Any

from chemworld.eval.known_policy_threshold import (
    build_qualification_report,
    build_threshold_binding,
    validate_qualification_report,
    validate_threshold_binding,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT = (
    ROOT
    / "workstreams/arxiv_v1/reports/"
    "work-i-known-policy-threshold-qualification-v0.1.json"
)
DEFAULT_BINDING = ROOT / "configs/benchmark/work_i_known_policy_threshold_v0.1.json"
DEFAULT_MARKDOWN = (
    ROOT
    / "workstreams/arxiv_v1/reports/"
    "work-i-known-policy-threshold-qualification-v0.1.md"
)


def build_markdown(report: dict[str, Any], binding: dict[str, Any]) -> str:
    selection = report["selection"]
    signals = [
        float(signal["conversion"])
        for campaign in report["original_campaigns"]
        for signal in campaign["signals"]
    ]
    lines = [
        "# Work I Known-Policy Threshold Qualification",
        "",
        f"Status: **{report['status']}**",
        "",
        f"Qualification report SHA-256: `{report['report_sha256']}`",
        "",
        f"Threshold binding SHA-256: `{binding['binding_sha256']}`",
        "",
        "## Frozen result",
        "",
        f"The public UV-vis conversion threshold is **{binding['threshold']:.17g}**. "
        f"The comparator is `{binding['comparator']}`: values at or above the "
        "threshold take one further electrolysis step and proceed to final assay; "
        "values below it are discarded.",
        "",
        "This value was selected only from qualification world seeds "
        f"{report['qualification_world_seeds']}. Formal seeds "
        f"{report['formal_world_seeds_excluded']} were not executed or inspected by "
        "this qualification and cannot be used for retuning.",
        "",
        "## Selection",
        "",
        f"- Original qualification signals: {report['counts']['original_signals']}",
        f"- Unique signal values: {selection['unique_signal_count']}",
        f"- Midpoint candidates: {selection['candidate_count']}",
        f"- Admissible candidates: {selection['admissible_candidate_count']}",
        f"- Pooled median: {selection['pooled_median']:.17g}",
        f"- Selected threshold: {selection['selected_threshold']:.17g}",
        f"- Signal range: {min(signals):.17g} to {max(signals):.17g}",
        f"- Signal median: {statistics.median(signals):.17g}",
        "",
        "| Information arm | Discard branch | Continue-and-assay branch |",
        "| --- | ---: | ---: |",
    ]
    for arm in report["information_arms"]:
        counts = selection["selected_branch_counts_by_arm"][arm]
        lines.append(
            f"| `{arm}` | {counts['discard']} | {counts['continue_and_assay']} |"
        )
    lines.extend(
        [
            "",
            "## Qualification-world signals",
            "",
            "The paired arms must have identical vectors because the policies do not "
            "read the material dossier and the paired worlds share keyed-noise "
            "coordinates.",
            "",
            "| World | Opaque conversion vector | Nominal conversion vector | Match |",
            "| ---: | --- | --- | --- |",
        ]
    )
    by_cell = {
        (int(campaign["world_seed"]), str(campaign["information_arm"])): campaign
        for campaign in report["original_campaigns"]
    }
    arms = report["information_arms"]
    for world_seed in report["qualification_world_seeds"]:
        vectors = []
        for arm in arms:
            campaign = by_cell[(world_seed, arm)]
            vectors.append(
                "["
                + ", ".join(
                    f"{float(item['conversion']):.6f}"
                    for item in campaign["signals"]
                )
                + "]"
            )
        audit = report["matched_arm_audit"][f"seed-{world_seed}"]
        lines.append(
            f"| {world_seed} | `{vectors[0]}` | `{vectors[1]}` | "
            f"{all(audit.values())} |"
        )
    lines.extend(
        [
            "",
            "## Gates and provenance",
            "",
            "| Gate | Pass |",
            "| --- | --- |",
        ]
    )
    for gate in sorted(report["checks"]):
        passed = report["checks"][gate]
        lines.append(f"| `{gate}` | {passed} |")
    lines.extend(
        [
            "",
            f"The source manifest contains {len(report['source_manifest'])} files and "
            f"has SHA-256 `{report['source_manifest_sha256']}`. Execution comprised "
            f"{report['counts']['original_campaigns']} original campaigns plus "
            f"{report['counts']['replay_campaigns']} exact replays, "
            f"{report['counts']['original_actions'] + report['counts']['replay_actions']} "
            "committed actions, and zero provider calls.",
            "",
            "State/resource evidence is canonically serialized to "
            f"{report['artifact_float_canonicalization']['significant_digits']} "
            "significant digits with absolute residuals below "
            f"{report['artifact_float_canonicalization']['absolute_zero_tolerance']:.0e} "
            "mapped to zero; raw public diagnostic values remain the input to "
            "threshold selection.",
            "",
            "## Claim boundary",
            "",
            report["claim_boundary"],
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
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--binding-output", type=Path, default=DEFAULT_BINDING)
    parser.add_argument("--markdown-output", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = build_qualification_report(ROOT)
    report_errors = validate_qualification_report(report)
    if report_errors:
        raise SystemExit("qualification failed: " + "; ".join(report_errors))
    binding = build_threshold_binding(report)
    binding_errors = validate_threshold_binding(binding, report)
    if binding_errors:
        raise SystemExit("binding failed: " + "; ".join(binding_errors))
    report_text = _json_text(report)
    binding_text = _json_text(binding)
    markdown_text = build_markdown(report, binding)
    if args.check:
        if args.report_output.read_text(encoding="utf-8") != report_text:
            raise SystemExit("qualification report does not match deterministic rebuild")
        if args.binding_output.read_text(encoding="utf-8") != binding_text:
            raise SystemExit("threshold binding does not match deterministic rebuild")
        if args.markdown_output.read_text(encoding="utf-8") != markdown_text:
            raise SystemExit("qualification markdown does not match deterministic rebuild")
    else:
        for path, text in (
            (args.report_output, report_text),
            (args.binding_output, binding_text),
            (args.markdown_output, markdown_text),
        ):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8", newline="\n")
    print(
        json.dumps(
            {
                "binding_sha256": binding["binding_sha256"],
                "checks_passed": sum(report["checks"].values()),
                "checks_total": len(report["checks"]),
                "provider_call_count": report["counts"]["provider_calls"],
                "qualification_report_sha256": report["report_sha256"],
                "status": report["status"],
                "threshold": binding["threshold"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
