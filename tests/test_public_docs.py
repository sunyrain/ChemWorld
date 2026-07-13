from __future__ import annotations

from pathlib import Path

from scripts.audit_public_docs import audit_public_docs

ROOT = Path(__file__).resolve().parents[1]


def test_public_documentation_is_user_facing_and_matches_v05_truth() -> None:
    report = audit_public_docs(ROOT)
    assert report["passed"] is True, report
    assert report["checks"]["no_maintainer_paths_or_commands"] is True
    assert report["checks"]["no_unimplemented_cli"] is True
    assert report["checks"]["task_truth_matches_v05_protocol"] is True
    assert report["checks"]["pre_v05_results_marked_diagnostic"] is True
    assert report["missing_task_hashes"] == {}


def test_professional_narrative_navigation_has_unique_existing_targets() -> None:
    report = audit_public_docs(ROOT)
    assert report["checks"]["professional_information_architecture"] is True, report
    assert report["missing_navigation_targets"] == []
    assert report["duplicate_navigation_targets"] == []
    assert report["unlisted_public_pages"] == []
    assert report["navigation_checks"]["professional_narrative_order"] is True
    assert report["navigation_checks"]["english_navigation_present"] is True


def test_left_and_right_navigation_fold_but_content_folding_is_opt_in() -> None:
    report = audit_public_docs(ROOT)
    assert report["checks"]["folding_contract"] is True, report
    assert all(report["folding_checks"].values())

    mkdocs = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    assert "assets/javascripts/navigation-v7.js" in mkdocs
    assert "navigation.sections" not in mkdocs
