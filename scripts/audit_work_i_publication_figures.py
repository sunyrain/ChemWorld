"""Audit the six canonical Work I publication figures without rewriting them."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
import xml.etree.ElementTree as ET
from collections.abc import Mapping
from copy import deepcopy
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FIGURE_SYSTEM_PATH = Path("paper/figures/experimental-intelligence-v1/figure-system-v0.1.json")
PUBLICATION_DIR = Path("paper/figures/experimental-intelligence-v1/publication")
SCRIPT_PATH = Path("scripts/audit_work_i_publication_figures.py")
REPORT_JSON_PATH = PUBLICATION_DIR / "figure-publication-audit-v0.1.json"
REPORT_MD_PATH = PUBLICATION_DIR / "figure-publication-audit-v0.1.md"

EXPECTED_FIGURE_TASKS = {
    "F1": "W1-P02",
    "F2": "W1-P03",
    "F3": "W1-P04",
    "F4": "W1-P05",
    "F5": "W1-P06",
    "F6": "W1-P07",
}
EXPECTED_FORMATS = ("svg", "pdf", "png")
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
PDF_POINTS_PER_INCH = 72.0
PNG_DPI = 300


class PublicationFigureAuditError(RuntimeError):
    """Raised when a canonical publication figure fails closed."""


def _read_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PublicationFigureAuditError(f"cannot read JSON object: {path}") from exc
    if not isinstance(payload, dict):
        raise PublicationFigureAuditError(f"JSON root must be an object: {path}")
    return payload


def _mapping(payload: Mapping[str, Any], key: str) -> Mapping[str, Any]:
    value = payload.get(key)
    if not isinstance(value, Mapping):
        raise PublicationFigureAuditError(f"{key} must be an object")
    return value


def _mapping_rows(payload: Mapping[str, Any], key: str) -> list[Mapping[str, Any]]:
    value = payload.get(key)
    if not isinstance(value, list) or any(not isinstance(row, Mapping) for row in value):
        raise PublicationFigureAuditError(f"{key} must be a list of objects")
    return value


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError as exc:
        raise PublicationFigureAuditError(f"cannot read bound file: {path}") from exc
    return digest.hexdigest()


def _canonical_sha256(payload: Mapping[str, Any], hash_field: str) -> str:
    unhashed = deepcopy(dict(payload))
    unhashed.pop(hash_field, None)
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


def validate_bound_file(
    path: Path, expected_sha256: str, expected_bytes: int | None = None
) -> None:
    """Validate one immutable file binding and fail with its concrete path."""

    if not path.is_file():
        raise PublicationFigureAuditError(f"bound file is missing: {path}")
    if expected_bytes is not None and path.stat().st_size != expected_bytes:
        raise PublicationFigureAuditError(f"bound file byte count mismatch: {path}")
    if _file_sha256(path) != expected_sha256:
        raise PublicationFigureAuditError(f"bound file hash mismatch: {path}")


def _float_attribute(value: str | None, suffix: str, label: str) -> float:
    if value is None or not value.endswith(suffix):
        raise PublicationFigureAuditError(f"SVG {label} lacks the required {suffix} unit")
    try:
        return float(value[: -len(suffix)])
    except ValueError as exc:
        raise PublicationFigureAuditError(f"SVG {label} is not numeric") from exc


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _audit_svg(
    path: Path, expected_width_points: float, expected_height_points: float
) -> dict[str, Any]:
    try:
        root = ET.parse(path).getroot()
    except (OSError, ET.ParseError) as exc:
        raise PublicationFigureAuditError(f"invalid SVG: {path}") from exc
    if _local_name(root.tag) != "svg":
        raise PublicationFigureAuditError(f"SVG root element is invalid: {path}")
    width_points = _float_attribute(root.get("width"), "pt", "width")
    height_points = _float_attribute(root.get("height"), "pt", "height")
    try:
        view_box = [float(value) for value in str(root.get("viewBox", "")).split()]
    except ValueError as exc:
        raise PublicationFigureAuditError(f"SVG viewBox is invalid: {path}") from exc
    if len(view_box) != 4:
        raise PublicationFigureAuditError(f"SVG viewBox is incomplete: {path}")
    text_count = sum(_local_name(node.tag) == "text" for node in root.iter())
    image_count = sum(_local_name(node.tag) == "image" for node in root.iter())
    if text_count == 0:
        raise PublicationFigureAuditError(f"SVG text is outlined or absent: {path}")
    if image_count != 0:
        raise PublicationFigureAuditError(f"SVG contains embedded raster images: {path}")
    tolerance = 0.01
    if (
        abs(width_points - expected_width_points) > tolerance
        or abs(height_points - expected_height_points) > tolerance
        or abs(view_box[2] - expected_width_points) > tolerance
        or abs(view_box[3] - expected_height_points) > tolerance
    ):
        raise PublicationFigureAuditError(
            f"SVG final dimensions differ from the figure system: {path}"
        )
    return {
        "embedded_image_count": image_count,
        "height_points": height_points,
        "text_element_count": text_count,
        "text_is_editable": True,
        "vector_only": True,
        "view_box": view_box,
        "width_points": width_points,
    }


def _png_chunks(raw: bytes, path: Path) -> list[tuple[bytes, bytes]]:
    if not raw.startswith(PNG_SIGNATURE):
        raise PublicationFigureAuditError(f"invalid PNG signature: {path}")
    chunks: list[tuple[bytes, bytes]] = []
    offset = len(PNG_SIGNATURE)
    while offset + 12 <= len(raw):
        length = struct.unpack(">I", raw[offset : offset + 4])[0]
        chunk_type = raw[offset + 4 : offset + 8]
        end = offset + 12 + length
        if end > len(raw):
            raise PublicationFigureAuditError(f"truncated PNG chunk: {path}")
        chunks.append((chunk_type, raw[offset + 8 : offset + 8 + length]))
        offset = end
        if chunk_type == b"IEND":
            break
    if not chunks or chunks[-1][0] != b"IEND":
        raise PublicationFigureAuditError(f"PNG lacks IEND: {path}")
    return chunks


def _audit_png(
    path: Path,
    expected_width_pixels: int,
    expected_height_pixels: int,
    expected_dpi: int,
) -> dict[str, Any]:
    raw = path.read_bytes()
    chunks = _png_chunks(raw, path)
    ihdr_rows = [data for chunk_type, data in chunks if chunk_type == b"IHDR"]
    phys_rows = [data for chunk_type, data in chunks if chunk_type == b"pHYs"]
    if len(ihdr_rows) != 1 or len(ihdr_rows[0]) != 13:
        raise PublicationFigureAuditError(f"PNG IHDR is invalid: {path}")
    width, height = struct.unpack(">II", ihdr_rows[0][:8])
    if (width, height) != (expected_width_pixels, expected_height_pixels):
        raise PublicationFigureAuditError(
            f"PNG final dimensions differ from the figure system: {path}"
        )
    if len(phys_rows) != 1 or len(phys_rows[0]) != 9:
        raise PublicationFigureAuditError(f"PNG lacks one physical-resolution chunk: {path}")
    pixels_per_meter_x, pixels_per_meter_y, unit = struct.unpack(">IIB", phys_rows[0])
    if unit != 1:
        raise PublicationFigureAuditError(f"PNG physical resolution lacks metric units: {path}")
    dpi_x = pixels_per_meter_x * 0.0254
    dpi_y = pixels_per_meter_y * 0.0254
    if abs(dpi_x - expected_dpi) > 0.05 or abs(dpi_y - expected_dpi) > 0.05:
        raise PublicationFigureAuditError(f"PNG physical resolution is not 300 dpi: {path}")
    return {
        "dpi_x": round(dpi_x, 4),
        "dpi_y": round(dpi_y, 4),
        "height_pixels": height,
        "physical_unit": "meter",
        "pixels_per_meter_x": pixels_per_meter_x,
        "pixels_per_meter_y": pixels_per_meter_y,
        "width_pixels": width,
    }


def _audit_pdf(
    path: Path, expected_width_points: float, expected_height_points: float
) -> dict[str, Any]:
    raw = path.read_bytes()
    if not raw.startswith(b"%PDF") or b"%%EOF" not in raw[-1024:]:
        raise PublicationFigureAuditError(f"invalid PDF envelope: {path}")
    page_count = len(re.findall(rb"/Type\s*/Page\b", raw))
    media_rows = re.findall(rb"/MediaBox\s*\[([^]]+)\]", raw)
    embedded_truetype_count = raw.count(b"/FontFile2")
    if page_count != 1 or len(media_rows) != 1:
        raise PublicationFigureAuditError(f"PDF must contain one final-size page: {path}")
    try:
        media_box = [float(value) for value in media_rows[0].split()]
    except ValueError as exc:
        raise PublicationFigureAuditError(f"PDF MediaBox is invalid: {path}") from exc
    if len(media_box) != 4:
        raise PublicationFigureAuditError(f"PDF MediaBox is incomplete: {path}")
    width_points = media_box[2] - media_box[0]
    height_points = media_box[3] - media_box[1]
    if (
        abs(width_points - expected_width_points) > 0.01
        or abs(height_points - expected_height_points) > 0.01
    ):
        raise PublicationFigureAuditError(
            f"PDF page dimensions differ from the figure system: {path}"
        )
    if embedded_truetype_count == 0:
        raise PublicationFigureAuditError(f"PDF lacks embedded TrueType fonts: {path}")
    return {
        "embedded_truetype_font_stream_count": embedded_truetype_count,
        "height_points": height_points,
        "media_box": media_box,
        "page_count": page_count,
        "width_points": width_points,
    }


def _validate_system(root: Path, figure_system: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    if figure_system.get("status") != "frozen":
        raise PublicationFigureAuditError("P01 figure system is not frozen")
    if figure_system.get("system_sha256") != _canonical_sha256(figure_system, "system_sha256"):
        raise PublicationFigureAuditError("P01 figure-system self-hash mismatch")
    for binding in _mapping_rows(figure_system, "source_bindings"):
        path_value = binding.get("path")
        sha_value = binding.get("sha256")
        if not isinstance(path_value, str) or not isinstance(sha_value, str):
            raise PublicationFigureAuditError("invalid P01 source binding")
        validate_bound_file(root / path_value, sha_value)
    figures = sorted(
        _mapping_rows(figure_system, "figures"), key=lambda row: int(row.get("order", 0))
    )
    if len(figures) != 6 or [row.get("figure_id") for row in figures] != list(
        EXPECTED_FIGURE_TASKS
    ):
        raise PublicationFigureAuditError("P01 canonical six-figure inventory changed")
    for order, row in enumerate(figures, start=1):
        figure_id = str(row.get("figure_id"))
        pending_panels = row.get("pending_result_panels")
        if (
            row.get("order") != order
            or row.get("owner_task") != EXPECTED_FIGURE_TASKS[figure_id]
            or row.get("grid_template") != "two_by_two"
            or not isinstance(row.get("output_stem"), str)
            or not isinstance(pending_panels, list)
            or any(panel not in list("ABCD") for panel in pending_panels)
        ):
            raise PublicationFigureAuditError(f"P01 assignment is incomplete for {figure_id}")
    return figures


def _audit_one_figure(
    root: Path,
    spec: Mapping[str, Any],
    criteria: Mapping[str, Any],
) -> dict[str, Any]:
    figure_id = str(spec["figure_id"])
    stem = str(spec["output_stem"])
    manifest_path = PUBLICATION_DIR / f"{stem}.manifest.json"
    manifest = _read_json(root / manifest_path)
    if manifest.get("manifest_sha256") != _canonical_sha256(manifest, "manifest_sha256"):
        raise PublicationFigureAuditError(f"figure manifest self-hash mismatch: {manifest_path}")
    pending_panels = list(spec.get("pending_result_panels", []))
    expected_manifest_status = (
        "frozen_structure_pending_latent_results" if pending_panels else "frozen_render"
    )
    if (
        manifest.get("status") != expected_manifest_status
        or manifest.get("figure_id") != figure_id
        or manifest.get("owner_task") != spec.get("owner_task")
        or manifest.get("title") != spec.get("title")
    ):
        raise PublicationFigureAuditError(f"figure manifest identity differs from P01: {figure_id}")
    for binding in _mapping_rows(manifest, "source_bindings"):
        path_value = binding.get("path")
        sha_value = binding.get("sha256")
        if not isinstance(path_value, str) or not isinstance(sha_value, str):
            raise PublicationFigureAuditError(f"invalid source binding in {manifest_path}")
        validate_bound_file(root / path_value, sha_value)

    rendering = _mapping(manifest, "rendering")
    if (
        rendering.get("width_inches") != criteria["width_inches"]
        or rendering.get("height_inches") != criteria["height_inches"]
        or rendering.get("png_dpi") != criteria["png_dpi"]
        or rendering.get("svg_text_editable") is not True
        or rendering.get("pdf_fonttype") != 42
        or rendering.get("background") != "opaque_white"
        or rendering.get("deterministic_metadata") is not True
    ):
        raise PublicationFigureAuditError(f"rendering contract differs from P01/P08: {figure_id}")

    output_rows = _mapping_rows(manifest, "outputs")
    if [row.get("format") for row in output_rows] != list(EXPECTED_FORMATS):
        raise PublicationFigureAuditError(f"figure output formats or order changed: {figure_id}")
    output_audits: list[dict[str, Any]] = []
    for row in output_rows:
        suffix = str(row["format"])
        expected_path = PUBLICATION_DIR / f"{stem}.{suffix}"
        if row.get("path") != expected_path.as_posix():
            raise PublicationFigureAuditError(f"noncanonical output path for {figure_id}/{suffix}")
        sha_value = row.get("sha256")
        bytes_value = row.get("bytes")
        if not isinstance(sha_value, str) or not isinstance(bytes_value, int):
            raise PublicationFigureAuditError(f"invalid output binding for {figure_id}/{suffix}")
        absolute_path = root / expected_path
        validate_bound_file(absolute_path, sha_value, bytes_value)
        if suffix == "svg":
            properties = _audit_svg(
                absolute_path,
                float(criteria["pdf_width_points"]),
                float(criteria["pdf_height_points"]),
            )
        elif suffix == "pdf":
            properties = _audit_pdf(
                absolute_path,
                float(criteria["pdf_width_points"]),
                float(criteria["pdf_height_points"]),
            )
        else:
            if (
                row.get("pixel_width") != criteria["png_width_pixels"]
                or row.get("pixel_height") != criteria["png_height_pixels"]
                or row.get("dpi") != criteria["png_dpi"]
            ):
                raise PublicationFigureAuditError(f"PNG manifest dimensions changed: {figure_id}")
            properties = _audit_png(
                absolute_path,
                int(criteria["png_width_pixels"]),
                int(criteria["png_height_pixels"]),
                int(criteria["png_dpi"]),
            )
        output_audits.append(
            {
                "bytes": bytes_value,
                "format": suffix,
                "path": expected_path.as_posix(),
                "properties": properties,
                "sha256": sha_value,
                "status": "PASS",
            }
        )
    return {
        "figure_id": figure_id,
        "manifest_path": manifest_path.as_posix(),
        "manifest_sha256": manifest["manifest_sha256"],
        "manifest_status": manifest["status"],
        "order": spec["order"],
        "outputs": output_audits,
        "owner_task": spec["owner_task"],
        "pending_result_panels": pending_panels,
        "status": "PASS",
        "title": spec["title"],
    }


def audit_sha256(payload: Mapping[str, Any]) -> str:
    """Return the audit digest excluding its embedded self-hash."""

    return _canonical_sha256(payload, "audit_sha256")


def audit_publication_figures(root: Path = ROOT) -> dict[str, Any]:
    """Audit all six P01-assigned publication figures and return a frozen report."""

    resolved = root.resolve()
    figure_system = _read_json(resolved / FIGURE_SYSTEM_PATH)
    specs = _validate_system(resolved, figure_system)
    canvas = _mapping(figure_system, "canvas")
    width_inches = float(canvas["two_column_width"])
    height_inches = float(canvas["default_two_by_two_height"])
    criteria: dict[str, Any] = {
        "background": "opaque_white",
        "canonical_figure_count": 6,
        "height_inches": height_inches,
        "pdf_embedded_font_stream_type": "FontFile2",
        "pdf_height_points": height_inches * PDF_POINTS_PER_INCH,
        "pdf_page_count": 1,
        "pdf_width_points": width_inches * PDF_POINTS_PER_INCH,
        "png_dpi": PNG_DPI,
        "png_height_pixels": round(height_inches * PNG_DPI),
        "png_width_pixels": round(width_inches * PNG_DPI),
        "required_formats": list(EXPECTED_FORMATS),
        "svg_embedded_raster_count": 0,
        "svg_text_elements_required": True,
        "width_inches": width_inches,
    }
    figure_rows = [_audit_one_figure(resolved, spec, criteria) for spec in specs]
    canonical_asset_paths = {
        str(output["path"])
        for figure in figure_rows
        for output in figure["outputs"]
        if isinstance(output, Mapping)
    }
    legacy_assets = sorted(
        path.relative_to(resolved).as_posix()
        for path in (resolved / PUBLICATION_DIR).iterdir()
        if path.is_file()
        and path.suffix.lower() in {".svg", ".pdf", ".png"}
        and path.relative_to(resolved).as_posix() not in canonical_asset_paths
    )
    manifest_paths = [Path(str(row["manifest_path"])) for row in figure_rows]
    source_paths = [FIGURE_SYSTEM_PATH, *manifest_paths, SCRIPT_PATH]
    audit: dict[str, Any] = {
        "schema_id": "chemworld.work_i_publication_figure_audit",
        "schema_version": "0.1.0",
        "audit_id": "work-i-six-figure-publication-audit-v0.1",
        "status": "PASS",
        "owner_task": "W1-P08",
        "figure_system_sha256": figure_system["system_sha256"],
        "criteria": criteria,
        "source_bindings": [
            {"path": path.as_posix(), "sha256": _file_sha256(resolved / path)}
            for path in source_paths
        ],
        "figures": figure_rows,
        "aggregate": {
            "canonical_assets_passed": len(canonical_asset_paths),
            "canonical_assets_total": 18,
            "canonical_figures_passed": len(figure_rows),
            "canonical_figures_total": 6,
            "embedded_raster_images_in_svg": 0,
            "figures_with_300_dpi_png": 6,
            "figures_with_editable_svg_text": 6,
            "figures_with_embedded_pdf_fonts": 6,
            "figures_with_final_two_column_dimensions": 6,
            "figures_with_pending_result_panels": sum(
                bool(figure["pending_result_panels"]) for figure in figure_rows
            ),
            "legacy_unmanifested_assets_excluded": len(legacy_assets),
        },
        "legacy_unmanifested_assets": legacy_assets,
        "claim_boundary": {
            "audit_only_no_figure_rewrite": True,
            "canonical_inventory_resolved_from_frozen_p01": True,
            "legacy_unmanifested_assets_are_current_figures": False,
            "scientific_result_validation_repeated": False,
            "visual_job_or_narrative_changed": False,
        },
    }
    if audit["aggregate"] != {
        "canonical_assets_passed": 18,
        "canonical_assets_total": 18,
        "canonical_figures_passed": 6,
        "canonical_figures_total": 6,
        "embedded_raster_images_in_svg": 0,
        "figures_with_300_dpi_png": 6,
        "figures_with_editable_svg_text": 6,
        "figures_with_embedded_pdf_fonts": 6,
        "figures_with_final_two_column_dimensions": 6,
        "figures_with_pending_result_panels": 1,
        "legacy_unmanifested_assets_excluded": len(legacy_assets),
    }:
        raise PublicationFigureAuditError("global six-figure publication gate failed")
    audit["audit_sha256"] = audit_sha256(audit)
    return audit


def build_markdown_report(audit: Mapping[str, Any]) -> str:
    """Build a compact human-readable rendering of the machine audit."""

    aggregate = _mapping(audit, "aggregate")
    criteria = _mapping(audit, "criteria")
    lines = [
        "# Work I publication figure audit",
        "",
        f"Status: **{audit['status']}**  ",
        f"Audit SHA-256: `{audit['audit_sha256']}`",
        "",
        (
            "The canonical inventory is resolved from the frozen P01 figure system. "
            "No figure was rewritten."
        ),
        "",
        (
            "| Figure | Owner | Pending panels | Editable SVG text | SVG rasters | "
            "PNG | PDF fonts | Final size |"
        ),
        "| --- | --- | --- | ---: | ---: | --- | --- | --- |",
    ]
    for figure in _mapping_rows(audit, "figures"):
        outputs = {str(row["format"]): row for row in _mapping_rows(figure, "outputs")}
        svg = _mapping(outputs["svg"], "properties")
        png = _mapping(outputs["png"], "properties")
        pdf = _mapping(outputs["pdf"], "properties")
        lines.append(
            "| "
            f"{figure['figure_id']} | {figure['owner_task']} | "
            f"{', '.join(figure['pending_result_panels']) or 'none'} | "
            f"{svg['text_element_count']} | "
            f"{svg['embedded_image_count']} | {png['width_pixels']}x{png['height_pixels']} @ "
            f"{png['dpi_x']:.4f} dpi | {pdf['embedded_truetype_font_stream_count']} embedded | "
            f"{criteria['width_inches']:.2f}x{criteria['height_inches']:.1f} in |"
        )
    lines.extend(
        [
            "",
            "## Gate summary",
            "",
            f"- Canonical figures: {aggregate['canonical_figures_passed']}/6 passed.",
            f"- Canonical assets: {aggregate['canonical_assets_passed']}/18 passed.",
            "- All SVGs retain editable text and contain no embedded raster images.",
            "- All PNGs are 2124x1560 pixels with a 300 dpi physical-resolution declaration.",
            "- All PDFs are single-page 7.08x5.2 inch assets with embedded TrueType fonts.",
            (
                "- Figure 3 panels C/D remain explicitly pending L05/L06 scientific results; "
                "this does not fail the asset-property audit."
            ),
            (
                "- Legacy unmanifested assets excluded from the canonical set: "
                f"{aggregate['legacy_unmanifested_assets_excluded']}."
            ),
            "",
            (
                "This report validates publication-asset properties and immutable bindings only; "
                "it does not rerun scientific analyses."
            ),
            "",
        ]
    )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_publication_figures(ROOT)
    json_text = _json_text(audit)
    markdown_text = build_markdown_report(audit)
    if args.check:
        if (ROOT / REPORT_JSON_PATH).read_text(encoding="utf-8") != json_text:
            raise SystemExit("committed JSON audit differs from deterministic rebuild")
        if (ROOT / REPORT_MD_PATH).read_text(encoding="utf-8") != markdown_text:
            raise SystemExit("committed Markdown audit differs from deterministic rebuild")
    else:
        (ROOT / REPORT_JSON_PATH).write_text(json_text, encoding="utf-8", newline="\n")
        (ROOT / REPORT_MD_PATH).write_text(markdown_text, encoding="utf-8", newline="\n")
    print(
        json.dumps(
            {
                "audit_sha256": audit["audit_sha256"],
                "canonical_assets_passed": audit["aggregate"]["canonical_assets_passed"],
                "canonical_figures_passed": audit["aggregate"]["canonical_figures_passed"],
                "check": bool(args.check),
                "status": audit["status"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
