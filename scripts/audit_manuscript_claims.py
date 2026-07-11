"""Fail-closed audit for the evidence-gated Nature-style manuscript draft."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def audit(root: Path = ROOT, *, require_pdf: bool = True) -> dict[str, Any]:
    paper = root / "paper"
    claims = _load(paper / "claims.json")
    manuscript = (paper / "main.tex").read_text(encoding="utf-8")
    architecture = _load(root / "workstreams/benchmark_v1/reports/architecture-readiness.json")
    source_manifest = _load(paper / "source_data/manifest.json")

    evidence_digests_match = all(
        (root / path).is_file() and hashlib.sha256((root / path).read_bytes()).hexdigest() == digest
        for path, digest in source_manifest.get("evidence_sha256", {}).items()
    )
    referenced_sources_exist = all((root / claim["source"]).is_file() for claim in claims["claims"])
    blocked_claims_not_asserted = all(
        claim["status"] != "blocked" or claim["assertion"] not in manuscript
        for claim in claims["claims"]
    )
    current_evidence_markers = (
        "0.018752",
        "100,000",
        "80,000",
        "Nine mechanism-family controls",
        "no real provider trajectory",
    )
    figure_markers = tuple(f"figure{index}_" for index in range(1, 6))
    checks = {
        "claim_schema": claims.get("schema_version") == "chemworld-manuscript-claims-0.2",
        "draft_not_publication_ready": claims.get("publication_ready") is False,
        "architecture_controls_ready": architecture.get("controls_ready") is True,
        "architecture_formal_evidence_incomplete": architecture.get("formal_evidence_ready")
        is False,
        "architecture_not_publication_ready": architecture.get("publication_ready") is False,
        "referenced_sources_exist": referenced_sources_exist,
        "blocked_claims_not_asserted_verbatim": blocked_claims_not_asserted,
        "current_evidence_markers_present": all(
            marker.lower() in manuscript.lower() for marker in current_evidence_markers
        ),
        "all_five_figures_referenced": all(marker in manuscript for marker in figure_markers),
        "private_reasoning_not_required": "private chain-of-thought" in manuscript,
        "limitations_present": "\\section*{Limitations}" in manuscript,
        "source_data_evidence_class_current": source_manifest.get("evidence_class")
        == "confirmatory_slice_development_diagnostics_and_controls",
        "source_data_not_publication_ready": source_manifest.get("publication_ready") is False,
        "source_evidence_digests_match": evidence_digests_match,
        "submission_metadata_explicit": "AUTHORS AND AFFILIATIONS TO BE FINALIZED" in manuscript,
        "pdf_rendered": (paper / "main.pdf").is_file() if require_pdf else True,
    }
    passed = all(checks.values())
    return {
        "schema_version": "chemworld-manuscript-claim-audit-0.2",
        "passed": passed,
        "publication_ready": False,
        "checks": checks,
        "status": "submission_draft_evidence_incomplete" if passed else "blocked",
        "remaining_gates": architecture.get("critical_path", []),
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
