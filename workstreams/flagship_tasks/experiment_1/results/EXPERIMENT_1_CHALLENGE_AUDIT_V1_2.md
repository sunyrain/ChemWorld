# Experiment 1 challenge audit

Status: **challenge complete; locus-wise fail-closed**

The audit covers every locus whose five Worlds are currently `qualified-development`. A development gate is not silently promoted into challenge evidence.

| Block | Symmetry | Plausibility | Non-triviality | Information choice | Budget window | Consequence | Leakage | Confirmation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EC-E | passed | passed | passed | passed | passed | passed | passed | eligible-for-process-isolated-confirmation |
| EC-P | passed | passed | passed | passed | passed | passed | passed | eligible-for-process-isolated-confirmation |
| EC-S | passed | passed | passed | passed | passed | passed | passed | eligible-for-process-isolated-confirmation |
| RX-P | passed | passed | passed | passed | passed | passed | passed | eligible-for-process-isolated-confirmation |
| RX-S | passed | passed | passed | failed | failed | passed | passed | confirmation-blocked-fail-closed |
| PA-E | passed | passed | passed | passed | passed | passed | passed | eligible-for-process-isolated-confirmation |
| PA-P | passed | passed | failed | failed | failed | passed | passed | confirmation-blocked-fail-closed |
| PA-S | passed | passed | passed | failed | failed | passed | passed | confirmation-blocked-fail-closed |
| C-E | passed | passed | passed | passed | passed | passed | passed | eligible-for-process-isolated-confirmation |
| C-P | passed | passed | passed | passed | passed | passed | passed | eligible-for-process-isolated-confirmation |

Candidate loci: `10`; confirmation eligible: `7`; blocked: `3`.

Challenge decisions are locus-wise. A failed locus remains blocked while passing loci may proceed to a separately frozen process-isolated confirmation contract. This audit does not itself generate or consume confirmation secret material.
