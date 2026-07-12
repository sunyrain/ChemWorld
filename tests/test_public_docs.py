from __future__ import annotations

from pathlib import Path

from scripts.audit_public_docs import audit_public_docs


def test_public_documentation_is_user_facing_and_current() -> None:
    report = audit_public_docs(Path(__file__).resolve().parents[1])
    assert report["passed"] is True, report
    assert report["checks"]["no_maintainer_paths"] is True
    assert report["checks"]["current_evidence_markers_present"] is True
    assert report["checks"]["user_journey_navigation"] is True


def test_published_docs_ship_visible_outline_and_section_folding() -> None:
    root = Path(__file__).resolve().parents[1]
    mkdocs = (root / "mkdocs.yml").read_text(encoding="utf-8")
    navigation = (root / "docs" / "assets" / "javascripts" / "navigation-v7.js").read_text(
        encoding="utf-8"
    )

    assert "assets/javascripts/navigation-v7.js" in mkdocs
    assert "navigation.sections" not in mkdocs
    assert "cw-toc-heading" in navigation
    assert "setupContentSections" in navigation
    assert "cw-section-toggle" in navigation
