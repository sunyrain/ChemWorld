# Experimental knowledge and decision figures

Python/matplotlib produces editable-text SVG/PDF and 600 dpi PNG/TIFF assets. The current
[display plan](../../prior_discovery_display_items.md) is the single description of panel roles,
denominators and interpretation limits. Captions live in the two manuscript sources.

Figures 1–6 were redesigned around readable text, paired measurements, direct denominators and
explicit missing outputs. Historical four-panel descriptions are superseded. The compact ICLR
manuscript currently uses Figures 1 and 3–6 and renumbers them consecutively; Figure 2 remains
available for the long manuscript.

## Reproduction

From the repository root:

```powershell
uv run --no-sync python paper/figures/prior-discovery/render_prior_discovery_figures.py
uv run --no-sync python paper/tools/build_prior_discovery_draft.py
uv run --no-sync python paper/tools/build_prior_discovery_iclr.py
```

Existing evidence is resolved through `configs/current.json`. The renderer reads sanitized
reports without depending on ignored raw run directories. Figure source tables retain the
underlying rows; source/output hashes and row counts belong in `figure_manifest.json`.

Builds write to `paper/exports/prior-discovery-draft/` and
`paper/exports/prior-discovery-iclr2027/`. Review exported PDFs at page scale after changing
figures or prose. Labels, uncertainty and availability must remain legible at manuscript width.

The independent-world M1 block has its own fixed experiment note. Its figure will use the
completed formal report; planned or development outcomes do not substitute for that report.
