# Figure 5: panel a / b layout concepts

Eight independent concepts generated with the built-in Imagegen tool on 2026-09-25. Open [the comparison gallery](index.html) to choose one a and one b. These are layout and icon concepts, not final quantitative figures. The current manuscript, its Figure 5 and PDFs were not changed by this task.

## Options

| Panel a | Focus | Panel b | Focus |
| --- | --- | --- | --- |
| [A1](A1-evidence-coverage.png) | 覆盖地图 | [B1](B1-absolute-error-bars.png) | 绝对误差条形图 |
| [A2](A2-response-range.png) | 响应区间对比 | [B2](B2-signed-error-difference.png) | 相对 Opaque 的误差差值 |
| [A3](A3-research-evidence-chain.png) | 研究—证据—新条件 | [B3](B3-relative-error-ruler.png) | 相对误差倍数 |
| [A4](A4-graphical-evidence-matrix.png) | 条件 × 响应矩阵 | [B4](B4-graphical-comparison-table.png) | 图形数字表 |

Preferred starting combination: **A2 + B3**, showing the observed/withheld response contrast and the reversal relative to Opaque. **A3 + B3** emphasizes the autonomous research/evidence sequence.

## Numerical anchors and scope

- Source evidence: 15 campaigns, 180 assays; nominal concentrations 0.0185–2.0 M; pooled observed dissociation range 5.5–9.2%.
- Three dilute query concentrations: 13.3, 133 and 167 µM. There were no source assays in this dilute region.
- 44.8–71.6% is the range of five world reference means at **13.3 µM only**, not the range over all three dilute queries.
- Observed and reference ranges are not confidence intervals. Withheld reference outcomes are evaluator-only.
- The condition grouping is post hoc. “Other nine conditions” does not imply that all nine are interpolation.
- Mean macro MAE over five worlds:

| Arm | Other nine conditions | Three most dilute conditions |
| --- | ---: | ---: |
| Opaque | 0.01008 | 0.01833 |
| Aligned | 0.00465 | 0.15862 |
| MisIndexed | 0.00439 | 0.14397 |

B2 uses arm-minus-Opaque differences: Aligned −0.00543 / +0.14029; MisIndexed −0.00569 / +0.12564. B3 uses ratios of five-world means within the same condition group: Aligned 0.46× / 8.65×; MisIndexed 0.44× / 7.85×. These are descriptive contrasts, not significance claims.

Underlying sources: `output/figures/applicability-closeout/diagnostics.json` and `figure05-source-assays.csv`, alongside the existing Figure 5 evidence.

## Production notes

The numeric labels have been checked against the anchors above. Imagegen geometry remains illustrative: endpoint placement, logarithmic tick placement, bar lengths, icon scale and spacing must be reconstructed precisely from the retained data for any selected final design. A1's erroneous clinical wording was corrected to “Withheld dilute tests”. Early transparent variants were discarded; the eight delivered variants use white backgrounds.

[Exact generation and edit prompts](prompts.json) include the built-in tool mode and source/output mapping. Final PNGs are copied unchanged from generated outputs. No new scientific data, manuscript replacement, commit or push.
