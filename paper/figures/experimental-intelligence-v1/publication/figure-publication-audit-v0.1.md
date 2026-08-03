# Work I publication figure audit

Status: **PASS**  
Audit SHA-256: `a585f6407c2bb92f3e8567154263b0b2a09cc7b79db999349a017631eea7316e`

The canonical inventory is resolved from the frozen P01 figure system. No figure was rewritten.

| Figure | Owner | Pending panels | Editable SVG text | SVG rasters | PNG | PDF fonts | Final size |
| --- | --- | --- | ---: | ---: | --- | --- | --- |
| F1 | W1-P02 | none | 70 | 0 | 2124x1560 @ 299.9994 dpi | 2 embedded | 7.08x5.2 in |
| F2 | W1-P03 | none | 60 | 0 | 2124x1560 @ 299.9994 dpi | 2 embedded | 7.08x5.2 in |
| F3 | W1-P04 | C, D | 81 | 0 | 2124x1560 @ 299.9994 dpi | 4 embedded | 7.08x5.2 in |
| F4 | W1-P05 | none | 62 | 0 | 2124x1560 @ 299.9994 dpi | 2 embedded | 7.08x5.2 in |
| F5 | W1-P06 | none | 63 | 0 | 2124x1560 @ 299.9994 dpi | 2 embedded | 7.08x5.2 in |
| F6 | W1-P07 | none | 94 | 0 | 2124x1560 @ 299.9994 dpi | 2 embedded | 7.08x5.2 in |

## Gate summary

- Canonical figures: 6/6 passed.
- Canonical assets: 18/18 passed.
- All SVGs retain editable text and contain no embedded raster images.
- All PNGs are 2124x1560 pixels with a 300 dpi physical-resolution declaration.
- All PDFs are single-page 7.08x5.2 inch assets with embedded TrueType fonts.
- Figure 3 panels C/D remain explicitly pending L05/L06 scientific results; this does not fail the asset-property audit.
- Legacy unmanifested assets excluded from the canonical set: 12.

This report validates publication-asset properties and immutable bindings only; it does not rerun scientific analyses.
