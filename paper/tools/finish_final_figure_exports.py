"""Crop native PowerPoint exports to their declared figure bounds; preserve aspect."""

import json
import os
import shutil
import sys
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "paper/figures/final-ppt"
TEMP = Path(os.environ["TEMP"]) / "chemworld-final-ppt"
if "--style" in sys.argv:
    path = (
        Path(sys.argv[sys.argv.index("--pptx") + 1]).resolve()
        if "--pptx" in sys.argv
        else ROOT / "output/pptx/chemworld-figures-final.pptx"
    )
    TEMP.mkdir(parents=True, exist_ok=True)
    staged = TEMP / "markers-final.pptx"
    ns = {
        "c": "http://schemas.openxmlformats.org/drawingml/2006/chart",
        "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    }
    count = 0
    with ZipFile(path) as source, ZipFile(staged, "w") as target:
        for item in source.infolist():
            content = source.read(item.filename)
            if (
                "/charts/" in item.filename
                and item.filename.endswith(".xml")
                and "/_rels/" not in item.filename
            ):
                tree = ET.fromstring(content)
                if "--regular-chart-text" in sys.argv:
                    for tag in ("a:rPr", "a:defRPr", "a:endParaRPr"):
                        for props in tree.findall(".//" + tag, ns):
                            props.set("b", "0")
                names = [v.text or "" for v in tree.findall(".//c:ser/c:tx//c:v", ns)]
                manual = None
                if any(n.startswith("EQ Withheld reference") for n in names):
                    manual = (0.07, 0.025, 0.90, 0.84)
                    for labels in tree.findall(".//c:dLbls", ns):
                        for props in labels.findall(".//a:defRPr", ns):
                            props.set("sz", "1350")
                            for font in props.findall("a:latin", ns):
                                font.set("typeface", "Arial")
                        fmt = labels.find("c:numFmt", ns)
                        if fmt is not None:
                            fmt.set("formatCode", "0.0")
                            fmt.set("sourceLinked", "0")
                    for fmt in tree.findall(".//c:valAx/c:numFmt", ns):
                        fmt.set("formatCode", "0")
                        fmt.set("sourceLinked", "0")
                elif any(n.startswith("Purity observations ") for n in names):
                    manual = (0.075, 0.035, 0.90, 0.85)
                if manual:
                    plot = tree.find(".//c:plotArea", ns)
                    layout = plot.find("c:layout", ns)
                    if layout is None:
                        layout = ET.Element("{" + ns["c"] + "}layout")
                        plot.insert(0, layout)
                    layout.clear()
                    position = ET.SubElement(layout, "{" + ns["c"] + "}manualLayout")
                    ET.SubElement(position, "{" + ns["c"] + "}layoutTarget", {"val": "inner"})
                    for key in ("xMode", "yMode", "wMode", "hMode"):
                        ET.SubElement(position, "{" + ns["c"] + "}" + key, {"val": "factor"})
                    for key, value in zip(("x", "y", "w", "h"), manual, strict=True):
                        ET.SubElement(position, "{" + ns["c"] + "}" + key, {"val": str(value)})
                # In an XY chart each axis declares where the other axis crosses it.
                # Explicit minima avoid PowerPoint's zero-axis placement and clipping.
                for axis in tree.findall(".//c:valAx", ns):
                    crossing = axis.find("c:crossesAt", ns)
                    if crossing is not None:
                        axis.remove(crossing)
                    crossing = axis.find("c:crosses", ns)
                    if crossing is None:
                        cross_id = axis.find("c:crossAx", ns)
                        crossing = ET.Element("{" + ns["c"] + "}crosses")
                        axis.insert(list(axis).index(cross_id) + 1, crossing)
                    crossing.set("val", "min")
                for marker in tree.findall(".//c:marker", ns):
                    symbol = marker.find("c:symbol", ns)
                    if symbol is None or symbol.get("val") != "x":
                        continue
                    props = marker.find("c:spPr", ns)
                    if props is None:
                        props = ET.SubElement(marker, "{" + ns["c"] + "}spPr")
                    props.clear()
                    ET.SubElement(props, "{" + ns["a"] + "}noFill")
                    line = ET.SubElement(props, "{" + ns["a"] + "}ln", {"w": "12700"})
                    fill = ET.SubElement(line, "{" + ns["a"] + "}solidFill")
                    ET.SubElement(fill, "{" + ns["a"] + "}srgbClr", {"val": "A35F42"})
                    count += 1
                content = ET.tostring(tree, encoding="utf-8", xml_declaration=True)
            target.writestr(item, content)
    shutil.copyfile(staged, path)
    print(f"figures stage=marker-outline x-series={count}", flush=True)
    raise SystemExit(0)
meta = json.loads((OUT / "style-and-export.json").read_text(encoding="utf-8"))
for index, item in enumerate(meta["figures"], 1):
    with Image.open(TEMP / (item["name"] + "-full.png")) as image:
        assert image.size == (4320, 5700), image.size
        cropped = image.crop((0, 0, 4320, item["height"] * 3))
        cropped.save(OUT / (item["name"] + ".png"))
        cropped.thumbnail((1440, 1900))
        cropped.save(TEMP / (item["name"] + "-preview.png"))
    print(f"figures stage=crop completed={index}/{len(meta['figures'])}", flush=True)
meta["renderSource"] = "Final PowerPoint file reopened and exported by Microsoft PowerPoint"
(OUT / "style-and-export.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
