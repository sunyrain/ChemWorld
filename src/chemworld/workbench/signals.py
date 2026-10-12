"""Chart public instrument packets without inventing missing observations."""

from __future__ import annotations

import math
from typing import Any

AXES = {
    "time_min": ("保留时间", "min", False),
    "wavelength_nm": ("波长", "nm", False),
    "wavenumber_cm-1": ("波数", "cm⁻¹", True),
    "wavenumber_cm_1": ("波数", "cm⁻¹", True),
    "chemical_shift_ppm": ("化学位移", "ppm", True),
    "shift_ppm": ("化学位移", "ppm", True),
    "mz": ("质荷比", "m/z", False),
    "m_z": ("质荷比", "m/z", False),
}


def chart_series(raw: dict[str, Any], instrument: str = "instrument") -> list[dict[str, Any]]:
    """Keep paired finite samples and report display downsampling explicitly."""
    result: list[dict[str, Any]] = []

    def visit(packet: dict[str, Any], label: str) -> None:
        axis_meta = packet.get("axis")
        signal_meta = packet.get("raw_signal")
        axes = {**packet, **(axis_meta if isinstance(axis_meta, dict) else {})}
        signals = {**packet, **(signal_meta if isinstance(signal_meta, dict) else {})}
        axis_definitions = dict(AXES)
        if isinstance(axis_meta, dict) and isinstance(axis_meta.get("values"), list):
            unit = axis_meta.get("unit", "a.u.")
            axis_definitions = {"values": ("观测轴", unit, unit in {"ppm", "cm-1", "cm⁻¹"})}
        for key, (title, unit, reverse) in axis_definitions.items():
            x = axes.get(key)
            y_key = next(
                (
                    k
                    for k in ("intensity", "absorbance", "transmittance", "signal", "values")
                    if isinstance(signals.get(k), list)
                ),
                None,
            )
            if not isinstance(x, list) or y_key is None:
                continue
            pairs = [
                (a, b)
                for a, b in zip(x, signals[y_key], strict=False)
                if isinstance(a, int | float)
                and isinstance(b, int | float)
                and math.isfinite(a)
                and math.isfinite(b)
            ]
            if not pairs:
                continue
            count = len(pairs)
            if count > 1500:
                pairs = [pairs[round(i * (count - 1) / 1499)] for i in range(1500)]
            result.append(
                {
                    "label": label,
                    "x_label": title,
                    "x_unit": unit,
                    "y_label": y_key,
                    "y_unit": signal_meta.get("unit", "a.u.")
                    if isinstance(signal_meta, dict)
                    else "fraction"
                    if y_key == "transmittance"
                    else "a.u.",
                    "reverse_x": reverse,
                    "points": pairs,
                    "original_points": count,
                    "downsampled": count > 1500,
                }
            )
            return
        for key, child in packet.items():
            if isinstance(child, dict) and key not in {"axis", "processed_estimates"}:
                visit(child, label if key in {"spectra", "raw_signal"} else key)

    visit(raw, instrument)
    return result
