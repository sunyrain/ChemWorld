from __future__ import annotations

from scripts.audit_ncs_manuscript import audit


def test_ncs_working_manuscript_is_evidence_bound_but_not_publication_ready() -> None:
    report = audit(require_pdf=False)
    assert report["status"] == "working_draft_valid"
    assert report["publication_ready"] is False
    assert all(report["checks"].values())
    assert all(report["diagnostics"]["pending_slots"].values())
    # A stale or diagnostic report may already occupy a future result path.
    # Path existence never authorizes removing a manuscript placeholder.
    assert report["diagnostics"]["pending_artifacts_already_present"]["PENDING-LLM"]
