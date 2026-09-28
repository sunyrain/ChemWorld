"""Replace the selected figure slides, preserving the seven other slides exactly."""

from __future__ import annotations

import argparse
import json
import posixpath
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

from package_current_figure_collection import CT, NS, REL, A, R, encode, patch_curves


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build", type=Path, required=True)
    parser.add_argument(
        "--figures", nargs="+", choices=("figure04", "figure05"), default=("figure04", "figure05")
    )
    args = parser.parse_args()
    build = args.build
    with zipfile.ZipFile(build / "source.pptx") as z:
        original = {n: z.read(n) for n in z.namelist()}
    parts = dict(original)
    assert len(ET.fromstring(parts["ppt/presentation.xml"]).find("p:sldIdLst", NS)) == 9
    with zipfile.ZipFile(build / "new-figures-native.pptx") as z:
        native = {n: z.read(n) for n in z.namelist()}
    ct = ET.fromstring(parts["[Content_Types].xml"])
    for index, stem in enumerate(("figure04", "figure05")):
        if stem not in args.figures:
            continue
        num = index + 8
        slide = ET.fromstring(native[f"ppt/slides/slide{index + 1}.xml"])
        figure = json.loads((build / f"{stem}-vector.json").read_text(encoding="utf-8"))
        patch_curves(slide, figure, index)
        if index == 1:
            meta = json.loads((build / "figure05-image.json").read_text(encoding="utf-8"))
            for fill in slide.findall(".//p:pic/p:blipFill", NS):
                for child in list(fill):
                    if child.tag != f"{{{A}}}blip":
                        fill.remove(child)
                ET.SubElement(
                    fill,
                    f"{{{A}}}srcRect",
                    **{
                        k: str(round(meta["crop"][v] * 100000))
                        for k, v in (("l", "left"), ("t", "top"), ("r", "right"), ("b", "bottom"))
                    },
                )
                ET.SubElement(ET.SubElement(fill, f"{{{A}}}stretch"), f"{{{A}}}fillRect")
        rels = ET.fromstring(parts[f"ppt/slides/_rels/slide{num}.xml.rels"])
        for rel in list(rels):
            if rel.get("Type", "").endswith("/image"):
                rels.remove(rel)
        image_rels = ET.fromstring(native[f"ppt/slides/_rels/slide{index + 1}.xml.rels"])
        for rel in image_rels:
            if not rel.get("Type", "").endswith("/image"):
                continue
            old_id = rel.get("Id")
            rid = f"rId{20 + len(rels)}"
            target = f"../media/selected-concept-{num}.png"
            source = posixpath.normpath(posixpath.join("ppt/slides", rel.get("Target"))).lstrip("/")
            parts[f"ppt/media/selected-concept-{num}.png"] = native[source]
            ET.SubElement(rels, f"{{{REL}}}Relationship", Id=rid, Type=f"{R}/image", Target=target)
            for node in slide.findall(".//a:blip", NS):
                if node.get(f"{{{R}}}embed") == old_id:
                    node.set(f"{{{R}}}embed", rid)
        parts[f"ppt/slides/slide{num}.xml"] = encode(slide)
        parts[f"ppt/slides/_rels/slide{num}.xml.rels"] = encode(rels)
        notes_name = f"ppt/notesSlides/notesSlide{num}.xml"
        notes = ET.fromstring(parts[notes_name])
        body = next(
            s.find("p:txBody", NS)
            for s in notes.findall(".//p:sp", NS)
            if s.find("p:nvSpPr/p:nvPr/p:ph", NS) is not None
            and s.find("p:nvSpPr/p:nvPr/p:ph", NS).get("type") == "body"
        )
        text_nodes = body.findall(".//a:t", NS)
        text_nodes[0].text = (
            "Selected layout F4-C / F5-B reconstructed using retained numerical evidence. "
            "Display order: GPT-5.5, GPT-5.6 Luna, GPT-5.6 Terra, GPT-5.6 Sol, GPT-6 Astra. "
            "This display order is not a measured intelligence ranking. "
            "Source records remain in paper/figures/narrative-final/source-data.json. "
            + (
                "Figure 4b: bars are five-world means, starting at 0.001 on a log axis. "
                "Figure 4c: grouped horizontal bars of five-world means, log baseline 0.001. "
                "Lowest concentration conditions (n=3) and remaining conditions (n=9) retain "
                "all twelve queries in the original posthoc concentration grouping. "
                "Figure 4a: reference error bars are sample SD, not confidence intervals. "
                "Other nine queries are not all in-distribution."
                if index == 0
                else "Figure 5a: three arm-colored boxplots per model, five worlds per box. "
                "Boxes show Q1-Q3, lines show medians, whiskers show minimum and maximum. "
                "Quartiles use original positive concentration values before log-axis display. "
                "The dashed 1 mM line is descriptive. Figure 5b: Sol World 1/Opaque, "
                "12 source assays. Figure 5c: all five Sol/Opaque original 80% intervals. "
                "Figure 5d: Astra World 3/MisIndexed, all 12 batches, then condensed public K1 "
                "and original Q08. K1 is after experiments, not private contemporaneous thought. "
                "The small researcher/screen illustration is a separately cropped raster from "
                "the selected concept; scientific content is editable native shapes. "
                "No causal effect or necessity of dilute sampling is identified."
            )
        )
        for t in text_nodes[1:]:
            t.text = ""
        parts[notes_name] = encode(notes)
    if not any(n.get("Extension") == "png" for n in ct):
        ET.SubElement(ct, f"{{{CT}}}Default", Extension="png", ContentType="image/png")
    ET.register_namespace("", CT)
    parts["[Content_Types].xml"] = encode(ct)
    ET.register_namespace("", REL)
    for n in range(1, 8):
        assert parts[f"ppt/slides/slide{n}.xml"] == original[f"ppt/slides/slide{n}.xml"]
    for stem, n in (("figure04", 8), ("figure05", 9)):
        if stem not in args.figures:
            assert parts[f"ppt/slides/slide{n}.xml"] == original[f"ppt/slides/slide{n}.xml"]
    with zipfile.ZipFile(build / "assembled-candidate.pptx", "w", zipfile.ZIP_DEFLATED) as z:
        for name, value in parts.items():
            z.writestr(name, value)
    print(f"Replaced {', '.join(args.figures)}; other slide XML parts are unchanged.", flush=True)


if __name__ == "__main__":
    main()
