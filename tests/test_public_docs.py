from __future__ import annotations

from pathlib import Path

from scripts.audit_public_docs import audit_public_docs


def test_public_documentation_is_user_facing_and_current() -> None:
    report = audit_public_docs(Path(__file__).resolve().parents[1])
    assert report["passed"] is True, report
    assert report["checks"]["no_maintainer_paths"] is True
    assert report["checks"]["current_evidence_markers_present"] is True
    assert report["checks"]["user_journey_navigation"] is True
