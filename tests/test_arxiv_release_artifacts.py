from __future__ import annotations

import base64
import copy
import hashlib
import importlib.util
import io
import json
import re
import struct
import tarfile
import zipfile
from pathlib import Path
from typing import Any

from paper.tools import finalize_arxiv_release as finalizer

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
    manifest_path = (
        ROOT / "paper/figures/first-paper-world-instrument-v1/"
        "first-paper-publication-figure-manifest-v1.json"
    )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    declared = manifest.pop("manifest_sha256")
    assert declared == _canonical_sha(manifest)
    assert manifest["status"] == "PASS"
    assert manifest["canonical_figure_count"] == 4
    assert manifest["canonical_asset_count"] == 12
    files = [output for figure in manifest["figures"] for output in figure["outputs"]]
    assert len(files) == 12
    assert {Path(row["path"]).suffix for row in files} == {
        ".pdf",
        ".png",
        ".svg",
    }
    for row in files:
        artifact = ROOT / row["path"]
        assert artifact.stat().st_size == row["bytes"]
        assert _sha(artifact) == row["sha256"]


def test_key_workflow_svgs_keep_structure_editable_and_icons_independent() -> None:
    required_labels = {
        "figure-1-controlled-apparatus.svg": (
            ("executable world", "resource ledger", "immutable trace", "physical"),
            21,
            80,
            100,
        ),
        "figure-3-autonomous-lifecycle.svg": (
            ("reagent", "UV-vis", "agent selects", "final assay"),
            7,
            100,
            140,
        ),
    }
    for filename, settings in required_labels.items():
        labels, image_count, minimum_paths, minimum_long_edge = settings
        svg = (ARXIV / "figures" / filename).read_text(encoding="utf-8")
        # Complex apparatus icons are isolated high-resolution crops. Text,
        # cards, arrows, and charts remain native SVG rather than a flattened plate.
        assert svg.count("<image") == image_count
        assert svg.count("<text") >= 20
        assert svg.count("<path") >= minimum_paths
        assert all(label in svg for label in labels)
        payloads = re.findall(r"data:image/png;base64,\s*([^\"]+)", svg)
        dimensions = []
        for payload in payloads:
            raw = base64.b64decode(re.sub(r"\s+", "", payload))
            assert raw.startswith(b"\x89PNG\r\n\x1a\n")
            dimensions.append(struct.unpack(">II", raw[16:24]))
        assert min(max(width, height) for width, height in dimensions) >= minimum_long_edge

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
    assert manifest["pdf_page_count"] >= 10
    assert manifest["canonical_figure_count"] == 4
    assert manifest["figure_manifest"].endswith("first-paper-publication-figure-manifest-v1.json")
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
        *{f"figures/figure-{number}" for number in range(1, 5)},
    }
    zip_path = ROOT / manifest["source_zip"]
    tar_path = ROOT / manifest["source_tar_gz"]
    with zipfile.ZipFile(zip_path) as archive:
        zip_members = set(archive.namelist())
    with tarfile.open(tar_path, mode="r:gz") as archive:
        tar_members = {member.name for member in archive.getmembers() if member.isfile()}
    assert zip_members == tar_members
    assert required - {f"figures/figure-{number}" for number in range(1, 5)} <= zip_members
    for number in range(1, 5):
        assert any(
            member.startswith(f"figures/figure-{number}-") and member.endswith(".pdf")
            for member in zip_members
        )


def test_generated_tex_has_launch_order_and_standard_abstract() -> None:
    tex = (ARXIV / "main.tex").read_text(encoding="utf-8")
    assert (
        "\\begin{abstract}\nAutonomous chemistry needs an experimental regime in which"
        in tex
    )
    assert "\\subsection{Abstract}" not in tex
    assert "\\section{1. Introduction}" in tex
    assert "\\section{10. Conclusion}" in tex
    assert "\\fancyhead[L]{\\footnotesize Programmable Chemical Worlds}" in tex
    positions = [tex.index(f"figures/figure-{number}-") for number in range(1, 5)]
    assert positions == sorted(positions)
    assert "figure-1-system-overview.pdf" in tex
    assert "figure-4-forks-and-agent.pdf" in tex
    assert "\\titleformat{\\section}" not in tex or "{\\thesection.}" not in tex


def test_release_manifest_records_completed_p0_gates(tmp_path: Path) -> None:
    manifest = json.loads((RELEASE / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["paper"]["working_title"] == (
        "ChemWorld: A Programmable Virtual Instrument for Measuring Experimental Process Profiles"
    )
    if manifest["publication_ready"]:
        assert manifest["status"] == "publication_ready"
        assert manifest["gates"]["raw_data_archive"].startswith("passed_")
        assert manifest["gates"]["author_metadata"].startswith("passed_")
        assert "g0_raw_data_archive" in manifest["evidence"]
    else:
        assert manifest["status"] == "building_not_publication_ready"
        assert manifest["gates"]["raw_data_archive"] == "open"
        assert manifest["gates"]["author_metadata"] == "open"
    derived = json.loads((RELEASE / "arxiv-v1-derived-data.json").read_text(encoding="utf-8"))
    derived_hash = derived["derived_data_sha256"]
    assert manifest["evidence"]["frozen_derived_data"]["derived_data_sha256"] == derived_hash
    assert manifest["gates"]["frozen_derived_table_and_figures"] == (
        f"passed_derived_{derived_hash}"
    )
    fvl = manifest["evidence"]["work_i_fvl_incremental_evidence"]
    derived_manifest = json.loads(
        (RELEASE / "arxiv-v1-derived-data.manifest.json").read_text(encoding="utf-8")
    )
    current = json.loads((ROOT / fvl["evidence_registry_path"]).read_text(encoding="utf-8"))
    verification_attestation = json.loads(
        (RELEASE / "verification-attestation.json").read_text(encoding="utf-8")
    )
    assert fvl["data_contract_sha256"] == (derived["work_i_incremental"]["data_contract_sha256"])
    assert (
        fvl["evidence_graph_sha256"] == (verification_attestation["evidence_graph"]["graph_sha256"])
    )
    assert (
        fvl["evidence_graph_node_count"]
        == (verification_attestation["evidence_graph"]["node_count"])
    )
    assert (
        current["evidence_dag"]["nodes"]["first_paper_composition_qualification"]["artifact_state"]
        == "current"
    )
    assert fvl["work_i_fvl_nodes_current"] == fvl["work_i_fvl_node_count"] == 13
    assert fvl["latent_resolved_shadow_receipts"] == 6
    assert fvl["latent_unresolved_shadow_receipts"] == 30
    assert fvl["latent_complete_case_substitution_used"] is False
    assert (
        manifest["evidence"]["frozen_derived_data"]["manifest_sha256"]
        == (derived_manifest["manifest_sha256"])
    )
    assert manifest["gates"]["work_i_fvl_release_binding"].startswith("passed_13_of_13")
    assert manifest["gates"]["latent_terminal_primary_analysis"].startswith("blocked_")
    data_card = (RELEASE / manifest["data_card"]).read_text(encoding="utf-8")
    assert "6; 30 remain unresolved" in data_card
    assert "Complete-case substitution is forbidden" in data_card
    assert manifest["gates"]["final_claim_audit"].startswith("passed_")
    # This benchmark release manifest is a preserved Work I data-release record.
    # The current first-paper PDF/source binding is verified independently above
    # through the arXiv build manifest and must not rewrite the historical gate.
    assert manifest["gates"]["standard_arxiv_render"].startswith("passed_two_column_")

    pending = json.loads((ARXIV / "release-metadata.pending.json").read_text(encoding="utf-8"))
    pending_blockers = finalizer.validate_release_metadata(pending)
    assert "status must equal ready" in pending_blockers
    assert "at least one author is required" in pending_blockers
    assert "archive.publicly_resolvable must be explicitly true" in pending_blockers

    ready = {
        "schema_version": finalizer.SCHEMA,
        "status": "ready",
        "authors": [
            {
                "name": "Jane Q. Scientist",
                "affiliation_ids": ["1"],
                "corresponding": True,
                "email": "jane.scientist@university.edu",
                "orcid": "0000-0002-1825-0097",
            }
        ],
        "affiliations": [
            {
                "id": "1",
                "name": "Institute of Molecular Systems, Research City, Country",
            }
        ],
        "archive": {
            "provider": "Zenodo",
            "identifier": "10.5281/zenodo.12345678",
            "url": "https://doi.org/10.5281/zenodo.12345678",
            "publicly_resolvable": True,
            "raw_file_index_sha256": finalizer.EXPECTED_RAW_INDEX_SHA256,
            "byte_count": finalizer.EXPECTED_RAW_BYTE_COUNT,
        },
    }
    assert finalizer.validate_release_metadata(ready) == []
    manuscript = (ROOT / "paper/experimental_intelligence_v1_manuscript.md").read_text(
        encoding="utf-8"
    )
    injected = finalizer.inject_manuscript_metadata(manuscript, ready)
    assert "pdf_author: 'Jane Q. Scientist'" in injected
    assert "  - name: 'Jane Q. Scientist'" in injected
    assert "    affiliation_markers: '1,*'" in injected
    assert "affiliation:" in injected
    assert "correspondence: 'jane.scientist@university.edu'" in injected
    assert "author_block:" not in injected
    assert "publicly archived by Zenodo" in injected
    assert "permits inspection of the raw execution records" in injected
    assert "SHA-256" not in injected
    assert "versioned release manifest" not in injected
    assert finalizer.inject_manuscript_metadata(injected, ready) == injected
    rendered_readme = finalizer.render_release_readme(
        (RELEASE / "README.md").read_text(encoding="utf-8"), ready
    )
    assert "publication package finalized and externally archived" in rendered_readme
    assert "[10.5281/zenodo.12345678]" in rendered_readme
    finalized = finalizer.finalized_manifest(manifest, ready)
    assert finalized["publication_ready"] is True
    assert finalized["status"] == "publication_ready"
    assert finalized["evidence"]["g0_raw_data_archive"]["file_count"] == 1441

    invalid = copy.deepcopy(ready)
    invalid["authors"][0]["orcid"] = "0000-0002-1825-0098"
    invalid["archive"]["byte_count"] -= 1
    invalid_blockers = finalizer.validate_release_metadata(invalid)
    assert "authors[0].orcid has invalid syntax or checksum" in invalid_blockers
    assert "archive.byte_count does not match the frozen G0 byte count" in invalid_blockers

    expected_preflight_blockers = []
    if importlib.util.find_spec("markdown") is None:
        expected_preflight_blockers.append(
            "Python package 'markdown' is unavailable; run with "
            "`uv run --extra paper python paper/tools/finalize_arxiv_release.py ...`"
        )
    assert finalizer.apply_preflight_blockers() == expected_preflight_blockers
    generated = tmp_path / "generated"
    generated.mkdir()
    original = generated / "artifact.pdf"
    original.write_bytes(b"original-pdf")
    snapshot = finalizer._snapshot_generated_files((generated,))
    original.write_bytes(b"partial-build")
    created = generated / "partial-source.zip"
    created.write_bytes(b"partial")
    finalizer._restore_generated_files(snapshot, (generated,))
    assert original.read_bytes() == b"original-pdf"
    assert not created.exists()

    unsafe_zip = tmp_path / "unsafe-source.zip"
    with zipfile.ZipFile(unsafe_zip, mode="w") as archive:
        archive.writestr("../escape.tex", "unsafe")
    try:
        finalizer._extract_verified_source_zip(unsafe_zip, tmp_path / "extracted")
    except RuntimeError as exc:
        assert "unsafe or unexpected arXiv ZIP member" in str(exc)
    else:
        raise AssertionError("path-traversing arXiv source member was accepted")

    zip_archive = tmp_path / "source.zip"
    with zipfile.ZipFile(zip_archive, mode="w") as archive:
        archive.writestr("main.tex", "zip-content")
    tar_archive = tmp_path / "source.tar.gz"
    with tarfile.open(tar_archive, mode="w:gz") as archive:
        content = b"tar-content"
        info = tarfile.TarInfo("main.tex")
        info.size = len(content)
        archive.addfile(info, io.BytesIO(content))
    assert finalizer._archive_member_hashes(zip_archive) != (
        finalizer._archive_member_hashes(tar_archive)
    )
