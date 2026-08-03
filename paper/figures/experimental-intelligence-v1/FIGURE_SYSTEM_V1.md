# Work I six-figure visual system

Status: **FROZEN**  
Task: `W1-P01`  
Machine contract: `figure-system-v0.1.json`  
System SHA-256: `c7abb490d247121e47fe20efca909df28527de64e7d1110699ccd104f6873643`

## Purpose

This document freezes one visual grammar for the six Work I main figures before
figure-specific rendering begins. The information architecture comes from the W1-S02
story freeze. Existing figures are migration inputs only; their numbering and panel jobs
do not override this contract.

## Global grammar

- Use a 7.08-inch two-column canvas for every main figure. Use the 3.39-inch width only
  for explicitly approved single-column derivatives.
- Use Arial when available, then Liberation Sans and DejaVu Sans. All stated font sizes
  are final-size points; nothing may fall below 6.5 pt after scaling.
- Use uppercase panel labels in left-to-right, top-to-bottom order. Do not duplicate the
  caption title as an in-canvas suptitle.
- Use white backgrounds, dark ink, light neutral grids, and direct labels when no more
  than four series are present.
- Preserve the information-arm colors everywhere: opaque is navy (`#355C7D`), anonymous
  nominal is coral (`#D95F59`), and misindexed is purple (`#8A6BBE`).
- Encode known policies by marker and line style, not by introducing a second competing
  color system. Encode completion and censoring by fill state and symbols.
- Never use color alone. Every comparison must retain a marker, line style, direct
  label, position, or hatch that survives grayscale and common color-vision variants.
- Quantitative panels show units, numerator/denominator where applicable, and all
  censored or unresolved units. Missing is never drawn as zero.

## Stroke and spacing system

At final width, use 0.35 pt grids, 0.5 pt axes, 0.75 pt data strokes, 1.1 pt emphasis,
and 1.4 pt focal strokes. The minimum permitted stroke is 0.35 pt. Default gutters are
0.18 inches horizontally and 0.22 inches vertically. Panel area follows information
density, not decoration.

The default grid is 2×2 with at most four main panels. A wide-top/two-bottom layout is
available when one conceptual diagram needs more width. Shared axes are preferred for
comparable quantities, and legends may not cover data.

## Figure jobs

| Figure / task | Title | Panel jobs | Result status |
| --- | --- | --- | --- |
| 1 / W1-P02 | ChemWorld apparatus and controlled world forks | A interaction loop; B controls and replay; C parent--child fork; D 6-pair/24-trace qualification | frozen |
| 2 / W1-P03 | Known policies validate the experimental-agency profile | A policy definitions; B 30 primary profiles; C discriminant readouts; D retest reliability | frozen |
| 3 / W1-P04 | Lifecycle completion does not specify terminal policy | A 84-assay/36-discard census; B complete-system profiles; C latent scores/regret; D thresholds/censoring | C--D pending L05/L06 |
| 4 / W1-P05 | Compiled controls separate outcome, prediction, calibration and claims | A outcome; B prediction/calibration; C epistemic readouts; D non-composite profile | frozen |
| 5 / W1-P06 | Primitive-control agents expose complete experimental lifecycles | A lifecycle; B resource receipt; C identity/replay; D failure and closure | frozen |
| 6 / W1-P07 | Fresh trajectories reveal process structure omitted by endpoints | A matched design; B 2/8 endpoint diagnostic; C continuous process contrasts; D censoring and 6/8 sensitivity | frozen |

Figure 3 owns the terminal-policy comparison. Figure 5 owns lifecycle anatomy and must
not repeat that comparison. Figure 6 keeps 2/8 as an endpoint diagnostic and 6/8 as a
threshold-sensitive supporting classification.

## Figure 3 pending panels

Panels C and D are structural slots, not optional panels selected after results. They
remain in the same positions whether latent outcomes are favorable, unfavorable, null,
or partially unresolved. `cell-02` has no discard opportunity and remains null in the
campaign-oracle panel. All 36 registered discards remain visible under the frozen
censoring and bounds rules.

## Export and audit

Every P02--P07 renderer must emit editable SVG, typesetting PDF, and a review PNG of at
least 300 dpi at final size. SVG text remains editable; PDF fonts are embedded or
subset. Exports use a tight bounding box, opaque white background, and deterministic
metadata.

The P08/P09 manifest must record relative path, byte count, SHA-256, figure ID, format,
source-data SHA-256, and this figure-system SHA-256 for every output. Captions must bind
claims to frozen evidence and figures must be first referenced in numeric order.

## Acceptance checklist for P02--P09

- [ ] Correct task, title, output stem, panel jobs, and panel order.
- [ ] Final physical dimensions and final-size typography meet the machine contract.
- [ ] Information-arm colors and entity symbols match the global grammar.
- [ ] Meaning survives grayscale and does not rely on red/green opposition.
- [ ] Units, denominators, missingness, censoring, and unresolved records are explicit.
- [ ] No replay, retest, qualification, shadow, or operation count inflates a primary
  denominator.
- [ ] SVG is editable, PDF fonts are embedded, and PNG resolution is sufficient.
- [ ] Output hashes and source bindings are recorded without mutating the existing
  global figure manifest before P08/P09.
