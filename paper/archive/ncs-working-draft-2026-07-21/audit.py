"""Fail-closed audit retained with the archived NCS working manuscript."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
PAPER = Path(__file__).resolve().parent
LEDGER_PATH = PAPER / "evidence-ledger.json"
MANUSCRIPT_PATH = PAPER / "main.tex"
PDF_PATH = PAPER / "main.pdf"
AUDIT_PATH = PAPER / "manuscript-audit.json"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _abstract_word_count(manuscript: str) -> int:
    match = re.search(
        r"% ABSTRACT_START.*?\\begin\{abstract\}(.*?)\\end\{abstract\}",
        manuscript,
        flags=re.DOTALL,
    )
    if match is None:
        return -1
    text = re.sub(r"\\[A-Za-z]+(?:\[[^]]*\])?(?:\{[^}]*\})?", " ", match.group(1))
    text = re.sub(r"[^A-Za-z0-9\u2013\u2014'-]+", " ", text)
    return len([token for token in text.split() if token])


def audit(*, require_pdf: bool = True) -> dict[str, Any]:
    ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    manuscript = MANUSCRIPT_PATH.read_text(encoding="utf-8")

    digest_results: dict[str, bool] = {}
    for item in ledger["current_evidence"]:
        path = ROOT / item["path"]
        digest_results[item["id"]] = path.is_file() and _sha256(path) == item["sha256"]

    pending_ids = [item["id"] for item in ledger["pending_results"]]
    pending_presence = {pending_id: pending_id in manuscript for pending_id in pending_ids}
    completed_pending_paths = {
        item["id"]: (ROOT / item["required_path"]).is_file() for item in ledger["pending_results"]
    }
    section_positions = {
        name: manuscript.find(marker)
        for name, marker in {
            "results": r"\section*{Results}",
            "discussion": r"\section*{Discussion}",
            "online_methods": r"\section*{Online Methods}",
        }.items()
    }
    abstract_words = _abstract_word_count(manuscript)
    document_body = manuscript.split(r"\begin{document}", maxsplit=1)[-1]
    display_item_count = document_body.count(r"\begin{figure}") + document_body.count(
        r"\figurepending{"
    )
    structure_ordered = (
        -1
        < section_positions["results"]
        < section_positions["discussion"]
        < section_positions["online_methods"]
    )
    checks = {
        "ledger_not_publication_ready": ledger.get("publication_ready") is False,
        "evidence_digests_match": all(digest_results.values()),
        "all_pending_slots_visible": all(pending_presence.values()),
        "article_structure_ordered": structure_ordered,
        "introduction_is_unheaded": r"\section*{Introduction}" not in manuscript,
        "abstract_within_150_words": 0 < abstract_words <= 150,
        "display_items_within_limit": display_item_count
        <= int(ledger["format_contract"]["display_item_limit"]),
        "submission_status_explicit": "Not for submission" in manuscript,
        "ai_assistance_disclosed": "An AI coding assistant was used" in manuscript,
        "pdf_rendered": PDF_PATH.is_file() and PDF_PATH.read_bytes().startswith(b"%PDF-"),
    }
    if not require_pdf:
        checks["pdf_rendered"] = True

    report = {
        "schema_version": "chemworld-ncs-manuscript-audit-0.1",
        "status": "working_draft_valid" if all(checks.values()) else "blocked",
        "publication_ready": False,
        "checks": checks,
        "diagnostics": {
            "abstract_word_count": abstract_words,
            "display_item_count": display_item_count,
            "evidence_digests": digest_results,
            "pending_slots": pending_presence,
            "pending_artifacts_already_present": completed_pending_paths,
        },
    }
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--allow-missing-pdf", action="store_true")
    args = parser.parse_args()
    report = audit(require_pdf=not args.allow_missing_pdf)
    AUDIT_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "working_draft_valid" else 1


if __name__ == "__main__":
    raise SystemExit(main())
