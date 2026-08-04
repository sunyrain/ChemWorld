# ChemWorld serious v1 data card

## Scope

The evidence package combines two interfaces rather than treating them as interchangeable competitors:

- G0 `compiled_recipe`: low-action-authority calibration and sequential matched prior-information conditions;
- G2 `closed_loop_primitive`: agent-directed additions, controls, characterization, termination, and final assay under a campaign resource ledger.

G1 is a development-only interface diagnostic and is not a scientific layer in the manuscript.

## Experiment accounting

| Layer | Role | Nonduplicated physical experiments |
|---|---|---:|
| G0 classic baselines | calibration | 27,300 |
| G0 three-arm participant study | matched prior conditions and cognition diagnostics | 2,280 |
| G2 v0.4 | autonomous development / hypothesis generation | 60 |
| Existing audited total |  | 29,640 |
| G2 v0.5 | planned fresh-trajectory replication opportunities | 120 |
| Planned opportunity denominator after terminal audit |  | 29,760 |
| G2 v0.5 | executed vessels | 114 |
| G2 v0.5 | completed final assays | 112 |
| Pre-parallel-agent total | executed physical experiments | 29,754 |
| Pre-parallel-agent total | completed experiments/final assays | 29,752 |
| G2 DeepSeek v0.6 | closed batch lifecycles | 60 |
| G2 DeepSeek v0.6 | final assays / explicit discards | 24 / 36 |
| Current full evidence total | executed or closed lifecycles | 29,814 |
| Current full evidence total | final assays | 29,776 |

An opaque G0 slice occurs in both the v1.0 and v1.2 summaries and is counted only once. Two G2 qualification attempts and the entire first interrupted G2 v0.5 launch are excluded.

The 29,760 figure is a design denominator, not the count of executed or
completed experiments. Eighteen G2 cells completed and two were right-censored.
For the DeepSeek v0.6 complete-system demonstration, all 60 started batches
closed: 24 by final assay and 36 by explicit discard. Closure and final-assay
counts are therefore reported separately.
Those cells left six opportunities unstarted and two started vessels without a
final assay, yielding the distinct final totals above. There are zero pending
cells and zero unresolved opportunities.

## Incremental F/V/L evidence layers

The frozen incremental layer reports three distinct measurement objects. They
are not pooled with each other or added to the historical G0/G2 physical-
experiment totals above.

| Track | Primary or audit unit | Frozen rows | Counting boundary |
|---|---|---:|---|
| F world forks | parent-child pair | 6 pairs, 12 within-pair expectations, 24 original/replay traces | exact replays are audit evidence, not new primary pairs |
| V known policies | original campaign profile | 30 profiles, 180 original lifecycles, 30 deterministic retests | retests are reliability-only and excluded from the primary estimand |
| L latent terminals | discarded lifecycle | 60 terminal lifecycles, 36 discard units, 10 campaign cells | evaluator shadows are not original agent experiments or choices |

These additions made zero provider calls. The L execution retained all 36
registered discard units but resolved only 6; 30 remain unresolved because of
the frozen evaluator/binding failure. Complete-case substitution is forbidden
and was not used, so latent-dependent primary point estimates are withheld and
the L result is not main-text eligible in its current state. This is a published
negative audit boundary, not a reason to replace or rerun the frozen result.

## Current raw-data state

Four G0 raw roots exist locally: 1,441 files and 17,725,724,603 bytes. Their historical source commits are all immutable ancestors of `origin/main`. A deterministic public index now binds every file by root-relative path, byte count, and SHA-256 (`g0-raw-file-index.json`, index SHA-256 `f49884b6e2d2b87a707dce9f93f96041dd7b3636b8e97ea4de93f0b3b429d961`). The raw bytes have not yet been deposited in a durable external archive. Until an archive identifier is added, this release candidate is not publication-ready.

G2 v0.5 is terminal. Its 18 completed and two right-censored cells passed
attempt-selection, within-pair identity, resource-replay, and exact-replay
checks. The terminal package is bound by a 677-file hash index. A paper-sufficient
public archive contains compact physical-transition trajectories for all 20
formal cells, plus the completed and partial durable trajectories from the
excluded first launch. All 22 compact trajectories pass exact physical replay;
provider response content and hidden evaluator identity are omitted. The
DeepSeek v0.6 archive separately contains all ten matched demonstration cells
and 889 replay-verified primitive operations under the same public boundary.

## Derived-data and figure state

`arxiv-v1-derived-data.json` is the frozen source for primary manuscript values.
It is bound at SHA-256
`1d639b09215ade3b84e9c2e5a9e30479fed1387890ab272d29b0996e7a06a2c4`.
The immutable 16-file manifest
`arxiv-v1-derived-data.manifest.json` binds that JSON and 15 CSV views at
manifest SHA-256
`deb80ae1e0fd40cb0bf40cee34d79e3450167624739dc990f4197be2ba6b542f`.
`arxiv-v1-p0-sensitivity.json` adds the self-hashed robustness layer without
changing that primary analysis. The release figures are generated only from
these frozen objects. G2 v0.5 contributes eight complete pairs and retains two
right-censored pairs without imputation. Best-score and algebraically independent
raw-terminal contrasts were sign-discordant in two of eight complete pairs
($r=+0.826$). All ten planned pairs remain visible as continuous process
profiles. Six of eight world-by-core-lifecycle classifications were mixed under
the frozen rule; this thresholded count and its missing-sign grid are retained as
supporting sensitivity analyses. These matched-world readouts are reported
descriptively rather than pooled into a population-level prior-effect test.

## Paper artifact state

The P0 manuscript is rendered as a 19-page, two-column arXiv PDF with six
publication figures. The upload bundle includes generated `main.tex`, the
BibTeX database, `main.bbl`, source Markdown and exact figure PDFs. Its build
manifest records byte counts and SHA-256 hashes for every submitted artifact.

## Release verification

Repository commit `03d1ec69b112b699c512e2d52d417207d90f9c3c` passed 2,106 tests
with three declared skips and no unresolved failures across eight deterministic filename
shards. A non-editable isolated installation of
`chemworld_bench-0.2.0-py3-none-any.whl` passed the serious-suite smoke contract; the
1,728,195-byte wheel has SHA-256
`e5447b6469433df520bd3e73fc9592c0ac765bd3e72dc2068267b540a281a72c`.

A detached checkout of the same commit passed the 50-test release suite with zero
differences in regenerated derived data, sensitivity data, display items, or figure
manifests. The 68-node evidence graph passes structural validation: 57 nodes are current,
11 historical bindings remain explicitly stale, and all 13 Work I F/V/L nodes are current.
Those historical bindings are not silently promoted. Publication readiness remains false
while the separately deferred raw archive and corresponding-author metadata gates remain
open.

## Sensitive and excluded content

Provider authentication, private evaluation seeds, hidden physical identities, unrestricted provider response bodies, and any secrets are excluded from the public package. Necessary provider accounting is published through redacted receipts and aggregate token/session fields.

## Intended use

The package supports reproduction and critique of the reported experimental-intelligence analyses. It is not evidence of real-world laboratory executability, robot reliability, general chemical discovery, safety for autonomous deployment, or superiority over Bayesian optimization.
