# Work II prior discovery — one-seed breadth pilot

Status: **PASSED as a development qualification block; not a formal scientific result.**

The frozen breadth matrix completed **15/15 cells**: five tasks × three prior arms at world seed
0. Each cell completed five exploration experiments, four ordered snapshots, two autonomous
decisions, four held-out queries with two replicates each, and three blind recommendation
replicates. This gives 75 exploration experiments, 120 held-out replicates and 45 blind
replicates.

The participant was WellAU `gpt-5.6-sol` at medium reasoning through direct Responses requests.
Tools and MCP were disabled. Completed trajectories used **90 calls / 90 attempts** and
**502,405 total tokens**: 406,069 input, 33,152 provider-reported cache-hit, and 96,336 output
tokens. Including the recovered infrastructure attempt, the execution index records **91 calls /
92 attempts**. Pricing was not verifiable, so monetary cost remains unknown rather than zero.

One provider infrastructure timeout occurred at the first decision of cell 13
(`reaction-safety-constrained`, `opaque`, seed 0), after **0 physical experiments** and with
**0 reported tokens**. The immutable 12-cell prefix was validated by trajectory/protocol hashes;
`--resume` continued only from cell 13. No completed cell was reexecuted, no trajectory was
overwritten, and the final block has zero terminal failures or right-censored cells.

All 15 trajectories passed hash, cell-identity, four-stage snapshot-order, autonomous,
exploration, held-out and blind-denominator checks. Raw provider payloads were not retained.
This block qualifies the execution and evidence interface only; it does not estimate prior
benefit/harm, law discovery, wrong-prior rejection, transfer, or model capability.
