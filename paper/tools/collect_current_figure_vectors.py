"""Prepare current manuscript vector objects without changing published figures."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np
from matplotlib.backends.backend_agg import RendererAgg
from matplotlib.font_manager import FontProperties

ROOT = Path(__file__).resolve().parents[2]
SVG = "{http://www.w3.org/2000/svg}"
XLINK = "{http://www.w3.org/1999/xlink}href"
IDENTITY = np.eye(3)
RENDERER = RendererAgg(10, 10, 72)


def transform(value: str) -> np.ndarray:
    matrix = IDENTITY.copy()
    for kind, content in re.findall(r"(\w+)\(([^)]+)\)", value):
        values = [float(v) for v in re.findall(r"[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?", content)]
        item = IDENTITY.copy()
        if kind == "translate":
            item[:2, 2] = [values[0], values[1] if len(values) > 1 else 0]
        elif kind == "scale":
            item[0, 0], item[1, 1] = values[0], values[-1]
        elif kind == "rotate":
            angle = math.radians(values[0])
            item[:2, :2] = [[math.cos(angle), -math.sin(angle)], [math.sin(angle), math.cos(angle)]]
            if len(values) == 3:
                centre = np.array(values[1:])
                item[:2, 2] = centre - item[:2, :2] @ centre
        elif kind == "matrix":
            a, b, c, d, e, f = values
            item = np.array([[a, c, e], [b, d, f], [0, 0, 1]])
        else:
            raise ValueError(f"Unsupported SVG transform: {kind}")
        matrix = matrix @ item
    return matrix


def style_of(node: ET.Element, parent: dict) -> dict:
    result = dict(parent)
    result.update(
        dict(pair.split(":", 1) for pair in node.get("style", "").split(";") if ":" in pair)
    )
    result = {k.strip(): v.strip() for k, v in result.items()}
    for key in (
        "fill",
        "stroke",
        "opacity",
        "fill-opacity",
        "stroke-opacity",
        "stroke-width",
        "text-anchor",
    ):
        if key in node.attrib:
            result[key] = node.get(key)
    return result


def path_commands(value: str, matrix: np.ndarray) -> list:
    tokens = re.findall(r"[A-Za-z]|[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?", value)
    result, cursor, command, previous = [], 0, None, np.zeros(2)
    start = previous.copy()
    while cursor < len(tokens):
        if tokens[cursor].isalpha():
            command = tokens[cursor]
            cursor += 1
        upper = command.upper()
        if upper == "Z":
            result.append(["Z"])
            previous = start.copy()
            command = None
            continue
        count = {"M": 2, "L": 2, "C": 6, "Q": 4, "H": 1, "V": 1}[upper]
        values = list(map(float, tokens[cursor : cursor + count]))
        cursor += count
        if upper in ("H", "V"):
            p = previous.copy()
            index = upper == "V"
            p[index] = values[0] + (previous[index] if command.islower() else 0)
            points = [p]
            upper = "L"
        else:
            points = [np.array(values[i : i + 2]) for i in range(0, count, 2)]
            if command.islower():
                points = [p + previous for p in points]
        previous = points[-1]
        if upper == "M":
            start = previous.copy()
            command = "l" if command.islower() else "L"
        converted = [(matrix @ [p[0], p[1], 1])[:2].tolist() for p in points]
        result.append([upper, *converted])
    return result


def collect(path: Path) -> dict:
    root = ET.parse(path).getroot()
    width, height = list(map(float, root.get("viewBox").split()))[2:]
    ids = {n.get("id"): n for n in root.iter() if n.get("id")}
    objects = []
    clips = {}
    for key, node in ids.items():
        if node.tag == SVG + "clipPath":
            rect = node.find(SVG + "rect")
            if rect is not None:
                x, y, w, h = [float(rect.get(k)) for k in ("x", "y", "width", "height")]
                clips[key] = [x, y, x + w, y + h]

    def text_object(node, style, matrix, inherited_x=0, inherited_y=0):
        if list(node):
            for child in node:
                text_object(
                    child,
                    style_of(child, style),
                    matrix,
                    float(node.get("x", inherited_x)),
                    float(node.get("y", inherited_y)),
                )
            return
        content = node.text or ""
        if not content.strip():
            return
        x = float(node.get("x", inherited_x))
        y = float(node.get("y", inherited_y))
        size = float(style.get("font-size", "10px").removesuffix("px"))
        family = style.get("font-family", "Arial").strip("'\"").split(",")[0].strip("'\"")
        weight = style.get("font-weight", "normal")
        bold = weight in ("bold", "700", "600")
        italic = style.get("font-style", "normal") == "italic"
        font = FontProperties(
            family=family,
            size=size,
            weight="bold" if bold else "normal",
            style="italic" if italic else "normal",
        )
        tw, _, _ = RENDERER.get_text_width_height_descent(content, font, False)
        anchor = style.get("text-anchor", "start")
        x -= tw / 2 if anchor == "middle" else tw if anchor == "end" else 0
        # A baseline-positioned run stays a single editable PowerPoint text object.
        box_width, box_height = tw + 0.5 * size, 1.35 * size
        centre = matrix @ [x + box_width / 2, y - 0.92 * size + box_height / 2, 1]
        factor = math.hypot(matrix[0, 0], matrix[1, 0])
        objects.append(
            {
                "kind": "text",
                "text": content,
                "font": family,
                "fontSize": size * factor,
                "bold": bold,
                "italic": italic,
                "fill": style.get("fill", "#000000"),
                "x": float(centre[0] - box_width * factor / 2),
                "y": float(centre[1] - box_height * factor / 2),
                "w": box_width * factor,
                "h": box_height * factor,
                "rotation": math.degrees(math.atan2(matrix[1, 0], matrix[0, 0])),
            }
        )

    def visit(node, matrix=IDENTITY, inherited=None, inherited_clip=None, instance=False):
        tag = node.tag.removeprefix(SVG)
        if tag in ("defs", "metadata", "style", "clipPath"):
            return
        style = style_of(node, inherited or {})
        matrix = matrix @ transform(node.get("transform", ""))
        clip = inherited_clip
        if node.get("clip-path"):
            clip = clips.get(node.get("clip-path")[5:-1])
        if tag == "use":
            ref = ids[node.get(XLINK)[1:]]
            item = transform(f"translate({node.get('x', '0')} {node.get('y', '0')})")
            copy = ET.fromstring(ET.tostring(ref))
            copy.set(
                "style",
                ";".join(
                    f"{k}:{v}" for k, v in style_of(node, style_of(ref, inherited or {})).items()
                ),
            )
            visit(copy, matrix @ item, {}, clip, True)
        elif tag == "path":
            commands = path_commands(node.get("d", ""), matrix)
            if not commands:
                return
            factor = math.hypot(matrix[0, 0], matrix[1, 0])
            objects.append(
                {
                    "kind": "path",
                    "commands": commands,
                    "fill": style.get("fill", "#000000"),
                    "stroke": style.get("stroke", "none"),
                    "lineWidth": float(style.get("stroke-width", 1)) * factor,
                    "opacity": float(style.get("opacity", 1)),
                    "fillOpacity": float(style.get("fill-opacity", 1)),
                    "strokeOpacity": float(style.get("stroke-opacity", 1)),
                    "dash": style.get("stroke-dasharray", "none"),
                    "clip": clip,
                }
            )
        elif tag in ("text", "tspan"):
            text_object(node, style, matrix)
        elif tag in ("svg", "g"):
            for child in node:
                visit(child, matrix, style, clip)
        elif tag not in ("title", "desc"):
            raise ValueError(f"Unsupported visible SVG element: {tag}")

    visit(root)
    return {
        "width": width,
        "height": height,
        "objects": objects,
        "source": str(path),
        "texts": [r["text"] for r in objects if r["kind"] == "text"],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--build", type=Path, required=True)
    args = parser.parse_args()
    args.build.mkdir(parents=True, exist_ok=True)
    # Reuse the current supplementary renderer and values, routing vector output
    # to the private build directory instead of replacing publication PDFs.
    sys.path.insert(0, str(ROOT / "paper/tools"))
    import matplotlib.pyplot as plt
    import render_ncs_prior_graphical as prior

    plt.rcParams["svg.fonttype"] = "none"

    def save_vector(fig, name):
        fig.savefig(args.build / (name + ".svg"), format="svg", facecolor="white")
        plt.close(fig)

    prior.save = save_vector
    prior.main()
    source = ROOT / "paper/figures/venue-results"
    order = [
        ("Figure 1", "native", "FIgure1_2.pptx", 1, 1448, 1086),
        ("Figure 2", "native", "output/pptx/chemworld-figure2-typography.pptx", 1, 1440, 1040),
        ("Figure 3", "vector", "figure03-goals-paths-forecasts"),
        ("Figure 4", "native", "output/pptx/chemworld-figures-final.pptx", 4, 1440, 1050),
        ("Figure 5", "vector", "figure05-eq-coverage-reversal"),
        ("Figure 6", "vector", "figure06-crystal-generalization"),
        *[
            (f"Figure S1 ({a})", "vector", f"figureS1-prior-graphical-table-{i}")
            for i, a in enumerate(("a\u2013d", "e\u2013h", "i\u2013l", "m\u2013p"), 1)
        ],
        ("Figure S2 (a,b)", "vector", "figureS2-prior-difference-reaction"),
        ("Figure S2 (c\u2013f)", "vector", "figureS2-prior-difference-equilibrium"),
        ("Figure S3", "native", "output/pptx/chemworld-figures-final.pptx", 9, 1440, 960),
        ("Figure S4", "native", "output/pptx/chemworld-figures-final.pptx", 10, 1440, 1460),
        ("Figure S5", "native", "output/pptx/chemworld-figures-final.pptx", 11, 1440, 670),
        ("Figure S6", "vector", "figureS6-goal-world-means"),
    ]
    figures = []
    for row in order:
        name, kind, stem, *extra = row
        data = {"name": name, "kind": kind, "source": stem}
        if kind == "native":
            data.update(slide=extra[0], width=extra[1], height=extra[2])
        else:
            location = args.build if stem.startswith(("figureS1", "figureS2")) else source
            data.update(collect(location / (stem + ".svg")))
        figures.append(data)
        print(f"collect {len(figures)}/{len(order)} {name}", flush=True)
    (args.build / "vectors.json").write_text(
        json.dumps(figures, ensure_ascii=False), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
