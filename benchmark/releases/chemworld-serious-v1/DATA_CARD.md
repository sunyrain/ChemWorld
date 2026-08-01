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
| Projected total after terminal audit |  | 29,760 |

An opaque G0 slice occurs in both the v1.0 and v1.2 summaries and is counted only once. Two G2 qualification attempts and the entire first interrupted G2 v0.5 launch are excluded.

## Current raw-data state

Four G0 raw roots exist locally: 1,441 files and 17,725,724,603 bytes. Their historical source commits are all immutable ancestors of `origin/main`. A deterministic public index now binds every file by root-relative path, byte count, and SHA-256 (`g0-raw-file-index.json`, index SHA-256 `f49884b6e2d2b87a707dce9f93f96041dd7b3636b8e97ea4de93f0b3b429d961`). The raw bytes have not yet been deposited in a durable external archive. Until an archive identifier is added, this release candidate is not publication-ready.

G2 v0.5 is still running. Live trajectories are not promoted into the paper count; only terminal, identity-checked, ledger-audited, exact-replay-verified cells may enter the final derived table.

## Sensitive and excluded content

Provider authentication, private evaluation seeds, hidden physical identities, unrestricted provider response bodies, and any secrets are excluded from the public package. Necessary provider accounting is published through redacted receipts and aggregate token/session fields.

## Intended use

The package supports reproduction and critique of the reported experimental-intelligence analyses. It is not evidence of real-world laboratory executability, robot reliability, general chemical discovery, safety for autonomous deployment, or superiority over Bayesian optimization.
