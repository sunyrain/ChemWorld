# Prior-correction manuscript figures

These figures are venue-neutral manuscript assets. They use Python/matplotlib exclusively and export
editable-text SVG/PDF plus 600 dpi PNG/TIFF previews.

## Figure contracts

### Figure 1 — From prior to reusable law

- **Core conclusion:** a useful endpoint is insufficient evidence of law discovery.
- **Archetype:** schematic-led composite.
- **Panel map:** matched prior intervention; persistent campaign; participant/evaluator evidence
  separation; joint understanding/action phenotype.
- **Reviewer risk:** the diagram is a conceptual claim map, not an observed causal result.

### Figure 2 — Frozen cohort and evidence architecture

- **Core conclusion:** matched prior interventions preserve 25 independent world-level denominators
  while operations, experiments, checkpoints and evaluator executions remain nested.
- **Archetype:** schematic-led quantitative design summary.
- **Source:** frozen formal design and outcome-blind execution-blocked preflight.
- **Reviewer risk:** planned denominators must never be shown as completed outcomes.

### Figure 3 — Development evidence

- **Core conclusion:** explicit priors reshape development behavior and endpoints, but final verbal
  warnings do not selectively identify misindexed information.
- **Archetype:** quantitative grid with provider-separated paired contrasts.
- **Statistics:** paired seed points and descriptive means only; no confidence intervals, formal
  tests or cross-provider capability comparison.
- **Source data:** all retained endpoint pairs, warning denominators and execution denominators are
  written under `source_data/`; no rows are sampled or excluded for plotting. The completed DeepSeek
  five-task matrix is additionally bound as the operational denominator source. Its two continuation
  task patterns remain outside the common three-task paired endpoint panels because their source
  figure contract is provider/harness-specific, not because those experiments were omitted.
- **Reviewer risk:** WellAU and DeepSeek differ in provider, sampling and recovery contracts and must
  remain separate facets rather than a model leaderboard.

## Reproduction

From the repository root:

```powershell
.\.venv\Scripts\python.exe paper\figures\prior-discovery\render_prior_discovery_figures.py
```

The renderer refuses formal participant inputs for Figure 3 and records source hashes, output hashes,
row counts and interpretation limits in `figure_manifest.json`.

Build the current development/design manuscript PDF with:

```powershell
.\.venv\Scripts\python.exe paper\tools\build_prior_discovery_draft.py
```

The PDF, generated TeX and build manifest are written to
`paper/exports/prior-discovery-draft/`. The build fails on stale figure bindings, undefined citations
or LaTeX errors and records page count, source hashes and typesetting diagnostics.
