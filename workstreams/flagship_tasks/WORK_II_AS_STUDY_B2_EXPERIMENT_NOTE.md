# Work II A-S Study B2 matched phase-process evidence

Status: frozen before provider execution; independent follow-up to Study B.

## Question

When a fresh participant receives phase-process evidence that was pre-qualified to separate the
linear partition response from the registered 1.75-power response, does a misindexed initial law
update more selectively than an aligned law? This block is designed to distinguish insufficient
structural evidence from belief-updating failure; it is not a new autonomous-search benchmark.

## Units and frozen coverage

- Participant: `deepseek-v4-flash`, high reasoning, native Codex `exec` session.
- Task/locus: A-S `partition-discovery`, using the five registered public C2 seeds
  `527268922,946166808,650846081,110564668,241120479`.
- Arms: `opaque`, `aligned_nominal`, and `misindexed_nominal` in every world; 15 fresh two-turn sessions.
- Source coordinates: the 64 coordinate-only `phase_process` Q2-heldout coordinates in each preserved
  provider-free qualification world report. Sort by `coordinate_index`; use positions
  `[0,8,16,24,32,40,48,56]` as evidence and `[4,12,20,28,36,44,52,60]` as disjoint scoring.
  The resulting rosters are `c385,c401,c417,c433,c449,c465,c481,c497` and
  `c393,c409,c425,c441,c457,c473,c489,c505` respectively in all five worlds.
- The selected coordinates are re-executed provider-free under the registered 1.75-power intervention
  at each public C2 seed before any participant call. Evidence contains only their feature values and
  observed public metrics. It does not expose candidate labels, hidden law IDs, evaluator internals,
  or the paired linear prediction. Scoring uses the eight disjoint phase-process queries and all three
  registered metrics.
- Turn 1 receives the initial world model and commits a pre-evidence prediction. Turn 2, in the same
  thread, receives the fixed eight-row evidence packet and commits a post-evidence prediction.
- There are no participant physical experiments, simulator calls, or participant access to raw truth.

## Measurements

- Pre/post normalized absolute error over 8 scoring queries × 3 metric terms.
- Per-cell update gain: `pre_error - post_error`.
- Primary locus contrast: misindexed update gain minus aligned update gain, reported by world and as
  the five-world mean with all failures retained.
- Secondary structural outcomes: explicit recognition of the 1.75 power law, rejection of the linear
  law, evidence-limit statements, query/metric completeness, same-thread continuity, provider usage,
  and infrastructure/schema failures.

## Qualification, failure and stop rules

- Provider-free preflight must verify all five paired-law reports, the 8/8 disjoint roster, identical
  feature/query ordering across arms, exact metric denominators, and at least two metric channels
  above the frozen paired-law effect gate for every evidence and scoring coordinate in every world.
- A three-arm canary checks only two-turn continuity, output schema, packet identity and denominators;
  canary numerical outcomes are excluded from the 15-cell analysis.
- The scientific block is complete only when all 15 scheduled cells are terminal. Infrastructure
  retries retain all attempt receipts. Scientific/schema failures are retained and never replaced by
  a more favorable run.
- No directional result changes the design or acts as a platform gate. A positive primary contrast
  supports an evidence-seeking explanation; a small or negative contrast despite diagnostic evidence
  supports a belief-updating bottleneck. Mixed or weak results are reported as unresolved.
- Any execution-semantics fix after the first formal cell requires restarting all 15 cells from unit 1.

## Expected outputs

- One self-hashed input manifest with the exact 15-cell schedule and 16-query roster per world.
- One sanitized cell result and provider receipt per session, plus append-only progress under ignored
  `runs/`.
- One machine-readable summary and one Chinese interpretation report with exact denominators, all
  failures, per-world contrasts, and structural-summary audits.
- Paper 2 result/story updates that close or explicitly retain the A-S acquisition-versus-updating
  ambiguity without promoting the block to a cross-provider or transfer claim.
