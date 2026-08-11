# Work II reaction-safety matched-prior arm-compatibility correction

Date: 2026-08-11
Status: frozen before rerun

## Defect and correction

The first Q2 execution classified `605/605` provider-free surface queries and passed all five
scientific prior gates, but its generated D1 config used the external semantic arm IDs `aligned` and
`misspecified`. The current campaign checkpoint harness still requires the internal compatibility IDs
`aligned_nominal` and `misindexed_nominal`; static preflight therefore rejected the config before any
provider process or participant trajectory began.

This is an integration-output defect, not a scientific failure and not a participant result. The
original raw Q2 surface and generated outputs remain frozen under the ignored first-run root.

The correction changes only the outer configuration keys:

- external `aligned` semantics map to internal `aligned_nominal`;
- external `misspecified` semantics map to internal `misindexed_nominal`;
- the participant-facing initial-world-model objects remain byte-for-byte free of arm identity;
- reference selection, 11 × 11 surfaces, fitting split, thresholds, reflection order, held-out query
  selection and all pass/failure rules are unchanged.

Following the qualification restart rule, the complete five-world, 605-query block reruns from world
0 on a clean commit. It must again report all physical failures, zero platform failures, 5/5 worlds
passing, and a D1 config that passes checkpoint, initial-model and campaign-resource static preflight.
Provider calls remain zero.
