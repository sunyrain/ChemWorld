"""Deterministic, leakage-aware image observations for future VLM pilots."""

from __future__ import annotations

import hashlib
import json
import math
import re
from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Literal

from chemworld.agents.interaction import AgentDecisionContext
from chemworld.agents.multimodal import PublicImageArtifact
from chemworld.data.logging import to_builtin

VLM_OBSERVATION_CONTRACT_VERSION = "chemworld-vlm-observation-0.1"
VLMModality = Literal["numeric_only", "image_only", "image_plus_numeric"]
VLMDisclosure = Literal["assigned", "unassigned", "masked"]

_PACKET_KINDS = {
    "gc_chromatogram",
    "hplc_chromatogram",
    "ir_spectrum",
    "nmr_1h_spectrum",
    "ph_meter_signal",
    "uvvis_spectrum",
}


@dataclass(frozen=True)
class SpectrumRenderSpec:
    """Canonical raster layout whose full state participates in the hash."""

    contract_version: str = VLM_OBSERVATION_CONTRACT_VERSION
    width_px: int = 960
    height_px: int = 640
    margin_left_px: int = 92
    margin_right_px: int = 36
    margin_top_px: int = 58
    margin_bottom_px: int = 82
    background_rgb: tuple[int, int, int] = (255, 255, 255)
    axes_rgb: tuple[int, int, int] = (28, 36, 48)
    grid_rgb: tuple[int, int, int] = (224, 229, 236)
    curve_rgb: tuple[int, int, int] = (21, 101, 192)
    annotation_rgb: tuple[int, int, int] = (176, 55, 43)
    curve_width_px: int = 3
    png_compress_level: int = 9

    def __post_init__(self) -> None:
        if self.width_px < 320 or self.height_px < 240:
            raise ValueError("render dimensions are too small for an auditable spectrum")
        if self.curve_width_px <= 0 or not 0 <= self.png_compress_level <= 9:
            raise ValueError("invalid render line width or PNG compression level")

    @property
    def contract_hash(self) -> str:
        return _digest(asdict(self))


@dataclass(frozen=True)
class VLMObservationBundle:
    """One decision's conditioned text context and referenced public images."""

    contract_version: str
    decision_id: str
    modality: VLMModality
    disclosure: VLMDisclosure
    prompt_context: dict[str, Any]
    images: tuple[PublicImageArtifact, ...]
    manifest_hash: str

    def to_manifest(self) -> dict[str, Any]:
        return {
            "contract_version": self.contract_version,
            "decision_id": self.decision_id,
            "modality": self.modality,
            "disclosure": self.disclosure,
            "images": [image.to_dict() for image in self.images],
            "manifest_hash": self.manifest_hash,
        }


@dataclass(frozen=True)
class _SelectedPacket:
    spectrum_id: str
    source: Literal["current", "historical"]
    channel: str
    packet: dict[str, Any]


@dataclass(frozen=True)
class _Series:
    kind: str
    x: tuple[float, ...]
    y: tuple[float, ...]
    x_label: str
    y_label: str
    reverse_x: bool


def prepare_vlm_observation(
    context: AgentDecisionContext | Mapping[str, Any],
    *,
    artifact_root: str | Path,
    decision_id: str,
    modality: VLMModality,
    disclosure: VLMDisclosure,
    render_spec: SpectrumRenderSpec | None = None,
) -> VLMObservationBundle:
    """Condition one public decision context without preloading spectrum history.

    Only ``latest_spectra`` and the already retrieved
    ``requested_historical_spectrum`` can produce images.  The catalog is metadata
    only and is deliberately never dereferenced here.
    """

    if modality not in {"numeric_only", "image_only", "image_plus_numeric"}:
        raise ValueError(f"unsupported modality={modality!r}")
    if disclosure not in {"assigned", "unassigned", "masked"}:
        raise ValueError(f"unsupported disclosure={disclosure!r}")
    if not decision_id.strip():
        raise ValueError("decision_id must be non-empty")

    raw_context = (
        context.to_dict() if isinstance(context, AgentDecisionContext) else to_builtin(context)
    )
    conditioned = _condition_numeric_context(raw_context, disclosure=disclosure)
    spec = render_spec or SpectrumRenderSpec()
    images: list[PublicImageArtifact] = []
    selected = select_public_spectrum_packets(raw_context, decision_id=decision_id)

    if modality != "numeric_only" and disclosure != "masked":
        for item in selected:
            images.append(
                render_public_spectrum_packet(
                    item.packet,
                    artifact_root=artifact_root,
                    spectrum_id=item.spectrum_id,
                    source=item.source,
                    channel=item.channel,
                    disclosure=disclosure,
                    render_spec=spec,
                )
            )

    image_metadata = [image.to_dict() for image in images]
    observation_manifest = {
        "contract_version": VLM_OBSERVATION_CONTRACT_VERSION,
        "decision_id": decision_id,
        "modality": modality,
        "disclosure": disclosure,
        "image_artifacts": image_metadata,
        "history_policy": "catalog_only_until_explicit_id_request",
        "private_reasoning_retained": False,
    }
    if modality == "image_only":
        conditioned = _image_only_context(conditioned, images)
    conditioned["vlm_observation"] = observation_manifest
    manifest_hash = _digest(observation_manifest)
    return VLMObservationBundle(
        contract_version=VLM_OBSERVATION_CONTRACT_VERSION,
        decision_id=decision_id,
        modality=modality,
        disclosure=disclosure,
        prompt_context=conditioned,
        images=tuple(images),
        manifest_hash=manifest_hash,
    )


def select_public_spectrum_packets(
    context: AgentDecisionContext | Mapping[str, Any],
    *,
    decision_id: str,
) -> tuple[_SelectedPacket, ...]:
    """Select current and explicitly retrieved historical packets only."""

    raw = context.to_dict() if isinstance(context, AgentDecisionContext) else to_builtin(context)
    selected: list[_SelectedPacket] = []
    latest = raw.get("latest_spectra", {})
    requested = raw.get("requested_historical_spectrum", {})
    current_base = (
        str(latest.get("spectrum_id") or f"{decision_id}-current")
        if isinstance(latest, dict)
        else f"{decision_id}-current"
    )
    historical_base = (
        str(requested.get("spectrum_id") or f"{decision_id}-historical")
        if isinstance(requested, dict)
        else f"{decision_id}-historical"
    )
    for channel, packet in _extract_packets(latest):
        selected.append(
            _SelectedPacket(
                spectrum_id=_channel_spectrum_id(current_base, channel),
                source="current",
                channel=channel,
                packet=packet,
            )
        )
    for channel, packet in _extract_packets(requested):
        selected.append(
            _SelectedPacket(
                spectrum_id=_channel_spectrum_id(historical_base, channel),
                source="historical",
                channel=channel,
                packet=packet,
            )
        )
    return tuple(selected)


def render_public_spectrum_packet(
    packet: Mapping[str, Any],
    *,
    artifact_root: str | Path,
    spectrum_id: str,
    source: Literal["current", "historical"],
    channel: str,
    disclosure: Literal["assigned", "unassigned"],
    render_spec: SpectrumRenderSpec | None = None,
) -> PublicImageArtifact:
    """Render one public signal packet to a deterministic PNG artifact."""

    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError as exc:  # pragma: no cover - exercised by readiness audit
        raise RuntimeError("Pillow is required; install ChemWorld with the 'vlm' extra") from exc

    spec = render_spec or SpectrumRenderSpec()
    public_packet = to_builtin(packet)
    if disclosure == "unassigned":
        public_packet = _strip_assignments(public_packet)
    series = _series_from_packet(public_packet)
    signal_payload = {"kind": series.kind, "x": series.x, "y": series.y}
    signal_sha256 = _digest(signal_payload)
    public_packet_sha256 = _digest(public_packet)

    image = Image.new("RGB", (spec.width_px, spec.height_px), spec.background_rgb)
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    left = spec.margin_left_px
    right = spec.width_px - spec.margin_right_px
    top = spec.margin_top_px
    bottom = spec.height_px - spec.margin_bottom_px

    for index in range(6):
        fraction = index / 5
        x_pixel = round(left + fraction * (right - left))
        y_pixel = round(top + fraction * (bottom - top))
        draw.line((x_pixel, top, x_pixel, bottom), fill=spec.grid_rgb, width=1)
        draw.line((left, y_pixel, right, y_pixel), fill=spec.grid_rgb, width=1)
    draw.rectangle((left, top, right, bottom), outline=spec.axes_rgb, width=2)

    x_min, x_max = min(series.x), max(series.x)
    y_min, y_max = min(series.y), max(series.y)
    if math.isclose(x_min, x_max):
        x_min, x_max = x_min - 0.5, x_max + 0.5
    if math.isclose(y_min, y_max):
        y_min, y_max = y_min - 0.5, y_max + 0.5
    y_padding = 0.06 * (y_max - y_min)
    y_min -= y_padding
    y_max += y_padding

    def project_x(value: float) -> float:
        fraction = (value - x_min) / (x_max - x_min)
        if series.reverse_x:
            fraction = 1.0 - fraction
        return left + fraction * (right - left)

    def project_y(value: float) -> float:
        return bottom - (value - y_min) / (y_max - y_min) * (bottom - top)

    points = [(project_x(x), project_y(y)) for x, y in zip(series.x, series.y, strict=True)]
    if len(points) == 1:
        point_x, point_y = points[0]
        draw.ellipse((point_x - 3, point_y - 3, point_x + 3, point_y + 3), fill=spec.curve_rgb)
    else:
        draw.line(points, fill=spec.curve_rgb, width=spec.curve_width_px, joint="curve")

    title = f"{series.kind} | {disclosure}"
    draw.text((left, 20), title, fill=spec.axes_rgb, font=font)
    draw.text((left, bottom + 34), series.x_label, fill=spec.axes_rgb, font=font)
    draw.text((8, top), series.y_label, fill=spec.axes_rgb, font=font)
    draw.text(
        (left, bottom + 10),
        _number_label(x_max if series.reverse_x else x_min),
        fill=spec.axes_rgb,
        font=font,
    )
    right_label = _number_label(x_min if series.reverse_x else x_max)
    draw.text((right - 56, bottom + 10), right_label, fill=spec.axes_rgb, font=font)
    draw.text((12, bottom - 8), _number_label(y_min), fill=spec.axes_rgb, font=font)
    draw.text((12, top), _number_label(y_max), fill=spec.axes_rgb, font=font)

    if disclosure == "assigned":
        for center, label in _annotations(public_packet, series.kind)[:8]:
            if center < x_min or center > x_max:
                continue
            nearest = min(range(len(series.x)), key=lambda idx: abs(series.x[idx] - center))
            annotation_x = project_x(center)
            annotation_y = project_y(series.y[nearest])
            draw.line(
                (
                    annotation_x,
                    annotation_y,
                    annotation_x,
                    max(top, annotation_y - 24),
                ),
                fill=spec.annotation_rgb,
                width=1,
            )
            draw.text(
                (annotation_x + 3, max(top, annotation_y - 34)),
                label[:24],
                fill=spec.annotation_rgb,
                font=font,
            )

    packet_identity = {
        "spectrum_id": spectrum_id,
        "source": source,
        "channel": channel,
        "disclosure": disclosure,
        "signal_sha256": signal_sha256,
        "public_packet_sha256": public_packet_sha256,
        "render_contract_hash": spec.contract_hash,
    }
    artifact_id = f"vlm-img-{_digest(packet_identity)[:24]}"
    safe_channel = _slug(channel)
    relative_path = f"vlm_images/{artifact_id}-{safe_channel}.png"
    root = Path(artifact_root).resolve()
    output_path = (root / Path(relative_path)).resolve()
    if root not in output_path.parents:
        raise ValueError("render output escaped artifact_root")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path, format="PNG", optimize=False, compress_level=spec.png_compress_level)
    image_bytes = output_path.read_bytes()
    sha256 = hashlib.sha256(image_bytes).hexdigest()
    return PublicImageArtifact(
        artifact_id=artifact_id,
        spectrum_id=spectrum_id,
        source=source,
        spectrum_kind=series.kind,
        disclosure=disclosure,
        media_type="image/png",
        width_px=spec.width_px,
        height_px=spec.height_px,
        x_axis_direction=(
            "descending_left_to_right" if series.reverse_x else "ascending_left_to_right"
        ),
        sha256=sha256,
        signal_sha256=signal_sha256,
        public_packet_sha256=public_packet_sha256,
        render_contract_hash=spec.contract_hash,
        relative_path=relative_path,
    )


def _extract_packets(payload: Any) -> list[tuple[str, dict[str, Any]]]:
    if not isinstance(payload, dict):
        return []
    kind = str(payload.get("kind", ""))
    if kind in _PACKET_KINDS:
        return [(str(payload.get("instrument_id") or kind), to_builtin(payload))]
    if kind == "final_assay_packet":
        spectra = payload.get("spectra", {})
        if not isinstance(spectra, dict):
            return []
        result: list[tuple[str, dict[str, Any]]] = []
        for channel in sorted(spectra):
            for nested_channel, packet in _extract_packets(spectra[channel]):
                result.append((str(channel or nested_channel), packet))
        return result
    result = []
    for key in ("raw_signal", "spectra"):
        nested = payload.get(key)
        if isinstance(nested, dict):
            if key == "spectra":
                for channel in sorted(nested):
                    for nested_channel, packet in _extract_packets(nested[channel]):
                        result.append((str(channel or nested_channel), packet))
            else:
                result.extend(_extract_packets(nested))
    return result


def _series_from_packet(packet: Mapping[str, Any]) -> _Series:
    kind = str(packet.get("kind", ""))
    definitions = {
        "hplc_chromatogram": (
            "time_min",
            "intensity",
            "Retention time (min)",
            "Intensity (a.u.)",
            False,
        ),
        "gc_chromatogram": (
            "time_min",
            "intensity",
            "Retention time (min)",
            "Intensity (a.u.)",
            False,
        ),
        "uvvis_spectrum": ("wavelength_nm", "absorbance", "Wavelength (nm)", "Absorbance", False),
        "ir_spectrum": (
            "wavenumber_cm-1",
            "transmittance",
            "Wavenumber (cm-1)",
            "Transmittance",
            True,
        ),
        "nmr_1h_spectrum": (
            "chemical_shift_ppm",
            "intensity",
            "Chemical shift (ppm)",
            "Intensity (a.u.)",
            True,
        ),
    }
    if kind == "ph_meter_signal":
        raw_y = packet.get("replicate_pH", [])
        if not isinstance(raw_y, Sequence) or isinstance(raw_y, (str, bytes)) or not raw_y:
            raw_y = [packet.get("pH")]
        y = _finite_series(raw_y, name="replicate_pH")
        x = tuple(float(index + 1) for index in range(len(y)))
        return _Series(kind, x, y, "Replicate", "pH", False)
    if kind not in definitions:
        raise ValueError(f"unsupported public spectrum kind={kind!r}")
    x_key, y_key, x_label, y_label, reverse_x = definitions[kind]
    x = _finite_series(packet.get(x_key), name=x_key)
    y = _finite_series(packet.get(y_key), name=y_key)
    if len(x) != len(y):
        raise ValueError(f"{x_key} and {y_key} must have equal lengths")
    return _Series(kind, x, y, x_label, y_label, reverse_x)


def _finite_series(value: Any, *, name: str) -> tuple[float, ...]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise ValueError(f"{name} must be a numeric sequence")
    if not 1 <= len(value) <= 8192:
        raise ValueError(f"{name} must contain between 1 and 8192 values")
    result = tuple(float(item) for item in value)
    if not all(math.isfinite(item) for item in result):
        raise ValueError(f"{name} contains NaN or infinity")
    return result


def _annotations(packet: Mapping[str, Any], kind: str) -> list[tuple[float, str]]:
    center_keys = {
        "hplc_chromatogram": ("retention_time_min", "center"),
        "gc_chromatogram": ("retention_time_min", "center"),
        "uvvis_spectrum": ("wavelength_nm", "center"),
        "ir_spectrum": ("wavenumber_cm-1", "center"),
        "nmr_1h_spectrum": ("chemical_shift_ppm", "center"),
    }.get(kind, ("center",))
    result: list[tuple[float, str]] = []
    peaks = packet.get("peaks", [])
    if not isinstance(peaks, list):
        return result
    for index, peak in enumerate(peaks):
        if not isinstance(peak, dict):
            continue
        center = next((peak.get(key) for key in center_keys if peak.get(key) is not None), None)
        label = next(
            (
                str(peak[key])
                for key in ("assignment", "analyte_id", "species_id", "group")
                if peak.get(key)
            ),
            f"peak {index + 1}",
        )
        if center is None:
            continue
        try:
            numeric_center = float(center)
        except (TypeError, ValueError):
            continue
        if math.isfinite(numeric_center):
            result.append((numeric_center, label))
    return result


def _condition_numeric_context(
    context: dict[str, Any], *, disclosure: VLMDisclosure
) -> dict[str, Any]:
    conditioned = to_builtin(context)
    if disclosure == "masked":
        conditioned["latest_spectra"] = {"spectrum_condition": "masked", "available": False}
        requested = conditioned.get("requested_historical_spectrum", {})
        conditioned["requested_historical_spectrum"] = {
            "spectrum_id": requested.get("spectrum_id") if isinstance(requested, dict) else None,
            "status": requested.get("status") if isinstance(requested, dict) else None,
            "spectrum_condition": "masked",
            "available": False,
        }
        return conditioned
    if disclosure == "unassigned":
        for key in ("latest_spectra", "requested_historical_spectrum"):
            conditioned[key] = _strip_assignments(conditioned.get(key, {}))
    for key in ("latest_spectra", "requested_historical_spectrum"):
        packet = conditioned.get(key)
        if isinstance(packet, dict) and packet:
            packet["spectrum_condition"] = disclosure
    return conditioned


def _strip_assignments(value: Any) -> Any:
    if isinstance(value, dict):
        result: dict[str, Any] = {}
        for raw_key, nested in value.items():
            key = str(raw_key)
            normalized = key.lower()
            if normalized in {"species_id", "analyte_id", "group", "identity", "metadata"}:
                continue
            if normalized == "assignments":
                result[key] = []
            elif normalized == "assignment":
                result[key] = "unassigned"
            else:
                result[key] = _strip_assignments(nested)
        return result
    if isinstance(value, list):
        return [_strip_assignments(item) for item in value]
    return to_builtin(value)


def _image_only_context(
    context: dict[str, Any], images: Sequence[PublicImageArtifact]
) -> dict[str, Any]:
    current = [image.artifact_id for image in images if image.source == "current"]
    historical = [image.artifact_id for image in images if image.source == "historical"]
    requested = context.get("requested_historical_spectrum", {})
    context["latest_spectra"] = {
        "spectrum_condition": context.get("latest_spectra", {}).get("spectrum_condition"),
        "available": bool(current),
        "image_artifact_ids": current,
    }
    context["requested_historical_spectrum"] = {
        "spectrum_id": requested.get("spectrum_id") if isinstance(requested, dict) else None,
        "status": requested.get("status") if isinstance(requested, dict) else None,
        "spectrum_condition": requested.get("spectrum_condition")
        if isinstance(requested, dict)
        else None,
        "available": bool(historical),
        "image_artifact_ids": historical,
    }
    return context


def _channel_spectrum_id(base: str, channel: str) -> str:
    return f"{base}:{channel}" if channel and channel not in base else base


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9._-]+", "-", value).strip("-.").lower()
    return slug or "spectrum"


def _number_label(value: float) -> str:
    return f"{value:.4g}"


def _digest(value: Any) -> str:
    encoded = json.dumps(
        to_builtin(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


__all__ = [
    "VLM_OBSERVATION_CONTRACT_VERSION",
    "SpectrumRenderSpec",
    "VLMDisclosure",
    "VLMModality",
    "VLMObservationBundle",
    "prepare_vlm_observation",
    "render_public_spectrum_packet",
    "select_public_spectrum_packets",
]
