"""Render the six evidence figures for the ChemWorld arXiv release."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from itertools import pairwise
from pathlib import Path
from typing import Any

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Ellipse, FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle

ROOT = Path(__file__).resolve().parents[2]
DERIVED_SCHEMA = "chemworld-arxiv-v1-derived-data-0.1"
SENSITIVITY_SCHEMA = "chemworld-arxiv-v1-p0-sensitivity-0.1"
MANIFEST_SCHEMA = "chemworld-arxiv-release-figure-manifest-0.1"

INK = "#17222E"
MUTED = "#687481"
GRID = "#DCE3E8"
WASH = "#F4F7F8"
PAPER = "#FFFFFF"
OPAQUE = "#26577C"
NOMINAL = "#D95F52"
MISINDEXED = "#8066B3"
TEAL = "#3D9487"
AMBER = "#E3A43E"
RELEASE_TIMESTAMP = datetime(2026, 8, 2, tzinfo=UTC)


def _canonical_sha(value: Mapping[str, Any]) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()


def _file_sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _load_hashed(path: Path, *, schema: str, hash_key: str) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != schema:
        raise ValueError(f"unsupported schema: {path}")
    declared = data.pop(hash_key)
    actual = _canonical_sha(data)
    data[hash_key] = declared
    if declared != actual:
        raise ValueError(f"content hash is invalid: {path}")
    return data


def _configure() -> None:
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Liberation Sans", "DejaVu Sans"],
            "font.size": 7.6,
            "axes.titlesize": 8.8,
            "axes.labelsize": 7.8,
            "axes.titleweight": "semibold",
            "axes.edgecolor": MUTED,
            "axes.linewidth": 0.65,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "xtick.labelsize": 7.0,
            "ytick.labelsize": 7.0,
            "xtick.color": INK,
            "ytick.color": INK,
            "text.color": INK,
            "legend.frameon": False,
            "legend.fontsize": 7.0,
            "lines.linewidth": 1.25,
            "svg.hashsalt": "chemworld-arxiv-release-v1",
            "svg.fonttype": "none",
            "image.composite_image": False,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "savefig.facecolor": PAPER,
            "figure.facecolor": PAPER,
        }
    )


def _panel(ax: plt.Axes, label: str, title: str) -> None:
    ax.text(
        -0.09,
        1.08,
        label,
        transform=ax.transAxes,
        fontsize=11,
        fontweight="bold",
        va="top",
        ha="left",
    )
    ax.set_title(title, loc="left", pad=7)


def _box(
    ax: plt.Axes,
    xy: tuple[float, float],
    width: float,
    height: float,
    text: str,
    *,
    edge: str = INK,
    face: str = PAPER,
    fontsize: float = 7.0,
    weight: str = "normal",
) -> FancyBboxPatch:
    patch = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.012,rounding_size=0.025",
        transform=ax.transAxes,
        fc=face,
        ec=edge,
        lw=1.0,
    )
    ax.add_patch(patch)
    ax.text(
        xy[0] + width / 2,
        xy[1] + height / 2,
        text,
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=fontsize,
        fontweight=weight,
    )
    return patch


def _arrow(ax: plt.Axes, start: tuple[float, float], end: tuple[float, float]) -> None:
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            transform=ax.transAxes,
            arrowstyle="-|>",
            mutation_scale=9,
            lw=1.0,
            color=INK,
            shrinkA=2,
            shrinkB=2,
        )
    )


def _icon_line(
    ax: plt.Axes,
    points: Sequence[tuple[float, float]],
    *,
    color: str = INK,
    lw: float = 0.8,
) -> None:
    ax.plot(
        [point[0] for point in points],
        [point[1] for point in points],
        transform=ax.transAxes,
        color=color,
        lw=lw,
        solid_capstyle="round",
        solid_joinstyle="round",
        clip_on=False,
    )


def _icon(
    ax: plt.Axes,
    kind: str,
    center: tuple[float, float],
    size: float,
    *,
    color: str = INK,
    accent: str = TEAL,
    label: str | None = None,
) -> None:
    """Draw a small code-native scientific icon in axes coordinates."""
    x, y = center
    s = size
    patch_kwargs = {
        "transform": ax.transAxes,
        "fc": "none",
        "ec": color,
        "lw": 0.8,
        "clip_on": False,
    }

    if kind in {"flask", "assay"}:
        ax.add_patch(Rectangle((x - 0.10 * s, y + 0.13 * s), 0.20 * s, 0.30 * s, **patch_kwargs))
        ax.add_patch(
            Polygon(
                [
                    (x - 0.10 * s, y + 0.13 * s),
                    (x - 0.38 * s, y - 0.35 * s),
                    (x - 0.32 * s, y - 0.47 * s),
                    (x + 0.32 * s, y - 0.47 * s),
                    (x + 0.38 * s, y - 0.35 * s),
                    (x + 0.10 * s, y + 0.13 * s),
                ],
                **patch_kwargs,
            )
        )
        _icon_line(ax, [(x - 0.27 * s, y - 0.25 * s), (x + 0.27 * s, y - 0.25 * s)], color=accent)
        if kind == "assay":
            for dx in (-0.16, 0.0, 0.16):
                ax.add_patch(
                    Circle(
                        (x + dx * s, y - 0.34 * s),
                        0.035 * s,
                        transform=ax.transAxes,
                        fc=accent,
                        ec="none",
                        clip_on=False,
                    )
                )
        return

    if kind == "molecule":
        nodes = [(-0.34, 0.05), (-0.12, 0.30), (0.16, 0.18), (0.34, -0.12), (0.02, -0.28)]
        for first, second in pairwise(nodes):
            _icon_line(
                ax,
                [(x + first[0] * s, y + first[1] * s), (x + second[0] * s, y + second[1] * s)],
                color=color,
            )
        _icon_line(ax, [(x - 0.34 * s, y + 0.05 * s), (x + 0.02 * s, y - 0.28 * s)], color=color)
        for dx, dy in nodes:
            ax.add_patch(
                Circle(
                    (x + dx * s, y + dy * s),
                    0.07 * s,
                    transform=ax.transAxes,
                    fc=PAPER,
                    ec=color,
                    lw=0.8,
                    clip_on=False,
                )
            )
        return

    if kind == "eye":
        ax.add_patch(Ellipse((x, y), 0.85 * s, 0.52 * s, **patch_kwargs))
        ax.add_patch(
            Circle((x, y), 0.14 * s, transform=ax.transAxes, fc=color, ec="none", clip_on=False)
        )
        ax.add_patch(
            Circle(
                (x + 0.04 * s, y + 0.05 * s),
                0.035 * s,
                transform=ax.transAxes,
                fc=PAPER,
                ec="none",
                clip_on=False,
            )
        )
        return

    if kind in {"ledger", "document"}:
        ax.add_patch(Rectangle((x - 0.32 * s, y - 0.40 * s), 0.52 * s, 0.74 * s, **patch_kwargs))
        if kind == "ledger":
            ax.add_patch(
                Rectangle((x - 0.10 * s, y + 0.27 * s), 0.18 * s, 0.13 * s, **patch_kwargs)
            )
        for offset in (0.14, -0.02, -0.18):
            _icon_line(
                ax,
                [(x - 0.20 * s, y + offset * s), (x + 0.10 * s, y + offset * s)],
                color=color,
                lw=0.65,
            )
        return

    if kind == "trace":
        cube = [
            (-0.34, 0.18),
            (-0.16, 0.31),
            (0.02, 0.18),
            (0.02, -0.08),
            (-0.16, -0.21),
            (-0.34, -0.08),
        ]
        ax.add_patch(Polygon([(x + dx * s, y + dy * s) for dx, dy in cube], **patch_kwargs))
        _icon_line(
            ax,
            [
                (x - 0.34 * s, y + 0.18 * s),
                (x - 0.16 * s, y + 0.05 * s),
                (x + 0.02 * s, y + 0.18 * s),
            ],
            color=color,
        )
        _icon_line(ax, [(x - 0.16 * s, y + 0.05 * s), (x - 0.16 * s, y - 0.21 * s)], color=color)
        for index in range(4):
            cx = x + (0.14 + 0.16 * index) * s
            cy = y - (0.10 + 0.045 * (index % 2)) * s
            ax.add_patch(
                Circle(
                    (cx, cy),
                    0.045 * s,
                    transform=ax.transAxes,
                    fc=PAPER,
                    ec=color,
                    lw=0.7,
                    clip_on=False,
                )
            )
            if index:
                previous_x = x + (0.14 + 0.16 * (index - 1)) * s
                previous_y = y - (0.10 + 0.045 * ((index - 1) % 2)) * s
                _icon_line(ax, [(previous_x, previous_y), (cx, cy)], color=color, lw=0.65)
        return

    if kind == "sliders":
        for index, knob in enumerate((-0.18, 0.16, -0.02)):
            yy = y + (0.22 - 0.22 * index) * s
            _icon_line(ax, [(x - 0.38 * s, yy), (x + 0.38 * s, yy)], color=color)
            ax.add_patch(
                Circle(
                    (x + knob * s, yy),
                    0.075 * s,
                    transform=ax.transAxes,
                    fc=PAPER,
                    ec=color,
                    lw=0.8,
                    clip_on=False,
                )
            )
        return

    if kind == "folder":
        ax.add_patch(
            Polygon(
                [
                    (x - 0.39 * s, y - 0.30 * s),
                    (x - 0.39 * s, y + 0.24 * s),
                    (x - 0.08 * s, y + 0.24 * s),
                    (x + 0.02 * s, y + 0.10 * s),
                    (x + 0.39 * s, y + 0.10 * s),
                    (x + 0.39 * s, y - 0.30 * s),
                ],
                **patch_kwargs,
            )
        )
        return

    if kind == "database":
        ax.add_patch(Ellipse((x, y + 0.26 * s), 0.64 * s, 0.22 * s, **patch_kwargs))
        _icon_line(ax, [(x - 0.32 * s, y + 0.26 * s), (x - 0.32 * s, y - 0.28 * s)], color=color)
        _icon_line(ax, [(x + 0.32 * s, y + 0.26 * s), (x + 0.32 * s, y - 0.28 * s)], color=color)
        for yy in (0.0, -0.26):
            ax.add_patch(Ellipse((x, y + yy * s), 0.64 * s, 0.22 * s, **patch_kwargs))
        return

    if kind == "transaction":
        ax.add_patch(
            FancyArrowPatch(
                (x - 0.38 * s, y + 0.13 * s),
                (x + 0.38 * s, y + 0.13 * s),
                transform=ax.transAxes,
                arrowstyle="->",
                mutation_scale=6,
                lw=0.8,
                color=color,
            )
        )
        ax.add_patch(
            FancyArrowPatch(
                (x + 0.38 * s, y - 0.13 * s),
                (x - 0.38 * s, y - 0.13 * s),
                transform=ax.transAxes,
                arrowstyle="->",
                mutation_scale=6,
                lw=0.8,
                color=color,
            )
        )
        return

    if kind == "tube":
        ax.add_patch(Rectangle((x - 0.16 * s, y - 0.34 * s), 0.32 * s, 0.68 * s, **patch_kwargs))
        ax.add_patch(Ellipse((x, y - 0.34 * s), 0.32 * s, 0.18 * s, **patch_kwargs))
        _icon_line(ax, [(x - 0.13 * s, y - 0.10 * s), (x + 0.13 * s, y - 0.10 * s)], color=accent)
        return

    if kind == "chain":
        ax.add_patch(Ellipse((x - 0.16 * s, y), 0.50 * s, 0.25 * s, angle=45, **patch_kwargs))
        ax.add_patch(Ellipse((x + 0.16 * s, y), 0.50 * s, 0.25 * s, angle=45, **patch_kwargs))
        return

    if kind == "bars":
        for index, height in enumerate((0.26, 0.48, 0.70)):
            ax.add_patch(
                Rectangle(
                    (x + (-0.33 + index * 0.24) * s, y - 0.34 * s),
                    0.13 * s,
                    height * s,
                    **patch_kwargs,
                )
            )
        _icon_line(ax, [(x - 0.40 * s, y - 0.34 * s), (x + 0.38 * s, y - 0.34 * s)], color=color)
        return

    if kind == "target":
        for radius in (0.34, 0.22, 0.10):
            ax.add_patch(Circle((x, y), radius * s, **patch_kwargs))
        _icon_line(ax, [(x, y), (x + 0.38 * s, y + 0.38 * s)], color=color)
        return

    if kind == "potential":
        ax.add_patch(
            FancyBboxPatch(
                (x - 0.40 * s, y - 0.28 * s),
                0.80 * s,
                0.56 * s,
                boxstyle="round,pad=0.004,rounding_size=0.012",
                **patch_kwargs,
            )
        )
        ax.text(
            x,
            y,
            label or "potential",
            transform=ax.transAxes,
            ha="center",
            va="center",
            fontsize=4.5,
            fontweight="semibold",
            color=color,
        )
        return

    if kind == "cell":
        ax.add_patch(Rectangle((x - 0.35 * s, y - 0.38 * s), 0.70 * s, 0.55 * s, **patch_kwargs))
        _icon_line(
            ax, [(x - 0.22 * s, y + 0.35 * s), (x - 0.22 * s, y - 0.22 * s)], color=color, lw=1.5
        )
        _icon_line(
            ax, [(x + 0.22 * s, y + 0.35 * s), (x + 0.22 * s, y - 0.22 * s)], color=color, lw=1.0
        )
        _icon_line(ax, [(x - 0.30 * s, y - 0.12 * s), (x + 0.30 * s, y - 0.12 * s)], color=accent)
        return

    if kind == "spectrometer":
        ax.add_patch(Rectangle((x - 0.40 * s, y - 0.32 * s), 0.80 * s, 0.62 * s, **patch_kwargs))
        ax.add_patch(Rectangle((x - 0.27 * s, y - 0.17 * s), 0.52 * s, 0.34 * s, **patch_kwargs))
        _icon_line(
            ax,
            [
                (x - 0.22 * s, y - 0.10 * s),
                (x - 0.10 * s, y + 0.08 * s),
                (x + 0.02 * s, y - 0.04 * s),
                (x + 0.20 * s, y + 0.12 * s),
            ],
            color=accent,
        )
        return

    if kind == "agent":
        ax.add_patch(Circle((x, y), 0.38 * s, **patch_kwargs))
        nodes = [(-0.18, 0.14), (-0.20, -0.12), (0.02, 0.0), (0.20, 0.18), (0.20, -0.18)]
        for dx, dy in nodes:
            ax.add_patch(
                Circle(
                    (x + dx * s, y + dy * s),
                    0.045 * s,
                    transform=ax.transAxes,
                    fc=PAPER,
                    ec=color,
                    lw=0.7,
                    clip_on=False,
                )
            )
        for start, end in ((0, 2), (1, 2), (2, 3), (2, 4)):
            _icon_line(
                ax,
                [
                    (x + nodes[start][0] * s, y + nodes[start][1] * s),
                    (x + nodes[end][0] * s, y + nodes[end][1] * s),
                ],
                color=color,
                lw=0.6,
            )
        return

    raise ValueError(f"unsupported icon kind: {kind}")


def _save(
    fig: plt.Figure,
    output_dir: Path,
    stem: str,
    *,
    tight: bool = True,
) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []
    for suffix in ("pdf", "svg", "png"):
        path = output_dir / f"{stem}.{suffix}"
        metadata: dict[str, Any] = {"Creator": "ChemWorld arXiv release figure pipeline"}
        if suffix == "pdf":
            metadata |= {
                "CreationDate": RELEASE_TIMESTAMP,
                "ModDate": RELEASE_TIMESTAMP,
            }
        elif suffix == "svg":
            metadata["Date"] = "2026-08-02T00:00:00Z"
        kwargs: dict[str, Any] = {"metadata": metadata}
        if tight:
            kwargs |= {"bbox_inches": "tight", "pad_inches": 0.035}
        # SVG/PDF preserve vector primitives, but Matplotlib still rasterizes each
        # embedded scientific sprite at the save DPI.  Keep those crops at print
        # resolution instead of silently reducing them to the 100-DPI figure default.
        kwargs["dpi"] = 480 if suffix in {"svg", "pdf"} else 360
        fig.savefig(path, **kwargs)
        if suffix == "svg":
            normalized = "\n".join(
                line.rstrip() for line in path.read_text(encoding="utf-8").splitlines()
            )
            path.write_text(normalized + "\n", encoding="utf-8", newline="\n")
        outputs.append(path)
    plt.close(fig)
    return outputs


def figure_1(data: Mapping[str, Any], output_dir: Path) -> list[Path]:
    qualification = data["environment_qualification"]
    ink = "#071929"
    muted = "#53657a"
    blue = "#004c73"
    red = "#ef432f"
    teal = "#078b78"
    amber = "#e18b00"
    purple = "#7651b2"
    icon_atlas = (
        ROOT
        / "paper/figures/experimental-intelligence-v1/assets"
        / "figure-1-scientific-icons-hd-v2.png"
    )

    # Geometry is a normalized transcription of the 1632 x 963 image2 reference.
    fig = plt.figure(figsize=(7.2, 4.25), facecolor="#ffffff")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    def heading(letter: str, title: str, x: float, y: float, *, size: float = 8.2) -> None:
        ax.text(
            x,
            y,
            letter,
            transform=ax.transAxes,
            va="top",
            fontsize=13.6,
            fontweight="bold",
            color=ink,
        )
        ax.text(
            x + 0.043,
            y - 0.003,
            title,
            transform=ax.transAxes,
            va="top",
            fontsize=size,
            fontweight="bold",
            color=ink,
        )

    def arrow(start: tuple[float, float], end: tuple[float, float], *, color: str = ink) -> None:
        ax.add_patch(
            FancyArrowPatch(
                start,
                end,
                transform=ax.transAxes,
                arrowstyle="-|>",
                mutation_scale=8.5,
                color=color,
                lw=0.85,
                shrinkA=0,
                shrinkB=0,
                clip_on=False,
                zorder=3,
            )
        )

    heading("A", "The chemical world is the experimental apparatus", 0.009, 0.980)
    primary_cards = [
        (0.034, 0.736, 0.115, 0.137, teal, "#ffffff"),
        (0.196, 0.726, 0.136, 0.158, blue, "#ffffff"),
        (0.381, 0.736, 0.104, 0.136, amber, "#ffffff"),
    ]
    for x, y, width, height, edge, face in primary_cards:
        _workflow_card(ax, (x, y), width, height, edge=edge, face=face)
    _atlas_icon_crop(ax, icon_atlas, 0, 0, (0.044, 0.087, 0.753, 0.850))
    _atlas_icon_crop(
        ax,
        icon_atlas,
        0,
        1,
        (0.207, 0.321, 0.796, 0.872),
        inset=0.015,
        bleed=(0.0, 0.20, 0.0, 0.0),
    )
    _atlas_icon_crop(ax, icon_atlas, 0, 2, (0.393, 0.444, 0.797, 0.855), inset=0.14)
    ax.text(
        0.111,
        0.786,
        "agent\nselects\naction",
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=6.6,
        color=ink,
    )
    ax.text(
        0.264,
        0.763,
        "executable world\nchanges state",
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=6.6,
        fontweight="bold",
        color=ink,
    )
    ax.text(
        0.433,
        0.762,
        "public\nobservation",
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=6.5,
        color=ink,
    )
    arrow((0.151, 0.808), (0.194, 0.808))
    arrow((0.334, 0.808), (0.379, 0.808))

    ax.plot(
        [0.433, 0.433, 0.076],
        [0.733, 0.699, 0.699],
        transform=ax.transAxes,
        color=ink,
        lw=0.8,
        zorder=2,
    )
    arrow((0.076, 0.699), (0.076, 0.733))
    ax.text(
        0.260,
        0.675,
        "observation-conditioned next decision",
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=6.2,
        color=ink,
    )

    _workflow_card(ax, (0.098, 0.530), 0.152, 0.100, edge=purple, face="#ffffff")
    _workflow_card(ax, (0.283, 0.530), 0.145, 0.098, edge=purple, face="#ffffff")
    _atlas_icon_crop(ax, icon_atlas, 0, 3, (0.105, 0.150, 0.542, 0.620))
    _atlas_icon_crop(
        ax,
        icon_atlas,
        0,
        4,
        (0.290, 0.420, 0.535, 0.600),
        inset=0.015,
        bleed=(0.0, 0.10, 0.0, 0.0),
    )
    ax.text(
        0.154,
        0.581,
        "resource ledger",
        transform=ax.transAxes,
        ha="left",
        va="center",
        fontsize=6.0,
        color=ink,
    )
    ax.text(
        0.356,
        0.603,
        "immutable trace",
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=6.0,
        color=ink,
        zorder=8,
    )
    arrow((0.218, 0.661), (0.204, 0.632))
    arrow((0.298, 0.661), (0.320, 0.632))

    heading("B", "Controlled contrasts separate agent from world", 0.543, 0.980, size=8.0)
    contrast_rows = [
        (0.852, blue, "hidden physical identity", "matched", (0, 5)),
        (0.770, red, "material information", "intervened", (1, 0)),
        (0.687, teal, "action authority", "compiled / primitive", (1, 1)),
        (0.606, amber, "evidence access", "accounted", (1, 2)),
        (0.524, purple, "resource endowment", "accounted", (1, 3)),
    ]
    for y, color, control, role, atlas_cell in contrast_rows:
        _workflow_card(ax, (0.570, y), 0.236, 0.065, edge=color, face="#ffffff")
        _workflow_card(ax, (0.825, y), 0.161, 0.065, edge=color, face="#ffffff")
        _atlas_icon_crop(
            ax,
            icon_atlas,
            atlas_cell[0],
            atlas_cell[1],
            (0.580, 0.619, y + 0.007, y + 0.058),
        )
        ax.text(
            0.632,
            y + 0.0325,
            control,
            transform=ax.transAxes,
            ha="left",
            va="center",
            fontsize=6.3,
            color=ink,
        )
        ax.text(
            0.906,
            y + 0.0325,
            role,
            transform=ax.transAxes,
            ha="center",
            va="center",
            fontsize=6.3,
            fontweight="bold",
            color=ink,
        )

    heading("C", "Each transition remains auditable", 0.009, 0.447, size=8.2)
    stage_x = [0.061, 0.154, 0.256, 0.352, 0.435]
    for left, right in pairwise(stage_x):
        arrow((left + 0.018, 0.350), (right - 0.018, 0.350), color="#b8c4cc")
    stage_data = [
        ("typed\nstate", (1, 4), (0.043, 0.081, 0.223, 0.308)),
        ("transaction", (1, 5), (0.130, 0.178, 0.232, 0.301)),
        ("resource\nreceipt", (2, 0), (0.240, 0.273, 0.221, 0.309)),
        ("trace", (2, 1), (0.329, 0.375, 0.229, 0.304)),
        ("physical\nreplay", (2, 2), (0.416, 0.466, 0.220, 0.309)),
    ]
    for index, (x, (label, atlas_cell, extent)) in enumerate(
        zip(stage_x, stage_data, strict=True), start=1
    ):
        ax.add_patch(
            Ellipse(
                (x, 0.350),
                0.026,
                0.044,
                transform=ax.transAxes,
                fc=blue,
                ec="white",
                lw=0.65,
                zorder=4,
            )
        )
        ax.text(
            x,
            0.350,
            str(index),
            transform=ax.transAxes,
            ha="center",
            va="center",
            fontsize=6.3,
            fontweight="bold",
            color="white",
            zorder=5,
        )
        _atlas_icon_crop(ax, icon_atlas, atlas_cell[0], atlas_cell[1], extent)
        ax.text(
            x,
            0.194,
            label,
            transform=ax.transAxes,
            ha="center",
            va="center",
            fontsize=6.1,
            color=ink,
        )
    _workflow_card(ax, (0.055, 0.063), 0.400, 0.071, edge=red, face="#ffffff")
    _atlas_icon_crop(ax, icon_atlas, 2, 3, (0.061, 0.093, 0.072, 0.128))
    ax.text(
        0.098,
        0.099,
        "invalid actions, failures and costs remain part of the evidence",
        transform=ax.transAxes,
        ha="left",
        va="center",
        fontsize=5.9,
        color=ink,
    )

    heading("D", "Qualified surface and evidence scope", 0.543, 0.447, size=8.1)
    surface_cards = [
        (
            0.551,
            0.245,
            0.128,
            0.125,
            blue,
            qualification["registered_tasks"],
            "tasks",
            (2, 4),
            (0.560, 0.606, 0.258, 0.355),
        ),
        (
            0.685,
            0.245,
            0.144,
            0.125,
            teal,
            qualification["registered_operations"],
            "operations",
            (2, 5),
            (0.694, 0.747, 0.255, 0.357),
        ),
        (
            0.835,
            0.245,
            0.151,
            0.125,
            amber,
            qualification["registered_instruments"],
            "instruments",
            (3, 0),
            (0.844, 0.894, 0.253, 0.359),
        ),
        (
            0.578,
            0.109,
            0.181,
            0.119,
            purple,
            qualification["deterministic_complete_experiment_cases"],
            "boundary cases",
            (3, 1),
            (0.588, 0.637, 0.119, 0.216),
        ),
        (
            0.766,
            0.109,
            0.187,
            0.119,
            red,
            qualification["bound_success_endpoints"],
            "bound endpoints",
            (3, 2),
            (0.777, 0.830, 0.117, 0.216),
        ),
    ]
    for x, y, width, height, color, value, label, atlas_cell, extent in surface_cards:
        _workflow_card(ax, (x, y), width, height, edge=color, face="#ffffff")
        _atlas_icon_crop(ax, icon_atlas, atlas_cell[0], atlas_cell[1], extent)
        value_x = x + width * 0.66
        ax.text(
            value_x,
            y + height * 0.62,
            f"{value:,}",
            transform=ax.transAxes,
            ha="center",
            va="center",
            fontsize=11.4,
            fontweight="bold",
            color=color,
        )
        ax.text(
            value_x,
            y + height * 0.28,
            label,
            transform=ax.transAxes,
            ha="center",
            va="center",
            fontsize=6.0,
            color=ink,
        )
    ax.text(
        0.778,
        0.064,
        "paper evidence: 2 compiled tasks · 1 autonomous task",
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=6.0,
        color=muted,
    )
    return _save(fig, output_dir, "figure-1-controlled-apparatus", tight=False)


def _g0_world_lookup(data: Mapping[str, Any]) -> dict[tuple[str, int, str], float]:
    return {
        (str(row["task_id"]), int(row["world_seed"]), str(row["arm"])): float(row["primary_score"])
        for row in data["g0"]["world_arm_rows"]
    }


def figure_2(data: Mapping[str, Any], output_dir: Path) -> list[Path]:
    lookup = _g0_world_lookup(data)
    task_ids = ["electrochemical-conversion", "reaction-to-crystallization"]
    contrast_rows = {
        row["task_id"]: row
        for row in data["g0"]["task_arm_rows"]
        if row["arm"] == "derived_contrasts"
    }
    fig, axes = plt.subplots(2, 2, figsize=(7.2, 4.55))

    ax = axes[0, 0]
    _panel(ax, "A", "Information changes outcomes in a task-dependent way")
    for task_index, task_id in enumerate(task_ids):
        values = [
            lookup[(task_id, seed, "nominal")] - lookup[(task_id, seed, "opaque")]
            for seed in range(10)
        ]
        jitter = np.linspace(-0.12, 0.12, len(values))
        ax.scatter(values, task_index + jitter, s=19, color=INK, alpha=0.72, zorder=3)
        row = contrast_rows[task_id]
        mean = row["nominal_minus_opaque_mean"]
        low, high = row["nominal_minus_opaque_familywise_97_5_interval"]
        ax.errorbar(
            mean,
            task_index,
            xerr=[[mean - low], [high - mean]],
            fmt="s",
            ms=5.5,
            color=NOMINAL,
            capsize=2.5,
            lw=1.4,
            zorder=4,
        )
    ax.axvline(0, color=MUTED, lw=0.8)
    ax.set_yticks([0, 1], ["electrochemical\nconversion", "reaction to\ncrystallization"])
    ax.set_xlabel("nominal - opaque score (paired world)")
    ax.grid(axis="x", color=GRID, lw=0.5)
    ax.invert_yaxis()

    ax = axes[0, 1]
    _panel(ax, "B", "A misindexed prior redirects experimental choices")
    world_rows = data["g0"]["world_arm_rows"]
    for task_index, task_id in enumerate(task_ids):
        rows = [
            row for row in world_rows if row["task_id"] == task_id and row["arm"] == "misindexed"
        ]
        for row in rows:
            x = [0 + task_index * 2.6, 1 + task_index * 2.6]
            y = [row["early_misleading_share"], row["late_misleading_share"]]
            ax.plot(x, y, color=MISINDEXED, alpha=0.24, lw=0.8)
            ax.scatter(x, y, color=MISINDEXED, s=11, alpha=0.55)
    ax.set_xticks([0, 1, 2.6, 3.6], ["early", "late", "early", "late"])
    ax.text(
        0.5, -0.22, "electrochemical", transform=ax.get_xaxis_transform(), ha="center", fontsize=6.4
    )
    ax.text(
        3.1, -0.22, "crystallization", transform=ax.get_xaxis_transform(), ha="center", fontsize=6.4
    )
    ax.set_ylabel("misleading-action share")
    ax.set_ylim(-0.04, 1.04)
    ax.grid(axis="y", color=GRID, lw=0.5)

    ax = axes[1, 0]
    _panel(ax, "C", "Manipulation, correction and recovery are separable")
    components = [
        "behavior\nchanged",
        "actions\ncorrected",
        "performance\nrestored",
        "joint\ncriterion",
    ]
    matrix = np.asarray(
        [
            [
                contrast_rows[task_id]["manipulation_check_passed"],
                contrast_rows[task_id]["differential_action_correction_passed"],
                contrast_rows[task_id]["performance_recovery_to_opaque_passed"],
                contrast_rows[task_id]["overall_recovery_claim_passed"],
            ]
            for task_id in task_ids
        ],
        dtype=bool,
    )
    ax.imshow(
        matrix, cmap=mpl.colors.ListedColormap(["#E7EBEE", TEAL]), vmin=0, vmax=1, aspect="auto"
    )
    ax.set_xticks(range(4), components)
    ax.set_yticks([0, 1], ["electrochemical", "crystallization"])
    ax.tick_params(length=0)
    for row_index in range(2):
        for column_index in range(4):
            passed = bool(matrix[row_index, column_index])
            ax.text(
                column_index,
                row_index,
                "PASS" if passed else "FAIL",
                ha="center",
                va="center",
                fontsize=6.2,
                fontweight="bold",
                color=PAPER if passed else MUTED,
            )
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax = axes[1, 1]
    _panel(ax, "D", "Outcome and epistemic readouts form different profiles")
    opaque_rows = [row for row in data["g0"]["task_arm_rows"] if row["arm"] == "opaque"]
    metrics = [
        ("primary_score_mean", "endpoint\nscore", False),
        ("heldout_directional_accuracy", "held-out\naccuracy", False),
        ("heldout_brier_score", "Brier\nscore", True),
        ("unsupported_claim_rate", "unsupported\nclaims", True),
    ]
    x = np.arange(len(metrics))
    for row_index, row in enumerate(opaque_rows):
        for metric_index, (key, _label, lower_better) in enumerate(metrics):
            raw = float(row[key])
            favourable = 1.0 - raw if lower_better else raw
            ax.scatter(
                metric_index,
                row_index,
                s=42 + 90 * favourable,
                color=TEAL if row_index == 0 else AMBER,
                edgecolor=PAPER,
                linewidth=0.8,
            )
            ax.text(
                metric_index,
                row_index,
                f"{raw:.2f}",
                ha="center",
                va="center",
                fontsize=5.6,
                color=PAPER if favourable > 0.45 else INK,
                fontweight="semibold",
            )
    ax.set_xticks(x, [label for _key, label, _lower in metrics])
    ax.set_yticks([0, 1], ["electrochemical", "crystallization"])
    ax.set_xlim(-0.6, len(metrics) - 0.4)
    ax.set_ylim(-0.65, 1.65)
    ax.invert_yaxis()
    ax.grid(axis="x", color=GRID, lw=0.5)
    ax.tick_params(length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.text(
        0.995,
        0.01,
        "circle area follows favourable direction within each column",
        ha="right",
        fontsize=5.8,
        color=MUTED,
    )
    fig.subplots_adjust(left=0.105, right=0.995, top=0.93, bottom=0.16, wspace=0.43, hspace=0.58)
    return _save(fig, output_dir, "figure-2-compiled-controls")


def _workflow_card(
    ax: plt.Axes,
    position: tuple[float, float],
    width: float,
    height: float,
    *,
    edge: str,
    face: str,
) -> None:
    x, y = position
    for offset, alpha in (((0.004, -0.007), 0.08), ((0.002, -0.003), 0.045)):
        ax.add_patch(
            FancyBboxPatch(
                (x + offset[0], y + offset[1]),
                width,
                height,
                boxstyle="round,pad=0.002,rounding_size=0.012",
                transform=ax.transAxes,
                fc="#071929",
                ec="none",
                alpha=alpha,
                clip_on=False,
                zorder=0,
            )
        )
    ax.add_patch(
        FancyBboxPatch(
            (x, y),
            width,
            height,
            boxstyle="round,pad=0.002,rounding_size=0.012",
            transform=ax.transAxes,
            fc=face,
            ec=edge,
            lw=0.95,
            clip_on=False,
            zorder=1,
        )
    )


_REFERENCE_IMAGE_CACHE: dict[Path, np.ndarray] = {}


def _reference_icon_crop(
    ax: plt.Axes,
    reference: Path,
    crop: tuple[int, int, int, int],
    extent: tuple[float, float, float, float],
) -> None:
    """Embed one isolated image2 icon crop, never the complete reference plate."""
    source = _REFERENCE_IMAGE_CACHE.get(reference)
    if source is None:
        source = np.asarray(plt.imread(reference), dtype=float)
        _REFERENCE_IMAGE_CACHE[reference] = source
    x0, y0, x1, y1 = crop
    segment = source[y0:y1, x0:x1].copy()
    if segment.max() > 1.0:
        segment /= 255.0
    rgb = segment[..., :3]
    corner_pixels = np.concatenate(
        (
            rgb[:4, :4].reshape(-1, 3),
            rgb[:4, -4:].reshape(-1, 3),
            rgb[-4:, :4].reshape(-1, 3),
            rgb[-4:, -4:].reshape(-1, 3),
        )
    )
    background = np.median(corner_pixels, axis=0)
    distance = np.sqrt(np.sum((rgb - background) ** 2, axis=2))
    alpha = np.clip((distance - 0.012) / 0.075, 0.0, 1.0)
    if segment.shape[2] == 3:
        segment = np.dstack((segment, alpha))
    else:
        segment[..., 3] *= alpha
    ax.imshow(
        segment,
        extent=extent,
        origin="upper",
        interpolation="lanczos",
        aspect="auto",
        zorder=6,
    )


def _atlas_icon_crop(
    ax: plt.Axes,
    atlas: Path,
    row: int,
    column: int,
    extent: tuple[float, float, float, float],
    *,
    rows: int = 4,
    columns: int = 6,
    inset: float = 0.08,
    bleed: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0),
) -> None:
    """Embed one high-resolution sprite while preserving its physical aspect ratio."""
    source = _REFERENCE_IMAGE_CACHE.get(atlas)
    if source is None:
        source = np.asarray(plt.imread(atlas), dtype=float)
        _REFERENCE_IMAGE_CACHE[atlas] = source
    height, width = source.shape[:2]
    cell_width = width / columns
    cell_height = height / rows
    bleed_left, bleed_right, bleed_top, bleed_bottom = bleed
    x0 = round((column - bleed_left + inset) * cell_width)
    x1 = round((column + 1 + bleed_right - inset) * cell_width)
    y0 = round((row - bleed_top + inset) * cell_height)
    y1 = round((row + 1 + bleed_bottom - inset) * cell_height)
    x0, x1 = max(0, x0), min(width, x1)
    y0, y1 = max(0, y0), min(height, y1)
    segment = source[y0:y1, x0:x1].copy()
    if segment.max() > 1.0:
        segment /= 255.0
    rgb = segment[..., :3]
    border = np.concatenate(
        (
            rgb[:6].reshape(-1, 3),
            rgb[-6:].reshape(-1, 3),
            rgb[:, :6].reshape(-1, 3),
            rgb[:, -6:].reshape(-1, 3),
        )
    )
    background = np.median(border, axis=0)
    distance = np.sqrt(np.sum((rgb - background) ** 2, axis=2))
    alpha = np.clip((distance - 0.005) / 0.040, 0.0, 1.0)
    foreground = np.argwhere(alpha > 0.04)
    if foreground.size:
        fy0, fx0 = foreground.min(axis=0)
        fy1, fx1 = foreground.max(axis=0) + 1
        pad = max(4, round(min(segment.shape[:2]) * 0.035))
        fy0 = max(0, fy0 - pad)
        fx0 = max(0, fx0 - pad)
        fy1 = min(segment.shape[0], fy1 + pad)
        fx1 = min(segment.shape[1], fx1 + pad)
        segment = segment[fy0:fy1, fx0:fx1]
        alpha = alpha[fy0:fy1, fx0:fx1]
    keep_white_matte = atlas.name.startswith("figure-1-scientific-icons")
    if segment.shape[2] == 3:
        segment = np.dstack((segment, np.ones_like(alpha) if keep_white_matte else alpha))
    elif keep_white_matte:
        segment[..., 3] = 1.0
    else:
        segment[..., 3] *= alpha

    left, right, bottom, top = extent
    available_width = right - left
    available_height = top - bottom
    image_aspect = segment.shape[1] / segment.shape[0]
    axes_box = ax.get_position()
    figure = ax.get_figure()
    normalized_aspect = image_aspect * (
        figure.get_figheight() * axes_box.height / (figure.get_figwidth() * axes_box.width)
    )
    if available_width / available_height > normalized_aspect:
        fitted_width = available_height * normalized_aspect
        midpoint = (left + right) / 2
        left, right = midpoint - fitted_width / 2, midpoint + fitted_width / 2
    else:
        fitted_height = available_width / normalized_aspect
        midpoint = (bottom + top) / 2
        bottom, top = midpoint - fitted_height / 2, midpoint + fitted_height / 2
    ax.imshow(
        segment,
        extent=(left, right, bottom, top),
        origin="upper",
        interpolation="lanczos",
        aspect="auto",
        zorder=6,
    )


def _workflow_icon(
    ax: plt.Axes,
    kind: str,
    center: tuple[float, float],
    *,
    label: str | None = None,
) -> None:
    """Draw the image2 workflow-reference icons as independent vector elements."""
    x, y = center
    navy = "#071929"

    def line(points: Sequence[tuple[float, float]], *, color: str = navy, lw: float = 0.75) -> None:
        ax.plot(
            [point[0] for point in points],
            [point[1] for point in points],
            transform=ax.transAxes,
            color=color,
            lw=lw,
            solid_capstyle="round",
            solid_joinstyle="round",
            clip_on=False,
            zorder=5,
        )

    def ellipse(
        xy: tuple[float, float],
        width: float,
        height: float,
        *,
        face: str = "white",
        edge: str = navy,
        lw: float = 0.65,
        angle: float = 0,
        zorder: float = 4,
    ) -> None:
        ax.add_patch(
            Ellipse(
                xy,
                width,
                height,
                angle=angle,
                transform=ax.transAxes,
                fc=face,
                ec=edge,
                lw=lw,
                clip_on=False,
                zorder=zorder,
            )
        )

    def beaker(*, liquid: str) -> None:
        ax.add_patch(
            Polygon(
                [
                    (x - 0.014, y + 0.002),
                    (x - 0.014, y - 0.049),
                    (x - 0.011, y - 0.056),
                    (x + 0.014, y - 0.056),
                    (x + 0.017, y - 0.049),
                    (x + 0.017, y + 0.002),
                ],
                transform=ax.transAxes,
                fc="#fbfdfd",
                ec=navy,
                lw=0.7,
                zorder=3,
            )
        )
        ax.add_patch(
            Rectangle(
                (x - 0.0115, y - 0.049),
                0.026,
                0.030,
                transform=ax.transAxes,
                fc=liquid,
                ec="none",
                alpha=0.72,
                zorder=4,
            )
        )
        line([(x - 0.011, y - 0.019), (x + 0.014, y - 0.019)], color=liquid, lw=0.9)
        for yy, length in ((-0.029, 0.006), (-0.039, 0.0045), (-0.048, 0.006)):
            line([(x + 0.006, y + yy), (x + 0.006 + length, y + yy)], lw=0.45)
        line([(x - 0.016, y + 0.002), (x - 0.007, y + 0.002)], lw=0.55)

    if kind == "reagent":
        beaker(liquid="#66cdbf")
        ax.add_patch(
            Polygon(
                [
                    (x - 0.012, y + 0.020),
                    (x + 0.011, y + 0.071),
                    (x + 0.016, y + 0.064),
                    (x - 0.007, y + 0.014),
                ],
                transform=ax.transAxes,
                fc="#f4f7f6",
                ec=navy,
                lw=0.65,
                zorder=5,
            )
        )
        ellipse((x + 0.014, y + 0.070), 0.011, 0.024, face="#61c7b7", angle=-38, zorder=5)
        line([(x - 0.010, y + 0.017), (x - 0.015, y + 0.006)], lw=0.65)
        for dx, dy, scale in ((-0.015, -0.003, 1.0), (-0.011, -0.012, 0.65)):
            ellipse(
                (x + dx, y + dy),
                0.0045 * scale,
                0.009 * scale,
                face="#73d4c5",
                edge="#4eb9aa",
                lw=0.35,
            )
        return

    if kind == "solvent":
        beaker(liquid="#73b6df")
        ax.add_patch(
            Polygon(
                [
                    (x - 0.010, y + 0.018),
                    (x + 0.010, y + 0.068),
                    (x + 0.028, y + 0.047),
                    (x + 0.004, y + 0.009),
                ],
                transform=ax.transAxes,
                fc="#f8faf9",
                ec=navy,
                lw=0.65,
                zorder=5,
            )
        )
        line([(x + 0.003, y + 0.051), (x + 0.017, y + 0.038)], color="#60717d", lw=0.45)
        line([(x + 0.001, y + 0.044), (x + 0.014, y + 0.032)], color="#60717d", lw=0.45)
        line([(x - 0.010, y + 0.018), (x - 0.014, y + 0.006)], lw=0.65)
        ellipse((x - 0.013, y - 0.003), 0.0045, 0.009, face="#72b9e3", edge="#4c9fce", lw=0.35)
        return

    if kind == "potential":
        ax.add_patch(
            FancyBboxPatch(
                (x - 0.029, y - 0.045),
                0.058,
                0.094,
                boxstyle="round,pad=0.001,rounding_size=0.007",
                transform=ax.transAxes,
                fc="#f2f4f3",
                ec=navy,
                lw=0.75,
                zorder=4,
            )
        )
        ax.add_patch(
            FancyBboxPatch(
                (x - 0.023, y + 0.003),
                0.046,
                0.034,
                boxstyle="round,pad=0.001,rounding_size=0.003",
                transform=ax.transAxes,
                fc="#0c2638",
                ec=navy,
                lw=0.55,
                zorder=5,
            )
        )
        ax.text(
            x,
            y + 0.019,
            label or "potential",
            transform=ax.transAxes,
            ha="center",
            va="center",
            fontsize=5.0,
            fontweight="bold",
            color="white",
            zorder=6,
        )
        ax.add_patch(
            Rectangle(
                (x - 0.024, y - 0.005),
                0.048,
                0.009,
                transform=ax.transAxes,
                fc="#72b9dd",
                ec="none",
                alpha=0.8,
                zorder=5,
            )
        )
        ellipse((x - 0.017, y - 0.030), 0.010, 0.020, face="#f3f5f4", edge=navy, lw=0.7)
        ellipse((x - 0.017, y - 0.030), 0.0045, 0.009, face=navy, edge=navy, lw=0.3)
        ellipse((x + 0.017, y - 0.030), 0.010, 0.020, face="#ef392c", edge=navy, lw=0.7)
        ellipse((x + 0.017, y - 0.030), 0.0045, 0.009, face="#9f2019", edge=navy, lw=0.3)
        return

    if kind == "cell":
        ax.add_patch(
            FancyBboxPatch(
                (x - 0.029, y - 0.048),
                0.058,
                0.081,
                boxstyle="round,pad=0.001,rounding_size=0.006",
                transform=ax.transAxes,
                fc="#eef7fb",
                ec=navy,
                lw=0.75,
                zorder=3,
            )
        )
        ax.add_patch(
            Rectangle(
                (x - 0.026, y - 0.045),
                0.052,
                0.049,
                transform=ax.transAxes,
                fc="#8bc8e7",
                ec="none",
                alpha=0.72,
                zorder=4,
            )
        )
        for yy, length in ((-0.008, 0.010), (-0.019, 0.006), (-0.030, 0.012)):
            line([(x - 0.004, y + yy), (x - 0.004 + length, y + yy)], color="white", lw=0.45)
        ax.add_patch(
            FancyBboxPatch(
                (x - 0.023, y - 0.038),
                0.008,
                0.095,
                boxstyle="round,pad=0.001,rounding_size=0.002",
                transform=ax.transAxes,
                fc="#0e273a",
                ec=navy,
                lw=0.55,
                zorder=5,
            )
        )
        ax.add_patch(
            FancyBboxPatch(
                (x + 0.015, y - 0.038),
                0.008,
                0.074,
                boxstyle="round,pad=0.001,rounding_size=0.002",
                transform=ax.transAxes,
                fc="#d9e0e3",
                ec=navy,
                lw=0.55,
                zorder=5,
            )
        )
        line(
            [
                (x - 0.019, y + 0.057),
                (x - 0.019, y + 0.074),
                (x + 0.019, y + 0.074),
                (x + 0.019, y + 0.054),
            ],
            lw=0.75,
        )
        ax.text(x - 0.013, y + 0.061, "-", transform=ax.transAxes, fontsize=5.0, color=navy)
        ax.text(x + 0.022, y + 0.061, "+", transform=ax.transAxes, fontsize=5.0, color=navy)
        return

    if kind == "assay":
        ax.add_patch(
            Polygon(
                [
                    (x - 0.007, y + 0.057),
                    (x - 0.007, y + 0.012),
                    (x - 0.022, y - 0.045),
                    (x - 0.018, y - 0.054),
                    (x + 0.018, y - 0.054),
                    (x + 0.022, y - 0.045),
                    (x + 0.007, y + 0.012),
                    (x + 0.007, y + 0.057),
                ],
                transform=ax.transAxes,
                fc="#fff7f3",
                ec=navy,
                lw=0.75,
                zorder=4,
            )
        )
        line([(x - 0.008, y + 0.058), (x + 0.008, y + 0.058)], lw=0.8)
        ax.add_patch(
            Polygon(
                [
                    (x - 0.017, y - 0.030),
                    (x - 0.019, y - 0.046),
                    (x + 0.019, y - 0.046),
                    (x + 0.016, y - 0.030),
                ],
                transform=ax.transAxes,
                fc="#f18b78",
                ec="none",
                alpha=0.9,
                zorder=5,
            )
        )
        for dx, dy in ((-0.008, -0.037), (0.002, -0.032), (0.010, -0.041)):
            ellipse(
                (x + dx, y + dy), 0.003, 0.006, face="#bd493a", edge="#bd493a", lw=0.2, zorder=6
            )
        return

    if kind == "agent":
        lobes = [
            (-0.016, 0.030, 0.020, 0.034),
            (-0.026, 0.009, 0.019, 0.034),
            (-0.020, -0.019, 0.022, 0.038),
            (-0.008, -0.038, 0.020, 0.032),
            (0.016, 0.030, 0.020, 0.034),
            (0.026, 0.009, 0.019, 0.034),
            (0.020, -0.019, 0.022, 0.038),
            (0.008, -0.038, 0.020, 0.032),
        ]
        for dx, dy, width, height in lobes:
            ellipse((x + dx, y + dy), width, height, face="#fbfcfc", edge=navy, lw=0.65)
        line([(x, y + 0.047), (x, y - 0.052)], lw=0.8)
        nodes = [
            (-0.017, 0.019),
            (-0.022, -0.008),
            (-0.012, -0.030),
            (0.016, 0.026),
            (0.021, -0.005),
            (0.013, -0.031),
        ]
        for dx, dy in nodes:
            ellipse((x + dx, y + dy), 0.0045, 0.009, face="white", edge=navy, lw=0.5, zorder=6)
        line([(x - 0.017, y + 0.019), (x - 0.006, y + 0.010), (x - 0.022, y - 0.008)], lw=0.45)
        line([(x + 0.016, y + 0.026), (x + 0.006, y + 0.012), (x + 0.021, y - 0.005)], lw=0.45)
        line([(x - 0.012, y - 0.030), (x - 0.004, y - 0.019)], lw=0.45)
        line([(x + 0.013, y - 0.031), (x + 0.004, y - 0.020)], lw=0.45)
        return

    if kind == "uvvis":
        ax.add_patch(
            FancyBboxPatch(
                (x - 0.031, y - 0.048),
                0.062,
                0.091,
                boxstyle="round,pad=0.001,rounding_size=0.006",
                transform=ax.transAxes,
                fc="#cfd5d8",
                ec=navy,
                lw=0.75,
                zorder=4,
            )
        )
        ax.add_patch(
            Polygon(
                [
                    (x - 0.031, y + 0.043),
                    (x - 0.021, y + 0.059),
                    (x + 0.025, y + 0.059),
                    (x + 0.031, y + 0.043),
                ],
                transform=ax.transAxes,
                fc="#eef1f2",
                ec=navy,
                lw=0.6,
                zorder=4,
            )
        )
        ax.add_patch(
            Rectangle(
                (x - 0.014, y - 0.030),
                0.035,
                0.060,
                transform=ax.transAxes,
                fc="#10283a",
                ec=navy,
                lw=0.6,
                zorder=5,
            )
        )
        ax.add_patch(
            Rectangle(
                (x - 0.010, y - 0.022),
                0.027,
                0.045,
                transform=ax.transAxes,
                fc="#fbfcfb",
                ec="#526775",
                lw=0.4,
                zorder=6,
            )
        )
        line(
            [
                (x - 0.008, y - 0.014),
                (x - 0.003, y + 0.015),
                (x + 0.002, y + 0.021),
                (x + 0.008, y - 0.009),
                (x + 0.015, y - 0.013),
            ],
            color="#14619b",
            lw=0.65,
        )
        ax.add_patch(
            Rectangle(
                (x - 0.027, y - 0.033),
                0.010,
                0.044,
                transform=ax.transAxes,
                fc="#163247",
                ec=navy,
                lw=0.45,
                zorder=5,
            )
        )
        for yy in (-0.024, -0.010, 0.004):
            ellipse(
                (x - 0.022, y + yy), 0.003, 0.006, face="#91bbcf", edge="#91bbcf", lw=0.2, zorder=6
            )
        return

    raise ValueError(f"unsupported workflow icon: {kind}")


def figure_3(data: Mapping[str, Any], output_dir: Path) -> list[Path]:
    demo = data["g2_v0_4"]["one_experiment_demonstration"]
    potential_label = f"{demo['setpoint_policy'][0]['potential_V']:g} V"
    cells = data["g2_v0_4"]["cell_rows"]
    ledger = demo["campaign_resource_endpoints"]

    ink = "#071929"
    muted = "#41556a"
    teal = "#078b78"
    blue = "#004c73"
    red = "#ef432f"
    amber = "#e18b00"
    grid = "#dce3e7"
    icon_atlas = (
        ROOT
        / "paper/figures/experimental-intelligence-v1/assets"
        / "figure-3-workflow-icons-hd-v2.png"
    )

    # Geometry is a normalized transcription of the 1840 x 850 image2 reference.
    # Keep the reference's panel boundaries and element order; do not auto-reflow.
    fig = plt.figure(figsize=(7.2, 3.33), facecolor="#fdfdfc")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(
        0.010,
        0.966,
        "A",
        transform=ax.transAxes,
        fontsize=13.8,
        fontweight="bold",
        color=ink,
        va="top",
    )
    ax.text(
        0.054,
        0.958,
        "One vessel closes through agent-selected primitive operations",
        transform=ax.transAxes,
        fontsize=8.2,
        fontweight="bold",
        color=ink,
        va="top",
    )

    card_width = 0.090
    top_y = 0.572
    top_height = 0.271
    top_cards = [
        (0.040, "add\nreagent", (0, 0)),
        (0.162, "add\nsolvent", (0, 1)),
        (0.286, "set\npotential", (0, 2)),
        (0.408, "electrolyze", (0, 3)),
    ]
    for x, text_label, atlas_cell in top_cards:
        _workflow_card(ax, (x, top_y), card_width, top_height, edge=teal, face="#fbfdfc")
        _atlas_icon_crop(
            ax,
            icon_atlas,
            atlas_cell[0],
            atlas_cell[1],
            (x + 0.017, x + card_width - 0.017, top_y + 0.085, top_y + 0.237),
            rows=2,
            columns=4,
        )
        if text_label == "set\npotential":
            ax.add_patch(
                Rectangle(
                    (x + 0.027, top_y + 0.148),
                    0.036,
                    0.017,
                    transform=ax.transAxes,
                    fc="#8fc6df",
                    ec="none",
                    zorder=7,
                )
            )
            ax.add_patch(
                FancyBboxPatch(
                    (x + 0.027, top_y + 0.163),
                    0.036,
                    0.033,
                    boxstyle="round,pad=0.001,rounding_size=0.002",
                    transform=ax.transAxes,
                    fc="#0c2638",
                    ec="#071929",
                    lw=0.45,
                    zorder=7,
                )
            )
            ax.text(
                x + card_width / 2,
                top_y + 0.179,
                potential_label,
                transform=ax.transAxes,
                ha="center",
                va="center",
                fontsize=4.8,
                fontweight="bold",
                color="white",
                zorder=8,
            )
        ax.text(
            x + card_width / 2,
            top_y + 0.043,
            text_label,
            transform=ax.transAxes,
            ha="center",
            va="center",
            fontsize=7.0,
            fontweight="bold",
            color=ink,
            zorder=8,
        )

    def arrow(start: tuple[float, float], end: tuple[float, float]) -> None:
        ax.add_patch(
            FancyArrowPatch(
                start,
                end,
                transform=ax.transAxes,
                arrowstyle="-|>",
                mutation_scale=8.5,
                color=ink,
                lw=0.85,
                shrinkA=0,
                shrinkB=0,
                clip_on=False,
                zorder=3,
            )
        )

    for start_x, end_x in ((0.130, 0.160), (0.252, 0.284), (0.376, 0.406)):
        arrow((start_x, 0.731), (end_x, 0.731))
    arrow((0.453, 0.570), (0.453, 0.455))

    bottom_y = 0.236
    bottom_height = 0.216
    bottom_cards = [
        (0.040, 0.097, red, "#fff9f7", "final assay\n0.531", (1, 0)),
        (
            0.227,
            0.094,
            blue,
            "#fbfcfd",
            "agent selects\nterminate",
            (1, 1),
        ),
        (0.408, 0.093, amber, "#fffaf3", "UV-vis\nobservation", (1, 2)),
    ]
    for x, width, edge, face, text_label, atlas_cell in bottom_cards:
        _workflow_card(ax, (x, bottom_y), width, bottom_height, edge=edge, face=face)
        _atlas_icon_crop(
            ax,
            icon_atlas,
            atlas_cell[0],
            atlas_cell[1],
            (x + 0.015, x + width - 0.015, bottom_y + 0.075, bottom_y + 0.197),
            rows=2,
            columns=4,
        )
        ax.text(
            x + width / 2,
            bottom_y + 0.044,
            text_label,
            transform=ax.transAxes,
            ha="center",
            va="center",
            fontsize=6.9,
            fontweight="bold" if "agent" in text_label or "UV-vis" in text_label else "normal",
            color=ink,
            zorder=8,
        )
    arrow((0.408, 0.359), (0.323, 0.359))
    arrow((0.227, 0.359), (0.139, 0.359))

    feedback_color = "#3b566f"
    ax.plot(
        [0.453, 0.453, 0.088, 0.088],
        [0.233, 0.155, 0.155, 0.211],
        transform=ax.transAxes,
        color=feedback_color,
        lw=0.9,
        linestyle=(0, (4, 3)),
        solid_capstyle="round",
        clip_on=False,
        zorder=2,
    )
    ax.add_patch(
        FancyArrowPatch(
            (0.088, 0.207),
            (0.088, 0.233),
            transform=ax.transAxes,
            arrowstyle="-|>",
            mutation_scale=8.0,
            color=feedback_color,
            lw=0.85,
            clip_on=False,
            zorder=3,
        )
    )
    ax.text(
        0.270,
        0.104,
        "measurement enters the public state before the stop decision",
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=6.5,
        color=muted,
    )

    ax.text(
        0.570,
        0.966,
        "B",
        transform=ax.transAxes,
        fontsize=13.8,
        fontweight="bold",
        color=ink,
        va="top",
    )
    ax.text(
        0.607,
        0.958,
        "Ten campaigns completed all 60 vessels",
        transform=ax.transAxes,
        fontsize=8.4,
        fontweight="bold",
        color=ink,
        va="top",
    )
    row_y = [0.889 - index * 0.0415 for index in range(10)]
    vessel_x = [0.647 + index * 0.0405 for index in range(6)]
    for cell, y in zip(cells, row_y, strict=True):
        ax.text(
            0.614,
            y,
            f"w{cell['world_seed']} {cell['arm'][0]}",
            transform=ax.transAxes,
            ha="right",
            va="center",
            fontsize=6.9,
            color=ink,
        )
        square_color = blue if cell["arm"] == "opaque" else red
        for x in vessel_x:
            ax.add_patch(
                Rectangle(
                    (x - 0.0055, y - 0.0115),
                    0.011,
                    0.023,
                    transform=ax.transAxes,
                    fc=square_color,
                    ec="white",
                    lw=0.35,
                    zorder=3,
                )
            )
    for index, x in enumerate(vessel_x, start=1):
        ax.text(
            x,
            0.456,
            f"v{index}",
            transform=ax.transAxes,
            ha="center",
            va="center",
            fontsize=6.8,
            color=ink,
        )
    ax.text(
        0.743,
        0.414,
        "815 accepted primitive operations",
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=6.8,
        fontweight="bold",
        color=ink,
    )

    ax.text(
        0.570,
        0.376,
        "C",
        transform=ax.transAxes,
        fontsize=13.8,
        fontweight="bold",
        color=ink,
        va="top",
    )
    ax.text(
        0.607,
        0.366,
        "The campaign ledger makes resource use reconstructable",
        transform=ax.transAxes,
        fontsize=7.2,
        fontweight="bold",
        color=ink,
        va="top",
    )
    ledger_rows = [
        ("vessels", ledger["vessel_starts"], 6),
        ("final assays", ledger["final_assays"], 6),
        ("instruments", ledger["nonfinal_instrument_uses"], 18),
        ("operations", ledger["operation_attempts"], 144),
    ]
    for index, (label_text, used, total) in enumerate(ledger_rows):
        y = 0.281 - index * 0.066
        ax.text(
            0.594,
            y + 0.022,
            label_text,
            transform=ax.transAxes,
            ha="left",
            va="center",
            fontsize=6.7,
            color=muted,
        )
        ax.text(
            0.932,
            y + 0.022,
            f"{used}/{total}",
            transform=ax.transAxes,
            ha="right",
            va="center",
            fontsize=6.7,
            fontweight="bold",
            color=ink,
        )
        ax.add_patch(
            Rectangle(
                (0.594, y),
                0.338,
                0.012,
                transform=ax.transAxes,
                fc=grid,
                ec="none",
                zorder=1,
            )
        )
        ax.add_patch(
            Rectangle(
                (0.594, y),
                0.338 * min(float(used) / float(total), 1.0),
                0.012,
                transform=ax.transAxes,
                fc=amber if used == total else teal,
                ec="none",
                zorder=2,
            )
        )
    return _save(fig, output_dir, "figure-3-autonomous-lifecycle", tight=False)


def figure_4(data: Mapping[str, Any], output_dir: Path) -> list[Path]:
    cells = data["g2_v0_4"]["cell_rows"]
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.72), sharex=True, sharey=True)
    for panel_index, (ax, seed) in enumerate(zip(axes, (0, 2, 4), strict=True)):
        _panel(ax, chr(ord("A") + panel_index), f"Physical world {seed}")
        for arm, color in (("opaque", OPAQUE), ("nominal", NOMINAL)):
            row = next(item for item in cells if item["world_seed"] == seed and item["arm"] == arm)
            scores = np.asarray(row["final_score_sequence"], dtype=float)
            ordinals = np.arange(1, len(scores) + 1)
            ax.plot(ordinals, scores, "o-", color=color, ms=4.0, label=arm, zorder=2)
            best_index = int(np.argmax(scores))
            ax.scatter(
                ordinals[best_index],
                scores[best_index],
                s=85,
                facecolors="none",
                edgecolors=color,
                linewidth=1.4,
                zorder=3,
            )
            ax.scatter(
                ordinals[-1],
                scores[-1],
                s=30,
                marker="s",
                facecolors=PAPER,
                edgecolors=color,
                linewidth=1.2,
                zorder=4,
            )
        ax.set_xticks(range(1, 7))
        ax.set_ylim(-0.05, 0.92)
        ax.grid(color=GRID, lw=0.5)
        ax.set_xlabel("final-assay ordinal")
        if panel_index == 0:
            ax.set_ylabel("final-assay score")
            ax.legend(loc="lower right")
    handles = [
        plt.Line2D(
            [],
            [],
            marker="o",
            markerfacecolor="none",
            markeredgecolor=INK,
            linestyle="",
            label="first observed campaign best",
        ),
        plt.Line2D(
            [],
            [],
            marker="s",
            markerfacecolor=PAPER,
            markeredgecolor=INK,
            linestyle="",
            label="terminal assay",
        ),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=2, bbox_to_anchor=(0.52, 0.055))
    fig.text(
        0.99,
        0.01,
        "selected development examples; not the replication estimand",
        ha="right",
        fontsize=5.9,
        color=MUTED,
    )
    fig.subplots_adjust(left=0.07, right=0.995, top=0.89, bottom=0.29, wspace=0.16)
    return _save(fig, output_dir, "figure-4-trajectory-dynamics")


def figure_5(
    data: Mapping[str, Any],
    sensitivity: Mapping[str, Any],
    output_dir: Path,
) -> list[Path]:
    replication = data["g2_v0_5"]
    complete = [row for row in replication["paired_trajectories"] if row["pair_complete"]]
    classes = replication["interpretation"]["selected_branch"]["world_metric_classifications"]
    fig, (ax, bx) = plt.subplots(
        1,
        2,
        figsize=(7.2, 3.35),
        gridspec_kw={"width_ratios": (1.28, 1.0), "wspace": 0.42},
    )

    _panel(ax, "A", "Best-score direction does not fix terminal retention")
    x_limit = 0.43
    y_limit = 0.55
    for origin, width, height in (
        ((-x_limit, 0), x_limit, y_limit),
        ((0, -y_limit), x_limit, y_limit),
    ):
        ax.add_patch(
            Rectangle(
                origin,
                width,
                height,
                facecolor=NOMINAL,
                alpha=0.055,
                edgecolor="none",
                zorder=0,
            )
        )
    endpoints = []
    terminals = []
    for row in complete:
        delta = row["nominal_minus_opaque"]
        endpoint = float(delta["best_final_score"])
        terminal = float(delta["terminal_to_global_best_ratio"])
        endpoints.append(endpoint)
        terminals.append(terminal)
        color = TEAL if int(row["world_seed"]) == 1 else AMBER
        ax.scatter(endpoint, terminal, s=54, color=color, edgecolor=PAPER, linewidth=0.8, zorder=3)
        ax.annotate(
            str(row["trajectory_replicate_id"]),
            (endpoint, terminal),
            xytext=(4, 3),
            textcoords="offset points",
            fontsize=5.8,
            color=INK,
        )
    ax.axhline(0, color=MUTED, lw=0.8)
    ax.axvline(0, color=MUTED, lw=0.8)
    ax.set_xlim(-x_limit, x_limit)
    ax.set_ylim(-y_limit, y_limit)
    ax.set_xlabel("nominal - opaque best-of-campaign contrast")
    ax.set_ylabel("nominal - opaque terminal / best contrast")
    ax.grid(color=GRID, lw=0.45, zorder=0)
    correlation = float(np.corrcoef(np.asarray(endpoints), np.asarray(terminals))[0, 1])
    opposite = sum(x * y < 0 for x, y in zip(endpoints, terminals, strict=True))
    zero_terminal = sum(abs(value) <= 1e-12 for value in terminals)
    ax.text(
        0.02,
        0.98,
        f"{opposite}/8 sign reversals + {zero_terminal} zero\nPearson r = {correlation:.3f}",
        transform=ax.transAxes,
        va="top",
        fontsize=6.4,
        fontweight="semibold",
        bbox={"facecolor": PAPER, "edgecolor": GRID, "boxstyle": "round,pad=0.25"},
    )
    ax.legend(
        handles=[
            plt.Line2D([], [], marker="o", color="none", markerfacecolor=TEAL, label="world 1"),
            plt.Line2D([], [], marker="o", color="none", markerfacecolor=AMBER, label="world 3"),
        ],
        loc="lower left",
        ncol=2,
    )

    _panel(bx, "B", "Six of eight selected cells are mixed")
    metric_specs = [
        ("global_best_discovery_fraction", "earlier\ndiscovery", -1),
        ("online_incumbent_retention_rate", "retention", 1),
        ("maximum_absolute_incumbent_drawdown", "smaller\ndrawdown", -1),
        ("terminal_to_global_best_ratio", "terminal /\nbest", 1),
    ]
    matrix = np.zeros((2, len(metric_specs)), dtype=float)
    labels: list[list[str]] = []
    for row_index, seed in enumerate((1, 3)):
        row_labels = []
        for column_index, (metric, _label, direction) in enumerate(metric_specs):
            raw = str(classes[str(seed)][metric])
            value = {
                "directionally_positive": 1,
                "directionally_negative": -1,
                "mixed": 0,
                "stable_zero": 0,
            }[raw]
            value *= direction
            matrix[row_index, column_index] = value
            row_labels.append({1: "nominal", -1: "opaque", 0: "mixed"}[value])
        labels.append(row_labels)
    cmap = mpl.colors.ListedColormap(["#F5E7D0", "#EEF1F3", "#DDF0EC"])
    bx.imshow(matrix, cmap=cmap, vmin=-1, vmax=1, aspect="auto")
    bx.set_xticks(range(len(metric_specs)), [item[1] for item in metric_specs])
    bx.set_yticks((0, 1), ("world 1", "world 3"))
    bx.tick_params(length=0)
    for row_index in range(matrix.shape[0]):
        for column_index in range(matrix.shape[1]):
            bx.text(
                column_index,
                row_index,
                labels[row_index][column_index],
                ha="center",
                va="center",
                fontsize=6.2,
                fontweight="semibold",
                color=INK,
            )
    for spine in bx.spines.values():
        spine.set_visible(False)
    censoring = sensitivity["g2_v0_5"]["right_censoring_missing_sign_sensitivity"]
    minimum_mixed = censoring["minimum_possible_mixed_core_classifications"]
    bx.text(
        0.5,
        -0.20,
        f"6/8 mixed; at least {minimum_mixed}/8 remain mixed\n"
        "under every sign assignment to the two censored pairs",
        transform=bx.transAxes,
        ha="center",
        va="top",
        fontsize=6.2,
        color=MUTED,
    )
    fig.subplots_adjust(left=0.085, right=0.985, top=0.88, bottom=0.24)
    return _save(fig, output_dir, "figure-5-within-world-replication")


def figure_6(data: Mapping[str, Any], output_dir: Path) -> list[Path]:
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(7.2, 3.28), gridspec_kw={"wspace": 0.52})
    opaque_rows = [row for row in data["g0"]["task_arm_rows"] if row["arm"] == "opaque"]
    compiled = [
        ("primary_score_mean", "endpoint score", False),
        ("heldout_directional_accuracy", "held-out accuracy", False),
        ("heldout_brier_score", "Brier score", True),
        ("unsupported_claim_rate", "unsupported claims", True),
    ]
    _panel(ax, "A", "Compiled control: task-conditioned readouts")
    for row_index, row in enumerate(opaque_rows):
        color = TEAL if row_index == 0 else AMBER
        for metric_index, (key, _label, lower_better) in enumerate(compiled):
            raw = float(row[key])
            favourable = 1.0 - raw if lower_better else raw
            ax.scatter(
                favourable,
                metric_index + (row_index - 0.5) * 0.16,
                s=36,
                color=color,
                edgecolor=PAPER,
                linewidth=0.6,
                label=row["task_id"].replace("-", " ") if metric_index == 0 else None,
            )
            ax.text(
                favourable + 0.025,
                metric_index + (row_index - 0.5) * 0.16,
                f"{raw:.2f}",
                va="center",
                fontsize=5.9,
                color=color,
            )
    ax.set_yticks(
        range(len(compiled)), [label + (" ↓" if lower else " ↑") for _key, label, lower in compiled]
    )
    ax.set_xlim(-0.02, 1.10)
    ax.set_xlabel("column-specific favourable direction")
    ax.invert_yaxis()
    ax.grid(axis="x", color=GRID, lw=0.5)
    ax.legend(loc="upper left")

    _panel(bx, "B", "Primitive control: lifecycle readouts")
    aggregate = data["g2_v0_4"]["arm_descriptive_aggregates"]
    lifecycle = [
        ("mean_completion_rate", None, "completion"),
        ("trajectory_learning", "mean_online_retention_rate", "retention"),
        ("trajectory_learning", "pooled_recovery_rate", "recovery"),
        ("trajectory_learning", "mean_terminal_to_global_best_ratio", "terminal / best"),
    ]
    for arm_index, (arm, color) in enumerate((("opaque", OPAQUE), ("nominal", NOMINAL))):
        for metric_index, (parent, child, _label) in enumerate(lifecycle):
            value = float(
                aggregate[arm][parent] if child is None else aggregate[arm][parent][child]
            )
            bx.scatter(
                value,
                metric_index + (arm_index - 0.5) * 0.16,
                s=36,
                color=color,
                edgecolor=PAPER,
                linewidth=0.6,
                label=arm if metric_index == 0 else None,
            )
            bx.text(
                value + 0.025,
                metric_index + (arm_index - 0.5) * 0.16,
                f"{value:.2f}",
                va="center",
                fontsize=5.9,
                color=color,
            )
    bx.set_yticks(range(len(lifecycle)), [label + " ↑" for _parent, _child, label in lifecycle])
    bx.set_xlim(-0.02, 1.10)
    bx.set_xlabel("reported metric value")
    bx.invert_yaxis()
    bx.grid(axis="x", color=GRID, lw=0.5)
    bx.legend(loc="upper left")
    fig.text(
        0.995,
        0.01,
        "Metrics remain separate readouts; no cross-metric composite is computed.",
        ha="right",
        fontsize=5.9,
        color=MUTED,
    )
    fig.subplots_adjust(left=0.145, right=0.995, top=0.90, bottom=0.20)
    return _save(fig, output_dir, "figure-6-experimental-agency-profile")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--derived",
        type=Path,
        default=ROOT / "benchmark/releases/chemworld-serious-v1/arxiv-v1-derived-data.json",
    )
    parser.add_argument(
        "--sensitivity",
        type=Path,
        default=ROOT / "benchmark/releases/chemworld-serious-v1/arxiv-v1-p0-sensitivity.json",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "paper/arxiv/figures",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=ROOT / "paper/arxiv/figure-manifest.json",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    data = _load_hashed(
        args.derived.resolve(), schema=DERIVED_SCHEMA, hash_key="derived_data_sha256"
    )
    sensitivity = _load_hashed(
        args.sensitivity.resolve(), schema=SENSITIVITY_SCHEMA, hash_key="sensitivity_sha256"
    )
    _configure()
    output_dir = args.output_dir.resolve()
    outputs: list[Path] = []
    outputs.extend(figure_1(data, output_dir))
    outputs.extend(figure_2(data, output_dir))
    outputs.extend(figure_3(data, output_dir))
    outputs.extend(figure_4(data, output_dir))
    outputs.extend(figure_5(data, sensitivity, output_dir))
    outputs.extend(figure_6(data, output_dir))
    manifest: dict[str, Any] = {
        "schema_version": MANIFEST_SCHEMA,
        "status": "frozen_complete",
        "style_version": "arxiv-release-v1",
        "derived_data_sha256": data["derived_data_sha256"],
        "sensitivity_sha256": sensitivity["sensitivity_sha256"],
        "files": [
            {
                "path": path.relative_to(ROOT).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": _file_sha(path),
            }
            for path in outputs
        ],
    }
    manifest["manifest_sha256"] = _canonical_sha(manifest)
    manifest_path = args.manifest.resolve()
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "figure_count": len(outputs) // 3,
                "file_count": len(outputs),
                "manifest": str(manifest_path),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
