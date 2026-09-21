# EQ-S v0.2.1 provider-schema recovery

## Retained failure

The first `EQ-S-W01` canary preserved three complete 12-batch source trajectories and valid sealed `K1`, `Q`, and `K2` responses. All three `EQS` calls failed before inference because the Responses API rejected the `uniqueItems` keyword in the strict JSON output schema. The three original `RESULT.json` files remain `retained_nonconforming`; no source experiment is deleted or overwritten.

## Repair

Version v0.2.1 removes `uniqueItems` from the provider-facing schema for `selected_equation_ids` and `cited_source_batches`. The local validator continues to reject duplicate equation IDs and duplicate cited batch numbers, so the accepted-output contract is unchanged. Mechanism families, world parameters, public priors, prompts, query conditions, scoring rules, thresholds, model, and truth embargo are unchanged.

Recovery reuses each original thread and runs only the first invalid or missing sealed posttest. For this incident that is `EQS`; the 12 source batches and valid `K1`, `Q`, and `K2` payloads are reused exactly. Recovery outputs are written under `recoveries/<cell>/attempt-01`; original outputs are immutable.

