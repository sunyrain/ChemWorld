from __future__ import annotations

import hashlib
import json
import tarfile
import zipfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / "benchmark/releases/chemworld-serious-v1"
ARXIV = ROOT / "paper/arxiv"
EXPORT = ROOT / "paper/exports/experimental-intelligence-v1-arxiv"


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


def test_public_trajectory_archive_is_complete_and_bound() -> None:
    archive = RELEASE / "g2-v0.5-public-trajectory-archive"
    manifest = json.loads((archive / "manifest.json").read_text(encoding="utf-8"))
    declared = manifest.pop("archive_sha256")
    assert declared == _canonical_sha(manifest)
    assert manifest["provider_response_content_included"] is False
    assert manifest["hidden_evaluator_identity_included"] is False
    assert manifest["formal_matrix"]["cell_count"] == 20
    assert manifest["formal_matrix"]["completed_cell_count"] == 18
    assert manifest["formal_matrix"]["right_censored_cell_count"] == 2
    assert manifest["formal_matrix"]["completed_final_assay_count"] == 112
    assert manifest["excluded_first_launch"]["cell_count"] == 2
    assert manifest["excluded_first_launch"]["primary_analysis_included"] is False
    cells = [
        *manifest["formal_matrix"]["cells"],
        *manifest["excluded_first_launch"]["cells"],
    ]
    assert len(cells) == 22
    for cell in cells:
        trajectory = archive / cell["compact_path"]
        assert trajectory.stat().st_size == cell["compact_bytes"]
        assert _sha(trajectory) == cell["compact_sha256"]
        assert cell["exact_physical_replay_verified"] is True
        rows = [
            json.loads(line)
            for line in trajectory.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        scores = [
            row["leaderboard_score"]
            for row in rows
            if row.get("transaction_status") == "committed"
            and row.get("operation_type") == "measure"
            and row.get("instrument") == "final_assay"
        ]
        assert cell["completed_final_assays"] == len(scores)
        assert cell["final_score_sequence"] == scores


def test_arxiv_figure_manifest_binds_all_release_formats() -> None:
    manifest = json.loads((ARXIV / "figure-manifest.json").read_text(encoding="utf-8"))
    declared = manifest.pop("manifest_sha256")
    assert declared == _canonical_sha(manifest)
    assert manifest["status"] == "frozen_complete"
    assert manifest["style_version"] == "arxiv-release-v1"
    assert len(manifest["files"]) == 18
    assert {Path(row["path"]).suffix for row in manifest["files"]} == {
        ".pdf",
        ".png",
        ".svg",
    }
    for row in manifest["files"]:
        artifact = ROOT / row["path"]
        assert artifact.stat().st_size == row["bytes"]
        assert _sha(artifact) == row["sha256"]


def test_key_workflow_svgs_keep_structure_editable_and_icons_independent() -> None:
    required_labels = {
        "figure-1-controlled-apparatus.svg": (
            ("executable world", "resource ledger", "immutable trace", "physical"),
            22,
            80,
        ),
        "figure-3-autonomous-lifecycle.svg": (
            ("reagent", "UV-vis", "agent selects", "final assay"),
            7,
            100,
        ),
    }
    for filename, (labels, image_count, minimum_paths) in required_labels.items():
        svg = (ARXIV / "figures" / filename).read_text(encoding="utf-8")
        # Complex apparatus icons are isolated reference crops.  Text, cards,
        # arrows, and charts remain native SVG rather than a flattened plate.
        assert svg.count("<image") == image_count
        assert svg.count("<text") >= 20
        assert svg.count("<path") >= minimum_paths
        assert all(label in svg for label in labels)

    derived = json.loads((RELEASE / "arxiv-v1-derived-data.json").read_text(encoding="utf-8"))
    potential = derived["g2_v0_4"]["one_experiment_demonstration"]["setpoint_policy"][0][
        "potential_V"
    ]
    lifecycle_svg = (ARXIV / "figures" / "figure-3-autonomous-lifecycle.svg").read_text(
        encoding="utf-8"
    )
    assert f">{potential:g} V<" in lifecycle_svg
    assert 'viewBox="0 0 518.4 239.76"' in lifecycle_svg
    assert all(color in lifecycle_svg for color in ("#078b78", "#004c73", "#ef432f", "#e18b00"))


def test_arxiv_build_manifest_binds_pdf_and_self_contained_sources() -> None:
    manifest = json.loads((EXPORT / "build-manifest.json").read_text(encoding="utf-8"))
    declared = manifest.pop("manifest_sha256")
    assert declared == _canonical_sha(manifest)
    assert manifest["status"] == "compiled_arxiv_release"
    assert manifest["pdf_page_count"] == 11
    for row in manifest["files"]:
        artifact = ROOT / row["path"]
        assert artifact.stat().st_size == row["bytes"]
        assert _sha(artifact) == row["sha256"]
    pdf = ROOT / manifest["pdf"]
    assert pdf.read_bytes().startswith(b"%PDF-")
    assert pdf.stat().st_size > 500_000
    required = {
        "main.tex",
        "main.bbl",
        "manuscript.md",
        "references.bib",
        *{f"figures/figure-{number}" for number in range(1, 7)},
    }
    zip_path = ROOT / manifest["source_zip"]
    tar_path = ROOT / manifest["source_tar_gz"]
    with zipfile.ZipFile(zip_path) as archive:
        zip_members = set(archive.namelist())
    with tarfile.open(tar_path, mode="r:gz") as archive:
        tar_members = {member.name for member in archive.getmembers() if member.isfile()}
    assert zip_members == tar_members
    assert required - {f"figures/figure-{number}" for number in range(1, 7)} <= zip_members
    for number in range(1, 7):
        assert any(
            member.startswith(f"figures/figure-{number}-") and member.endswith(".pdf")
            for member in zip_members
        )


def test_generated_tex_has_launch_order_and_standard_abstract() -> None:
    tex = (ARXIV / "main.tex").read_text(encoding="utf-8")
    assert "\\begin{abstract}\nA best-of-campaign score is an incomplete readout" in tex
    assert "\\subsection{Abstract}" not in tex
    assert "\\section{1. Introduction}" in tex
    assert "\\section{12. Conclusion}" in tex
    positions = [tex.index(f"figures/figure-{number}-") for number in range(1, 7)]
    assert positions == sorted(positions)
    assert "\\titleformat{\\section}" not in tex or "{\\thesection.}" not in tex


def test_release_manifest_records_completed_p0_gates() -> None:
    manifest = json.loads((RELEASE / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["paper"]["working_title"] == (
        "Executable Chemical Worlds Reveal the Hidden Dynamics of Experimental Agency"
    )
    assert manifest["gates"]["raw_data_archive"] == "open"
    assert manifest["publication_ready"] is False
    assert manifest["gates"]["final_claim_audit"].startswith("passed_")
    assert manifest["gates"]["standard_arxiv_render"].startswith("passed_")
