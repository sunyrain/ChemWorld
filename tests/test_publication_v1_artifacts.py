from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FIGURE_ROOT = ROOT / "paper/figures/experimental-intelligence-v1"
BUILD_ROOT = ROOT / "paper/exports/experimental-intelligence-v1"


def _sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _canonical_sha(value: dict[str, Any]) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()


def test_publication_figure_manifest_is_self_hashed_and_complete() -> None:
    path = FIGURE_ROOT / "publication-figure-manifest.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    declared = manifest.pop("manifest_sha256")
    assert declared == _canonical_sha(manifest)
    assert manifest["status"] == "frozen_complete"
    assert manifest["style_version"] == "nature-editorial-v1"
    assert len(manifest["files"]) == 12
    assert manifest["figure_5_rendered"] is True
    for row in manifest["files"]:
        artifact = ROOT / row["path"]
        assert artifact.stat().st_size == row["bytes"]
        assert _sha(artifact) == row["sha256"]
        if artifact.suffix == ".svg":
            source = artifact.read_text(encoding="utf-8")
            assert "<text" in source
            assert "\r\n" not in source
        else:
            assert artifact.read_bytes().startswith(b"\x89PNG\r\n\x1a\n")


def test_image_generated_concepts_are_separate_from_result_figures() -> None:
    concept_root = FIGURE_ROOT / "concept-placeholders"
    readme = (concept_root / "README.md").read_text(encoding="utf-8")
    normalized_readme = " ".join(readme.lower().split())
    assert "not experimental evidence" in normalized_readme
    concepts = sorted(concept_root.glob("concept-figure-*-v1.png"))
    assert len(concepts) == 6
    assert all(path.stat().st_size > 500_000 for path in concepts)
    publication_html = (
        BUILD_ROOT / "experimental-intelligence-v1-publication-proof.html"
    ).read_text(encoding="utf-8")
    assert "concept-figure-" not in publication_html
    for number in range(1, 7):
        assert f"figure-{number}-" in publication_html


def test_publication_proof_manifest_binds_sources_and_outputs() -> None:
    path = BUILD_ROOT / "publication-proof-manifest.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    declared = manifest.pop("manifest_sha256")
    assert declared == _canonical_sha(manifest)
    assert manifest["status"] == "working_proof"
    for collection in ("sources", "outputs"):
        for row in manifest[collection]:
            artifact = ROOT / row["path"]
            assert artifact.stat().st_size == row["bytes"]
            assert _sha(artifact) == row["sha256"]
    publication_pdf = BUILD_ROOT / "experimental-intelligence-v1-publication-proof.pdf"
    concept_pdf = BUILD_ROOT / "experimental-intelligence-v1-concept-atlas.pdf"
    assert publication_pdf.read_bytes().startswith(b"%PDF-")
    assert concept_pdf.read_bytes().startswith(b"%PDF-")
    assert publication_pdf.stat().st_size > 100_000
    assert concept_pdf.stat().st_size > 1_000_000


def test_display_legend_order_and_data_card_match_the_arxiv_release() -> None:
    display = (ROOT / "paper/experimental_intelligence_v1_display_items.md").read_text(
        encoding="utf-8"
    )
    expected_titles = [
        "ChemWorld is a controlled apparatus for experimental intelligence.",
        "Compiled controls distinguish task outcome, information response and epistemic readouts.",
        "Primitive-control agents close complete experimental lifecycles.",
        "Similar endpoints can arise from different experimental trajectories.",
        "Fresh trajectories test within-world repeatability.",
        "Experimental intelligence is a profile, not a scalar.",
    ]
    positions = [
        display.index(f"**Figure {number} | {title}**")
        for number, title in enumerate(expected_titles, start=1)
    ]
    assert positions == sorted(positions)

    build_manifest = json.loads(
        (
            ROOT
            / "paper/exports/experimental-intelligence-v1-arxiv/build-manifest.json"
        ).read_text(encoding="utf-8")
    )
    data_card = (
        ROOT / "benchmark/releases/chemworld-serious-v1/DATA_CARD.md"
    ).read_text(encoding="utf-8")
    assert f"an {build_manifest['pdf_page_count']}-page, two-column arXiv PDF" in data_card
