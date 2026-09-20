# Shared runtime performance validation

Development engineering evidence; no model/provider calls. Fifteen task configurations are software coverage, not fifteen independent scientific systems or qualified worlds.

Normal runner: the same 201 operations / 12 final assays, including exact replay, took 19.141 s versus the retained historical 1357.672 s (70.9x ratio). Historical timing is not a controlled repeated baseline.
First candidate: 199.079 s; retained separately. The final candidate also reuses resource snapshots within one read-only view request.

View comparison: 31/31 states; 0 semantic mismatches. Three timing repetitions per state; the table reports medians. State remained unchanged by all view reads.
Normal-run comparison: 201/201 steps, 0 mismatches across 24 selected fields; all 12 truth/assay results are identical. Exact replay max absolute error is 0. Both original and candidate resource ledgers were reconstructed and all 201 receipt hashes checked independently.

Random campaign IDs and their derived event-ID suffixes/hash values are normalized only for cross-run equality. All amounts, costs, counters, ordered event indices, resource decisions, observations and rewards remain compared. The raw comparisons are preserved.

| Task/state | Before (ms) | After (ms) | Ratio | Precondition calls |
| --- | ---: | ---: | ---: | ---: |
| electrochemical-conversion/reset | 17.665 | 0.806 | 21.9x | 3770 -> 56 |
| electrochemical-conversion/charged | 19.966 | 1.082 | 18.5x | 3770 -> 56 |
| equilibrium-characterization/reset | 20.810 | 1.842 | 11.3x | 4031 -> 56 |
| equilibrium-characterization/charged | 23.764 | 2.810 | 8.5x | 4031 -> 56 |
| flow-reaction-optimization/reset | 21.004 | 1.874 | 11.2x | 3857 -> 56 |
| flow-reaction-optimization/charged | 23.440 | 2.540 | 9.2x | 3857 -> 56 |
| low-budget-characterization/reset | 21.735 | 1.787 | 12.2x | 4031 -> 56 |
| low-budget-characterization/charged | 24.815 | 2.601 | 9.5x | 4031 -> 56 |
| partition-discovery/reset | 19.773 | 0.772 | 25.6x | 4031 -> 56 |
| partition-discovery/charged | 21.728 | 1.208 | 18.0x | 4031 -> 56 |
| public-private-generalization/reset | 21.924 | 1.797 | 12.2x | 4031 -> 56 |
| public-private-generalization/charged | 24.578 | 2.703 | 9.1x | 4031 -> 56 |
| purity-yield-tradeoff/reset | 27.994 | 2.823 | 9.9x | 4814 -> 56 |
| purity-yield-tradeoff/charged | 30.978 | 3.720 | 8.3x | 4814 -> 56 |
| reaction-mechanism-explanation/reset | 21.857 | 1.879 | 11.6x | 4031 -> 56 |
| reaction-mechanism-explanation/charged | 24.406 | 2.670 | 9.1x | 4031 -> 56 |
| reaction-optimization-standard/reset | 22.051 | 1.803 | 12.2x | 4031 -> 56 |
| reaction-optimization-standard/charged | 24.655 | 2.822 | 8.7x | 4031 -> 56 |
| reaction-safety-constrained/reset | 21.932 | 1.955 | 11.2x | 4031 -> 56 |
| reaction-safety-constrained/charged | 24.436 | 2.704 | 9.0x | 4031 -> 56 |
| reaction-to-assay/reset | 22.313 | 1.837 | 12.1x | 4031 -> 56 |
| reaction-to-assay/charged | 24.347 | 2.703 | 9.0x | 4031 -> 56 |
| reaction-to-crystallization/reset | 19.197 | 0.879 | 21.8x | 4292 -> 56 |
| reaction-to-crystallization/charged | 21.937 | 1.400 | 15.7x | 4292 -> 56 |
| reaction-to-distillation/reset | 23.776 | 1.848 | 12.9x | 4292 -> 56 |
| reaction-to-distillation/charged | 25.991 | 2.756 | 9.4x | 4292 -> 56 |
| reaction-to-purification/reset | 28.444 | 2.792 | 10.2x | 4814 -> 56 |
| reaction-to-purification/charged | 31.004 | 3.595 | 8.6x | 4814 -> 56 |
| tool-agent-planning/reset | 28.339 | 2.692 | 10.5x | 4814 -> 56 |
| tool-agent-planning/charged | 31.440 | 3.761 | 8.4x | 4814 -> 56 |
| reaction-to-crystallization/history-heavy | 7259.102 | 1.706 | 4254.8x | 4292 -> 56 |

The optimization removes repeated full action-mask construction, unrelated history copies, duplicate lab reports and repeated resource snapshots in a single read. Defensive copies, physics, solver accuracy, preflight resource checks, resource integrity, rejected actions and exact replay are retained. Read scopes expire on return or exception; there is no persistent identity cache.

Consumption: 147 setup steps, 402 normal-run steps and 402 physical replay steps; 951 environment steps in this benchmark block, with 24 final assays before replay. These are development checks and do not replace any formal qualification unit.

Formal C launch decision: hold for design repair. The retained v2 attempt has 646 operations / 40 final assays and zero model sources. W01 passed; W02 has only two quality-positive queries against the minimum of three; W03/W04 stopped on an illegal cooling target above current temperature; W05 is incomplete. Earlier v1 adds 62 operations / three assays. No failure or qualification threshold was removed.

Future C prompts: crystal_yield is seed-excluded crystallization-stage recovery relative to target product before separation. The pilot incorrectly described a reactant-charge denominator; its prompts and outcomes remain preserved and this interpretation limitation must accompany the pilot.

For later systems: use this shared runtime automatically; measure one representative history-rich complete reference path before scaling. Keep task-specific physical feasibility and public-contract checks; separate engineering failures from coverage and scientific outcomes. Do not repeat global release audits after each edit.

| Control | Class | Decision | Validation |
| --- | --- | --- | --- |
| Repeated masks/views/history copies | K3 redundancy | Batch and project | 31-state comparison, 201-step normal path |
| Repeated snapshot validation per field | K3 redundancy | One snapshot per read | All 201 receipts and hashes reconstruct |
| Physical legality, budgets, ledger integrity | K0/K1 | Keep at execution boundary | Rejected actions, budget exhaustion, corruption and replay tests |
| Formal provenance | K2 | Freeze the next stable block once | Old bindings and failed qualification retained |
