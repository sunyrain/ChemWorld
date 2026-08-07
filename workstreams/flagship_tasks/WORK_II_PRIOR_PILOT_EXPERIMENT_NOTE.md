# Work II prior pilot experiment note

Date: 2026-08-07  
Claim: `Codex /root — W2-04/W2-06/W2-10-PILOT — DOING`

## Question

Can five prior-identifiable reference tasks expose matched `opaque`, `aligned_nominal` and
`misindexed_nominal` public contracts, and can WellAU `gpt-5.6-sol` at medium reasoning use those
contracts through one direct Responses call per scientific decision without schema, transport,
prompt-budget or execution failure?

This block qualifies the prior interface and provider path only. It is not a test of law discovery,
wrong-prior rejection, transfer or comparative task performance.

## Tested units and staged coverage

- Tasks: electrochemical conversion, reaction-to-crystallization, reaction-to-distillation,
  partition discovery and safety-constrained reaction.
- Prior arms: opaque codes, aligned nominal properties and one fixed two-row misindexing per task.
- Stage A: deterministic/mock contract preflight, all 5 tasks × 3 arms × world seed 0, one complete
  experiment per cell.
- Stage B: smallest real-provider probe, electrochemical conversion × 3 arms × world seed 0, one
  complete experiment and one provider decision per cell.
- Stage C: only after A and B pass, one-seed breadth pilot across 5 tasks × 3 arms. Its horizon and
  law-summary snapshots must be frozen before execution.
- Any later multi-seed block stops at five independent world seeds `[0,1,2,3,4]`; exceeding five
  requires explicit user authorization. Provider repeats remain technical repeats, not seeds.

## Measurements

- exact task/arm/seed denominators and every failed cell;
- material-condition ID and dossier hash, with matched property-bundle multisets;
- model identity, Responses wire, provider calls/attempts, input/cache/output tokens and wall time;
- schema-valid decisions, compiled complete-experiment execution and terminal completion;
- prompt estimates/caps, invalid responses, retries and redacted failure class;
- exact report and receipt hashes. Raw provider payloads are not retained in Git.

## Pass and failure rules

- Stage A passes only at 15/15 completed cells with no schema, material-contract or execution failure.
- Stage B passes only at 3/3 completed cells using exact model `gpt-5.6-sol`, medium reasoning and
  Responses wire. Each decision allows at most two provider attempts: one initial call plus one retry.
- Per provider attempt timeout is 180 s; maximum output is 3,000 tokens. A timed-out or invalid first
  attempt may be repeated once, but scientific execution is not repeated after a completed result.
- The complete recipe includes required quench/transfer/closeout operations. One extra operation of
  executor guard margin is reserved for workflow closure and is not exposed as agent budget.
- Any task whose anonymous material mapping lacks a category-specific causal response fails
  prior-identifiability and must be replaced rather than silently reducing task count.
- Any Stage A/B failure stops expansion. No task, target field, permutation or pass rule may be changed
  in response to provider performance.

## Expected outputs

- ignored per-cell protocols, receipts and reports under the chosen local `runs/` output;
- one machine-readable execution index with exact denominators, hashes and all failures;
- one concise tracked Markdown/JSON summary after the real probe;
- a progress JSON outside the repository, updated at cell start, provider-call in-flight, experiment
  completion, failure and run completion.
