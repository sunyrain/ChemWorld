"""Bind the final Work I manuscript captions to six publication figures and 18 assets."""

# ruff: noqa: E402

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections.abc import Mapping
from copy import deepcopy
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.audit_work_i_publication_figures import audit_publication_figures

MANUSCRIPT_PATH = Path("paper/experimental_intelligence_v1_manuscript.md")
DISPLAY_ITEMS_PATH = Path("paper/experimental_intelligence_v1_display_items.md")
PUBLICATION_DIR = Path("paper/figures/experimental-intelligence-v1/publication")
LEGACY_AUDIT_PATH = PUBLICATION_DIR / "figure-publication-audit-v0.1.json"
SCRIPT_PATH = Path("scripts/audit_work_i_figure_integration.py")
MANIFEST_PATH = Path(
    "paper/figures/experimental-intelligence-v1/"
    "work-i-publication-figure-manifest-v0.1.json"
)

FIGURES = (
    ("F1", "figure-1-apparatus-world-forks", "ChemWorld apparatus and controlled world forks."),
    (
        "F2",
        "figure-2-known-policy-validity",
        "Known policies qualify the experimental-process profile.",
    ),
    (
        "F3",
        "figure-3-terminal-policy",
        "Lifecycle completion does not specify terminal policy.",
    ),
    (
        "F4",
        "figure-4-compiled-controls",
        "Compiled controls separate outcome, prediction, calibration and claims.",
    ),
    (
        "F5",
        "figure-5-complete-lifecycles",
        "Primitive-control agents expose complete experimental lifecycles.",
    ),
    (
        "F6",
        "figure-6-fresh-trajectories",
        "Fresh trajectories reveal process structure omitted by endpoints.",
    ),
)

EVIDENCE_TITLES = {
    "F2": "Known policies validate the experimental-agency profile",
}


class FigureIntegrationError(RuntimeError):
    """Raised when the final captions, references, or assets diverge."""


def _read_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise FigureIntegrationError(f"cannot read JSON object: {path}") from exc
    if not isinstance(payload, dict):
        raise FigureIntegrationError(f"JSON root must be an object: {path}")
    return payload


def _file_sha256(path: Path) -> str:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError as exc:
        raise FigureIntegrationError(f"cannot read bound file: {path}") from exc


def manifest_sha256(payload: Mapping[str, Any]) -> str:
    """Return the canonical digest after excluding the embedded self-hash."""

    unhashed = deepcopy(dict(payload))
    unhashed.pop("manifest_sha256", None)
    return hashlib.sha256(
        json.dumps(
            unhashed,
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()


def _json_text(payload: Mapping[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def _ordered_positions(text: str, needles: list[str], label: str) -> list[int]:
    positions: list[int] = []
    for needle in needles:
        count = text.count(needle)
        if count != 1:
            raise FigureIntegrationError(
                f"{label} must contain exactly one {needle!r}; found {count}"
            )
        positions.append(text.index(needle))
    if positions != sorted(positions):
        raise FigureIntegrationError(f"{label} figure order differs from F1-F6")
    return positions


def build_integration_manifest(root: Path = ROOT) -> dict[str, Any]:
    """Build the canonical final Work I figure inventory without rerunning analyses."""

    resolved = root.resolve()
    manuscript = (resolved / MANUSCRIPT_PATH).read_text(encoding="utf-8")
    display_items = (resolved / DISPLAY_ITEMS_PATH).read_text(encoding="utf-8")
    legacy_audit = _read_json(resolved / LEGACY_AUDIT_PATH)
    rebuilt_audit = audit_publication_figures(resolved)
    if legacy_audit != rebuilt_audit or legacy_audit.get("status") != "PASS":
        raise FigureIntegrationError("committed publication-asset audit is stale or failed")

    caption_needles = [f"\\caption{{\\textbf{{{title}}}" for _, _, title in FIGURES]
    reference_needles = [
        "figures/experimental-intelligence-v1/publication/" + stem + ".pdf"
        for _, stem, _ in FIGURES
    ]
    display_needles = [
        f"**Figure {order} | {title}**"
        for order, (_, _, title) in enumerate(FIGURES, 1)
    ]
    caption_positions = _ordered_positions(manuscript, caption_needles, "manuscript captions")
    reference_positions = _ordered_positions(manuscript, reference_needles, "manuscript references")
    _ordered_positions(display_items, display_needles, "display-item legends")
    if any(
        reference > caption
        for reference, caption in zip(reference_positions, caption_positions, strict=True)
    ):
        raise FigureIntegrationError("a manuscript figure caption precedes its publication asset")

    audit_rows = {str(row["figure_id"]): row for row in rebuilt_audit["figures"]}
    figure_rows: list[dict[str, Any]] = []
    source_paths = [MANUSCRIPT_PATH, DISPLAY_ITEMS_PATH, LEGACY_AUDIT_PATH, SCRIPT_PATH]
    asset_count = 0
    for order, (figure_id, stem, title) in enumerate(FIGURES, 1):
        audit_row = audit_rows.get(figure_id)
        if not isinstance(audit_row, Mapping):
            raise FigureIntegrationError(f"publication audit lacks {figure_id}")
        manifest_path = PUBLICATION_DIR / f"{stem}.manifest.json"
        per_figure = _read_json(resolved / manifest_path)
        if (
            per_figure.get("manifest_sha256") != audit_row.get("manifest_sha256")
            or per_figure.get("title")
            != EVIDENCE_TITLES.get(figure_id, title.removesuffix("."))
            or audit_row.get("status") != "PASS"
        ):
            raise FigureIntegrationError(f"per-figure identity or audit changed: {figure_id}")
        outputs = [dict(row) for row in audit_row["outputs"]]
        if [row.get("format") for row in outputs] != ["svg", "pdf", "png"]:
            raise FigureIntegrationError(f"publication formats changed: {figure_id}")
        asset_count += len(outputs)
        source_paths.append(manifest_path)
        figure_rows.append(
            {
                "figure_id": figure_id,
                "order": order,
                "title": title,
                "stem": stem,
                "owner_task": audit_row["owner_task"],
                "original_owner_task": audit_row["original_owner_task"],
                "manifest_path": manifest_path.as_posix(),
                "manifest_sha256": per_figure["manifest_sha256"],
                "manifest_status": per_figure["status"],
                "pending_result_panels": per_figure.get("pending_result_panels", []),
                "manuscript_reference": reference_needles[order - 1],
                "outputs": outputs,
            }
        )

    if asset_count != 18:
        raise FigureIntegrationError(f"expected 18 canonical assets; found {asset_count}")
    f3 = figure_rows[2]
    f3_manifest = _read_json(resolved / Path(str(f3["manifest_path"])))
    f3_result = f3_manifest.get("latent_result_summary")
    if not isinstance(f3_result, Mapping) or (
        f3["manifest_status"] != "frozen_latent_gate_failure_display"
        or f3["pending_result_panels"] != []
        or f3_result.get("main_text_eligible") is not False
        or f3_result.get("point_estimates_withheld") is not True
        or f3_result.get("resolved_shadow_receipts") != 6
        or f3_result.get("unresolved_shadow_receipts") != 30
    ):
        raise FigureIntegrationError("F3 latent-result disposition is incomplete")

    manifest: dict[str, Any] = {
        "schema_id": "chemworld.work_i_publication_figure_manifest",
        "schema_version": "0.1.0",
        "manifest_id": "work-i-final-six-figure-inventory-v0.1",
        "status": "PASS",
        "owner_task": "W1-P09",
        "canonical_figure_count": 6,
        "canonical_asset_count": 18,
        "caption_titles": [title for _, _, title in FIGURES],
        "source_bindings": [
            {"path": path.as_posix(), "sha256": _file_sha256(resolved / path)}
            for path in source_paths
        ],
        "figures": figure_rows,
        "latent_terminal_disposition": {
            "figure_id": "F3",
            "formal_gate_passed": False,
            "main_text_point_estimates_reported": False,
            "resolved_shadow_receipts": 6,
            "unresolved_shadow_receipts": 30,
            "finite_population_bounds_reported": True,
        },
        "legacy_arxiv_manifest_disposition": "superseded_migration_input_preserved",
        "claim_boundary": {
            "scientific_analyses_rerun": False,
            "publication_assets_recounted_from_per_figure_manifests": True,
            "manuscript_and_display_caption_order_exact": True,
            "legacy_unmanifested_assets_are_canonical": False,
        },
    }
    manifest["manifest_sha256"] = manifest_sha256(manifest)
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = build_integration_manifest(ROOT)
    rendered = _json_text(manifest)
    path = ROOT / MANIFEST_PATH
    if args.check:
        if path.read_text(encoding="utf-8") != rendered:
            raise SystemExit("committed Work I figure manifest differs from deterministic rebuild")
    else:
        path.write_text(rendered, encoding="utf-8", newline="\n")
    print(
        json.dumps(
            {
                "canonical_assets": manifest["canonical_asset_count"],
                "canonical_figures": manifest["canonical_figure_count"],
                "check": bool(args.check),
                "manifest_sha256": manifest["manifest_sha256"],
                "status": manifest["status"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
