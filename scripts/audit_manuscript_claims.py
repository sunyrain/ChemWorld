"""Fail-closed audit for the evidence-gated manuscript draft."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def audit(root: Path = ROOT, *, require_pdf: bool = True) -> dict[str, Any]:
    paper = root / "paper"
    claims = json.loads((paper / "claims.json").read_text(encoding="utf-8"))
    manuscript = (paper / "main.tex").read_text(encoding="utf-8")
    freeze = json.loads(
        (root / "workstreams/benchmark_v1/reports/confirmatory-freeze-controls.json").read_text(
            encoding="utf-8"
        )
    )
    source_manifest = json.loads((paper / "source_data/manifest.json").read_text(encoding="utf-8"))
    evidence_digests_match = all(
        hashlib.sha256((root / path).read_bytes()).hexdigest() == digest
        for path, digest in source_manifest.get("evidence_sha256", {}).items()
    )

    referenced_sources_exist = all((root / claim["source"]).is_file() for claim in claims["claims"])
    blocked_claims_not_asserted = all(
        claim["status"] != "blocked" or claim["assertion"] not in manuscript
        for claim in claims["claims"]
    )
    checks = {
        "claim_schema": claims.get("schema_version") == "chemworld-manuscript-claims-0.1",
        "draft_not_publication_ready": claims.get("publication_ready") is False,
        "upstream_not_publication_ready": freeze.get("publication_ready") is False,
        "referenced_sources_exist": referenced_sources_exist,
        "blocked_claims_not_asserted_verbatim": blocked_claims_not_asserted,
        "diagnostic_evidence_labelled": "legacy diagnostic" in manuscript.lower(),
        "private_reasoning_not_required": "private chain-of-thought" in manuscript,
        "limitations_present": "\\section*{Limitations}" in manuscript,
        "source_data_not_confirmatory": source_manifest.get("evidence_class")
        == "diagnostic_and_control_only",
        "source_evidence_digests_match": evidence_digests_match,
        "submission_metadata_explicit": "AUTHORS AND AFFILIATIONS TO BE FINALIZED" in manuscript,
        "pdf_rendered": (paper / "main.pdf").is_file() if require_pdf else True,
    }
    passed = all(checks.values())
    return {
        "schema_version": "chemworld-manuscript-claim-audit-0.1",
        "passed": passed,
        "publication_ready": False,
        "checks": checks,
        "status": "review_draft_only" if passed else "blocked",
        "remaining_gates": freeze.get("remaining_release_gates", []),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "paper/manuscript-audit.json")
    parser.add_argument("--allow-missing-pdf", action="store_true")
    args = parser.parse_args()
    report = audit(require_pdf=not args.allow_missing_pdf)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    if not report["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
