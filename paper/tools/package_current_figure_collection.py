"""Preserve native slide resources and exact SVG curves in the collection."""

from __future__ import annotations

import argparse
import copy
import json
import posixpath
import re
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

import numpy as np
from matplotlib.path import Path as MplPath
from matplotlib.transforms import Bbox

ROOT = Path(__file__).resolve().parents[2]
P = "http://schemas.openxmlformats.org/presentationml/2006/main"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
REL = "http://schemas.openxmlformats.org/package/2006/relationships"
CT = "http://schemas.openxmlformats.org/package/2006/content-types"
NS = {"p": P, "a": A, "r": R}
for prefix, uri in NS.items():
    ET.register_namespace(prefix, uri)
ET.register_namespace("", REL)
EMU = 9525
WIDTH, HEIGHT, MARGIN = 1440, 1200, 36


def encode(node):
    return ET.tostring(node, encoding="utf-8", xml_declaration=True)


def rel_path(part):
    folder, name = posixpath.split(part)
    return posixpath.join(folder, "_rels", name + ".rels")


def mpl_path(commands):
    vertices, codes = [], []
    for command in commands:
        kind = command[0]
        if kind == "Z":
            vertices.append([0, 0])
            codes.append(MplPath.CLOSEPOLY)
        else:
            for point in command[1:]:
                vertices.append(point)
                codes.append(
                    {
                        "M": MplPath.MOVETO,
                        "L": MplPath.LINETO,
                        "Q": MplPath.CURVE3,
                        "C": MplPath.CURVE4,
                    }[kind]
                )
    return MplPath(np.array(vertices), np.array(codes))


def line_clip(p1, p2, clip):
    x1, y1 = p1
    dx, dy = p2[0] - x1, p2[1] - y1
    lower, upper = 0.0, 1.0
    for a, b in ((-dx, x1 - clip[0]), (dx, clip[2] - x1), (-dy, y1 - clip[1]), (dy, clip[3] - y1)):
        if abs(a) < 1e-15:
            if b < 0:
                return None
            continue
        u = b / a
        if a < 0:
            lower = max(lower, u)
        else:
            upper = min(upper, u)
        if lower > upper:
            return None
    return [[x1 + lower * dx, y1 + lower * dy], [x1 + upper * dx, y1 + upper * dy]]


def clipped_commands(obj):
    commands, clip = obj["commands"], obj["clip"]
    if not clip:
        return commands
    points = [p for c in commands for p in c[1:]]
    if all(
        clip[0] - 1e-5 <= p[0] <= clip[2] + 1e-5 and clip[1] - 1e-5 <= p[1] <= clip[3] + 1e-5
        for p in points
    ):
        return commands
    curve = mpl_path(commands)
    if obj["fill"] != "none":
        result = []
        for values, code in curve.clip_to_bbox(Bbox.from_extents(*clip)).iter_segments(
            curves=False
        ):
            result.append(
                ["Z"]
                if code == MplPath.CLOSEPOLY
                else ["M" if code == MplPath.MOVETO else "L", values.tolist()]
            )
        return result
    result, previous = [], None
    for values, code in curve.iter_segments(curves=False):
        point = values.tolist()
        if code == MplPath.MOVETO:
            previous = point
        elif code == MplPath.LINETO:
            segment = line_clip(previous, point, clip)
            if segment:
                result.extend([["M", segment[0]], ["L", segment[1]]])
            previous = point
    return result


def patch_curves(root, figure, figure_index):
    objects = figure["objects"]
    k = min((WIDTH - 2 * MARGIN) / figure["width"], (HEIGHT - 2 * MARGIN) / figure["height"])
    dx, dy = (WIDTH - figure["width"] * k) / 2, (HEIGHT - figure["height"] * k) / 2
    for shape in root.findall(".//p:sp", NS):
        props = shape.find("p:nvSpPr/p:cNvPr", NS)
        match = re.fullmatch(r"vector-(\d+)-(\d+)", props.get("name", ""))
        if not match:
            continue
        assert int(match[1]) == figure_index
        obj = objects[int(match[2])]
        if obj["kind"] == "text":
            props.set("name", obj["text"][:110])
            continue
        props.set("name", f"{figure['name']} plot object {match[2]}")
        commands = clipped_commands(obj)
        if not commands:
            shape.find("p:spPr", NS).clear()
            continue
        points = [p for c in commands for p in c[1:]]
        x, y = min(p[0] for p in points), min(p[1] for p in points)
        w = max(0.001, max(p[0] for p in points) - x)
        h = max(0.001, max(p[1] for p in points) - y)
        sppr = shape.find("p:spPr", NS)
        xfrm = sppr.find("a:xfrm", NS)
        xfrm.find("a:off", NS).attrib.update(
            x=str(round((dx + x * k) * EMU)), y=str(round((dy + y * k) * EMU))
        )
        xfrm.find("a:ext", NS).attrib.update(cx=str(round(w * k * EMU)), cy=str(round(h * k * EMU)))
        geom = sppr.find("a:custGeom", NS)
        paths = geom.find("a:pathLst", NS)
        paths.clear()
        path = ET.SubElement(
            paths,
            f"{{{A}}}path",
            w=str(max(1, round(w * k * EMU))),
            h=str(max(1, round(h * k * EMU))),
        )
        for command in commands:
            node = ET.SubElement(
                path,
                f"{{{A}}}"
                + {"M": "moveTo", "L": "lnTo", "C": "cubicBezTo", "Q": "quadBezTo", "Z": "close"}[
                    command[0]
                ],
            )
            for point in command[1:]:
                ET.SubElement(
                    node,
                    f"{{{A}}}pt",
                    x=str(round((point[0] - x) * k * EMU)),
                    y=str(round((point[1] - y) * k * EMU)),
                )
        # The native dash lengths retain the SVG's source units.
        line = sppr.find("a:ln", NS)
        if line is not None and obj["dash"] != "none":
            for child in list(line):
                if child.tag in (f"{{{A}}}prstDash", f"{{{A}}}custDash"):
                    line.remove(child)
            dash = [float(v) for v in obj["dash"].replace(",", " ").split()]
            if len(dash) % 2:
                dash *= 2
            custom = ET.SubElement(line, f"{{{A}}}custDash")
            for d, gap in zip(dash[::2], dash[1::2], strict=True):
                ET.SubElement(
                    custom,
                    f"{{{A}}}ds",
                    d=str(round(d / max(obj["lineWidth"], 0.001) * 100000)),
                    sp=str(round(gap / max(obj["lineWidth"], 0.001) * 100000)),
                )


def group_native(root, figure):
    tree = root.find("p:cSld/p:spTree", NS)
    children = [n for n in tree if n.tag not in (f"{{{P}}}nvGrpSpPr", f"{{{P}}}grpSpPr")]
    max_id = max([int(n.get("id", 0)) for n in tree.findall(".//p:cNvPr", NS)] + [1])
    group = ET.Element(f"{{{P}}}grpSp")
    nv = ET.SubElement(group, f"{{{P}}}nvGrpSpPr")
    ET.SubElement(nv, f"{{{P}}}cNvPr", id=str(max_id + 1), name=figure["name"])
    ET.SubElement(nv, f"{{{P}}}cNvGrpSpPr")
    ET.SubElement(nv, f"{{{P}}}nvPr")
    properties = ET.SubElement(group, f"{{{P}}}grpSpPr")
    xfrm = ET.SubElement(properties, f"{{{A}}}xfrm")
    w, h = figure["width"], figure["height"]
    k = min((WIDTH - 2 * MARGIN) / w, (HEIGHT - 2 * MARGIN) / h)
    # PowerPoint keeps explicit run sizes when adding an outer group. Scale the
    # copied run sizes along with its geometry to avoid introducing line wraps.
    for node in root.iter():
        if (
            node.tag in (f"{{{A}}}rPr", f"{{{A}}}defRPr", f"{{{A}}}endParaRPr")
            and "sz" in node.attrib
        ):
            node.set("sz", str(round(int(node.get("sz")) * k)))
    ET.SubElement(
        xfrm,
        f"{{{A}}}off",
        x=str(round((WIDTH - w * k) / 2 * EMU)),
        y=str(round((HEIGHT - h * k) / 2 * EMU)),
    )
    ET.SubElement(xfrm, f"{{{A}}}ext", cx=str(round(w * k * EMU)), cy=str(round(h * k * EMU)))
    ET.SubElement(xfrm, f"{{{A}}}chOff", x="0", y="0")
    ET.SubElement(xfrm, f"{{{A}}}chExt", cx=str(round(w * EMU)), cy=str(round(h * EMU)))
    for child in children:
        tree.remove(child)
        group.append(child)
    tree.append(group)
    root.find("p:cSld", NS).set("name", figure["name"])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--build", type=Path, required=True)
    args = parser.parse_args()
    figures = json.loads((args.build / "vectors.json").read_text(encoding="utf-8"))
    with zipfile.ZipFile(args.build / "vector-candidate.pptx") as archive:
        output = {name: archive.read(name) for name in archive.namelist()}
    content_types = ET.fromstring(output["[Content_Types].xml"])
    defaults = {n.get("Extension") for n in content_types if n.tag.endswith("Default")}
    sources, mappings = {}, {}

    def copy_part(source_path, part, destination=None):
        if source_path not in sources:
            with zipfile.ZipFile(ROOT / source_path) as archive:
                sources[source_path] = {name: archive.read(name) for name in archive.namelist()}
        source = sources[source_path]
        key = (source_path, part)
        if key in mappings:
            return mappings[key]
        if destination is None:
            folder, name = posixpath.split(part)
            destination = posixpath.join(
                folder, f"import{list(sources).index(source_path) + 1}-{name}"
            )
        mappings[key] = destination
        output[destination] = source[part]
        types = ET.fromstring(source["[Content_Types].xml"])
        for entry in types:
            if entry.get("PartName") == "/" + part:
                new = copy.deepcopy(entry)
                new.set("PartName", "/" + destination)
                if not any(e.get("PartName") == "/" + destination for e in content_types):
                    content_types.append(new)
            elif entry.tag.endswith("Default") and entry.get("Extension") not in defaults:
                content_types.append(copy.deepcopy(entry))
                defaults.add(entry.get("Extension"))
        rels = rel_path(part)
        if rels in source:
            relationships = ET.fromstring(source[rels])
            for rel in relationships:
                if rel.get("TargetMode") == "External":
                    continue
                target = posixpath.normpath(
                    posixpath.join(posixpath.dirname(part), rel.get("Target"))
                )
                copied = copy_part(source_path, target)
                rel.set("Target", posixpath.relpath(copied, posixpath.dirname(destination)))
            output[rel_path(destination)] = encode(relationships)
        return destination

    summary = []
    for i, figure in enumerate(figures):
        slide_path = f"ppt/slides/slide{i + 2}.xml"
        # Keep newly authored, current figure notes when importing historical slide sources.
        current_rels = ET.fromstring(output[rel_path(slide_path)])
        note_rel = next(
            (copy.deepcopy(n) for n in current_rels if n.get("Type", "").endswith("/notesSlide")),
            None,
        )
        if figure["kind"] == "native":
            original = f"ppt/slides/slide{figure['slide']}.xml"
            copy_part(figure["source"], original, slide_path)
            root = ET.fromstring(output[slide_path])
            group_native(root, figure)
            rels = ET.fromstring(output[rel_path(slide_path)])
            for rel in list(rels):
                if rel.get("Type", "").endswith("/notesSlide"):
                    rels.remove(rel)
            if note_rel is not None:
                note_rel.set("Id", "rIdCollectionNotes")
                rels.append(note_rel)
            output[rel_path(slide_path)] = encode(rels)
        else:
            root = ET.fromstring(output[slide_path])
            patch_curves(root, figure, i)
            root.find("p:cSld", NS).set("name", figure["name"])
        output[slide_path] = encode(root)
        row = {
            "slide": i + 2,
            "figure": figure["name"],
            "type": figure["kind"],
            "shapes": len(root.findall(".//p:sp", NS)),
            "pictures": len(root.findall(".//p:pic", NS)),
            "text_runs": len(root.findall(".//a:t", NS)),
            "charts": len(
                root.findall(".//{http://schemas.openxmlformats.org/drawingml/2006/chart}chart")
            ),
        }
        if figure["kind"] == "vector":
            actual = [n.text or "" for n in root.findall(".//a:t", NS)]
            assert actual == figure["texts"], (figure["name"], "text content differs")
        summary.append(row)
        print(
            f"package {i + 1}/{len(figures)} {figure['name']} objects={row['shapes']}", flush=True
        )
    # The retained chart workbooks already contain their series headers. Repair
    # legacy literal strings stored as formulas by pointing to those same cells.
    chart_ns = "http://schemas.openxmlformats.org/drawingml/2006/chart"
    for name, data in list(output.items()):
        if not name.startswith("ppt/charts/") or not name.endswith(".xml"):
            continue
        chart = ET.fromstring(data)
        changed = False
        for series in chart.findall(f".//{{{chart_ns}}}ser"):
            formula = series.find(f"{{{chart_ns}}}tx/{{{chart_ns}}}strRef/{{{chart_ns}}}f")
            if formula is None or "!" in (formula.text or ""):
                continue
            values = series.find(f"{{{chart_ns}}}yVal/{{{chart_ns}}}numRef/{{{chart_ns}}}f")
            match = re.fullmatch(r"(.+!)\$([A-Z]+)\$2:\$[A-Z]+\$\d+", values.text)
            assert match is not None, values.text
            formula.text = match[1] + "$" + match[2] + "$1"
            changed = True
        if changed:
            output[name] = encode(chart)
    ET.register_namespace("", CT)
    output["[Content_Types].xml"] = encode(content_types)
    ET.register_namespace("", REL)
    # Validate every internal target after resource remapping.
    for name, data in output.items():
        if not name.endswith(".rels"):
            continue
        folder = posixpath.dirname(posixpath.dirname(name))
        for rel in ET.fromstring(data):
            if rel.get("TargetMode") != "External":
                target = posixpath.normpath(posixpath.join(folder, rel.get("Target"))).lstrip("/")
                assert target in output, (name, target)
    destination = args.build / "assembled-candidate.pptx"
    with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, data in output.items():
            archive.writestr(name, data)
    (args.build / "editable-inventory.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    print(destination)


if __name__ == "__main__":
    main()
