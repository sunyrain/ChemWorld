# Work II strict A-S five-world paired-law Q1/Q2

Status: frozen implementation; first development launch stopped on a validator defect at
`1,121/10,240` primary executions. The partial world-0 report and world-1 trajectories are retained
at the original output root and are not a scientific result. No runtime physical or platform failure
occurred. The validator incorrectly required a compiled-mechanism hash change for the partition
domain-parameter intervention; after repairing this platform contract, the entire 10,240-primary
block must restart from execution 0. Coverage, scientific thresholds, and selection rules are
unchanged.

## Question

Can two registered structural/mechanistic law contrasts be distinguished from public measurements under matched action plans and keyed observation noise, in every one of five worlds, before any participant session is authorized?

The candidates are fixed as:

1. `partition-discovery`: the executable baseline linear partition response versus `partition_power_response_stress_v1` with exponent 1.75. The two intervention families are nominal solvent–extractant identity and phase/process conditions.
2. `reaction-to-crystallization`: the executable baseline target pathway versus `reversible_target_pathway_stress_v1` with the registered reverse rate. The two intervention families are reaction temperature and reaction duration.

Equilibrium characterization is not a candidate. Its load and volume axes collapse to concentration and do not provide two independent intervention families.

## Coverage and exact denominator

The frozen roster contains 512 coordinates for every `candidate × world` unit, in worlds `0,1,2,3,4`. Each coordinate is executed once under each of the two laws with the same action plan, world seed, and keyed noise coordinate, and each trajectory receives tolerance-zero exact replay.

- Per candidate-world: 512 coordinates, 1,024 primary law executions, and 1,024 exact replays.
- Full block: 2 candidates × 5 worlds × 1,024 = 10,240 primary executions and 10,240 exact replays.
- Within each candidate-world, each intervention family supplies 256 coordinates: 192 Q1 coverage coordinates and a disjoint 64-coordinate Q2 held-out pool.
- Q2 selects eight coordinates per family, 16 per candidate-world, by an evenly spaced coordinate-only rule frozen before outcomes. All five worlds must pass; no favorable-world selection is permitted.

## Measurements and Q2 comparison

Partition uses public final-assay `product_in_organic`, `product_in_aqueous`, and `phase_ratio`. Crystallization uses the public pre-crystallization HPLC `yield`, `conversion`, and `selectivity`, which directly exposes the reversible reaction topology before downstream crystallization can obscure it. Safety is classified from the final assay in both tasks.

Q2 does not fit a generic linear or quadratic surrogate and never treats categorical material IDs as numeric. At every frozen held-out coordinate it compares predictions produced by direct provider-free execution of the two registered laws. The altered executable law is the blinded truth candidate; selection of queries does not read outcomes.

## Pass, failure, and stop rules

Every candidate-world must satisfy all of the following:

- exactly 1,024 classified and completed primary executions and 1,024 exact replays;
- complete paired-law roster with identical action-plan and observation-coordinate hashes;
- deterministic mechanism/intervention binding and trajectory-file hash binding;
- candidate-specific mechanism semantics: the partition exponent intervention must leave the
  compiled reaction-mechanism hash unchanged while changing only the registered domain parameter;
  the crystallization topology intervention must change the compiled mechanism and add exactly one
  reaction;
- zero physical failures, platform failures, unsafe completions, or participant-visible hidden-law leakage;
- 384 Q1 coverage coordinates split 192/192 across the two intervention families;
- exactly 16 frozen Q2 queries split 8/8 across families;
- at least four of eight Q2 queries in each family separate the laws by the frozen metric-specific effect gate;
- at least two public metrics separate the laws in that world.

Any platform failure stops the block and requires a full restart after the defect is fixed. Any scientific gate failure is retained as a candidate rejection; thresholds, worlds, coordinates, and selection rules are not changed. D1 configuration is generated only if both candidates pass all five worlds, and remains explicitly execution-unauthorized pending W2-26 and external provider authorization.

## Expected outputs

The runner writes ten self-hashed world reports, one readable five-world summary with all failures and exact denominators, one Q2 executable-law package, and—only after 10/10 world passes—two complete 12-experiment D1 configurations with checkpoints at `0/3/6/9/12`. Raw trajectories remain under ignored `runs/development/`; no provider calls or participant sessions occur in Q1/Q2.
