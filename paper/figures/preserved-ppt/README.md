# English figures with preserved illustrations

This correction restores the approved Imagegen artwork in Figures 1, 4 and 7. The preceding all-native reconstruction changed their visual design beyond the user's request and is superseded for manuscript use.

The [PowerPoint master](../../../output/pptx/chemworld-figures-preserved.pptx) retains the original illustration composition, icons, agent figures, arrows and blue/teal comparison. It crops only the overall title/header area and replaces labels with editable Arial text. Necessary panel labels, conditions, numbers and scientific caveats remain. The artwork is raster, not a fully editable vector illustration. Labels and their background covers can be edited separately in PowerPoint.

The other six figures retain the preceding PowerPoint layouts and numerical inputs. The deck still contains 31 native charts with embedded data snapshots. Primary labels use 20 px, secondary labels 18 px, panel labels 27–30 px, and highlighted values 30 px on the 1,440 px master. Dense framework annotations use smaller 14–16 px tiers. No new data are produced.

The [English PDF](../../../output/pdf/chemworld-ncs-en-preserved.pdf) uses exports made after reopening the finalized PPTX. The article's prose, captions, Methods and supplementary evidence are unchanged by this correction.

Original artwork is retained unchanged under `../ncs-full/`. Editable label positions are in [preserved_figure_labels.mjs](../../tools/preserved_figure_labels.mjs); [the overlay module](../../tools/preserved_figure_overlay.mjs) places them onto the original artwork. The [builder](../../tools/build_preserved_figure_deck.mjs) packages, checks, reopens and exports all nine figures. Earlier reconstruction files remain available for comparison.

```powershell
$env:UV_CACHE_DIR = Join-Path $env:TEMP 'chemworld-uv-cache'
$env:PYTHONIOENCODING = 'utf-8'
uv run --no-sync 'C:/Users/Admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe' paper/tools/build_preserved_figure_deck.mjs
uv run --no-sync python paper/tools/build_venue_manuscripts.py --venue ncs --output output/pdf/chemworld-ncs-en-preserved.pdf
```

The retained C-W05 case uses independent 12- and 24-batch Aligned sessions. Immediate considerations are illustrative, Q remains sealed during K2, and the proposed cooling substitution was not executed. The 35% to 100% evaluator reference concerns the reheating question only.

Package and layout checks use the presentation runtime. Native Microsoft PowerPoint is unavailable, so interactive editing in that application has not been tested.
