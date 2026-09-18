# Experiment 1 challenge v1.1.1 adapter deviation receipt

Status: **FROZEN BEFORE ATTEMPT 2 RESTART 1**

## Bound failed attempt

- executable source commit: `2227652d4563a7052b20f016a80fabb04602eaf3`;
- run: `runs/challenge/experiment-1-challenge-probes-v1.1-attempt2`;
- summary file SHA-256: `e80bd2a386547f9061d7c592ffacfd0609ac7b617ecfd8db31a7d0c07e25b786`;
- summary self-hash: `e417e1ce28aa95d7859875fbeda240591dc47a50420374d532eaa49a6d3eda27`;
- report file SHA-256: `0bd44a1b470a5a70f1063fe24bb9f6e0208d39784aa6f1c7f69ec9ccc11b80cf`;
- completed denominator: `40/50`;
- provisional locus result: `5/10` passed.

The attempt is retained unchanged.  PA-E and C-E each produced five
`entity report lacks a descriptor permutation` probe errors.  Their public
World reports bind prior hashes and checks but omit the permutation payload.

## Exact adapter change

The v1.1.1 adapter may read `loci.entity.descriptor_permutation` only from the
already hash-bound source contract listed in the v1.0 parent challenge
contract.  It must verify the source-contract file digest before reading.  It
may not read World outcomes, truth, measured effects, gates, or arm labels from
that fallback.  Exactly one bound permutation must be present.

No sequential policy, action order, metric, repeated-noise requirement,
information-gain threshold, reliable-stop threshold, participant budget,
World, prior, or Q1--Q8 gate changes in v1.1.1.  All 50 World rows must restart
from unit zero into a new immutable run directory.

