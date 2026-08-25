# Experimental-intelligence manuscript figures

These figures are venue-neutral manuscript assets. They use Python/matplotlib exclusively and export
editable-text SVG/PDF plus 600 dpi PNG/TIFF previews.

## Figure contracts

### Figure 1 — From an initial world model to a reusable law

- **Core conclusion:** a useful endpoint is insufficient evidence of law discovery.
- **Archetype:** schematic-led composite.
- **Panel map:** programmable initial-model layers with the current entity/ontology instantiation;
  persistent campaign; participant/evaluator evidence separation; joint understanding/action
  phenotype.
- **Reviewer risk:** the diagram is a conceptual claim map, not an observed causal result.

### Figure 2 — Entity-level confirmatory core and study architecture

- **Core conclusion:** the entity/ontology core preserves 25 independent world-level denominators,
  while non-entity extensions, matched-evidence probes, private replication and artifact-only transfer
  retain separate protocols and denominators.
- **Archetype:** schematic-led quantitative design summary.
- **Source:** frozen formal design and outcome-blind execution-blocked preflight.
- **Reviewer risk:** planned denominators must never be shown as completed outcomes, and within-family
  private replication must not be relabelled compositional transfer.

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

### Figure 4 — Held-out development confirmation

- **Core conclusion:** DeepSeek development trajectories often improve held-out predictions, but
  wrong-prior correction does not exceed aligned-prior improvement; compressed law summaries and
  committed recommendations add little or negative value beyond the final typed predictions and
  observed incumbent.
- **Archetype:** quantitative grid with the H3 paired-improvement plane as the hero panel.
- **Panel map:** aligned-versus-misindexed prediction improvement; task-wise H3 contrasts; executable
  law-summary compression error; paired blind recommendation outcomes.
- **Statistics:** all 25 task×seed clusters, all 71 executable law summaries and all 69 qualified
  blind-evaluated cells; descriptive values only, with no confidence intervals or formal tests.
- **Source data:** 25 cluster rows, 71 law-summary rows and 69 blind-recommendation rows are exported
  without sampling. Frozen missing-outcome rules remain in the H3 denominator.
- **Reviewer risk:** this is post-hoc development evaluation, not the preregistered public matrix or
  private transfer confirmation.

### Figure 6 — Action selection and evaluator validity

- **Core conclusion:** unseen-plan selection, thresholded law adequacy and complete-ranking oracle
  qualification are distinct readouts; full-rank correlation can pass while Top-1 is wrong or fail
  while the selected action has zero regret.
- **Archetype:** evidence-bound four-panel quantitative diagnostic.
- **Panel map:** W2-50 selected ranks; W2-50 law--action categories; W2-51/W2-52 qualification
  funnels; W2-53 Spearman--regret unit scatter with Top-1 markers.
- **Source data:** all 45 scheduled W2-50 cells, the three terminal W2-51/W2-52 qualification
  dispositions and all 16 frozen W2-53 unit versions are exported without sampling.
- **Reviewer risk:** W2-51/W2-52 contain no participant sessions, exposed construction is not fresh
  qualification, and W2-53 is a zero-execution retrospective diagnostic rather than a new causal
  experiment.

## Reproduction

From the repository root:

```powershell
uv run --no-sync python paper\figures\prior-discovery\render_prior_discovery_figures.py
```

The renderer refuses formal participant inputs for Figure 3 and records source hashes, output hashes,
row counts and interpretation limits in `figure_manifest.json`.

Build the current development/design manuscript PDF with:

```powershell
uv run --no-sync python paper\tools\build_prior_discovery_draft.py
```

The PDF, generated TeX and build manifest are written to
`paper/exports/prior-discovery-draft/`. The build fails on stale figure bindings, undefined citations
or LaTeX errors and records page count, source hashes and typesetting diagnostics.
