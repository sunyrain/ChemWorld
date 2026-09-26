"""Prepare exact editable Figure 5 geometry and patch only its collection slide."""

from __future__ import annotations

import argparse
import copy
import json
import posixpath
import shutil
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

from collect_current_figure_vectors import collect
from package_current_figure_collection import NS, A, P, encode, patch_curves

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "output/pptx/chemworld-current-figures-editable.pptx"


def prepare(build: Path) -> None:
    build.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SOURCE, build / "source.pptx")
    figure = {"name": "Figure 5", "kind": "vector", **collect(build / "figure05.svg")}
    fonts = {o["font"] for o in figure["objects"] if o["kind"] == "text"}
    sizes = {round(o["fontSize"], 6) for o in figure["objects"] if o["kind"] == "text"}
    assert fonts == {"Times New Roman"}, fonts
    assert sizes <= {16, 18, 20}, sizes
    (build / "vector.json").write_text(json.dumps(figure, ensure_ascii=False), encoding="utf-8")
    print(f"Figure 5 native preparation: {len(figure['objects'])} objects, sizes={sorted(sizes)}")


def package(build: Path) -> None:
    with zipfile.ZipFile(build / "source.pptx") as z:
        original = {name: z.read(name) for name in z.namelist()}
    parts = dict(original)
    with zipfile.ZipFile(build / "figure05-native.pptx") as z:
        replacement = ET.fromstring(z.read("ppt/slides/slide1.xml"))
    figure = json.loads((build / "vector.json").read_text(encoding="utf-8"))
    patch_curves(replacement, figure, 0)
    slide_name = "ppt/slides/slide5.xml"
    old = ET.fromstring(parts[slide_name])
    tree = old.find("p:cSld/p:spTree", NS)
    for node in list(tree):
        if node.tag not in {f"{{{P}}}nvGrpSpPr", f"{{{P}}}grpSpPr"}:
            tree.remove(node)
    for node in replacement.find("p:cSld/p:spTree", NS):
        if node.tag not in {f"{{{P}}}nvGrpSpPr", f"{{{P}}}grpSpPr"}:
            tree.append(copy.deepcopy(node))
    parts[slide_name] = encode(old)
    relationships = ET.fromstring(parts["ppt/slides/_rels/slide5.xml.rels"])
    for rel in relationships:
        if rel.get("Type", "").endswith("/notesSlide"):
            note_path = posixpath.normpath(posixpath.join("ppt/slides", rel.get("Target")))
            notes = ET.fromstring(parts[note_path])
            for shape in notes.findall(".//p:sp", NS):
                placeholder = shape.find("p:nvSpPr/p:nvPr/p:ph", NS)
                if placeholder is None or placeholder.get("type") != "body":
                    continue
                body = shape.find("p:txBody", NS)
                for paragraph in list(body.findall("a:p", NS)):
                    body.remove(paragraph)
                paragraph = ET.SubElement(body, f"{{{A}}}p")
                run = ET.SubElement(paragraph, f"{{{A}}}r")
                ET.SubElement(run, f"{{{A}}}t").text = (
                    "Figure 5. Source: retained EQ_AUTONOMOUS_PROCESS.json and "
                    "STORY_WORLD_ANALYSIS.json, work-ii-evidence-closeout-20260921. "
                    "All 180 source assays, 60 world-query references, 30 world-level errors "
                    "and 20 original forecasts/reference values are retained. "
                    "Panels a/b show sample SD across five reused worlds, "
                    "not confidence intervals. Panel c shows the pooled source response range. "
                    "Concentration grouping is post hoc. "
                    "Rebuild: paper/tools/render_figure05_readable.py "
                    "and update_figure05_collection.py."
                )
            parts[note_path] = encode(notes)
    for index in (1, 2, 3, 4, 6, 7):
        assert parts[f"ppt/slides/slide{index}.xml"] == original[f"ppt/slides/slide{index}.xml"]
    for node in old.findall(".//a:rPr", NS):
        if node.get("sz"):
            assert int(node.get("sz")) in {1600, 1800, 2000}, node.attrib
    with zipfile.ZipFile(build / "assembled-candidate.pptx", "w", zipfile.ZIP_DEFLATED) as z:
        for name, content in parts.items():
            z.writestr(name, content)
    print("Figure 5 packaged; six other slide XML parts unchanged.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("prepare", "package"))
    parser.add_argument("--build", required=True, type=Path)
    args = parser.parse_args()
    (prepare if args.stage == "prepare" else package)(args.build)
