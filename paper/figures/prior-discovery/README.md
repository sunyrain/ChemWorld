# Experimental knowledge and decision figures

Python/matplotlib produces editable-text SVG/PDF and 600 dpi PNG/TIFF assets. The current
[display plan](../../prior_discovery_display_items.md) is the single description of panel roles,
denominators and interpretation limits. Captions live in the two manuscript sources.

The eight current assets use readable text, paired measurements, direct denominators and explicit
missing outputs. The compact ICLR manuscript uses assets 1, 3, 5, 6 and 8 in the main text, with
assets 4 and 7 in the appendix, and renumbers them consecutively. The long manuscript uses all eight.
Old development-only figure exports are retired; their numerical reports remain in the evidence index.

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

M1 and M3 each read their completed formal reports through the current registry. M1 displays the
unsupported primary material-benefit result; M3 displays independent artifact utility and the
nearest-evidence zero-regret boundary. Reused worlds and nested sessions remain distinguishable.
Publication QA status belongs in the [submission checklist](../../ICLR_2027_SUBMISSION_CHECKLIST.md);
do not maintain another copied QA report or figure hash inventory.
