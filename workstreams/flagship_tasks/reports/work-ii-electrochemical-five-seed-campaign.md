# Work II electrochemical five-seed campaign summary

Date: 2026-08-08. Status: development evidence; not a formal or held-out result.

## Execution result

The frozen matrix completed 15/15 cells: five paired world seeds and three prior arms per seed.
Each cell used one persistent WellAU `gpt-5.6-sol` medium Codex session, four complete experiments,
one shared campaign ledger and four typed checkpoints. The three arms within one seed ran as
OS-isolated concurrent cells; seeds remained sequential.

- Source commit: `1099c4a4171023d412a4713860babafa7e781c64`
- Machine report: ignored development artifact
  `runs/development/work-ii-electrochemical-five-seed-20260808T184013/matrix_report.json`
- Matrix wall time: 2,661.4 s (44.4 min)
- Sum of cell wall times: 7,354.8 s; observed concurrency speed-up: 2.76x
- Seed-triplet wall times: 494.8, 512.4, 533.0, 574.5 and 546.6 s
- Cell wall time: min 378.0 s, median 490.2 s, max 573.4 s

## Exact denominators and failures

| Unit | Completed / total | Failures or rejections |
|---|---:|---:|
| World-level cells | 15 / 15 | 0 terminal cell failures |
| Complete experiments | 60 / 60 | 0 incomplete lifecycles |
| Participant operation attempts | 367 / 367 committed | 0 resource rejections |
| Typed belief checkpoints | 60 / 60 valid | 3 recovered invalid checkpoint submissions |
| Structured decision audits | 367 / 367 provided | 0 missing |
| Exact replay | 15 / 15 cells verified | 0 replay mismatch |
| MCP tool calls | 446 total | 4 recovered tool-call failures |
| Provider sessions | 15 / 15 completed | 1 recovered provider error event |

The four recovered MCP failures were three `commit_belief_snapshot` `ValueError` responses and one
`step` `PermissionError`. They remained inside their original session, produced no scientific
operation, and were followed by a valid call. No raw provider payload or private reasoning was
retained. Future formal protocol must state the allowed validator/tool retry cap explicitly rather
than inferring it from successful final checkpoints.

## Provider and context accounting

- Cumulative input: 19,459,659 tokens
- Cached input: 17,652,224 tokens (90.7%)
- Uncached input: 1,807,435 tokens
- Output: 157,356 tokens
- Provider-reported reasoning output: 29,385 tokens; reasoning bodies were not retained
- MCP schema improvement reduced the earlier `seed0/opaque` checkpoint pattern from 14 attempts
  with 10 failures to four successful submissions with no retries in the replacement seed-0 cell.

## Descriptive participant outcomes

These are five-world paired development descriptions only. They are not inferential claims.

| Prior arm | Mean final score | Mean best observed score | Mean operations | Final experiment retained the cell best |
|---|---:|---:|---:|---:|
| Opaque | 0.283 | 0.411 | 24.0 | 2 / 5 |
| Aligned nominal | 0.612 | 0.622 | 24.8 | 4 / 5 |
| Misindexed nominal | 0.325 | 0.458 | 24.6 | 1 / 5 |

Paired final-score differences across seeds 0--4 were:

- aligned minus opaque: `+0.163, +0.210, +0.078, +0.602, +0.591`; mean `+0.329`;
- aligned minus misindexed: `+0.172, +0.166, +0.078, +0.737, +0.280`; mean `+0.286`;
- misindexed minus opaque: `-0.009, +0.044, 0.000, -0.135, +0.312`; mean `+0.042`.

Aligned information produced the highest final score in all five paired worlds. Misindexed
information did not show a consistent advantage or harm relative to opaque information: its paired
direction changed across worlds. Endpoint performance therefore does not by itself establish
whether the agent discovered, rejected or silently worked around an incorrect prior.

## Prior-revision behavior

Final aligned-prior reliability probabilities were `0.83, 0.74, 0.78, 0.38, 0.78`. Four cells
retained the aligned dossier without naming a misindexed field; one cell incorrectly suspected both
fields and reduced reliability to 0.38 despite high endpoint performance.

Final misindexed-prior reliability probabilities were `0.86, 0.38, 0.84, 0.58, 0.30`. Only two of
five cells ended by explicitly suspecting both manipulated fields. Three cells did not explicitly
reject the wrong dossier; two of those retained high final reliability (0.86 and 0.84). This is the
most important development observation: the agent sometimes rejected a wrong prior, but correction
was not reliable, and a favorable endpoint could coexist with epistemically incorrect confidence.

## Scope boundary

The participant block did not execute evaluator-owned held-out queries or blind recommendation
replicates. The typed law summaries and predictions are therefore recorded but not yet transfer
validated. No law-recovery, generalization or causal prior-rejection claim should be made from this
block alone. The next evidence task is the sealed evaluator block, followed by retry-policy freeze
before any formal matrix.
