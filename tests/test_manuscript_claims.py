from __future__ import annotations

import json
import subprocess
from pathlib import Path

from scripts.audit_manuscript_claims import ROOT, audit


def test_manuscript_claim_audit_passes_without_render_requirement() -> None:
    report = audit(require_pdf=False)
    assert report["passed"] is True
    assert report["publication_ready"] is False
    assert all(report["checks"].values())


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
