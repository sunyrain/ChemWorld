# Integrated manuscript: evidence and reproduction

This is the author-facing source index for the 21 September 2026 review manuscript.
It records retained-data analysis and editorial integration, not a new experiment,
qualification block, or release freeze. The original first-paper manuscript, exports,
bibliography, and bound qualification artifacts are unchanged by this revision.

## Manuscript and outputs

- Canonical English source: [chemworld_integrated_manuscript.md](chemworld_integrated_manuscript.md).
- Chinese abstract and author argument: [prior_discovery_story_zh.md](prior_discovery_story_zh.md).
- Generated all-metric appendix: [chemworld_integrated_results_appendix.md](chemworld_integrated_results_appendix.md).
- Generated campaign data: [campaign_metrics.csv](figures/integrated-results/campaign_metrics.csv), 240 campaigns and 1,065 campaign/metric rows.
- Paired goal contrasts and totals: [analysis.json](figures/integrated-results/analysis.json).
- Five vector figures, with PNG previews: [figure directory](figures/integrated-results).
- Review PDF: [chemworld-integrated-review.pdf](../output/pdf/chemworld-integrated-review.pdf).

The PDF includes the English source, protocol appendix, generated full metric appendix,
and references. It is a review artifact, not a replacement for the frozen platform release.
The original six-author order, affiliation, equal-contribution statement, and correspondence
are retained. No submission venue or page limit is imposed.

## Rebuild

From the repository root, with the locked environment:

```powershell
uv run --no-sync python paper/tools/render_integrated_results.py
uv run --no-sync python paper/tools/build_integrated_review.py
```

The first command reads existing JSON and pinned Git objects only. It does not import
an experiment runner, call a provider, execute the simulator, or change a frozen result.
It regenerates the figures, campaign metrics, goal contrasts, and Appendix B. The second
uses Pandoc and XeLaTeX to write the review PDF to `output/pdf/`; temporary TeX, logs,
and rendered QA pages reside in the operating-system temporary directory. Rebuilding
does not require a globally clean worktree or a new platform certificate.

## Authoritative inputs

The closure snapshot includes the newly merged EQ-E exports. To regenerate it from the fixed input commit:

```powershell
uv run --no-sync python -m scripts.report_work_ii_evidence_inventory --remote-commit 6a5ff6fc --p-summary workstreams/flagship_tasks/reports/work-ii-p-five-world-20260921-v4/summary.json --output workstreams/flagship_tasks/reports/work-ii-evidence-closeout-20260921
```

The closure snapshot is
[the current evidence inventory](../workstreams/flagship_tasks/reports/work-ii-evidence-closeout-20260921/summary.json),
generated at 2026-09-21 10:32:30 +08:00. It resolves remote EQ evidence at the explicit
commit `6a5ff6fc5f98fc24df1f0b141c3b441c34ebe73f`. The rendering script uses this binding,
not the current tip of a remote branch. RX and EQ reference targets are already released
in those completed exports; the reanalysis performs no new truth generation.

| Evidence | Input and use |
|---|---|
| Frozen platform qualification | `configs/current.json` → `publication`; composition, deterministic use-case, and agent-instrument reports under `workstreams/arxiv_v1/reports/` |
| EC / PA | `workstreams/flagship_tasks/reports/work-ii-ec-pa-five-world-en-20260919/completed-block-analysis.json`; all 90 E campaigns, metric means, world pairs, first-attempt sensitivity |
| RX | `workstreams/flagship_tasks/reports/work-ii-rx-ps-five-world-dual-goal-20260919-final/SUMMARY.json`; all 60 cells, six-response scores and retests |
| EQ entity prior | Pinned remote `workstreams/flagship_tasks/reports/work-ii-eq-e-canonical-20260921-v0.2-final/`; all fifteen sources, fixed common topology, entity/concentration/scale prediction queries |
| EQ parameter prior | Pinned remote `workstreams/flagship_tasks/reports/work-ii-eq-bounded-equilibrium-20260920/v2-public/`; index and all fifteen `sources/*/RESULT.json` |
| EQ structural prior | Pinned remote `workstreams/flagship_tasks/reports/work-ii-eq-s-canonical-20260920-v0.3-final/`; full canonical cells and aggregate embedded in closure snapshot |
| C | `workstreams/flagship_tasks/reports/work-ii-c-formal-20260920-v3-auto/summary.json`; normalized rows and all retests embedded in closure snapshot |
| P | `workstreams/flagship_tasks/reports/work-ii-p-five-world-20260921-v4/summary.json`, `analysis.json`, and `ANALYSIS.md`; corrected complete matrix, all failures retained |

Relevant experiment notes remain the authority for each executed contract, including
the English EC/PA five-world note, C reference-v3 note and recovery amendments, P parallel
study note, and pinned remote RX/EQ protocols. Historical notes do not authorize new work.

## Evidence boundaries reconciled in this revision

The current pool is 240 scheduled campaigns, 238 protocol-conforming chains, 3,597/3,600
final-assayed source batches, 720/720 canonical posttests, fifteen additional EQ supplements,
and 165 recommendation retests. P's two discards count as consumed vessel starts. C's
missing assay follows solvent exhaustion and a discarded twelfth vessel; it is not reconstructed or imputed. References, qualification, replay,
superseded runs, and additional infrastructure attempts are different units.

Two late method checks are important:

1. The RX and EQ runner/export contracts retain Chinese K1/Q/K2 instructions requesting
   English responses. The manuscript now discloses this instead of asserting every
   prompt was English. No historical prompt is edited.
2. C prediction scoring uses noiseless pre-final-assay values captured by
   `TruthCapture.step` in `scripts/run_work_ii_c_pilot.py`, then consumed by
   `scripts/run_work_ii_c_formal.py`. C's observed recommendation retests are a different
   target. PA also uses noiseless fractions; EC/P use single seeded observations;
   RX/EQ point predictions use five-repeat means and coverage uses individual repeats.

The earlier EC/PA eight-call numerical limit remains part of its saved protocol. Later
blocks use disclosed 128-attempt allowances. These differences limit cross-system
interpretation without invalidating matched within-block comparisons.

## New analysis in this revision

The principal added comparison is RX **score-only** prediction under the goal contrast,
to align the endpoint with EC's score-prediction result. It uses sealed existing values:
optimization gives a better retest in 9/30 pairs, lower score MAE in 8/30, and a better
retest with worse score prediction in 5/30. The original six-metric macro comparison
remains 9/30, 6/30, and 5/30. Equal counts need not identify the same set of campaigns;
the machine file retains each paired contrast. This is a descriptive reanalysis, not
a prospectively registered additional primary endpoint.

All plotted means weight campaign metrics equally. There are no pooled cross-system
MAEs, query-level significance tests, fabricated confidence intervals, or new judge
scores. The prior figure shows all arms and worlds for selected readouts; Appendix B
and the CSV preserve all response metrics. The two nonconforming sources are marked.

## Citation and prose handling

The integrated manuscript has its own nine-entry bibliography, drawn from established
entries already used by the project. It retains the BoxingGym preprint label. Used
citation keys and bibliography entries are checked at build time. Crossref title/DOI
checks succeeded for Bran, Szymanski, Summit, and Smart Predict-then-Optimize during
this revision; transient lookup errors for three other DOI entries did not justify
changing their existing metadata. No unverified novelty superlative or negative claim
about another environment's capabilities is introduced.

The prospective nine-system abstract is replaced by observed six-system results. The
nine-system scope remains a platform/task-design capability statement. Free mechanism
expression remains central; local fixed-form surrogate fitting is not recast as free
mechanistic discovery. Same-context predictions are not presented as report-only
transfer or evidence that compression caused information loss.

## Remaining substantive analysis

The current paper is complete as a platform-plus-descriptive-study draft. A stronger
claim about systematic scientific information loss requires cohort-wide alignment of
experiments, explicit K1 claims, and Q predictions, with successes and justified
non-identifiability included. That annotation is not completed or implied by this
editorial pass. The selected EC trajectory is an illustration, not a prevalence estimate.
An actual causal report-compression claim would require a separate matched-information
experiment. Further systems or model replications would also be separate authorized
blocks; the present paper does not require reopening completed scientific cells.

## Completed verification

The review build contains 20 pages, five vector figures, the protocol appendix, the
complete all-metric appendix, and nine cited references. The 233-word abstract uses
observed results. Both new scripts pass Ruff. Retained-data checks confirm 240 unique
campaigns, 238 conforming sources, 1,065 metric rows, and the eight headline budget
means within displayed rounding. Local document links and cited keys resolve. All
pages were rendered for visual review; pages changed by the final figure enlargement
were rechecked. The final LaTeX log has no overflow, missing-character, or unresolved
reference diagnostics. No experiment execution was part of this verification.


## Remote integration and failure disposition

The remote runtime and sanitized exports were merged without rerunning historical scientific cells. EQ-E adds fifteen complete campaigns and forty-five canonical stages, making 240 campaigns across eight blocks in six families. The prior overview figure retains sixteen selected readout panels; the full data and Appendix B additionally contain all three EQ-E metrics. Existing goals, budget comparisons and recommendation outcomes are unchanged.

The failure review distinguishes two source nonconformances (C solvent exhaustion and P discards), two C public-baseline parser omissions (`campaign_resource_rejected` in C-W02/12/Opaque and C-W05/24/MisIndexed), and one historical EC supplement with missing Q/K2. The C baseline omissions are outside the reported agent prediction/retest comparisons; they require deterministic reanalysis only if that baseline is used. No main-matrix model rerun is required. See the [record-level decisions](../workstreams/flagship_tasks/reports/work-ii-evidence-closeout-20260921/ANALYSIS.md#failure-disposition-after-remote-integration).
