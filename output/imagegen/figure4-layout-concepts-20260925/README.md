# Figure 4 layout concepts (2026-09-25)

Six **ImageGen concept images**, made to compare layouts before rebuilding a
source-driven publication figure. The user selected A2, which was rebuilt as
native PowerPoint marks from retained data and inserted as main Figure 4.
The concept images themselves are not publication figures. The source
references were the former Figure 4 and Supplementary Figure S3; all summary
labels below were checked against
`paper/figures/academic-ppt/retained-figure-data.json`.

| Concept | Layout | Readouts |
| --- | --- | --- |
| [A1](A1-six-readouts-2x3-paired-differences.png) | 2×3 paired-difference mini-panels | All six |
| [A2](A2-six-readouts-2x3-mean-and-swarm.png) | 2×3 mean pairs plus compact effect swarms | All six |
| [A3](A3-six-readouts-2x3-sign-matrix.png) | 2×3 world × information-arm sign matrices | All six |
| [B1](B1-four-readouts-2x2-paired-differences.png) | 2×2 larger paired-difference panels | Current four |
| [B2](B2-four-readouts-horizontal-tracks.png) | Four full-width result tracks | Current four |
| [B3](B3-four-readouts-asymmetric-columns.png) | Two positive systems at left; crystallization prediction and delivery at right | Current four |

The six readouts are EC discovery score MAE (0.1738→0.1122; 11/15 improved),
EC optimization score MAE (0.1781→0.1082; 12/15), partitioning
organic-fraction MAE (0.0829→0.0238; 13/15), crystallization recovery MAE
(0.1043→0.0794; 8/15), crystallization fines interval coverage
(35.6%→43.9%; 7/15), and crystallization retested recovery
(42.1%→39.9%; 7/15). The 12- and 24-batch histories are matched independent
sessions, not one continued trajectory.

**Scientific status.** ImageGen rendered all six images directly. Text and
layout are useful for selection; the generated point positions and point counts
in A1/A2/B1/B2/B3 are *not validated plotting data*. B2's legend also describes
the recovery direction imprecisely. A3's 90 plus/minus/zero/source-shortfall
cells were checked against the retained pairwise data, but that concept hides
effect magnitudes. The C-W02/Opaque source-assay shortfall is retained, not
excluded, in the source-based figures. If a concept is selected, rebuild it
deterministically from the retained campaign metrics and recheck every point.

The prompt set used the built-in ImageGen tool with white journal-page styling,
charcoal text, restrained teal/rust marks, no decoration or overall title, the
exact readout names/means/counts above and the current figure/S3 as style and
content references. Variant directives were:

- A1: six equal paired-difference panels with world-arm rows and mean diamond.
- A2: six panels with a 12/24 mean dumbbell above a fifteen-pair effect swarm.
- A3: six 5×3 world-by-arm signed-cell matrices, using the exact source sign
  triplets; targeted edits restored a pure white background and corrected the
  labels without changing cells.
- B1: four larger panels in a 2×2 paired-difference grid.
- B2: four wide horizontal tracks with mean and median markers.
- B3: an asymmetric three-column layout pairing crystallization prediction
  with operating delivery.

The selected A2 layout led to a manuscript revision and a source-driven figure
replacement. No new experiment was made.
