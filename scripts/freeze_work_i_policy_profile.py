"""Freeze the Work I experimental-agency profile contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from chemworld.eval.policy_validity_contract import (
    build_profile_contract,
    profile_contract_sha256,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_JSON = (
    ROOT / "configs/benchmark/work_i_policy_profile_contract_v0.1.json"
)
DEFAULT_MARKDOWN = (
    ROOT
    / "workstreams/arxiv_v1/reports/work-i-policy-profile-contract-v0.1.md"
)


def build_artifact() -> dict[str, Any]:
    contract = build_profile_contract()
    artifact = {**contract, "contract_sha256": profile_contract_sha256(contract)}
    return json.loads(json.dumps(artifact))


def build_markdown(artifact: dict[str, Any]) -> str:
    construct = artifact["construct"]
    metrics = artifact["metrics"]
    lines = [
        "# Work I Experimental-Agency Profile Contract",
        "",
        f"Schema: `{artifact['schema_id']}@{artifact['schema_version']}`",
        "",
        f"Contract SHA-256: `{artifact['contract_sha256']}`",
        "",
        "## Construct",
        "",
        construct["operational_definition"],
        "",
        f"The measurement unit is **{construct['unit_of_measurement']}**. The result is a "
        f"**{construct['representation']}**.",
        "",
        "The profile measures observable experimental policy. It does not claim:",
        "",
    ]
    lines.extend(f"- {claim}." for claim in construct["explicit_non_claims"])
    lines.extend(
        [
            "",
            "## Construct axes",
            "",
            "| Axis | Operational role | Metrics |",
            "| --- | --- | ---: |",
        ]
    )
    for axis in artifact["axes"]:
        count = sum(metric["axis_id"] == axis["axis_id"] for metric in metrics)
        lines.append(
            f"| `{axis['axis_id']}` | {axis['construct_role']} | {count} |"
        )
    lines.extend(
        [
            "",
            "## Frozen metric dictionary",
            "",
            (
                "Endpoint scores are listed separately below; they are never combined with "
                "the construct axes. `null` denotes an absent denominator, not zero behavior."
            ),
            "",
            "| Metric | Axis | Unit | Denominator | Null rule | Positive-control role |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for metric in metrics:
        null_rule = metric["null_when"] or "never"
        lines.append(
            f"| `{metric['metric_id']}` | `{metric['axis_id']}` | "
            f"{metric['unit']} | `{metric['denominator']}` | {null_rule} | "
            f"{metric['known_policy_role']} |"
        )
    lines.extend(
        [
            "",
            "## Endpoint context (outside the construct)",
            "",
            "| Metric | Definition |",
            "| --- | --- |",
        ]
    )
    for metric in artifact["endpoint_context"]:
        lines.append(
            f"| `{metric['metric_id']}` | {metric['operational_definition']} |"
        )
    lines.extend(
        [
            "",
            "## Counting and aggregation",
            "",
        ]
    )
    for name, rule in artifact["counting_rules"].items():
        lines.append(f"- **{name.replace('_', ' ')}:** {rule}")
    lines.extend(
        [
            "",
            f"Profiles are computed at the `{artifact['aggregation']['primary_unit']}` level. "
            f"A formal cell is `{artifact['aggregation']['formal_cell']}`, with "
            f"{artifact['aggregation']['lifecycle_count_per_formal_cell']} lifecycles. "
            f"{artifact['aggregation']['pooling_rule']}",
            "",
            "## Frozen invariants and reliability",
            "",
        ]
    )
    lines.extend(f"- `{invariant}`" for invariant in artifact["invariants"])
    lines.extend(
        [
            "",
            "Exact replay requires matching event, state, resource, and profile hashes. "
            "Known-policy controls make zero provider calls. The construct and all metric "
            "definitions were frozen before formal policy outcomes; threshold values are "
            "reserved to W1-V03 qualification worlds.",
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
            raise SystemExit("machine profile contract does not match deterministic rebuild")
        if args.markdown_output.read_text(encoding="utf-8") != markdown_text:
            raise SystemExit("human profile contract does not match deterministic rebuild")
    else:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(json_text, encoding="utf-8")
        args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
        args.markdown_output.write_text(markdown_text, encoding="utf-8")
    print(
        json.dumps(
            {
                "axis_count": len(artifact["axes"]),
                "construct_metric_count": len(artifact["metrics"]),
                "contract_sha256": artifact["contract_sha256"],
                "endpoint_context_metric_count": len(artifact["endpoint_context"]),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
