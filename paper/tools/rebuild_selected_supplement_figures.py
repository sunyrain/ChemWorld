"""Reproduce the user-selected S3/S4 layouts in the manuscript PowerPoint master.

The layout follows the two user-selected concepts. Every quantitative S3 mark
comes from the retained figure data; S4 uses the documented W05/Aligned pair.
The S4 graphical layer is the exact user-supplied reference with editable
scientific corrections. This script edits only slides 9 and 10 of the master.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from statistics import mean

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
from pptx.util import Emu, Pt

ROOT = Path(__file__).resolve().parents[2]
MASTER = ROOT / "output/pptx/chemworld-figures-final.pptx"
DATA = ROOT / "paper/figures/academic-ppt/retained-figure-data.json"
UNIT = 9525  # one design coordinate in EMU; the master is 1440 x 1900
INK = "252B30"
MUTED = "66737B"
GRID = "CED8DD"
BLUE = "426D96"
TEAL = "277F8A"
RUST = "A35F42"
PALE_BLUE = "EEF5FA"
PALE_TEAL = "EDF7F7"
PALE_RUST = "FBF1EC"
PALE_GRAY = "F5F7F8"
ARMS = ("Opaque", "Aligned", "MisIndexed")


def emu(v: float) -> Emu:
    return Emu(round(v * UNIT))


def rgb(value: str) -> RGBColor:
    return RGBColor.from_string(value.lstrip("#"))


def rect(slide, x, y, w, h, *, fill="FFFFFF", edge=GRID, weight=1.0, rounded=False, dash=False):
    kind = MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE
    shape = slide.shapes.add_shape(kind, emu(x), emu(y), emu(w), emu(h))
    if fill is None:
        shape.fill.background()
    else:
        shape.fill.solid()
        shape.fill.fore_color.rgb = rgb(fill)
    if edge is None:
        shape.line.fill.background()
    else:
        shape.line.color.rgb = rgb(edge)
        shape.line.width = Pt(weight * 0.75)
        if dash:
            shape.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    return shape


def oval(slide, x, y, w, h, *, fill="FFFFFF", edge=None, weight=1):
    shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, emu(x), emu(y), emu(w), emu(h))
    if fill is None:
        shape.fill.background()
    else:
        shape.fill.solid()
        shape.fill.fore_color.rgb = rgb(fill)
    if edge is None:
        shape.line.fill.background()
    else:
        shape.line.color.rgb = rgb(edge)
        shape.line.width = Pt(weight * 0.75)
    return shape


def diamond(slide, cx, cy, radius=7, color=INK):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.DIAMOND,
        emu(cx - radius),
        emu(cy - radius),
        emu(2 * radius),
        emu(2 * radius),
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = rgb(color)
    shape.line.fill.background()
    return shape


def line(slide, x1, y1, x2, y2, *, color=INK, weight=1.0, dash=False):
    shape = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, emu(x1), emu(y1), emu(x2), emu(y2))
    shape.line.color.rgb = rgb(color)
    shape.line.width = Pt(weight * 0.75)
    if dash:
        shape.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    return shape


def arrow(slide, x1, y1, x2, y2, *, color=INK, weight=1.4):
    line(slide, x1, y1, x2, y2, color=color, weight=weight)
    if x2 > x1:
        line(slide, x2, y2, x2 - 9, y2 - 5, color=color, weight=weight)
        line(slide, x2, y2, x2 - 9, y2 + 5, color=color, weight=weight)
    elif y2 > y1:
        line(slide, x2, y2, x2 - 5, y2 - 9, color=color, weight=weight)
        line(slide, x2, y2, x2 + 5, y2 - 9, color=color, weight=weight)


def text(
    slide,
    value,
    x,
    y,
    w,
    h,
    *,
    size=20,
    bold=False,
    color=INK,
    align="left",
    valign="middle",
    margin=0,
    font="Arial",
    italic=False,
):
    shape = slide.shapes.add_textbox(emu(x), emu(y), emu(w), emu(h))
    frame = shape.text_frame
    frame.clear()
    frame.word_wrap = True
    frame.auto_size = MSO_AUTO_SIZE.NONE
    frame.margin_left = frame.margin_right = emu(margin)
    frame.margin_top = frame.margin_bottom = emu(0)
    frame.vertical_anchor = MSO_ANCHOR.MIDDLE if valign == "middle" else MSO_ANCHOR.TOP
    for idx, part in enumerate(str(value).split("\n")):
        para = frame.paragraphs[0] if idx == 0 else frame.add_paragraph()
        para.alignment = {
            "left": PP_ALIGN.LEFT,
            "center": PP_ALIGN.CENTER,
            "right": PP_ALIGN.RIGHT,
        }[align]
        para.space_before = Pt(0)
        para.space_after = Pt(0)
        run = para.add_run()
        run.text = part
        run.font.name = font
        run.font.size = Pt(size * 0.75)
        run.font.bold = bold
        run.font.italic = italic
        run.font.color.rgb = rgb(color)
    return shape


def cross(slide, cx, cy, *, color=RUST, radius=5.2):
    line(slide, cx - radius, cy - radius, cx + radius, cy + radius, color=color, weight=2)
    line(slide, cx - radius, cy + radius, cx + radius, cy - radius, color=color, weight=2)


def agent(slide, x, y, scale=1.0):
    oval(slide, x + 18 * scale, y, 27 * scale, 27 * scale, fill="FFFFFF", edge=INK, weight=1.4)
    line(slide, x + 9 * scale, y + 55 * scale, x + 15 * scale, y + 39 * scale, weight=1.5)
    line(slide, x + 15 * scale, y + 39 * scale, x + 31 * scale, y + 32 * scale, weight=1.5)
    line(slide, x + 31 * scale, y + 32 * scale, x + 49 * scale, y + 39 * scale, weight=1.5)
    line(slide, x + 49 * scale, y + 39 * scale, x + 55 * scale, y + 55 * scale, weight=1.5)
    oval(slide, x + 52 * scale, y - 2 * scale, 6 * scale, 6 * scale, fill="FFFFFF", edge=INK)
    oval(slide, x + 63 * scale, y - 10 * scale, 8 * scale, 8 * scale, fill="FFFFFF", edge=INK)


def document(slide, x, y, color=BLUE):
    rect(slide, x, y, 44, 54, fill="FFFFFF", edge=color, weight=1.5)
    for dy in (16, 27, 38):
        line(slide, x + 9, y + dy, x + 34, y + dy, color=color, weight=1)


def beaker(slide, x, y):
    oval(slide, x, y, 73, 16, fill="FFFFFF", edge=INK, weight=1.3)
    line(slide, x + 3, y + 8, x + 3, y + 80, weight=1.5)
    line(slide, x + 70, y + 8, x + 70, y + 80, weight=1.5)
    oval(slide, x + 3, y + 72, 67, 16, fill="FFFFFF", edge=INK, weight=1.3)
    rect(slide, x + 5, y + 54, 63, 26, fill="DFF1F6", edge=None)
    line(slide, x + 5, y + 54, x + 68, y + 54, color=TEAL, weight=1.1)


def clear_slide(slide):
    tree = slide.shapes._spTree
    for shape in list(slide.shapes):
        tree.remove(shape._element)


def budget_data():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    specs = [
        ("EC", "discovery", "score", "mae", "EC discovery score MAE", 0.3, (0.17378, 0.11222, 11)),
        (
            "EC",
            "optimization",
            "score",
            "mae",
            "EC optimization score MAE",
            0.3,
            (0.17811, 0.10818, 12),
        ),
        (
            "PA",
            "discovery",
            "product_in_organic",
            "mae",
            "Partitioning organic-fraction MAE",
            0.2,
            (0.08291, 0.02379, 13),
        ),
        (
            "C",
            "delivery",
            "crystal_yield",
            "mae",
            "Crystallization recovery MAE",
            0.3,
            (0.10433, 0.07937, 8),
        ),
        (
            "C",
            "delivery",
            "crystal_fines_fraction",
            "coverage",
            "Fines interval coverage",
            50.0,
            (35.6, 43.9, 7),
        ),
        (
            "C",
            "delivery",
            "crystal_yield",
            "retest",
            "Independently retested recovery",
            0.6,
            (0.42054, 0.39939, 7),
        ),
    ]
    out = []
    for system, goal, metric, field, title, limit, expected in specs:
        rows = [
            r
            for r in data["campaigns"]
            if r["system"] == system and r["goal"] == goal and r["metric"] == metric
        ]
        pairs = []
        for wi in range(1, 6):
            for ai, arm in enumerate(ARMS):
                world = f"{system}-W{wi:02d}"
                matched = [r for r in rows if r["world"] == world and r["arm"] == arm]
                assert len(matched) == 2, (system, goal, metric, world, arm, len(matched))
                budgets = {r["budget"]: r for r in matched}
                assert set(budgets) == {12, 24}
                r12, r24 = budgets[12], budgets[24]
                scale = 100 if field == "coverage" else 1
                v12, v24 = r12[field] * scale, r24[field] * scale
                delta = v12 - v24 if field == "mae" else v24 - v12
                pairs.append(
                    {
                        "world": wi,
                        "arm": ai,
                        "v12": v12,
                        "v24": v24,
                        "delta": delta,
                        "shortfall": not r12["conforming"] or not r24["conforming"],
                    }
                )
        assert len(pairs) == 15
        means = (mean(p["v12"] for p in pairs), mean(p["v24"] for p in pairs))
        improved = sum(p["delta"] > 1e-12 for p in pairs)
        tolerance = 0.1 if field == "coverage" else 5e-5
        assert abs(means[0] - expected[0]) <= tolerance, (title, means)
        assert abs(means[1] - expected[1]) <= tolerance, (title, means)
        assert improved == expected[2], (title, improved)
        assert max(abs(p["delta"]) for p in pairs) <= limit + 1e-10, (title, limit)
        if system == "C":
            assert [(p["world"], p["arm"]) for p in pairs if p["shortfall"]] == [(2, 0)]
        else:
            assert not any(p["shortfall"] for p in pairs)
        out.append(
            {
                "title": title,
                "field": field,
                "limit": limit,
                "means": means,
                "improved": improved,
                "pairs": pairs,
                "mean_delta": mean(p["delta"] for p in pairs),
            }
        )
    return out


class Canvas:
    """Draw in reference-image coordinates, applying one uniform scale."""

    def __init__(self, slide, reference_width):
        self.slide = slide
        self.scale = 1440 / reference_width

    def text(self, value, x, y, w, h, **kw):
        for key in ("size", "margin"):
            if key in kw:
                kw[key] *= self.scale
        return text(self.slide, value, *(v * self.scale for v in (x, y, w, h)), **kw)

    def rect(self, x, y, w, h, **kw):
        if "weight" in kw:
            kw["weight"] *= self.scale
        return rect(self.slide, *(v * self.scale for v in (x, y, w, h)), **kw)

    def line(self, x1, y1, x2, y2, **kw):
        if "weight" in kw:
            kw["weight"] *= self.scale
        return line(self.slide, *(v * self.scale for v in (x1, y1, x2, y2)), **kw)

    def arrow(self, x1, y1, x2, y2, **kw):
        if "weight" in kw:
            kw["weight"] *= self.scale
        return arrow(self.slide, *(v * self.scale for v in (x1, y1, x2, y2)), **kw)

    def point(self, x, y, radius, color):
        return oval(
            self.slide,
            (x - radius) * self.scale,
            (y - radius) * self.scale,
            2 * radius * self.scale,
            2 * radius * self.scale,
            fill=color,
            edge=None,
        )

    def diamond(self, x, y, radius=7, color="000000"):
        return diamond(self.slide, x * self.scale, y * self.scale, radius * self.scale, color)

    def cross(self, x, y, radius=4.5, color=RUST):
        return cross(
            self.slide, x * self.scale, y * self.scale, radius=radius * self.scale, color=color
        )


def draw_s3(slide, values):
    """Match the selected 1536 x 1024 layout, using real paired estimates.

    The concept's fictional error bars have no matching uncertainty estimate in
    the retained data. Plot honest point estimates at the same layout anchors;
    do not invent intervals or replace the point plot with zero-connected stems.
    """
    clear_slide(slide)
    c = Canvas(slide, 1536)
    ink, grid, teal, rust = "000000", "B1B8BC", "006366", "B03E1C"
    c.line(511, 6, 511, 1010, color=grid, weight=0.9)
    c.line(1024, 6, 1024, 1010, color=grid, weight=0.9)
    c.line(6, 506, 1530, 506, color=grid, weight=0.9)
    for i, d in enumerate(values):
        x, y = (i % 3) * 512, (i // 3) * 512
        c.text("abcdef"[i], x + 14, y + 0, 28, 35, size=28, bold=True, color=ink)
        c.text(d["title"], x + 95, y + 1, 413, 26, size=18, bold=True, color=ink, align="center")
        c.text("12 vs 24 (mean)", x + 164, y + 27, 306, 20, size=16, color=ink, align="center")
        a, b = d["means"]
        fmt = (lambda z: f"{z:.1f}%") if d["field"] == "coverage" else (lambda z: f"{z:.4f}")
        c.text(
            f"{fmt(a)}   vs   {fmt(b)}",
            x + 178,
            y + 50,
            278,
            21,
            size=16,
            color=ink,
            align="center",
        )
        c.text("World", x + 16, y + 68, 93, 20, size=13, color=ink)
        c.text("Information arm", x + 117, y + 68, 131, 20, size=13, color=ink)
        c.text("Favors 24", x + 405, y + 72, 75, 19, size=13, color=ink)
        c.arrow(x + 463, y + 82, x + 488, y + 82, color=ink, weight=0.7)
        mid, reach = x + 316, 145
        c.line(mid, y + 83, mid, y + 438, color=ink, weight=0.8)
        for j, pair in enumerate(d["pairs"]):
            wi, ai = divmod(j, 3)
            yy = y + 100 + wi * 62 + ai * 17
            if ai == 0:
                c.text(f"World {wi + 1}", x + 16, yy + 6, 93, 18, size=13, color=ink)
            c.text(ARMS[ai], x + 117, yy - 9, 94, 18, size=13, color=ink)
            xx = mid + pair["delta"] / d["limit"] * reach
            color = teal if pair["delta"] > 1e-12 else rust if pair["delta"] < -1e-12 else "6A737B"
            if pair["shortfall"]:
                c.cross(xx, yy, radius=4.4, color=color)
            else:
                c.point(xx, yy, 3.8, color)
            if ai == 2:
                c.line(x + 16, yy + 12, x + 493, yy + 12, color=grid, weight=0.65, dash=True)
        c.text("Mean (all 15)", x + 16, y + 410, 112, 22, size=13, color=ink)
        c.diamond(mid + d["mean_delta"] / d["limit"] * reach, y + 420, 7, ink)
        c.line(x + 168, y + 439, x + 485, y + 439, color=ink, weight=0.9)
        for f in (-1, -0.5, 0, 0.5, 1):
            v = f * d["limit"]
            xx = mid + f * reach
            label = f"{v:g}" if v else "0"
            c.line(xx, y + 439, xx, y + 446, color=ink, weight=0.75)
            c.text(label, xx - 25, y + 448, 50, 20, size=12, color=ink, align="center")
        label = (
            "Paired difference in MAE (12 \u2212 24)"
            if d["field"] == "mae"
            else "Paired difference in coverage (24 \u2212 12), pp"
            if d["field"] == "coverage"
            else "Paired difference in recovery (24 \u2212 12)"
        )
        c.text(label, x + 163, y + 474, 343, 23, size=13, color=ink, align="center")
        if i == 3:
            pair = next(p for p in d["pairs"] if p["shortfall"])
            xx = mid + pair["delta"] / d["limit"] * reach
            c.text(
                "Source-assay\nshortfall",
                x + 404,
                y + 173,
                95,
                27,
                size=11,
                color=ink,
                align="left",
            )
            c.line(x + 425, y + 174, xx - 2, y + 168, color=ink, weight=0.65)
            c.line(xx - 2, y + 168, xx, y + 162, color=ink, weight=0.65)


def draw_s4(slide):
    """Preserve the actual selected art; correct only scientific text and marks.

    This intentionally embeds the reference graphical layer rather than
    substituting new icons, headers, table geometry or colour treatments.
    Editable patches occupy the corresponding reference text/plot rectangles.
    """
    clear_slide(slide)
    reference = ROOT / "output/imagegen/s3-s4-layout-concepts-20260925/selected/S4-reference.png"
    slide.shapes.add_picture(str(reference), 0, 0, emu(1440), emu(1286 * 1440 / 1223))
    c = Canvas(slide, 1223)
    dark, body = "101010", "3D424B"

    def replace(
        value,
        x,
        y,
        w,
        h,
        *,
        size=18,
        bold=False,
        color=body,
        align="left",
        fill="FFFFFF",
        font="Arial Narrow",
        italic=False,
    ):
        c.rect(x, y, w, h, fill=fill, edge=None)
        c.text(
            value,
            x,
            y,
            w,
            h,
            size=size,
            bold=bold,
            color=color,
            align=align,
            font=font,
            italic=italic,
        )

    # A: the same abbreviated timeline and the same stage-label anchors.
    replace("First feasible\nbatch", 19, 181, 105, 44, size=18, align="center")
    replace("B1\u201319 fail the fines limit", 765, 183, 199, 38, size=17, align="center")
    replace("B20 feasible\nB23 selected", 966, 180, 116, 45, size=17, align="center")

    # B: common withheld question, twin forecast cards and original locked art.
    replace(
        "For this formulation, which option produces\nfewer fines?",
        399,
        382,
        440,
        48,
        size=20,
        align="center",
    )
    # Keep the thermal-plot footprint. The hold is constant at the actual target.
    c.rect(457, 521, 135, 57, fill="DFE8EE", edge=None)
    c.arrow(456, 574, 585, 574, color="151D25", weight=1)
    c.line(460, 544, 575, 544, color="215E85", weight=2.3)
    c.text(
        "278.15 K · 2 h",
        474,
        516,
        121,
        21,
        size=15,
        color="215E85",
        font="Arial Narrow",
        align="center",
    )
    # Required profiles are schematic: the requested reheat target is 315 K.
    c.text(
        "toward 315 K",
        694,
        494,
        118,
        19,
        size=14,
        color="B74319",
        font="Arial Narrow",
        align="center",
    )
    replace("17% → 12%", 929, 568, 125, 18, size=16, bold=True, color="396F98", align="center")
    replace("49% → 35%", 1079, 568, 123, 18, size=16, bold=True, color="B74319", align="center")

    # C: retain the illustrated thinking agents; use condensed public K2 text.
    replace(
        "Agent review (K2)",
        457,
        701,
        282,
        26,
        size=19,
        bold=True,
        color=dark,
        fill="F4F5F6",
        align="center",
    )
    replace(
        "•  B1 first met the fines rule\n"
        "•  12 source batches completed\n•  Reheat\u2013recool was untested",
        142,
        774,
        280,
        80,
        size=18,
    )
    replace(
        "•  B1\u201319 failed the fines limit\n"
        "•  B20 first passed; B23 selected\n•  B8 showed no improvement",
        142,
        896,
        280,
        112,
        size=18,
    )
    replace(
        "Thermal cycling\nwas untested; seed\nsurvival had been\nassumed.",
        570,
        774,
        182,
        87,
        size=18,
    )
    replace(
        "B8 negative evidence\nwas underused; even\nthe predicted direction\nis uncertain.",
        570,
        901,
        182,
        112,
        size=18,
    )
    replace("(B23: staged → direct cooling)", 788, 914, 260, 23, size=16, align="center")
    # The original cooling icon and the unexecuted status box remain unchanged.

    # D: the evaluator reference remains separate from the proposed cooling test.
    replace(
        "Independent evaluation of H vs R, using the same formulation.\n"
        "Unavailable during the agents\u2019 Q forecasts and K2 reviews.",
        353,
        1145,
        560,
        57,
        size=18,
    )
    replace(
        "Fines reference",
        934,
        1138,
        139,
        24,
        size=17,
        bold=True,
        italic=True,
        color=dark,
        fill="FAF2E6",
        align="center",
    )
    replace(
        "(revealed here)", 934, 1162, 139, 22, size=17, color=dark, fill="FAF2E6", align="center"
    )
    c.rect(1078, 1128, 114, 62, fill="FAF2E6", edge=None)
    base, max_h = 1189, 43
    c.rect(1096, base - max_h * 0.35, 19, max_h * 0.35, fill="42799A", edge=None)
    c.rect(1142, base - max_h, 19, max_h, fill="BF481E", edge=None)
    c.text(
        "35%",
        1088,
        base - max_h * 0.35 - 18,
        37,
        16,
        size=12,
        color=dark,
        align="center",
        font="Arial Narrow",
    )
    c.text(
        "100%",
        1133,
        base - max_h - 18,
        42,
        16,
        size=12,
        color=dark,
        align="center",
        font="Arial Narrow",
    )
    c.line(1080, base, 1174, base, color="263744", weight=1.1)
    # Omit only the concept watermark; crop/export preserves all four sections.
    c.rect(1053, 1244, 161, 36, fill="FFFFFF", edge=None)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=MASTER)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    values = budget_data()
    print("s3 data: " + ", ".join(f"{d['title']} {d['improved']}/15" for d in values), flush=True)
    deck = Presentation(args.source)
    assert len(deck.slides) == 11
    assert abs(deck.slide_width - emu(1440)) <= 1
    assert abs(deck.slide_height - emu(1900)) <= 1
    draw_s3(deck.slides[8], values)
    print("slide 9 rebuilt", flush=True)
    draw_s4(deck.slides[9])
    print("slide 10 rebuilt", flush=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    deck.save(args.output)
    print(f"saved editable PowerPoint {args.output}", flush=True)


if __name__ == "__main__":
    main()
