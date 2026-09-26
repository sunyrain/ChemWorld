"""Crop native exports of the editable main or supplementary figures without reflow."""

from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[2]
LABELS = {
    "main": ("01", "02", "03", "04", "05", "06", "S4"),
    "supplementary": ("S1-1", "S1-2", "S1-3", "S1-4", "S2-ab", "S2-cf", "S3", "S5", "S6"),
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kind", choices=LABELS, default="main")
    parser.add_argument(
        "--exports",
        type=Path,
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "paper/figures/current-editable",
    )
    parser.add_argument(
        "--dependency-path",
        type=Path,
        help="Optional bundled site-packages directory containing pypdf.",
    )
    args = parser.parse_args()
    labels = LABELS[args.kind]
    if args.exports is None:
        folder = (
            "chemworld-user-ppt-integration"
            if args.kind == "main"
            else "chemworld-supplementary-ppt-integration"
        )
        args.exports = Path(tempfile.gettempdir()) / folder
    if args.dependency_path:
        sys.path.append(str(args.dependency_path))
    from pypdf import PdfReader, PdfWriter
    from pypdf.generic import RectangleObject

    reader = PdfReader(args.exports / "all-slides.pdf")
    if len(reader.pages) != len(labels):
        raise ValueError(f"Expected {len(labels)} pages for {args.kind}")
    args.output.mkdir(parents=True, exist_ok=True)
    for index, (label, page) in enumerate(zip(labels, reader.pages, strict=True), 1):
        with Image.open(args.exports / f"slide-{index}.png") as source:
            image = source.convert("RGB")
        difference = ImageChops.difference(image, Image.new("RGB", image.size, "white"))
        ink = difference.convert("L").point(lambda value: 255 if value > 15 else 0)
        bounds = ink.getbbox()
        if bounds is None:
            raise ValueError(f"Slide {index} is blank")
        left, top, right, bottom = bounds
        # Seven PDF points of external margin; no rescaling or internal cropping.
        scale_x = float(page.mediabox.width) / image.width
        scale_y = float(page.mediabox.height) / image.height
        margin_x, margin_y = round(7 / scale_x), round(7 / scale_y)
        left, top = max(0, left - margin_x), max(0, top - margin_y)
        right = min(image.width, right + margin_x)
        bottom = min(image.height, bottom + margin_y)
        x0, y0 = float(page.mediabox.left), float(page.mediabox.bottom)
        crop = RectangleObject(
            (
                x0 + left * scale_x,
                y0 + (image.height - bottom) * scale_y,
                x0 + right * scale_x,
                y0 + (image.height - top) * scale_y,
            )
        )
        page.mediabox = crop
        page.cropbox = crop
        page.trimbox = crop
        writer = PdfWriter()
        writer.add_page(page)
        writer.add_metadata(
            {
                "/Title": f"ChemWorld Figure {label.lstrip('0')}",
                "/Subject": "Native export of the user-edited figure collection",
            }
        )
        path = args.output / f"figure{label}.pdf"
        with path.open("wb") as stream:
            writer.write(stream)
        # A private preview is useful for reviewing the crop; only PDF is published.
        image.crop((left, top, right, bottom)).save(args.exports / f"figure{label}-cropped.png")
        print(
            f"Figure export: completed={index}/{len(labels)} {path.name} "
            f"size={float(crop.width):.1f}x{float(crop.height):.1f} pt",
            flush=True,
        )


if __name__ == "__main__":
    main()
