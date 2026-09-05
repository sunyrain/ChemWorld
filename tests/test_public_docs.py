from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
from scripts.audit_public_docs import _maintainer_token_hits, audit_public_docs

ROOT = Path(__file__).resolve().parents[1]


def test_repository_navigation_does_not_allow_maintainer_commands_in_public_docs(
    tmp_path: Path,
) -> None:
    readme = tmp_path / "README.md"
    page = tmp_path / "docs" / "guide.md"
    page.parent.mkdir()
    readme.write_text("[Research](workstreams/current.md)\n", encoding="utf-8")
    page.write_text("Public tutorial.\n", encoding="utf-8")
    assert _maintainer_token_hits([readme, page], tmp_path) == []

    readme.write_text("python scripts/private_runner.py\n", encoding="utf-8")
    page.write_text("[Internal](../workstreams/current.md)\n", encoding="utf-8")
    hits = _maintainer_token_hits([readme, page], tmp_path)
    assert {(hit["path"], hit["token"]) for hit in hits} == {
        ("README.md", "python scripts/"),
        ("docs/guide.md", "](../workstreams/"),
    }


def test_readme_uses_frozen_release_identity_independently_of_development_gate(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    current_path = ROOT / "configs/current.json"
    current = json.loads(current_path.read_text(encoding="utf-8"))
    current["mechanism_adaptation"]["gate_a_evidence_current"] = False
    original_read = Path.read_text

    def read_with_registry(path: Path, *args: Any, **kwargs: Any) -> str:
        if path == current_path:
            return json.dumps(current)
        return original_read(path, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", read_with_registry)
    report = audit_public_docs(ROOT)
    assert "README.md" not in report["status_surface_missing_markers"]

    current["publication"]["frozen_release"]["commit"] = "missing-release-for-test"
    report = audit_public_docs(ROOT)
    assert any(
        "missing-release-for-test" in marker
        for marker in report["status_surface_missing_markers"]["README.md"]
    )


def test_public_documentation_is_user_facing_and_matches_v05_truth() -> None:
    report = audit_public_docs(ROOT)
    assert report["passed"] is True, report
    assert report["checks"]["no_maintainer_paths_or_commands"] is True
    assert report["checks"]["no_unimplemented_cli"] is True
    assert report["checks"]["task_truth_matches_v05_protocol"] is True
    assert report["checks"]["pre_v05_results_marked_diagnostic"] is True
    assert report["checks"]["research_status_matches_current_registry"] is True
    assert report["checks"]["no_obsolete_status_phrases"] is True
    assert report["checks"]["canonical_result_numbers_are_not_duplicated"] is True
    assert report["checks"]["historical_certificate_numbers_have_one_summary"] is True
    assert report["checks"]["local_links_resolve"] is True
    assert report["checks"]["image_assets_are_referenced"] is True
    assert report["status_surface_missing_markers"] == {}
    assert report["status_surface_stale_markers"] == []
    assert report["broken_local_links"] == []
    assert report["unreferenced_images"] == []
    assert report["missing_task_hashes"] == {}


def test_curated_bilingual_navigation_and_reference_catalog_cover_public_pages() -> None:
    report = audit_public_docs(ROOT)
    assert report["checks"]["professional_information_architecture"] is True, report
    assert report["missing_navigation_targets"] == []
    assert report["duplicate_navigation_targets"] == []
    assert report["unlisted_public_pages"] == []
    assert report["navigation_checks"]["professional_narrative_order"] is True
    assert report["navigation_checks"]["english_navigation_present"] is True
    assert report["navigation_checks"]["english_is_not_a_chinese_nav_section"] is True
    assert report["navigation_checks"]["locale_sources_are_isolated"] is True
    assert report["navigation_checks"]["contextual_switch_compatible"] is True


def test_left_and_right_navigation_fold_but_content_folding_is_opt_in() -> None:
    report = audit_public_docs(ROOT)
    assert report["checks"]["folding_contract"] is True, report
    assert all(report["folding_checks"].values())

    mkdocs = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    assert "assets/javascripts/navigation-v7.js" in mkdocs
    assert "navigation.sections" not in mkdocs
    assert "navigation.instant" not in mkdocs


def test_language_switch_is_a_locale_dimension_not_a_navigation_bucket() -> None:
    report = audit_public_docs(ROOT)
    navigation = report["navigation_checks"]
    assert navigation["language_switch_present"] is True, report
    assert navigation["english_is_not_a_chinese_nav_section"] is True
    assert navigation["english_navigation_present"] is True

    mkdocs = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    assert "docs_structure: suffix" in mkdocs
    assert "fallback_to_default: false" in mkdocs
    assert "  - English:" not in mkdocs
    assert "extra:\n  alternate:" not in mkdocs
