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
