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

### Figure 3 — Prior uptake and selective correction

- **Core conclusion:** the initial-model intervention reaches the trajectory and prediction improves,
  but the registered DeepSeek C2 locus tests do not establish selective wrong-model repair.
- **Archetype:** evidence-bound four-panel quantitative result.
- **Panel map:** initial prediction error; first-recipe divergence; prediction improvement; registered
  A-E/A-P/A-S correction estimates and lower bounds.
- **Source data:** all 135 scheduled public C2 cells, including failures and censoring, plus the
  retrospective first-recipe manipulation check.
- **Reviewer risk:** first-recipe divergence has no repeated same-arm baseline and cannot isolate
  provider stochasticity; general learning must not be relabelled selective correction.

### Figure 4 — Matched evidence and identifiable-law action control

- **Core conclusion:** matched counterevidence drives numerical convergence but not reliable
  structural-law recovery or useful action.
- **Archetype:** cross-configuration four-panel quantitative result.
- **Panel map:** corrected DeepSeek-high B2 pre/post error; low-error versus exact-law recovery;
  DeepSeek-high/GPT-medium/DeepSeek-low matched contrasts; dual-model B3 completion, joint recovery,
  Top-1 and eligible action gain.
- **Source data:** all valid A-P/B2 matched formal denominators and all 30 scheduled B3 cells per
  model. Historical evaluator-defective structural evidence is excluded from the current claim.
- **Reviewer risk:** each matched block contains five independent worlds; DeepSeek-low is not
  reasoning-off, and B3 has differential schema failure. No configuration ranking is supported.

### Figure 5 — Dual-model C2 capability chain

- **Core conclusion:** better executable-law compression does not produce selective correction or
  blind action gain.
- **Archetype:** matched two-model four-panel quantitative result.
- **Panel map:** registered locus gates; prediction improvement; final-prediction versus law MAE;
  blind better/equivalent/worse/not-evaluable outcomes over all scheduled cells.
- **Source data:** matched 135-cell DeepSeek and Codex C2 scheduled surfaces, with all failures and
  censoring retained.
- **Reviewer risk:** model differences are matched descriptive rather than randomized provider
  effects; scheduled coverage is not all-cell completion or a leaderboard.

### Figure 6 — Action selection and evaluator validity

- **Core conclusion:** four-condition evidence and learned-law transfer do not establish a stable
  portable-law benefit; law quality and evaluator ranking remain misaligned with action.
- **Archetype:** evidence-bound four-panel quantitative diagnostic.
- **Panel map:** W2-61 four-condition failure-aware regret; W2-50 continuous law error versus regret;
  registered W2-61 contrasts and intervals; W2-53 Spearman--regret unit scatter with Top-1 markers.
- **Source data:** 180 scheduled W2-61 condition slots per model, all 45 scheduled W2-50 cells and all
  16 frozen W2-53 unit versions.
- **Reviewer risk:** W2-61 is a development successor with unequal donor eligibility and substantial
  yoked failure, so autonomous-minus-yoked is not a pure experiment-selection effect. W2-53 is a
  zero-execution retrospective diagnostic and does not revise W2-51/W2-52 stop decisions.

## Reproduction

From the repository root:

```powershell
uv run --no-sync python paper\figures\prior-discovery\render_prior_discovery_figures.py
```

The renderer records source hashes, output hashes, exact row counts and interpretation limits in
`figure_manifest.json`.

Build the current development/design manuscript PDF with:

```powershell
uv run --no-sync python paper\tools\build_prior_discovery_draft.py
```

The PDF, generated TeX and build manifest are written to
`paper/exports/prior-discovery-draft/`. The build fails on stale figure bindings, undefined citations
or LaTeX errors and records page count, source hashes and typesetting diagnostics.
