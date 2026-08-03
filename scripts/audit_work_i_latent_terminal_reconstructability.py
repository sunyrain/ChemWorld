"""Build the Work I 36-unit pre-discard reconstructability audit."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from chemworld.eval.latent_terminal_reconstructability import (
    build_reconstructability_report,
    discover_run_root,
    validate_reconstructability_report,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_JSON = (
    ROOT
    / "workstreams/arxiv_v1/reports/"
    "work-i-latent-terminal-reconstructability-v0.1.json"
)
DEFAULT_MARKDOWN = (
    ROOT
    / "workstreams/arxiv_v1/reports/"
    "work-i-latent-terminal-reconstructability-v0.1.md"
)


def _json_text(payload: dict[str, Any]) -> str:
    return json.dumps(
        payload,
        ensure_ascii=False,
        allow_nan=False,
        indent=2,
        sort_keys=True,
    ) + "\n"


def build_markdown(report: dict[str, Any]) -> str:
    census = report["census"]
    raw = report["raw_root_audit"]
    lines = [
        "# Work I Pre-discard Reconstructability Audit",
        "",
        f"Status: **{report['status']}**",
        "",
        f"Report SHA-256: `{report['report_sha256']}`",
        "",
        "## Result",
        "",
        f"All **{census['reconstructable_unit_count']}/"
        f"{census['discard_unit_count']}** frozen discard checkpoints were "
        "reconstructed before the original `discard_batch` action. Each hidden-state, "
        "resource-snapshot and complete checkpoint identity matched a second independent "
        "deterministic replay.",
        "",
        f"The indexed raw root contains **{raw['file_count']} files** and "
        f"**{raw['byte_count']} bytes**; every path, byte count and SHA-256 matches the "
        "frozen terminal index, with zero unindexed files.",
        "",
        "## Outcome boundary",
        "",
        "- Shadow terminal evaluations executed: **0**.",
        "- Latent discard scores accessed: **0**.",
        "- Agent/provider calls: **0**.",
        "- Hidden state publication: hashes only; no hidden payload is emitted.",
        "- Terminal replacement: not performed; L05 owns formal shadow execution.",
        "",
        "## Census",
        "",
        "| Cell | World | Arm | Raw steps | Discards | Full replay | Checkpoints |",
        "| --- | ---: | --- | ---: | ---: | --- | --- |",
    ]
    for cell in report["cells"]:
        lines.append(
            f"| `{cell['cell_id']}` | {cell['world_seed']} | "
            f"`{cell['information_arm']}` | {cell['record_count']} | "
            f"{cell['discard_count']} | "
            f"{'PASS' if cell['exact_full_trajectory_replay']['verified'] else 'FAIL'} | "
            f"{'PASS' if cell['all_discard_checkpoints_reconstructable'] else 'FAIL'} |"
        )
    lines.extend(
        [
            "",
            "## Gates",
            "",
        ]
    )
    lines.extend(
        f"- `{name}`: **{'PASS' if passed else 'FAIL'}**"
        for name, passed in report["gates"].items()
    )
    lines.extend(
        [
            "",
            "## Evidence limitation",
            "",
            report["historical_identity_limit"],
            "",
            "This audit establishes deterministic reconstructability only. It does not "
            "evaluate a discarded state and contains no terminal-quality result.",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-root", type=Path)
    parser.add_argument("--json-output", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--markdown-output", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    run_root = args.run_root.resolve() if args.run_root else discover_run_root(ROOT)
    report = build_reconstructability_report(ROOT, run_root)
    errors = validate_reconstructability_report(report, root=ROOT)
    if errors:
        raise SystemExit("reconstructability audit invalid: " + "; ".join(errors))
    json_text = _json_text(report)
    markdown_text = build_markdown(report)
    if args.check:
        if args.json_output.read_text(encoding="utf-8") != json_text:
            raise SystemExit("machine report differs from deterministic rebuild")
        if args.markdown_output.read_text(encoding="utf-8") != markdown_text:
            raise SystemExit("human report differs from deterministic rebuild")
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
                **report["census"],
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
