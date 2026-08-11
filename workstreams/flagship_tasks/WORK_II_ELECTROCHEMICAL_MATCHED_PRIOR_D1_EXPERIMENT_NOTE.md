# Work II electrochemical matched-prior D1

Date: 2026-08-11  
Status: frozen before provider execution; development evidence only

## Question and units

In the hardest qualifying electrochemical world, can one persistent Codex session use autonomous
operation-level experiments to challenge a matched but directionally wrong controlled-potential prior,
improve held-out predictions and produce an executable law consistent with its final action?

- World: `world_seed=0`, selected because Q2 gave it the smallest blind margin (`0.094693`); it is not
  a favorable-seed selection.
- Cells: opaque, aligned and misspecified matched prior arms; the participant never sees arm IDs.
- Provider: WellAU `gpt-5.6-sol`, medium reasoning, Codex Responses harness with ChemWorld MCP; one
  persistent Codex session per cell; three cells run concurrently and each cell is serial internally.
- Session: ten complete experiments chosen operation by operation in one shared campaign ledger. No
  protocol-owned diagnostic experiment is inserted.
- Checkpoints: pre-evidence, after experiments 2, 4 and 7, and final after experiment 10.
- No R5/formal denominator and no electrochemical D2 is scheduled unless a new, pre-registered
  trigger is created before execution.

## Frozen resources

- Eight unique recipes plus at most two participant-chosen exact repeats;
  `110` operation attempts and `20` electrolysis operations;
- `45,000 s` process time: `36,000 s` required stage maxima + `9,000 s` exact-repeat allowance +
  `0` quench/transfer allowance;
- ten vessel starts, ten final assays and thirty nonfinal instrument uses;
- stock limits `0.345 mol` reagent and `0.2875 L` solvent;
- provider development envelope per cell: `12,000,000` cumulative input tokens, `1,200,000` uncached
  input tokens, `96,000` output tokens, `6,600 s` provider session time and `7,200 s` method wall time;
- at most three recovered MCP failures, one consecutive MCP failure, one provider error and one
  resource rejection. All are retained in the denominator.

## Measurements and pass/failure

Record every operation, transaction status, resource ledger, snapshot, prediction, prior reliability,
challenged feature, executable-law summary, held-out prediction, recommendation, assay endpoint,
provider usage and exact replay. A cell is operationally qualified only if all ten experiments and five
snapshots close, the shared ledger reconciles, exact replay passes, and the provider/harness limits are
within their frozen envelopes.

Model-selected low score, wrong direction, unsafe/inefficient exploration, repeated recipes or failure
to form an executable law are participant outcomes, not platform failures. Contract mismatch, missing
outcome, replay mismatch, provider crash or harness failure is operational failure. Scientific and
operational failures are retained and never replaced by a favorable rerun.

Before any provider call, the clean-commit readiness receipt must pass config/resource construction,
single-session and MCP routing checks, credentials, historical current-code audit and the controlled-
potential direction audit against the exact 16 held-out evaluator queries.

## Expected outputs

One ignored zero-provider readiness receipt, one ignored three-cell participant matrix with 30-second
liveness, one tracked machine summary and one concise analysis. The result can authorize a later user-
reviewed expansion, but cannot establish a five-world or formal claim by itself.

## Readiness run-1 platform rejection

The first zero-provider readiness attempt made no provider call. All `3/3` historical WellAU
trajectories passed current-code audit, and every config, resource, credential, Codex/MCP and schedule
check passed. The controlled-potential truth stage failed before executing a query because the truth
compiler unconditionally forced the legacy `static_single_stage` electrochemical workflow while the
current Q2 and participant config use the public nine-field `autonomous_open_v1` contract. The
resulting `recipe_parameters fields do not match the contract` error is a readiness compiler defect,
not a participant or scientific result.

The correction makes evaluator truth honor the config-owned electrochemical workflow mode and adds a
regression that all 16 Q2 queries compile to the two-electrolysis, 11-action autonomous-open recipe.
No world, query, prior, threshold, resource or provider setting changes. The readiness block must
restart from historical trajectory 1 and truth query 1 on a new clean commit before any provider call.

## D1 phase result — retained operational failure

The frozen world-0 participant matrix reached terminal state in `682.1 s`. `aligned_nominal` and
`opaque` each completed `10/10` experiments with exact physical/resource replay; `misindexed_nominal`
was stopped before any physical operation after five consecutive belief-snapshot contract failures.
The final denominators were `20/30` complete experiments, `180` committed operations, `8/15`
checkpoints, `16/16` provider-free truth queries with exact replay, and `0/18` blind executions.
All three cells failed operational qualification because final checkpoints/recommendations were absent
and recovered MCP failures exceeded the frozen per-cell limit (`6`, `7`, and `5` respectively).

There were zero public unsafe outcomes, dynamic physical failures, resource rejections, provider errors
or platform execution failures. The completed trajectories therefore remain useful development evidence,
but the block cannot support a final executable law, final action, blind recommendation gain, H3, D2 or
R5. Intermediate held-out error improved from `0.290720` to `0.090182` in opaque and from `0.250258` to
`0.142923` in aligned by experiment 7, while both final checkpoints were unavailable. The
misspecified arm produced no physical trajectory, so no claim about correcting an incorrect prior is
authorized. Full interpretation is recorded in
`WORK_II_ELECTROCHEMICAL_MATCHED_PRIOR_D1_ANALYSIS_ZH.md` and the machine report.
