#!/usr/bin/env python3
"""Amend the retained U05 result with the missing declared-resource audit."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

from chemworld.eval.first_paper_u05_complete_agent import (
    amend_report_with_declared_resource_audit,
    render_markdown,
)

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "workstreams/arxiv_v1/reports/first-paper-agent-instrument-use-v1.json"
MARKDOWN = REPORT.with_suffix(".md")
EXPECTED_REPORT_SHA256 = (
    "2865cf40fb0f8bf032fdd1ee794c90e458ca2f2b5eeeea005760bdaa3f1defff"
)
EXPECTED_MARKDOWN_SHA256 = (
    "70cd16745f359b04375c06a1c76ca8f395f5f100074f6779007c7c4bfab769b8"
)
ORIGINAL_RESULT_COMMIT = "8d2667a2"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    observed_report_sha = _sha256(REPORT)
    observed_markdown_sha = _sha256(MARKDOWN)
    if observed_report_sha != EXPECTED_REPORT_SHA256:
        raise SystemExit("formal JSON changed; refusing postrun amendment")
    if observed_markdown_sha != EXPECTED_MARKDOWN_SHA256:
        raise SystemExit("formal Markdown changed; refusing postrun amendment")
    amendment_commit = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    amended = amend_report_with_declared_resource_audit(
        report,
        original_report_sha256=observed_report_sha,
        original_markdown_sha256=observed_markdown_sha,
        original_result_commit=ORIGINAL_RESULT_COMMIT,
        amendment_commit=amendment_commit,
    )
    REPORT.write_text(
        json.dumps(
            amended,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
            allow_nan=False,
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    MARKDOWN.write_text(render_markdown(amended), encoding="utf-8", newline="\n")
    print(
        json.dumps(
            {
                "status": amended["status"],
                "declared_resource_budget": amended[
                    "declared_resource_budget"
                ],
                "provider_rerun": False,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
