# Work II pattern-owned checkpoint compatibility correction

Date: 2026-08-11
Status: frozen before final Q2 rerun

## Defect and correction

The arm-compatible Q2 rerun reproduced the first scientific result exactly: `605/605` classified
surface queries, `64` physical failures, zero platform failures and `5/5` worlds passing. Its D1
static preflight then found a second legacy interface assumption before any provider process began:
the checkpoint layer and qualification receipt required exactly four snapshots and four completed
batches, while the frozen A-P pattern requires five checkpoints at `0/2/4/7/10` experiments.

The correction makes snapshot and terminal denominators pattern-owned:

- snapshot count must equal the frozen stage/count schedule, with unique stages and strictly
  increasing counts from zero to the campaign experiment total;
- the MCP snapshot schema and final-recommendation range derive from that same schedule;
- terminal closed-batch/final-assay checks use the configured experiment total;
- the participant prompt no longer says that exactly four experiments exist.

No prior text, reference context, world, query, surface value, fit, threshold, reflection choice or
failure classification changes. The two previous raw Q2 executions and their generated outputs stay
frozen under ignored development roots. Following the qualification restart rule, the complete
five-world, 605-query block reruns once more from world 0 on the checkpoint-compatible clean commit.
The final D1 config must pass checkpoint, initial-model, MCP-schema and campaign-resource static
preflight. Provider calls remain zero.
