# Work II catalyst-deactivation paired real-provider campaigns

Date: 2026-08-12

Status: frozen before provider execution

## Question and tested units

Can two matched real WellAU `gpt-5.6-sol` medium Codex campaigns produce a participant-relevant
effect above the frozen W2-33 topology gates when one fixed reaction-safety world contains catalyst
deactivation and the other removes that unique pathway? World seed is 0 in both campaigns.

There are exactly two participant cells: `deactivating_baseline` and `stable_catalyst`. Each cell is
one independent persistent Codex process that controls eight fresh batches and completes eight
autonomous experiments. Provider, model, reasoning, public task, opaque material information,
resource ledger, checkpoint contract, agent seed and keyed observation-noise namespace are matched.
The physical law is host-owned and is the only intended difference; it is not named in the public
prompt. The stable cell removes `Cat_active -> Cat_dead` from world construction.

The previously completed one-session/two-experiment pilot resulted from a scope misunderstanding.
It is retained under source commit `5d6da7f5` as a development pilot but is not part of this block,
does not enter its denominator and will not be used as a replacement result.

## Measurements and limits

- two persistent Codex processes, one per fixed law, WellAU `gpt-5.6-sol`, medium reasoning and
  ChemWorld MCP only;
- exactly eight participant-controlled complete experiments per process, each closed by final assay
  or retained as an operational failure if the frozen campaign cannot complete;
- per campaign: at most 80 operation attempts, eight heat stages, eight quenches, eight nonfinal
  measurements and eight final assays;
- per-campaign process-time ceiling `116,160 s = 8 x 14,400 s heat + 8 x 120 s quench`;
- checkpoints at `0/2/4/6/8` completed experiments;
- record operations, complete experiments, MCP calls and failures, exact replay, provider attempts,
  input/cached/uncached/output tokens and elapsed time.

## Frozen completion and interpretation rules

Operational completion is assessed separately for both cells and requires one terminal provider
session, eight closed experiments, all five checkpoints, one committed final recommendation, exact
replay, no platform failure and complete provider usage accounting. Participant-selected unsafe or
physically poor conditions remain participant outcomes rather than platform failures.

Two frozen scientific views are reported. First, the total agent-system contrast compares the two
autonomous campaigns' best, mean and eight-round trajectories; this includes policy adaptation and
therefore is not a pure physics effect. Second, all 16 provider-selected recipes are replayed by the
evaluator under both laws with paired action/noise bindings (`16 x 2 = 32` provider-free executions).
For each recipe, report stable-minus-deactivating yield, conversion and selectivity. The reference
gates remain exactly `0.050/0.050/0.054`; report per-metric maxima, gate ratios, the count exceeding
each gate and whether at least two metrics exceed their gates. No gate may be lowered after outcome.

The block passes the requested empirical claim only if both provider campaigns are operationally
complete, all 32 counterfactual executions are exact-replay complete without platform failure, and
the frozen paired analysis observes above-gate separation. Failure is retained; no session or recipe
is replaced. This seed-0 development result cannot replace W2-33 or authorize a multi-seed claim.

## Outputs

Raw trajectories and provider receipts remain under ignored `runs/`. Tracked outputs are one
machine-readable paired summary with exact denominators and all failures, one concise Chinese
analysis and an updated Work II TODO entry.
