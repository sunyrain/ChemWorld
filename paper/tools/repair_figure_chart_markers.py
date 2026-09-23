"""Make native chart points visible in PowerPoint when series lines are hidden."""

from __future__ import annotations

import copy
import sys
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

NS = {
    "c": "http://schemas.openxmlformats.org/drawingml/2006/chart",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}
for prefix, uri in NS.items():
    ET.register_namespace(prefix, uri)


def main(path: Path):
    target = path.with_suffix(".markers.pptx")
    with ZipFile(path) as source, ZipFile(target, "w") as output:
        for entry in source.infolist():
            content = source.read(entry.filename)
            if "/charts/" in entry.filename and entry.filename.endswith(".xml"):
                root = ET.fromstring(content)
                for series in root.findall(".//c:ser", NS):
                    marker = series.find("c:marker", NS)
                    color = series.find("c:spPr/a:solidFill", NS)
                    if marker is None or color is None:
                        continue
                    symbol = marker.find("c:symbol", NS)
                    if symbol is not None and symbol.get("val") == "none":
                        continue
                    properties = marker.find("c:spPr", NS)
                    if properties is None:
                        properties = ET.SubElement(marker, f"{{{NS['c']}}}spPr")
                    properties.clear()
                    properties.append(copy.deepcopy(color))
                    outline = ET.SubElement(properties, f"{{{NS['a']}}}ln", {"w": "0"})
                    ET.SubElement(outline, f"{{{NS['a']}}}noFill")
                content = ET.tostring(root, encoding="utf-8", xml_declaration=True)
            output.writestr(entry, content)
    target.replace(path)


if __name__ == "__main__":
    main(Path(sys.argv[1]))
