"""Integrate new Figures 4/5 while retaining the user-edited source slides."""

from __future__ import annotations

import argparse
import copy
import json
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

from package_current_figure_collection import CT, NS, REL, A, P, R, encode, patch_curves

ROOT = Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build", type=Path, required=True)
    args = parser.parse_args()
    build = args.build
    source = ROOT / "output/pptx/chemworld-current-figures-editable.pptx"
    snapshot = build / "source.pptx"
    if not snapshot.exists():
        snapshot.write_bytes(source.read_bytes())
    with zipfile.ZipFile(snapshot) as z:
        original = {name: z.read(name) for name in z.namelist()}
    parts = dict(original)
    with zipfile.ZipFile(build / "new-figures-native.pptx") as z:
        native = {name: z.read(name) for name in z.namelist()}
    content_types = ET.fromstring(parts["[Content_Types].xml"])
    rels = ET.fromstring(parts["ppt/_rels/presentation.xml.rels"])
    pres = ET.fromstring(parts["ppt/presentation.xml"])
    ids = pres.find("p:sldIdLst", NS)
    existing = list(ids)
    next_rid = max(int(r.get("Id")[3:]) for r in rels if r.get("Id", "").startswith("rId")) + 1
    next_id = max(int(s.get("id")) for s in ids) + 1
    original_slide_rels = ET.fromstring(parts["ppt/slides/_rels/slide4.xml.rels"])
    layout_target = next(
        r.get("Target") for r in original_slide_rels if r.get("Type", "").endswith("/slideLayout")
    )
    inserted = []
    for index, stem in enumerate(("figure04", "figure05")):
        number = index + 8
        slide = ET.fromstring(native[f"ppt/slides/slide{index + 1}.xml"])
        figure = json.loads((build / f"{stem}-vector.json").read_text(encoding="utf-8"))
        patch_curves(slide, figure, index)
        parts[f"ppt/slides/slide{number}.xml"] = encode(slide)
        # Native scientific diagrams require no image/chart resource relationships.
        slide_rels = ET.Element(f"{{{REL}}}Relationships")
        ET.SubElement(
            slide_rels,
            f"{{{REL}}}Relationship",
            Id="rId1",
            Type=f"{R}/slideLayout",
            Target=layout_target,
        )
        ET.SubElement(
            slide_rels,
            f"{{{REL}}}Relationship",
            Id="rId2",
            Type=f"{R}/notesSlide",
            Target=f"../notesSlides/notesSlide{number}.xml",
        )
        parts[f"ppt/slides/_rels/slide{number}.xml.rels"] = encode(slide_rels)
        notes = ET.fromstring(parts["ppt/notesSlides/notesSlide4.xml"])
        for shape in notes.findall(".//p:sp", NS):
            ph = shape.find("p:nvSpPr/p:nvPr/p:ph", NS)
            if ph is None or ph.get("type") != "body":
                continue
            body = shape.find("p:txBody", NS)
            for para in list(body.findall("a:p", NS)):
                body.remove(para)
            para = ET.SubElement(body, f"{{{A}}}p")
            run = ET.SubElement(para, f"{{{A}}}r")
            ET.SubElement(run, f"{{{A}}}t").text = (
                "Retained scientific evidence only. Source: source-data.json in "
                "paper/figures/narrative-final, EQ_AUTONOMOUS_PROCESS.json and "
                "STORY_WORLD_ANALYSIS.json in work-ii-evidence-closeout-20260921, "
                "eq-astra-medium-20260927 and eq-three-model-matrix-20260927. "
                "All worlds and arms retained. Rebuild: render_ncs_narrative_closeout.py, "
                "build_ncs_narrative_figures.mjs, package_ncs_narrative_figures.py. "
                + (
                    "Figure 4: world sample SD is descriptive, not a confidence interval. "
                    "Other nine queries include unobserved conditions."
                    if index == 0
                    else "Figure 5: Astra W03/MisIndexed K1 is a condensed public report "
                    "after all 12 experiments and before Q. Sol/Opaque keeps all five "
                    "original forecasts and 80% intervals. Minima include positive loading "
                    "only; the shaded test range is not a physical transition boundary."
                )
            )
        parts[f"ppt/notesSlides/notesSlide{number}.xml"] = encode(notes)
        note_rels = ET.fromstring(parts["ppt/notesSlides/_rels/notesSlide4.xml.rels"])
        for rel in note_rels:
            if rel.get("Type", "").endswith("/slide"):
                rel.set("Target", f"../slides/slide{number}.xml")
        parts[f"ppt/notesSlides/_rels/notesSlide{number}.xml.rels"] = encode(note_rels)
        for kind, typ in (("slides/slide", "slide"), ("notesSlides/notesSlide", "notesSlide")):
            ET.SubElement(
                content_types,
                f"{{{CT}}}Override",
                PartName=f"/ppt/{kind}{number}.xml",
                ContentType=f"application/vnd.openxmlformats-officedocument.presentationml.{typ}+xml",
            )
        rid = f"rId{next_rid + index}"
        ET.SubElement(
            rels,
            f"{{{REL}}}Relationship",
            Id=rid,
            Type=f"{R}/slide",
            Target=f"slides/slide{number}.xml",
        )
        inserted.append(
            ET.Element(f"{{{P}}}sldId", {"id": str(next_id + index), f"{{{R}}}id": rid})
        )
    ids[:] = [
        existing[0],
        existing[1],
        existing[2],
        *inserted,
        existing[5],
        existing[6],
        existing[3],
        existing[4],
    ]
    parts["ppt/presentation.xml"] = encode(pres)
    parts["ppt/_rels/presentation.xml.rels"] = encode(rels)
    ET.register_namespace("", CT)
    parts["[Content_Types].xml"] = encode(content_types)
    ET.register_namespace("", REL)
    # Change the scope line only; retain the accepted platform illustration.
    s1 = ET.fromstring(parts["ppt/slides/slide1.xml"])
    for shape in s1.findall(".//p:sp", NS):
        text = "".join(t.text or "" for t in shape.findall(".//a:t", NS))
        if "240" not in text or "chemical system families" not in text:
            continue
        paragraph = shape.find("p:txBody/a:p", NS)
        run = copy.deepcopy(paragraph.find("a:r", NS))
        run.find("a:t", NS).text = "240 Sol campaigns / 6 families + 60 equilibrium campaigns"
        for node in list(paragraph):
            if node.tag in (f"{{{A}}}r", f"{{{A}}}br", f"{{{A}}}fld"):
                paragraph.remove(node)
        paragraph.insert(1, run)
        for prop in run.findall("a:rPr", NS):
            prop.set("b", "0")
    parts["ppt/slides/slide1.xml"] = encode(s1)
    for n in range(2, 8):
        assert parts[f"ppt/slides/slide{n}.xml"] == original[f"ppt/slides/slide{n}.xml"]
    app = ET.fromstring(parts["docProps/app.xml"])
    for node in app.iter():
        if node.tag.endswith("}Slides"):
            node.text = "9"
    parts["docProps/app.xml"] = encode(app)
    with zipfile.ZipFile(build / "assembled-candidate.pptx", "w", zipfile.ZIP_DEFLATED) as z:
        for name, payload in parts.items():
            z.writestr(name, payload)
    print(
        "Nine-slide collection: six main figures, S4, preserved budget S7, preserved Sol detail S8."
    )


if __name__ == "__main__":
    main()
