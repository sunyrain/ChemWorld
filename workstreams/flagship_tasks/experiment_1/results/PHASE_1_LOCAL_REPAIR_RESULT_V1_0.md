# Experiment 1 Phase 1 local-repair result v1.0

Status: **DEVELOPMENT EVIDENCE FROZEN; PARTICIPANT NOT AUTHORIZED**

## PA-P

The v1.0.2 discriminator keeps the five Worlds, simulator physics, prior centers, false factors,
response grid, gap threshold, SNR threshold, runtime contract, and participant budget unchanged.
It corrects Q6 to test a realizable three-unique-experiment design rather than requiring both
qualification endpoints.

- result: `PA-W01..W05` all `qualified-development`;
- denominator: `75/75` primary executions with exact replay;
- raw summary SHA-256:
  `3b451114ee4d9dc9776bfe066f221e7fbaa630f210dea9457896a640db51c290`;
- current composite registry SHA-256:
  `f8eabe596c5d53cc00aedab7038b122d56057658a93cf6a44653a5dbc75fe759`.

This does not erase the four v1.0.1 Q6 failures. They remain bound through each replacement row's
`supersedes` field.

## C-P

The v1.0.2 repair replaces an ill-matched absolute crossing claim with the task-relevant cooling
response `deltaY40 = crystal_yield(270 K) - crystal_yield(310 K)`. It keeps the five Worlds, PBM
physics, runtime contract, three-experiment budget, and noise gates unchanged.

- result: `C-W01..W05` all `qualified-development`;
- denominator: `45/45` primary executions with exact replay;
- raw summary SHA-256:
  `ecfde7e9a4e7c077692add14166fe308ccec6659a5ecd308374fb63f59851fe0`;
- current composite registry SHA-256:
  `2f7377733d6e53f2203aa4d9f5b1c6e0ba4632ae2ca0f57cc81816776b4a5371`.

C remains `10/15` at this point because all five C-S units retain their v1.0.1 failures pending the
separate structural redesign.

## RX-E

The preregistered authoring calibration executed `2 anchors x 4 catalysts x 3 replicates x 5
calibration Worlds = 120` provider-free runs, all with exact replay. All six global transpositions
were evaluated on the same receipts. The only pair qualifying all five calibration Worlds was
`C1 <-> C2`, with minimum anchor mean separation `0.0806429485` and minimum SNR `7.7894`.

That pair is identical to v1.0.1. It therefore does not constitute a repair. Moreover, the retained
v1.0.1 evidence shows that RX-W02's world residual makes one nominal row closer to the swapped row
than to its own row, so the aligned-prior fidelity requirement remains false. Re-running the same
formal design would only reproduce the same scientific defect.

- authoring summary SHA-256:
  `fbfafd6f0f39ac12ab1d7182bbe39d89a2a0f778e5f9d5c1bdffd6ce82630623`;
- decision: no formal v1.0.2 requalification run;
- current status: `failed-development`;
- thresholds were not reduced and formal Worlds were not replaced.

## Boundary

All evidence in this phase is provider-free development qualification. No Participant Agent or
external model/provider was used. Confirmation qualification has not yet been run.
