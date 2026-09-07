# Experimental knowledge and decision figures

Python/matplotlib produces vector SVG/PDF and high-resolution PNG assets; historical panels also provide TIFF. The current
[display plan](../../prior_discovery_display_items.md) is the single description of panel roles,
denominators and interpretation limits. Captions live in the two manuscript sources.

The ten manuscript assets use direct denominators and explicit missing outputs. The compact
ICLR manuscript uses assets 1, 3, 10, 5 and 8 in the main text, with assets 4, 6, 7 and 9 in
the appendix, and renumbers them consecutively. The long manuscript uses all ten.
The disclosure comparison retains original failures; separate GPT and DeepSeek world views
are available as standalone PDF/SVG/PNG assets. Selected retries are reported in a methods table.
Old development-only figure exports are retired; their numerical reports remain in the evidence index.

The design overview separates four conversion questions. The correction figure now shows both
models across all three intervention loci, with exact counts in the two-model source table.
The prediction/law figure uses matched dumbbells and an explicit replay-outcome count table.

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
