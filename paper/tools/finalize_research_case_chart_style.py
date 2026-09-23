"""Set explicit native marker colors without changing chart data."""
import copy
import sys
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

C = "http://schemas.openxmlformats.org/drawingml/2006/chart"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
NS = {"c": C, "a": A}
ET.register_namespace("c", C)
ET.register_namespace("a", A)


def main(path: Path) -> None:
    output = path.with_suffix(".styled.pptx")
    count = 0
    with ZipFile(path) as source, ZipFile(output, "w") as target:
        for item in source.infolist():
            content = source.read(item.filename)
            if "/charts/" in item.filename and item.filename.endswith(".xml") and "/_rels/" not in item.filename:
                root = ET.fromstring(content)
                series = root.findall(".//c:ser", NS)
                if len(series) != 4:
                    raise ValueError("Expected four series per chart")
                count += 1
                good = "0066DB" if count <= 2 else "009BB5"
                for index, symbol, color in [(2, "circle", good), (3, "x", "BA6A56")]:
                    marker = series[index].find("c:marker", NS)
                    marker.find("c:symbol", NS).set("val", symbol)
                    properties = marker.find("c:spPr", NS)
                    if properties is None:
                        properties = ET.SubElement(marker, f"{{{C}}}spPr")
                    properties.clear()
                    fill = ET.Element(f"{{{A}}}solidFill")
                    ET.SubElement(fill, f"{{{A}}}srgbClr", {"val": color})
                    if symbol == "x":
                        ET.SubElement(properties, f"{{{A}}}noFill")
                    else:
                        properties.append(copy.deepcopy(fill))
                    outline = ET.SubElement(properties, f"{{{A}}}ln", {"w": "12700" if symbol == "x" else "0"})
                    outline.append(copy.deepcopy(fill))
                for ser in series:
                    smooth = ser.find("c:smooth", NS)
                    if smooth is not None:
                        smooth.set("val", "0")
                content = ET.tostring(root, encoding="utf-8", xml_declaration=True)
            target.writestr(item, content)
    if count != 4:
        raise ValueError(f"Expected four charts, found {count}")
    output.replace(path)
    print("figure chart styles: four charts, explicit markers, no smoothing")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
