from __future__ import annotations

import json
import subprocess
from pathlib import Path

from scripts.audit_manuscript_claims import ROOT, audit


def test_manuscript_claim_audit_fails_closed_on_stale_source_evidence() -> None:
    report = audit(require_pdf=False)
    assert report["passed"] is False
    assert report["status"] == "blocked"
    assert report["publication_ready"] is False
    assert report["checks"]["source_evidence_digests_match"] is False
    assert all(
        value
        for name, value in report["checks"].items()
        if name != "source_evidence_digests_match"
    )


def test_no_allowed_claim_uses_an_untracked_evidence_source() -> None:
    claims = json.loads((ROOT / "paper/claims.json").read_text(encoding="utf-8"))
    tracked = {
        line.strip()
        for line in subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).splitlines()
    }
    for claim in claims["claims"]:
        assert claim["source"] in tracked or (ROOT / claim["source"]).exists()


def test_rendered_pdf_has_pdf_signature_if_present() -> None:
    pdf = Path(ROOT / "paper/main.pdf")
    if pdf.exists():
        assert pdf.read_bytes().startswith(b"%PDF-")
