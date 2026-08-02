# ChemWorld serious v1 data card

## Scope

The evidence package combines two interfaces rather than treating them as interchangeable competitors:

- G0 `compiled_recipe`: low-action-authority calibration and prior-information interventions;
- G2 `closed_loop_primitive`: agent-directed additions, controls, characterization, termination, and final assay under a campaign resource ledger.

G1 is a development-only interface diagnostic and is not a scientific layer in the manuscript.

## Experiment accounting

| Layer | Role | Nonduplicated physical experiments |
|---|---|---:|
| G0 classic baselines | calibration | 27,300 |
| G0 three-arm participant study | prior intervention and cognition diagnostics | 2,280 |
| G2 v0.4 | autonomous development / hypothesis generation | 60 |
| Existing audited total |  | 29,640 |
| G2 v0.5 | planned fresh-trajectory replication opportunities | 120 |
| Planned opportunity denominator after terminal audit |  | 29,760 |
| G2 v0.5 | executed vessels | 114 |
| G2 v0.5 | completed final assays | 112 |
| Final project total | executed physical experiments | 29,754 |
| Final project total | completed experiments/final assays | 29,752 |

An opaque G0 slice occurs in both the v1.0 and v1.2 summaries and is counted only once. Two G2 qualification attempts and the entire first interrupted G2 v0.5 launch are excluded.

The 29,760 figure is a design denominator, not the count of executed or
completed experiments. Eighteen G2 cells completed and two were right-censored.
Those cells left six opportunities unstarted and two started vessels without a
final assay, yielding the distinct final totals above. There are zero pending
cells and zero unresolved opportunities.

## Current raw-data state

Four G0 raw roots exist locally: 1,441 files and 17,725,724,603 bytes. Their historical source commits are all immutable ancestors of `origin/main`. A deterministic public index now binds every file by root-relative path, byte count, and SHA-256 (`g0-raw-file-index.json`, index SHA-256 `f49884b6e2d2b87a707dce9f93f96041dd7b3636b8e97ea4de93f0b3b429d961`). The raw bytes have not yet been deposited in a durable external archive. Until an archive identifier is added, this release candidate is not publication-ready.

G2 v0.5 is terminal. Its 18 completed and two right-censored cells passed
attempt-selection, within-pair identity, resource-replay, and exact-replay
checks. The terminal package is bound by a 677-file hash index. A paper-sufficient
public archive contains compact physical-transition trajectories for all 20
formal cells, plus the completed and partial durable trajectories from the
excluded first launch. All 22 compact trajectories pass exact physical replay;
provider response content and hidden evaluator identity are omitted.

## Derived-data and figure state

`arxiv-v1-derived-data.json` is the frozen source for primary manuscript values.
`arxiv-v1-p0-sensitivity.json` adds the self-hashed robustness layer without
changing that primary analysis. The release figures are generated only from
these frozen objects. G2 v0.5 contributes eight complete pairs and retains two
right-censored pairs without imputation. Six of eight world-by-core-lifecycle
classifications were mixed; at least six remain mixed under every possible sign
of the two missing pair differences. The result is also stable at 80%, 90% and
95% retention definitions. These matched-world readouts are reported
descriptively rather than pooled into a population-level prior-effect test.

## Paper artifact state

The P0 manuscript is rendered as a 10-page, two-column arXiv PDF with six
publication figures. The upload bundle includes generated `main.tex`, the
BibTeX database, `main.bbl`, source Markdown and exact figure PDFs. Its build
manifest records byte counts and SHA-256 hashes for every submitted artifact.

## Sensitive and excluded content

Provider authentication, private evaluation seeds, hidden physical identities, unrestricted provider response bodies, and any secrets are excluded from the public package. Necessary provider accounting is published through redacted receipts and aggregate token/session fields.

## Intended use

The package supports reproduction and critique of the reported experimental-intelligence analyses. It is not evidence of real-world laboratory executability, robot reliability, general chemical discovery, safety for autonomous deployment, or superiority over Bayesian optimization.
