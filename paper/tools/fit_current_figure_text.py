"""Fit existing text boxes using measurements from the native presentation app."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from style_current_figure_ppt import NS, encode, slide_order, text_of, text_size


def objects(root):
    found = {}

    def walk(parent, prefix="", sx=1, sy=1, tx=0, ty=0):
        for shape in parent:
            tag = shape.tag.rsplit("}", 1)[-1]
            nv = shape.find("p:nvSpPr/p:cNvPr", NS)
            if tag == "grpSp":
                nv = shape.find("p:nvGrpSpPr/p:cNvPr", NS)
            if nv is None:
                continue
            path = prefix + nv.get("id")
            if tag == "grpSp":
                xf = shape.find("p:grpSpPr/a:xfrm", NS)
                if xf is None or xf.find("a:ext", NS) is None:
                    walk(shape, path + "/", sx, sy, tx, ty)
                    continue
                off, ext = xf.find("a:off", NS), xf.find("a:ext", NS)
                co, ce = xf.find("a:chOff", NS), xf.find("a:chExt", NS)
                kx, ky = (
                    int(ext.get("cx")) / int(ce.get("cx")),
                    int(ext.get("cy")) / int(ce.get("cy")),
                )
                walk(
                    shape,
                    path + "/",
                    sx * kx,
                    sy * ky,
                    tx + sx * (int(off.get("x")) - kx * int(co.get("x"))) / 12700,
                    ty + sy * (int(off.get("y")) - ky * int(co.get("y"))) / 12700,
                )
            else:
                found[path] = (shape, sx, sy, tx, ty)

    walk(root.find("p:cSld/p:spTree", NS))
    return found


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("metrics", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--kind", choices=("main", "supplementary"), required=True)
    args = parser.parse_args()
    with ZipFile(args.source) as archive:
        parts = {n: archive.read(n) for n in archive.namelist()}
    from xml.etree import ElementTree as ET

    paths = slide_order(parts)
    roots = {i: ET.fromstring(parts[path]) for i, path in enumerate(paths, 1)}
    maps = {i: objects(root) for i, root in roots.items()}
    metrics = json.loads(args.metrics.read_text(encoding="utf-8-sig"))
    changed = set()

    def patch(m, x=None, y=None, w=None, h=None):
        shape, sx, sy, tx, ty = maps[m["slide"]][m["path"]]
        xf = shape.find("p:spPr/a:xfrm", NS)
        for key, value, scale, offset in (("x", x, sx, tx), ("y", y, sy, ty)):
            if value is not None:
                xf.find("a:off", NS).set(key, str(round((value - offset) / scale * 12700)))
        for key, value, scale in (("cx", w, sx), ("cy", h, sy)):
            if value is not None:
                xf.find("a:ext", NS).set(key, str(round(value / scale * 12700)))
        changed.add((m["slide"], m["path"]))

    for m in metrics:
        if abs(m["rotation"]) > 0.1:
            continue
        shape = maps[m["slide"]][m["path"]][0]
        body = shape.find("p:txBody/a:bodyPr", NS)
        paragraph = shape.find("p:txBody/a:p/a:pPr", NS)
        align = paragraph.get("algn", "l") if paragraph is not None else "l"
        anchor = body.get("anchor", "t") if body is not None else "t"
        dw = max(0, m["boundW"] + m["left"] + m["right"] + 1.0 - m["w"])
        dh = max(0, m["boundH"] + m["top"] + m["bottom"] + 1.0 - m["h"])
        if dw > 0.5 or dh > 0.5:
            patch(
                m,
                x=m["x"] - dw * {"r": 1, "ctr": 0.5}.get(align, 0),
                y=m["y"] - dh * {"b": 1, "ctr": 0.5}.get(anchor, 0),
                w=m["w"] + dw,
                h=m["h"] + dh,
            )

    def by_id(slide, ident):
        return next(m for m in metrics if m["slide"] == slide and m["id"] == ident)

    if args.kind == "main":
        # Separate short labels that occupied consecutive single-line boxes.
        for slide, ident, dy in (
            (1, 129, -3), (1, 130, -3), (1, 131, -3), (1, 132, 1.5),
            (3, 223, 8), (3, 228, -6.5), (3, 229, .5), (3, 230, 7.5),
            (5, 304, 5), (5, 406, 5), (5, 423, 5),
            (7, 57, 4), (7, 60, 4), (7, 67, 4), (7, 116, 4), (7, 183, 4),
        ):
            m = by_id(slide, ident)
            patch(m, y=m["y"] + dy)
        # Give the complete system name one line instead of breaking the word.
        m = by_id(1, 168)
        patch(m, x=m["x"] - (94 - m["w"]) / 2, w=94, h=17)
        # Restore normal word spacing in an axis title imported as separate glyphs.
        m = by_id(5, 65)
        shape = maps[5][m["path"]][0]
        shape.find(".//a:t", NS).text = "Nominal concentration (mol L⁻¹; log scale)"
        paragraph = shape.find("p:txBody/a:p", NS)
        properties = paragraph.find("a:pPr", NS)
        if properties is None:
            properties = ET.Element(f"{{{NS['a']}}}pPr")
            paragraph.insert(0, properties)
        properties.set("algn", "ctr")
        patch(m, x=153, y=441.5, w=310, h=19)
        parents = {child: parent for parent in roots[5].iter() for child in parent}
        for ident in range(66, 102):
            item = maps[5][by_id(5, ident)["path"]][0]
            parents[item].remove(item)
        # Keep adjacent data labels distinct after the 17 -> 18 pt change.
        for ident, dy in ((97, 6), (101, -6), (103, -12)):
            m = by_id(6, ident)
            patch(m, y=m["y"] + dy)
        # S4 review text stays inside its table rows, and the two option labels
        # retain a visible gap below the reference bars.
        m = by_id(7, 156)
        patch(m, y=m["y"] - 7)
        m = by_id(7, 194)
        patch(m, x=m["x"] - 5)
        m = by_id(7, 195)
        patch(m, x=m["x"] + 4)
    else:
        # Leave a full line gap between each S3 title and its mean summary.
        for ident in (5, 6, 70, 71, 135, 136, 200, 201, 269, 270, 335, 336):
            m = by_id(7, ident)
            patch(m, y=m["y"] - 5)
        shape = maps[8][by_id(8, 6)["path"]][0]
        assert text_of(shape) == "Size index"
        text_size(shape, 18)

    for index, root in roots.items():
        parts[paths[index - 1]] = encode(root)
    with ZipFile(args.output, "w", ZIP_DEFLATED) as archive:
        for name, data in parts.items():
            archive.writestr(name, data)
    print(f"Text fit: adjusted={len(changed)} boxes; output={args.output}")


if __name__ == "__main__":
    main()
