from __future__ import annotations

import json
from pathlib import Path

from paper.tools.render_first_paper_world_instrument_figures import (
    DEFAULT_OUTPUT_DIR,
    FIGURES,
    MANIFEST_SCHEMA,
    build_manifest,
    render,
)
from PIL import Image
from scripts.build_first_paper_figure_data import canonical_sha256, file_sha256

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = (
    ROOT / "paper/figures/first-paper-world-instrument-v1" / "first-paper-figure-data-v1.json"
)
MANIFEST_PATH = (
    ROOT
    / "paper/figures/first-paper-world-instrument-v1"
    / "first-paper-publication-figure-manifest-v1.json"
)


def _manifest() -> dict:
    value = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_manifest_binds_three_figures_and_nine_current_assets() -> None:
    manifest = _manifest()
    assert manifest["schema_version"] == MANIFEST_SCHEMA
    assert manifest["status"] == "PASS"
    assert manifest["canonical_figure_count"] == 3
    assert manifest["canonical_asset_count"] == 9
    assert manifest["caption_titles"] == [row[2] for row in FIGURES]
    declared = manifest["manifest_sha256"]
    unhashed = {key: value for key, value in manifest.items() if key != "manifest_sha256"}
    assert declared == canonical_sha256(unhashed)
    assert manifest["figure_data"]["sha256"] == file_sha256(DATA_PATH)
    assert all(manifest["claim_boundary"].values())


def test_manifest_render_binding_does_not_overwrite_direct_plates() -> None:
    paths = sorted(DEFAULT_OUTPUT_DIR.glob("figure-*.*"))
    before = {path: file_sha256(path) for path in paths}
    outputs = render({}, DEFAULT_OUTPUT_DIR)
    after = {path: file_sha256(path) for path in paths}
    assert before == after
    assert set(outputs) == {row[1] for row in FIGURES}


def test_every_bound_asset_exists_and_has_the_expected_publication_geometry() -> None:
    manifest = _manifest()
    expected_geometry = {
        "figure-1-system-overview": (2124, 1195),
        "figure-2-composition-and-qualification": (9599, 5400),
        "figure-3-controlled-forks": (7200, 5400),
    }
    for figure in manifest["figures"]:
        assert [row["format"] for row in figure["outputs"]] == ["svg", "pdf", "png"]
        for output in figure["outputs"]:
            path = ROOT / output["path"]
            assert path.is_file()
            assert path.stat().st_size == output["bytes"]
            assert file_sha256(path) == output["sha256"]
        png = ROOT / figure["outputs"][2]["path"]
        with Image.open(png) as image:
            assert image.size == expected_geometry[figure["stem"]]
        svg = (ROOT / figure["outputs"][0]["path"]).read_text(encoding="utf-8")
        if figure["stem"] in {
            "figure-1-system-overview",
            "figure-2-composition-and-qualification",
            "figure-3-controlled-forks",
        }:
            assert svg.count("<image") == 1
            assert "<text" not in svg
        else:
            assert "<text" in svg
        assert "D:\\Projects" not in svg
        assert "sha256" not in svg.lower()
        assert "source_commit" not in svg.lower()
        assert "run_id" not in svg.lower()


def test_committed_manifest_rebuilds_from_bound_assets() -> None:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    outputs = {
        stem: [
            ROOT / f"paper/figures/first-paper-world-instrument-v1/publication/{stem}.{suffix}"
            for suffix in ("svg", "pdf", "png")
        ]
        for _, stem, _ in FIGURES
    }
    assert _manifest() == build_manifest(data, outputs)
