"""Compact public instrument signals for model prompts and browser charts."""

from __future__ import annotations

from typing import Any, Literal

SpectrumDisclosure = Literal["raw", "unassigned", "assigned"]

_AXES = (
    ("time_min", "intensity", "Retention time", "min", "Intensity", "a.u.", False),
    ("wavelength_nm", "absorbance", "Wavelength", "nm", "Absorbance", "a.u.", False),
    (
        "wavenumber_cm-1",
        "transmittance",
        "Wavenumber",
        "cm⁻¹",
        "Transmittance",
        "fraction",
        True,
    ),
    (
        "chemical_shift_ppm",
        "intensity",
        "Chemical shift",
        "ppm",
        "Intensity",
        "a.u.",
        True,
    ),
    ("x", "y", "Signal axis", "a.u.", "Response", "a.u.", False),
)


def spectral_payload(
    raw_signal: object,
    *,
    instrument: object = None,
    max_points: int = 240,
    disclosure: SpectrumDisclosure = "assigned",
) -> dict[str, Any]:
    """Return a bounded JSON-safe view of public raw instrument data."""

    if disclosure not in {"raw", "unassigned", "assigned"}:
        raise ValueError("disclosure must be raw, unassigned, or assigned")

    raw = raw_signal if isinstance(raw_signal, dict) else {}
    kind = str(raw.get("kind") or "")
    packets = raw.get("spectra") if kind == "final_assay_packet" else None
    if not isinstance(packets, dict):
        packets = {str(instrument or kind or "instrument"): raw}

    series: list[dict[str, Any]] = []
    for channel, packet in packets.items():
        if not isinstance(packet, dict):
            continue
        chart = _chart_series(
            str(channel),
            packet,
            max_points=max_points,
            disclosure=disclosure,
        )
        if chart is not None:
            series.append(chart)

    return {
        "available": bool(series),
        "disclosure": disclosure,
        "instrument": None if instrument is None else str(instrument),
        "kind": kind or None,
        "series": series,
    }


def _chart_series(
    channel: str,
    packet: dict[str, Any],
    *,
    max_points: int,
    disclosure: SpectrumDisclosure,
) -> dict[str, Any] | None:
    packet_kind = str(packet.get("kind") or channel)
    if packet_kind == "ph_meter_signal":
        values = _numbers(packet.get("replicate_pH"))
        if not values and _number(packet.get("pH")) is not None:
            values = [float(packet["pH"])]
        if not values:
            return None
        return {
            "id": channel,
            "kind": packet_kind,
            "label": "pH meter",
            "x_label": "Replicate",
            "x_unit": "index",
            "y_label": "pH",
            "y_unit": "pH",
            "reverse_x": False,
            "x": list(range(1, len(values) + 1)),
            "y": values,
            "peaks": [],
        }

    for axis_key, signal_key, x_label, x_unit, y_label, y_unit, reverse_x in _AXES:
        x_values = _numbers(packet.get(axis_key))
        y_values = _numbers(packet.get(signal_key))
        if not x_values or not y_values:
            continue
        count = min(len(x_values), len(y_values))
        x_values, y_values = _downsample(
            x_values[:count],
            y_values[:count],
            max_points=max_points,
        )
        return {
            "id": channel,
            "kind": packet_kind,
            "label": _channel_label(channel, packet_kind),
            "x_label": x_label,
            "x_unit": x_unit,
            "y_label": y_label,
            "y_unit": y_unit,
            "reverse_x": reverse_x,
            "x": x_values,
            "y": y_values,
            "peaks": _peaks(packet, disclosure=disclosure),
        }
    return None


def _peaks(
    packet: dict[str, Any],
    *,
    disclosure: SpectrumDisclosure,
) -> list[dict[str, Any]]:
    if disclosure == "raw":
        return []
    raw_peaks = packet.get("peaks") or packet.get("bands") or []
    if not isinstance(raw_peaks, list):
        return []
    peaks: list[dict[str, Any]] = []
    center_keys = (
        "center",
        "retention_time_min",
        "shift_ppm",
        "center_nm",
        "center_cm-1",
    )
    for raw_peak in raw_peaks[:16]:
        if not isinstance(raw_peak, dict):
            continue
        center = next(
            (
                _number(raw_peak.get(key))
                for key in center_keys
                if _number(raw_peak.get(key)) is not None
            ),
            None,
        )
        if center is None:
            continue
        assigned_label = str(
            raw_peak.get("assignment")
            or raw_peak.get("species_id")
            or raw_peak.get("group")
            or "unassigned"
        )
        assigned_group = str(raw_peak.get("group") or "unknown")
        peaks.append(
            {
                "center": center,
                "label": assigned_label if disclosure == "assigned" else "unassigned",
                "group": assigned_group if disclosure == "assigned" else "unknown",
                "area": _number(raw_peak.get("area")),
                "detected": bool(raw_peak.get("detected", True)),
            }
        )
    return peaks


def _channel_label(channel: str, kind: str) -> str:
    labels = {
        "hplc": "HPLC chromatogram",
        "gc": "GC chromatogram",
        "uvvis": "UV-Vis spectrum",
        "ir": "IR spectrum",
        "nmr": "¹H NMR spectrum",
    }
    return labels.get(channel, kind.replace("_", " ").title())


def _downsample(
    x_values: list[float],
    y_values: list[float],
    *,
    max_points: int,
) -> tuple[list[float], list[float]]:
    limit = max(int(max_points), 2)
    if len(x_values) <= limit:
        return x_values, y_values
    indices = sorted({round(index * (len(x_values) - 1) / (limit - 1)) for index in range(limit)})
    return [x_values[index] for index in indices], [y_values[index] for index in indices]


def _numbers(value: object) -> list[float]:
    if not isinstance(value, (list, tuple)):
        return []
    return [number for item in value if (number := _number(item)) is not None]


def _number(value: object) -> float | None:
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    return None


__all__ = ["SpectrumDisclosure", "spectral_payload"]
