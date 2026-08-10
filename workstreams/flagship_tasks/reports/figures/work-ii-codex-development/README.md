# Work II Codex development figures

These figures are a reproducible visual audit of the retained development analysis. They are not
formal-study results and do not support claims of law discovery, causal prior effects, or transfer.

## Figure contract

- **Core conclusion:** In the retained five-seed WellAU/Codex development matrix, aligned-prior
  endpoint gains are concentrated in electrochemical conversion and crystallization, while
  misindexed priors are not consistently harmful and the explicit misindex warning is not reliably
  specific.
- **Archetype:** quantitative grid with a paired endpoint contrast as the hero panel.
- **Backend:** Python/matplotlib only.
- **Output:** 183 mm-wide editable-text SVG and PDF plus 600 dpi PNG and LZW-compressed TIFF.
- **Evidence hierarchy:** paired task×seed endpoint differences; paired reliability changes;
  arm-specific warning rates; exact cell and experiment denominators.
- **Statistics:** descriptive paired seed values and means only; no formal hypothesis tests or
  confidence intervals.
- **Reviewer risks:** five seeds per task, one retained failed cell, no evaluator-truth prediction
  scoring, no blind replay, and provider/harness differences that prevent a scientific
  WellAU-versus-DeepSeek comparison.

## Outputs

- `wellau_codex_prior_results.{svg,pdf,png,tiff}` — WellAU/Codex prior-arm results and the 44/45-cell
  completion map.
- `provider_separated_execution_audit.{svg,pdf,png,tiff}` — separate WellAU and DeepSeek completion,
  operational-event and token-accounting panels for the frozen pre-amendment baseline. DeepSeek
  remains harness evidence only; the later recovery-amended seed-0 pilots are deliberately excluded
  and recorded in `WORK_II_TODOLIST.md`.
- `source_data/*.csv` — exact plotted rows and denominators extracted from the frozen analysis.
- `figure_manifest.json` — source binding, row counts and interpretation limits.

## Reproduction

From the repository root:

```powershell
.\.venv\Scripts\python.exe workstreams\flagship_tasks\reports\figures\work-ii-codex-development\plot_work_ii_codex_development.py
```

The script reads the retained machine analysis by default and refuses inputs marked as formal or
provider-mixed. A different source can be passed explicitly with `--input`.

## Caption-ready interpretation

**WellAU/Codex development results.** Each endpoint point is a paired world-seed difference in the
best score observed across the four-experiment campaign. Aligned nominal information increased the
descriptive mean best score relative to opaque identifiers in electrochemical conversion
(+0.211; 5/5 paired seeds) and crystallization (+0.057; 5/5), but not distillation
(-0.036; 4/5 because one aligned cell failed). Misindexed information was not consistently harmful
relative to opaque identifiers. Reliability-update differences were heterogeneous, and final
misindex warnings included substantial aligned-arm false positives, most visibly in crystallization
(4/5 aligned versus 2/5 misindexed). The retained matrix contains 44/45 completed cells,
176/180 complete experiments and exact replay for 44/45 terminal cells. These are development-only
endpoint and self-report summaries; evaluator-truth prediction error and blind recommendation replay
were not available, so the figure does not establish law discovery or transfer.

**Provider-separated execution audit.** WellAU/Codex covers the complete scheduled 45-cell
development matrix with one retained failed cell. The frozen DeepSeek baseline covers a partial
33-cell pre-amendment attempt scope and is shown only as harness evidence; later recovery-amended
seed-0 pilots are outside this figure. All completion bars display their own denominators; DeepSeek
exact replay is 21/21 among retained terminal records, not 21/33 scheduled cells. Operational-event
rates are normalized by operation attempts but remain descriptive because provider, task coverage,
harness version and recovery policy differ. For legacy receipts without an explicit method-level
counter, the analysis counts all non-completed MCP calls, including both recovered and terminal
failures; the plotted `MCP tool failures` total therefore is not the same denominator as the explicit
recovery-gate count in the fallback completion report. Cached tokens are cached input tokens and do
not indicate repeated model output.
