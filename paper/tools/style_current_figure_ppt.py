"""Apply the approved font rules directly to existing editable figure objects."""

from __future__ import annotations

import argparse
import copy
import math
import posixpath
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

NS = {
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}
REL = "http://schemas.openxmlformats.org/package/2006/relationships"
CT = "http://schemas.openxmlformats.org/package/2006/content-types"
for prefix, uri in NS.items():
    ET.register_namespace(prefix, uri)

MAIN_TITLES = {
    1: {
        "Static benchmarks",
        "Real laboratories",
        "Single-endpoint evaluation",
        "A Representative Autonomous Campaign in ChemWorld",
        "Controlled study design",
        "Study scope",
    },
    2: {
        "Twelve-batch history: fines and recovery",
        "Batch 8 (B8) experiment in full detail",
        "Key observations, questions, and next tests",
    },
    3: {
        "Electrochemistry",
        "Reaction processing",
        "Two independent 12-batch research paths",
        "The optimization agent's subsequent predictions",
    },
    4: {
        "Electrochemistry Discovery",
        "Electrochemistry Optimization",
        "Partitioning",
        "Crystallization Recovery",
        "Crystallization Fines interval coverage",
        "Crystallization Retested recovery",
    },
    6: {
        "Observed and predicted purity",
        "Lower MAE than the source-mean baseline",
        "Information effects differ across responses",
        "Purity intervals can miss the reference",
    },
    7: {
        "Source research histories",
        "Withheld thermal comparison task",
        "Post-prediction reflection (K2) and proposed next test",
        "Evaluator reference for the withheld question",
    },
}


def encode(root):
    if root.tag == f"{{{CT}}}Types":
        ET.register_namespace("", CT)
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def relpath(part):
    folder, name = posixpath.split(part)
    return posixpath.join(folder, "_rels", name + ".rels")


def slide_order(parts):
    rels = ET.fromstring(parts["ppt/_rels/presentation.xml.rels"])
    targets = {
        r.get("Id"): posixpath.normpath(posixpath.join("ppt", r.get("Target"))).lstrip("/")
        for r in rels
    }
    root = ET.fromstring(parts["ppt/presentation.xml"])
    return [targets[s.get(f"{{{NS['r']}}}id")] for s in root.find("p:sldIdLst", NS)]


def select_slides(parts, indices):
    root = ET.fromstring(parts["ppt/presentation.xml"])
    slides = root.find("p:sldIdLst", NS)
    selected = [s for i, s in enumerate(slides, 1) if i in indices]
    selected_ids = {s.get(f"{{{NS['r']}}}id") for s in selected}
    slides[:] = selected
    for item in list(root):
        if item.tag.rsplit("}", 1)[-1] in {"custShowLst", "sectionLst", "extLst"}:
            root.remove(item)
    parts["ppt/presentation.xml"] = encode(root)
    rels = ET.fromstring(parts["ppt/_rels/presentation.xml.rels"])
    for rel in list(rels):
        if rel.get("Type").endswith("/slide") and rel.get("Id") not in selected_ids:
            rels.remove(rel)
    parts["ppt/_rels/presentation.xml.rels"] = encode(rels)
    # Retain only parts reachable through the selected slides and shared masters.
    keep, pending = {"[Content_Types].xml"}, [""]
    while pending:
        part = pending.pop()
        if part:
            keep.add(part)
        relationship = relpath(part) if part else "_rels/.rels"
        if relationship not in parts or relationship in keep:
            continue
        keep.add(relationship)
        for rel in ET.fromstring(parts[relationship]):
            if rel.get("TargetMode") == "External":
                continue
            target = rel.get("Target")
            target = (
                target.lstrip("/")
                if target.startswith("/")
                else posixpath.normpath(posixpath.join(posixpath.dirname(part), target))
            )
            if target not in keep:
                if target not in parts:
                    raise ValueError(f"Missing relationship target: {target}")
                pending.append(target)
    parts = {name: blob for name, blob in parts.items() if name in keep}
    types = ET.fromstring(parts["[Content_Types].xml"])
    for item in list(types):
        if item.tag == f"{{{CT}}}Override" and item.get("PartName").lstrip("/") not in parts:
            types.remove(item)
    parts["[Content_Types].xml"] = encode(types)
    return parts


def text_of(shape):
    return "".join(t.text or "" for t in shape.findall(".//a:t", NS))


def text_size(shape, size):
    for prop in shape.iter():
        if prop.tag in {f"{{{NS['a']}}}{name}" for name in ("rPr", "defRPr", "endParaRPr")}:
            prop.set("sz", str(size * 100))


def style_slides(parts, kind):
    counts = []
    size_tags = {f"{{{NS['a']}}}{name}" for name in ("rPr", "defRPr", "endParaRPr", "buSzPts")}
    for name, blob in list(parts.items()):
        if not name.startswith("ppt/") or not name.endswith(".xml"):
            continue
        root = ET.fromstring(blob)
        for prop in root.iter():
            if prop.tag in size_tags and prop.get("sz"):
                prop.set("sz", str(math.ceil(int(prop.get("sz")) / 200) * 200))
            if prop.tag.rsplit("}", 1)[-1] in {"latin", "ea", "cs", "buFont"}:
                prop.set("typeface", "Times New Roman")
            if prop.tag in {f"{{{NS['a']}}}normAutofit", f"{{{NS['a']}}}spAutoFit"}:
                prop.tag = f"{{{NS['a']}}}noAutofit"
                prop.attrib.clear()
        parts[name] = encode(root)
    for index, name in enumerate(slide_order(parts), 1):
        root = ET.fromstring(parts[name])
        shapes = root.findall(".//p:sp", NS)
        letters, titles = [], []
        for shape in shapes:
            text = text_of(shape)
            sizes = [int(p.get("sz")) for p in shape.iter() if p.tag in size_tags and p.get("sz")]
            is_letter = bool(re.fullmatch("[a-pA-D]", text)) and sizes and max(sizes) >= 1600
            if is_letter:
                text_size(shape, 20)
                letters.append(shape)
            if kind == "main" and text in MAIN_TITLES.get(index, set()):
                titles.append(shape)
        if kind == "supplementary":
            if index <= 6:
                # Imported vector panel titles immediately follow each panel letter;
                # S2 has an intervening baseline key, so use the known figure titles.
                for shape in shapes:
                    text = text_of(shape)
                    if (index <= 4 and " / " in text) or (
                        index in (5, 6)
                        and text
                        in {
                            "Reaction / discovery",
                            "Reaction / optimization",
                            "Other nine / macro MAE",
                            "Dilute three / macro MAE",
                            "Other nine / interval coverage",
                            "Dilute three / interval coverage",
                        }
                    ):
                        titles.append(shape)
            elif index == 7:
                title_ids = {6, 71, 136, 201, 270, 336}
                titles = [
                    s for s in shapes if int(s.find("p:nvSpPr/p:cNvPr", NS).get("id")) in title_ids
                ]
            elif index == 8:
                titles = [
                    s for s in shapes if text_of(s) in {"Purification", "Size index", "Fines"}
                ]
            elif index == 9:
                for shape in shapes:
                    text = text_of(shape)
                    if re.fullmatch(r"[a-d]\s+(EC|RX)", text):
                        paragraph = shape.find("p:txBody/a:p", NS)
                        run = paragraph.find("a:r", NS)
                        first = copy.deepcopy(run)
                        first.find("a:t", NS).text = text[0]
                        text_size(first, 20)
                        second = copy.deepcopy(run)
                        second.find("a:t", NS).text = "   " + text[-2:]
                        text_size(second, 18)
                        position = list(paragraph).index(run)
                        paragraph.remove(run)
                        paragraph.insert(position, first)
                        paragraph.insert(position + 1, second)
        for shape in titles:
            text_size(shape, 18)
        parts[name] = encode(root)
        counts.append((index, len(letters), len(titles)))
    return counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--kind", choices=("main", "supplementary"), required=True)
    parser.add_argument("--select", help="One-based slide numbers to retain from the source")
    args = parser.parse_args()
    if args.source.resolve() == args.output.resolve():
        parser.error("Work on a separate candidate; preserve the source until reviewed")
    with ZipFile(args.source) as archive:
        parts = {name: archive.read(name) for name in archive.namelist()}
    if args.select:
        parts = select_slides(parts, {int(value) for value in args.select.split(",")})
    counts = style_slides(parts, args.kind)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(args.output, "w", ZIP_DEFLATED) as archive:
        for name, blob in parts.items():
            archive.writestr(name, blob)
    for index, letters, titles in counts:
        print(
            f"Typography: slide={index} panel_letters={letters} panel_titles={titles}", flush=True
        )
    print(args.output, flush=True)


if __name__ == "__main__":
    main()
